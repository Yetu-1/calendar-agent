from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core import (
    RoutedAgent,
    SingleThreadedAgentRuntime,
    TopicId,
    TypeSubscription,
)
from src.tools.regular_tools import (
    get_datetime_tool,
    add_event_to_calendar_tool,
)
from src.tools.delegate_tools import (
    transfer_to_create_event_agent_tool,
    transfer_to_scheduler_agent_tool,
    transfer_to_rescheduler_agent_tool,
    transfer_to_read_event_agent_tool,
    transfer_to_delete_event_agent_tool,
    transfer_back_to_triage_tool,
    escalate_to_human_tool,
)
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

from autogen_core.models import SystemMessage
from src.config import Settings
from src.utils.messages import UserLogin

from src.agents.human_agent import HumanAgent
from src.agents.user_agent import UserAgent
from src.agents.ai_agent import AIAgent
import asyncio
import uuid

async def main():
    runtime = SingleThreadedAgentRuntime()

    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=Settings.OPENAI_API_KEY,
    )

    # Register the triage agent.
    triage_agent_type = await AIAgent.register(
        runtime,
        type=triage_agent_topic_type,  # Using the topic type as the agent type.
        factory=lambda: AIAgent(
            description="A triage agent.",
            system_message=SystemMessage(
                content="You are a triage agent for a calendar assistant system. "
                "Your only job is to identify the user's intent and transfer them "
                "to the correct specialized agent using the appropriate delegate tool. "
                "Do not ask follow-up questions or try to complete the user's task yourself. "
                "Respond concisely and confirm the transfer."
            ),
            model_client=model_client,
            tools=[],
            delegate_tools=[
                transfer_to_create_event_agent_tool,
                transfer_to_scheduler_agent_tool,
                transfer_to_rescheduler_agent_tool,
                transfer_to_read_event_agent_tool,
                transfer_to_delete_event_agent_tool,
                escalate_to_human_tool,
            ],
            agent_topic_type=triage_agent_topic_type,
            user_topic_type=user_topic_type,
        ),
    )
    # Add subscriptions for the triage agent: it will receive messages published to its own topic only.
    await runtime.add_subscription(TypeSubscription(topic_type=triage_agent_topic_type, agent_type=triage_agent_type.type))

   
    # Register the create event agent
    create_event_agent_type = await AIAgent.register(
        runtime,
        type=create_event_agent_topic_type,  # Using the topic type as the agent type.
        factory=lambda: AIAgent(
            description="An Agent that can create calendar events.",
            system_message=SystemMessage(
                content="You are an agent that creates google calendar events."
                "Always answer in a sentence or less."
                "Follow the following routine with the user:"
                "1. Always get the current date and time"
                "2. Ask them the details of the event they want to add to their calendar including the title of the event, time it starts and how long it is.\n"
                " - unless the user has already provided the details. If any have not been provided, ask for it."
                "3. Always Show the event created to the user in readable form and ask for a confirmation of details and always show the event In the required google calendar event json format."
                "4. Once the user is satisfied, go on to add the event to their google calendar.\n"
            ),
            model_client=model_client,
            tools=[get_datetime_tool],
            delegate_tools=[transfer_back_to_triage_tool, transfer_to_scheduler_agent_tool,],
            agent_topic_type=create_event_agent_topic_type,
            user_topic_type=user_topic_type,
        ),
    )
    # Add subscriptions for the create event agent: it will receive messages published to its own topic only.
    await runtime.add_subscription(TypeSubscription(topic_type=create_event_agent_topic_type, agent_type=create_event_agent_type.type))

    # Register the scheduler agent
    scheduler_agent_type = await AIAgent.register(
        runtime,
        type=scheduler_agent_topic_type,  # Using the topic type as the agent type.
        factory=lambda: AIAgent(
            description="An Agent that adds events to the calendar.",
            system_message=SystemMessage(
                content="You are an agent that adds events to the calendar."
                "Send a confirmation to the user if the event was successfully added to the calendar"
            ),
            model_client=model_client,
            tools=[add_event_to_calendar_tool],
            delegate_tools=[transfer_back_to_triage_tool],
            agent_topic_type=scheduler_agent_topic_type,
            user_topic_type=user_topic_type,
        ),
    )
    # Add subscriptions for the create event agent: it will receive messages published to its own topic only.
    await runtime.add_subscription(TypeSubscription(topic_type=scheduler_agent_topic_type, agent_type=scheduler_agent_type.type))

    # Register the human agent.
    human_agent_type = await HumanAgent.register(
        runtime,
        type=human_agent_topic_type,  # Using the topic type as the agent type.
        factory=lambda: HumanAgent(
            description="A human agent.",
            agent_topic_type=human_agent_topic_type,
            user_topic_type=user_topic_type,
        ),
    )
    # Add subscriptions for the human agent: it will receive messages published to its own topic only.
    await runtime.add_subscription(TypeSubscription(topic_type=human_agent_topic_type, agent_type=human_agent_type.type))

    # Register the user agent.
    user_agent_type = await UserAgent.register(
        runtime,
        type=user_topic_type,
        factory=lambda: UserAgent(
            description="A user agent.",
            user_topic_type=user_topic_type,
            agent_topic_type=triage_agent_topic_type,  # Start with the triage agent.
        ),
    )
    # Add subscriptions for the user agent: it will receive messages published to its own topic only.
    await runtime.add_subscription(TypeSubscription(topic_type=user_topic_type, agent_type=user_agent_type.type))

    # Start the runtime.
    runtime.start()

    # Create a new session for the user.
    session_id = str(uuid.uuid4())
    await runtime.publish_message(UserLogin(), topic_id=TopicId(user_topic_type, source=session_id))

    # Run until completion.
    await runtime.stop_when_idle()
    await model_client.close()


asyncio.run(main())