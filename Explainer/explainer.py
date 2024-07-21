from datetime import datetime
from aipptx_json import AIpptx
import sys 
sys.path.append('/home/ameer/exteam/python-Home-Work/final-ex/final-exercise-AmirAmmar123/server/')
from DB.chatgptDB import Upload, Session, sessionmaker
import asyncio
import time
import os 
class FileProcessor:

    UPLOADS = '/home/ameer/exteam/python-Home-Work/final-ex/final-exercise-AmirAmmar123/server/uploads/'
    def __init__(self, api_key: str = "OPENAI_API_KEY"):
        self.api_key = os.environ.get(api_key)
        self.setup = "Provide detailed explanations of the slides."

    async def process_file(self, upload: Upload, session: sessionmaker):
        """
        Asynchronously processes a single file.

        Parameters:
        upload (Upload): The Upload object representing the file to be processed.
        session (Session): The database session object for interacting with the database.

        Returns:
        None

        Raises:
        Exception: If any error occurs during the file processing.
        """    
        fullpath = self.UPLOADS+upload.uploaded_filename
        ai_pptx = AIpptx(self.api_key,fullpath, self.setup)
        await ai_pptx.run_on_slides_with_setup(ai_pptx.parser.total_slides)

        try:
            upload.status = 'done'
            upload.finish_time = datetime.now()
            upload.json_data = ai_pptx.getjsonData() 

            session.add(upload)
            session.commit()
            print(f"Processed file with UID: {upload.uid}")
            os.remove(fullpath)
        except Exception as e:
            session.rollback()
            print(f"Error occurred while processing file {upload.uid}: {e}")

    def run(self):
        try:
            while True:
               
                try:
                    session = Session()
                    pending_uploads = session.query(Upload).filter_by(status='pending').order_by(Upload.upload_time).all()

                    for upload in pending_uploads:
                        asyncio.run(self.process_file(upload, session))  # Process each upload asynchronously

                except Exception as e:
                    print(f"Error fetching or processing files: {e}")

                finally:
                    session.close()

                time.sleep(3)

        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Exiting...")

if __name__ == "__main__":
    processor = FileProcessor()
    processor.run()
