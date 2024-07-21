import os
import unittest
import json
import asyncio
from unittest.mock import patch
from Explainer.aipptx_json import AIpptx


class TestAIpptx(unittest.TestCase):

    @patch('Explainer.pptx_parser.PresentationParser')
    @patch('Explainer.openAI_integration.OpenAIIntegration')
    async def test_process_slides(self, mock_ai_agent, mock_parser):
        # Mock setup for slide 1
        mock_parser.return_value.total_slides = 3

        # Mock slide 1 content and AI response
        mock_parser.return_value.get_slide.side_effect = [
            {"content": ["Computer Vision", "Derek Hoiem, University of Illinois", "01/19/17",
                         "“Empire of Light”, Magritte"]},
            {"content": ["What determines a pixel’s brightness?", "How is light reflected?", "How is light measured?",
                         "What can be inferred about the world from those brightness values?"]},
            {"content": ["Third slide content"]}
        ]

        mock_ai_agent.return_value.chat.side_effect = [
            "Slide 1: The title of the presentation is \"Computer Vision\" and it is being presented by Derek Hoiem from the University of Illinois. The date of the presentation is January 19, 2017. Additionally, there is a reference to the artwork \"Empire of Light\" by the artist Magritte.\n\nBased on this information, it can be inferred that the presentation will likely cover topics related to computer vision, which is a field of artificial intelligence that focuses on giving machines the ability to interpret and understand visual information from the world. The reference to Magritte's artwork could suggest a discussion on how computer vision techniques are applied in art or how machines understand and interpret visual artworks.",
            "Explanation for slide 2",
            "Explanation for slide 3"
        ]

        ai_pptx = AIpptx(os.getenv("OPENAI_API_KEY"),
                         r"C:\Users\AMIR\ramatgan-window\cop1\ExcellentTeam\python-Home-Work\final-exercise"
                         r"-AmirAmmar123\server\uploads\16-Photometry.pptx_20240623011545_419eb622-3c13-458c-9c35"
                         r"-f58e56d31331",
                         "You are a pptx assistant. You will be given a pptx file as input. Your task is to generate "
                         "explanations for each slide.")

        await ai_pptx.run_on_slides_with_setup(3)

        ai_pptx.save_json_file("test_output.json")

        # Load JSON file and check content
        with open("test_output.json", 'r') as f:
            data = json.load(f)

        # Expected data
        expected_data = [
            {
                "slide_number": 1,
                "prompt": "Computer Vision\nDerek Hoiem, University of Illinois 01/19/17 “Empire of Light”, Magritte",
                "response": "Slide 1: The title of the presentation is \"Computer Vision\" and it is being presented by Derek Hoiem from the University of Illinois. The date of the presentation is January 19, 2017. Additionally, there is a reference to the artwork \"Empire of Light\" by the artist Magritte.\n\nBased on this information, it can be inferred that the presentation will likely cover topics related to computer vision, which is a field of artificial intelligence that focuses on giving machines the ability to interpret and understand visual information from the world. The reference to Magritte's artwork could suggest a discussion on how computer vision techniques are applied in art or how machines understand and interpret visual artworks."
            },
            {
                "slide_number": 2,
                "prompt": "What determines a pixel’s brightness?\nHow is light reflected?\nHow is light measured?\n\nWhat can be inferred about the world from those brightness values?",
                "response": "Explanation for slide 2"
            },
            {
                "slide_number": 3,
                "prompt": "Third slide content",
                "response": "Explanation for slide 3"
            }
        ]

        self.assertEqual(len(data), len(expected_data))
        for i in range(len(data)):
            self.assertEqual(data[i]["slide_number"], expected_data[i]["slide_number"])
            self.assertEqual(data[i]["prompt"], expected_data[i]["prompt"])
            self.assertEqual(data[i]["response"], expected_data[i]["response"])


async def main():
    await unittest.main()


if __name__ == '__main__':
    asyncio.run(main())
