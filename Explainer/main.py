import argparse
import asyncio
import os
from aipptx_json import AIpptx

class PPTXProcessor:
    def __init__(self, pptx_path:str, max_slides:int, setup:str, output_file:str, timeout:int):
        """
        Initializes the class with the provided parameters.

        Args:
            pptx_path (str): The path to the PowerPoint file.
            max_slides (int): The maximum number of slides to process.
            setup (str): The setup configuration.
            output_file (str): The output file path.
            timeout (int): The timeout value for the process.
        """

        self.pptx_path = pptx_path
        self.max_slides = max_slides
        self.setup = setup
        self.output_file = output_file
        self.timeout = timeout
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.ai_pptx = None

    async def process_pptx(self)-> None:
        """
        Processes the PowerPoint presentation using AI.

        Args:
            None

        Returns:
            None
        """
        try:
            print('Reading The Presentation', end='', flush=True)
            self.ai_pptx = AIpptx(api_key=self.api_key, pptx_path=self.pptx_path, setup=self.setup, timeout=self.timeout)
            print('[DONE]')

            print('Processing with AI (may take a minute)', end='', flush=True)
            await self.ai_pptx.run_on_slides_with_setup(self.max_slides)
            print('[DONE]')

            self.ai_pptx.save_json_file(self.output_file)
            print('Output Ready At:', self.output_file)
        except Exception as e:
            print(f"Error processing PowerPoint presentation: {str(e)}")

def parse_arguments()->argparse.Namespace:
    """
    Parses command-line arguments for processing a PowerPoint presentation.

    Args:
        None

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """

    parser = argparse.ArgumentParser(description="Process a PowerPoint presentation using OpenAI API.")
    parser.add_argument("pptx_path", type=str, help="Path to the PowerPoint presentation file.")
    parser.add_argument("--max_slides", type=int, default=10, help="Maximum number of slides to process (default: 10).")
    parser.add_argument("--setup", type=str, default="", help="Setup string for OpenAI integration.")
    parser.add_argument("--output_file", type=str, default="slide_responses.json", help="Output JSON file path (default: slide_responses.json).")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout for OpenAI API requests in seconds (default: 30).")
    return parser.parse_args()

def main():
    """
    Runs the main processing logic for the PowerPoint presentation.

    Args:
        None

    Returns:
        None
    """

    args = parse_arguments()
    processor = PPTXProcessor(
        pptx_path=args.pptx_path,
        max_slides=args.max_slides,
        setup=args.setup,
        output_file=args.output_file,
        timeout=args.timeout
    )
    asyncio.run(processor.process_pptx())

if __name__ == "__main__":
    main()
