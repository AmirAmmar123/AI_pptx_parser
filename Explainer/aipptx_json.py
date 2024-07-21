import json
from typing import Coroutine
from openAI_integration import OpenAIIntegration
from pptx_parser import PresentationParser


class AIpptx:
    """
    A class to process PowerPoint slides using OpenAI.

    Attributes:
        slide_responses (list): A list to store responses for each slide.
        parser (PresentationParser): An instance of the PresentationParser class.
        ai_agent (OpenAIIntegration): An instance of the OpenAIIntegration class.
    """

    def __init__(self, api_key: str, pptx_path: str, setup: str, timeout: int = 30):
        """
        Initializes the AIpptx class with the provided parameters.

        Args:
            api_key (str): The API key for accessing the OpenAI API.
            pptx_path (str): The path to the PowerPoint file.
            setup (str): The setup configuration.
            timeout (int): The timeout value for the process.
        """
        self.slide_responses = []
        self.parser = PresentationParser(pptx_path)
        self.parser.process_presentation(False)
        self.ai_agent = OpenAIIntegration(api_key, setup, timeout)

    async def run_on_slides_with_setup(self, slide_count: int) -> None:
        """
        Processes slides and gets responses from the AI agent.

        Args:
            slide_count (int): The number of slides to process.

        Returns:
            Coroutine[Any, Any, None]: Coroutine for async processing.
        """
        slide_count = min(self.parser.total_slides, slide_count)

        for slide_index in range(1, slide_count + 1):
            try:
                if slide_data := self.parser.get_slide(slide_index):
                    prompt = ' '.join(slide_data["content"])
                    response = await self.ai_agent.chat(prompt)
                    self.slide_responses.append({
                        "slide_number": slide_index,
                        "prompt": prompt if prompt.strip() else "empty",
                        "response": response if prompt.strip() else "empty"
                    })
            except Exception as e:
                print(f"Error processing slide {slide_index}: {str(e)}")
                self.slide_responses.append({
                    "slide_number": slide_index,
                    "prompt": "error",
                    "response": str(e)
                })

    def getjsonData(self) -> None:
        """
        Saves the slide responses to a JSON file.

        Args:
            filename (str): The name of the JSON file to save.

        Returns:
            None
        """
        try:
        
            return json.dumps(self.slide_responses, indent=4)
        except Exception as e:
            print(f"Error saving JSON to file: {str(e)}")
