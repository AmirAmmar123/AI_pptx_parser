import os
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, render_template, Response
import json
from DB.chatgptDB import Upload, User, Session


app = Flask(__name__)

UPLOAD_FOLDER = '/home/ameer/exteam/python-Home-Work/final-ex/final-exercise-AmirAmmar123/server/uploads'



def generateID():
       return str(uuid.uuid4()), datetime.now().strftime('%Y%m%d%H%M%S')
   
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index()->str:
    return render_template('upload.html')

@app.route('/status_check.html')
def status_check() -> str:
    return render_template('status_check.html')


@app.route('/upload', methods=['POST'])
def upload_file() -> Response:
    """
    Handles file uploads. It saves the uploaded file to the server, creates a new record in the database,
    and returns a unique identifier (UID) for the uploaded file.

    Parameters:
    - methods: The HTTP methods allowed for this route. In this case, only POST is allowed.

    Returns:
    - Response: A JSON response containing the UID if the file is successfully uploaded.
                If an error occurs, it returns a JSON response with an error message.

    Raises:
    - None
    """
    email = request.form.get('email')

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        uid, timestamp=generateID() 
        filename = f"{uid}_{timestamp}_{file.filename}"
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        session = Session()

        try:
            user = None
            id = None
            if email:
                user = session.query(User).filter_by(email=email).first()

                if not user:
                    user = User(email=email)
                    session.add(user)
                    session.commit()
                else:
                    id = user.id

            new_upload = Upload(
                uid=uid,
                filename=file.filename,
                upload_time=datetime.now(),
                status='pending',
                uploaded_filename=filename,
                finish_time=None,
                user=user,
                user_id=id if user else None
            )
            session.add(new_upload)
            session.commit()

            print(f"Uploaded file with UID: {uid}")  # Log successful upload

            return jsonify({"uid": uid}), 200

        except Exception as e:
            session.rollback()
            print(f"Error occurred: {e}")  # Log the error to help diagnose the issue
            if os.path.exists(filename):
                os.remove(UPLOAD_FOLDER+'/'+filename)
                print(f"Deleted file '{filename}' due to upload failure.")
                
            return jsonify({"error": "File upload failed"}), 500

        finally:
            session.close()

    return jsonify({"error": "File upload failed"}), 500

@app.route('/status', methods=['GET'])
def check_status()-> str | Response:
    """
    This function checks the status of a file upload based on the provided UID.
    It retrieves the upload record from the database and renders an appropriate template based on the status.

    Parameters:
    - None

    Returns:
    - str or Response: Rendered template displaying the status or an error message if no UID is provided.

    Raises:
    - None
    """

    uid = request.args.get('uid')
    if not uid:
        return jsonify({"error": "No UID provided"}), 400

    session = Session()
    try:
        upload = session.query(Upload).filter_by(uid=uid).first()

        if not upload:
            return render_template('error.html'), 404

        if upload.status == 'pending':
            return render_template('output_display.html', 
                                   status="pending", 
                                   filename=upload.filename, 
                                   timestamp=upload.upload_time.strftime("%Y-%m-%d %H:%M:%S"), 
                                   explanation=None)

        elif upload.status == 'done':
            explanation = json.loads(upload.json_data)
            return render_template('output_display.html', 
                                   status="done", 
                                   filename=upload.filename, 
                                   timestamp=upload.upload_time.strftime("%Y-%m-%d %H:%M:%S"), 
                                   explanation=explanation)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()

@app.route('/uid_display')
def uid_display():
    """
    Renders a template to display a provided UID.

    Args:
        uid (str): The unique identifier to display.

    Returns:
        str or Response: Rendered template displaying the UID or an error message if no UID is provided.
    """

    if uid := request.args.get('uid'):
        return render_template('uid_display.html', uid=uid)
    else:
        return "Error: No UID provided."

if __name__ == "__main__":
    app.run(debug=True, port=3000)