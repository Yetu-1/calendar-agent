from autogen_core.tools import FunctionTool
from src.utils.topics import (
    create_event_agent_topic_type,
    scheduler_agent_topic_type,
    rescheduler_agent_topic_type,
    read_event_agent_topic_type,
    delete_event_agent_topic_type,
    triage_agent_topic_type,
    human_agent_topic_type,
    user_topic_type,
)
def transfer_to_create_event_agent() -> str: 
    return create_event_agent_topic_type

def transfer_to_scheduler_agent() -> str:
    return scheduler_agent_topic_type

def transfer_to_rescheduler_agent() -> str:
    return rescheduler_agent_topic_type

def transfer_to_read_event_agent() -> str: 
    return read_event_agent_topic_type

def transfer_to_delete_event_agent() -> str:
    return delete_event_agent_topic_type

def transfer_back_to_triage() -> str:
    return triage_agent_topic_type

def escalate_to_human() -> str:
    return human_agent_topic_type

transfer_to_create_event_agent_tool = FunctionTool(
    transfer_to_create_event_agent, description="Use for creating new calendar events"
)

transfer_to_scheduler_agent_tool = FunctionTool(
    transfer_to_scheduler_agent, description="Use for adding created calendar events to the calendar"
)

transfer_to_rescheduler_agent_tool = FunctionTool(
    transfer_to_rescheduler_agent, description="Use for rescheduling or updating an event in the calendar"
)

transfer_to_read_event_agent_tool = FunctionTool(
    transfer_to_read_event_agent, description="Use for reading or fetching events from the calendar"
)

transfer_to_delete_event_agent_tool = FunctionTool(
    transfer_to_delete_event_agent, description="Use for deleting or removing events from the calendar"
)

transfer_back_to_triage_tool = FunctionTool(
    transfer_back_to_triage,
    description="Call this if the user brings up a topic outside of your purview,\nincluding escalating to human.",
)
escalate_to_human_tool = FunctionTool(escalate_to_human, description="Only call this if explicitly asked to.")
