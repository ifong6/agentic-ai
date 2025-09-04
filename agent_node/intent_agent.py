from agent_config.AgentState import agentState
from utils.invoke_llm import invoke_llm
from langchain_core.messages import AIMessage
from agent_node.prompts.intent_prompt_template import intent_prompt_template
from agent_node.prompts.intent_prompt_template import IntentClassifierOutput
    
def intent_agent_node(state: agentState):
    print("[INVOKE][intent_agent_node]")
  
    system_prompt = intent_prompt_template.format(user_input=state.user_input)
    parsed_response = invoke_llm(system_prompt, IntentClassifierOutput)

    try:
        intents = parsed_response.get("intents", []) or ["unknown"]
        llm_result_msg = parsed_response.get("messages", [])[-1]

    except Exception as e:
        return {
            "intents": ["unknown"],
            "messages": [AIMessage(content="[Error][intent_agent_node]: " + str(e))],
        }

    return {
        "intents": intents,
        "messages": [AIMessage(content=llm_result_msg)]
    }

    
  
    