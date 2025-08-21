from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from agent_config.AgentState import agentState
from agent_config.agent_registry import AGENT_NODES, STATIC_EDGES, CONDITIONAL_EDGES
from langgraph.checkpoint.memory import MemorySaver
from utils.UserRequest import UserRequest
from langchain_core.runnables import RunnableConfig
from utils.InterrutpException import InterruptException
from langgraph.types import Command

workflow_builder = StateGraph(agentState)
# register nodes
for agent_name, node in AGENT_NODES.items():
    workflow_builder.add_node(agent_name, node)
# wire static edges
for source, path in STATIC_EDGES:
    workflow_builder.add_edge(source, path)
# Wire conditional edges
for edge in CONDITIONAL_EDGES:
    workflow_builder.add_conditional_edges(
        source=edge["source"],
        path=edge["path"],
        path_map=edge["path_map"]
    )
    
workflow_builder.set_entry_point("intent_agent")
workflow_builder.set_finish_point("final_response_agent")

checkpointer = MemorySaver()
graph = workflow_builder.compile(checkpointer=checkpointer)


#---------------------------------------------------------------#
def run_agent(user_request: UserRequest):
    initial_state = {
        "user_input": user_request.message,
        "messages": [HumanMessage(content=user_request.message)],
        "human_feedback": [],
    }

    config: RunnableConfig = {
        "configurable": {
            "thread_id": user_request.session_id
        }
    }
    
    print("Invoking graph...\n")
    result = graph.invoke(initial_state, config=config)  # receive entire state here

    state = graph.get_state(config)
    print(state.values)
    print(state.tasks)

    if "__interrupt__" in result:
        print(result['__interrupt__'])
        interrupt_info = result["__interrupt__"][0]
        value = interrupt_info.value
        resumable = True
        ns = None

        # 通常是单个中断
        raise InterruptException(
            state=result,
            value=value,
            resumable=resumable,
            ns=ns
        )
    agent_response = result.get("final_response")
    print(f"agent_response: {agent_response}")
    return agent_response


def resume_agent(user_request: UserRequest):
    print(checkpointer.storage)
    
    config: RunnableConfig = {
        "configurable": {
            "thread_id": user_request.session_id
        }
    }

    resume_state = {
        "quotation_json": user_request.quotation_json,
        "human_feedback": [user_request.message],
    }

    try:
        command = Command(resume=resume_state)
        result = graph.invoke(command, config)
        
        # Check if there's an interrupt in the result
        if "__interrupt__" in result:
            interrupt_info = result["__interrupt__"][0]
            value = interrupt_info.value
            raise InterruptException(
                state=result,
                value=value,
                resumable=True,
                ns=None
            )
            
        return {
            "status": "resumed", 
            "result": result
        }
        
    
    except Exception as e:
        print("error:", {str(e)})
        
        return {
            "status": "error", 
            "result": str(e)
        }