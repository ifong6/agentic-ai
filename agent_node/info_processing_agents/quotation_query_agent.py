from langchain.schema import AIMessage
from langchain_core.prompts import PromptTemplate
from agent_config.AgentState import agentState
from langchain.agents import create_react_agent, AgentExecutor
from typing import Dict, Any
from entity.Quote import Quote
from entity.LineItem import LineItem
from datetime import datetime
from tools.quote_tools import quote_tools

# React prompt template
REACT_TEMPLATE = '''
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer 
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: Process the following information into Quote objects:

    Quotation Info:
    {quotations}

    Remember:
    - Quote IDs format: Q-JCP-YY-XX-1 (YY is year, XX is sequential number)
    - Each item needs a serial number starting from 1
    - Handle errors gracefully

    Thought:{agent_scratchpad}
'''

react_prompt = PromptTemplate.from_template(REACT_TEMPLATE)

def quote_info_processing_agent_node(state: agentState):
    print("[INVOKE][quote_info_processing_agent_node]")
    
    try:
        system_prompt = react_prompt.format(
            tools="\n".join(f"{t['name']}: {t['description']}" for t in quote_tools),
            tool_names=", ".join(t["name"] for t in quote_tools),
            quotations=state.quotations,
            agent_scratchpad=""  # Initial empty scratchpad
        )
        
    except Exception as e:
        error_msg = f"[Error][quote_info_processing_agent_node]: {str(e)}"
        print(error_msg)
        return {
            "quotations": [],
            "messages": [AIMessage(content=error_msg)]
        }