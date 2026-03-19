from dotenv import load_dotenv
load_dotenv(".env.local")

print("AGENT FILE STARTED")

from livekit import agents
from livekit.agents import AgentServer, AgentSession, Agent
from livekit.plugins import google
from jarvis_prompt import JARVIS_BEHAVIOR_PROMPT, JARVIS_REPLY_PROMPT
from datetime import datetime


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=JARVIS_BEHAVIOR_PROMPT
        )


server = AgentServer()


@server.rtc_session()
async def my_agent(ctx: agents.JobContext):

    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    current_date = now.strftime("%A, %d %B %Y")

    time_context = f"""
SYSTEM CONTEXT:
Current time is {current_time}.
Today's date is {current_date}.
"""

    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(
            voice="charon"   # deep & serious voice
        )
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
    )

    await session.generate_reply(
        instructions=JARVIS_REPLY_PROMPT + time_context
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
