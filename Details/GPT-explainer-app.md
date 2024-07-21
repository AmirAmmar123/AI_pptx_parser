Certainly! Here's an updated README file for your Flask application:

---

# Flask File Upload and Processing Application

This Flask application allows users to upload PowerPoint files (.pptx), processes them using AI, and saves the processed output as JSON files.

## Features

- **File Upload**: Users can upload PowerPoint files (.pptx) using a web interface.
- **Processing**: Each uploaded file undergoes processing to generate JSON output with detailed slide explanations.
- **Status Check**: Users can check the processing status of their uploaded files using a dedicated status endpoint.
- **UID Display**: Displays the UID in a formatted way after file upload.
- **Automated Processing**: Files are continuously monitored in the `uploads` directory, and processing begins automatically upon upload.
- **Output**: Processed JSON files are saved in the `outputs` directory with filenames formatted as `<original_filename>_<timestamp>_<uid>.json`.

## Setup Instructions

### Prerequisites

- Python 3.x installed
- Virtual environment (optional but recommended)

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Set up environment variables:
   
   - `CHATGPT_KEY`: API key for the AI service used to process PowerPoint files.
   
2. Configure directories:
   
   - `UPLOAD_FOLDER`: Directory where uploaded PowerPoint files are stored.
   - `OUTPUT_FOLDER`: Directory where processed JSON files are saved.

### Running the Application

1. Start the Flask application:

   ```bash
   python main.py
   ```

2. Access the application in your web browser at `http://localhost:5000`.

### Usage

1. **Upload File**:
   
   - Navigate to the homepage (`/`) and use the file upload form to select and upload a PowerPoint file (.pptx).

2. **Check File Status**:
   
   - Use the status check link (`/status_check.html`) to enter the UID generated upon file upload and check the processing status.

3. **UID Display**:

   - After uploading a file, you can view the UID in a formatted way by visiting `/uid_display?uid=<generated-uid>`.

### Notes

- **Environment**: Ensure that the Flask application is running in a suitable environment (development vs. production) for your use case.
- **Security**: This application is for demonstration purposes. Implement appropriate security measures before deploying in a production environment.
- **Dependencies**: Review and update dependencies periodically to ensure compatibility and security.

---

Adjust the `<repository-url>` and `<repository-directory>` placeholders with your actual repository URL and directory name. Customize the configuration and usage instructions based on any specific details or additional features of your application.