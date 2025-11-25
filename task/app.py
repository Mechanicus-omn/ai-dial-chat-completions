import asyncio

from task.clients.client import DialClient
from task.constants import DEFAULT_SYSTEM_PROMPT
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role


async def start(stream: bool) -> None:
    
    client = DialClient(
        deployment_name="gpt-4o-mini")
    
    conversation = Conversation()

    print("Insert system prompt or leave empty to use default:")
    sys_prompt = input("> ").strip()
    if not sys_prompt:
        sys_prompt = DEFAULT_SYSTEM_PROMPT
    
    while True:
        print("Type your message (or type 'exit' to quit):")
        user_input = input("> ").strip()
        if user_input.lower() == 'exit':
            break
        
        conversation.add_message(Message(role=Role.USER, content=user_input))
        
        print("Assistant response:")
        if stream:
            async for response in client.stream_completion(conversation, sys_prompt):
                print(response.content, end='', flush=True)
            print()
        else:
            response = await client.get_completion(conversation, sys_prompt)
            print(response.content)
        
        conversation.add_message(response)

asyncio.run(
    start(True)
)
