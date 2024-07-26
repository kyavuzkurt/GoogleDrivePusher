import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

class APIcall:
    def __init__(self, folder_path: str) -> None:
        self.credentials = google.auth.load_credentials_from_file("credentials.json")
        self.folder_path = folder_path
        load_dotenv()
        self.drive_folder_id = os.getenv('DRIVE_FOLDER_ID') 

    def upload_folder(self) -> None:
        allowed_extensions = ['csv', 'mp4', 'esp', 'mat', 'fig']

        try:
            service = build('drive', 'v3', credentials=self.credentials)
            for root, _, files in os.walk(self.folder_path):
                for file_name in files:
                    file_extension = file_name.split('.')[-1].lower()
                    if file_extension not in allowed_extensions:
                        print(f"File type {file_extension} is not supported for file {file_name}.")
                        continue

                    file_path = os.path.join(root, file_name)
                    file_metadata = {
                        'name': file_name,
                        'parents': [self.drive_folder_id]  # Add this line
                    }
                    media = MediaFileUpload(file_path, mimetype=f'application/{file_extension}')
                    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                    print(f"Uploaded {file_name} with File ID: {file.get('id')}")
        except HttpError as error:
            print(f"An error occurred: {error}")