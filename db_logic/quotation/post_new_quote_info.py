from agent_config.AgentState import agentState

def post_new_quote_info(state: agentState) -> int:

    """Returns the latest quote number from database to generate the next quote ID (Q-JCP-XX-1)"""
    
    return 