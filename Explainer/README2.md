# AI-Powered PowerPoint Presentation Processor

This project processes PowerPoint presentations using the OpenAI API to generate responses for each slide's content. The processed data is then saved to a JSON file.

## Features

- Parse PowerPoint presentations to extract slide data.
- Use OpenAI API to generate responses for slide content.
- Save the responses to a JSON file.

## Prerequisites

- Python 3.8+
- An OpenAI API key

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/aipptx-processor.git
    cd aipptx-processor
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your OpenAI API key as an environment variable:
    ```bash
    export OPENAI_API_KEY='your_openai_api_key_here'
    ```

## Usage

### Command-Line Interface

To process a PowerPoint presentation, run the following command:

```bash
python main.py path/to/your/presentation.pptx --max_slides 10 --setup "Your AI setup string here." --output_file "output.json" --timeout 30
