from openai import AsyncOpenAI
import asyncio

class OpenAIIntegration:
    """
    Class for integrating with OpenAI to chat using the provided API key, setup, and timeout.

    Args:
        api_key (str): The API key for OpenAI.
        setup (str): The initial setup string for OpenAI integration.
        timeout (int, optional): Timeout for OpenAI API requests in seconds (default is 30).

    """

    def __init__(self, api_key: str, setup: str, timeout: int = 30):
        self.api_key = api_key
        self.message_history = [{"role": "user", "content": setup}]
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.timeout = timeout 
        
    
    async def chat(self, prompt: str) -> str:
        """
    Chats with the OpenAI model using the provided prompt.

    Args:
        prompt (str): The prompt for the conversation.

    Returns:
        str: The response from the OpenAI model.
    """
        self.message_history.append({"role": "user", "content": prompt})
        
        completion = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.message_history,
            max_tokens=150,
            timeout=self.timeout
        )
        response = completion.choices[0].message.content.strip() if completion.choices else ""
        self.message_history.append({"role": "assistant", "content": response})
        
        return response


async def main():
    """
    Asynchronous function to interact with the OpenAI API by sending a prompt and printing the response.

    Args:
        None

    Returns:
        None
"""
    api_key = "your_openai_api_key_here"
    openai_integration = OpenAIIntegration(api_key)
    prompt = "Your prompt text here."
    response = await openai_integration.send_to_openai_api(prompt)
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
