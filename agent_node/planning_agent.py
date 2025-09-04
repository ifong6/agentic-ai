from langchain_core.messages import AIMessage
from agent_node.prompts.routing_prompt_template import PlanningResultOutput
from agent_config.AgentState import agentState
from utils.invoke_llm import invoke_llm
from agent_node.prompts.routing_prompt_template import routing_prompt_template
from agent_node.prompts.routing_prompt_template import build_routing_prompt
def planning_agent_node(state: agentState):
    print("- [INVOKE] [planning_agent_node]")
    
    system_prompt = build_routing_prompt.format(intents=state.intents)
    parsed_response = invoke_llm(system_prompt, PlanningResultOutput)

    try:
        next_agents = parsed_response.get("next_agents", [])  # the next agents per planning result
        messages = parsed_response.get("messages", "")[-1]

        return {
            "next_agents": next_agents,
            "messages": [AIMessage(content=messages)]
        }

    except Exception as e:
        print(f"[ERROR][planning_agent_node] {e}")
        return {
            "messages": [AIMessage(content=f"[PlanningAgent Error] {e}")]
        }

