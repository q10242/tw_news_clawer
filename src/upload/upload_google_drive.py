from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import os
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 認證憑證
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = service_account.Credentials.from_service_account_file('/app/credentials.json', scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

# 創建文件夾（如果不存在）
def create_folder(folder_name, parent_folder_id=None):
    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'"
    if parent_folder_id:
        query += f" and '{parent_folder_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    
    if files:
        logging.info(f"Found existing folder: {folder_name} with ID: {files[0]['id']}")
        return files[0]['id']
    else:
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
        }
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]
        folder = service.files().create(body=file_metadata, fields='id').execute()
        logging.info(f"Created folder: {folder_name} with ID: {folder.get('id')}")
        return folder.get('id')

# 檢查檔案是否已存在
def file_exists(file_name, folder_id):
    query = f"name='{file_name}' and '{folder_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    return len(files) > 0

# 上傳文件到指定文件夾
def upload_file(file_path, folder_id):
    file_name = os.path.basename(file_path)
    if file_exists(file_name, folder_id):
        logging.info(f"File already exists: {file_name}. Skipping upload.")
        return
    
    try:
        file_metadata = {'name': file_name, 'parents': [folder_id]}
        media = MediaFileUpload(file_path, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        logging.info(f"Uploaded {file_name} to Google Drive with ID: {file.get('id')}")
    except Exception as e:
        logging.error(f"Failed to upload {file_name}: {e}")

# 遞迴同步文件夾及文件
def sync_folder(local_folder, parent_folder_id):
    for item in os.listdir(local_folder):
        item_path = os.path.join(local_folder, item)
        if os.path.isdir(item_path):
            folder_id = create_folder(item, parent_folder_id)
            sync_folder(item_path, folder_id)
        elif os.path.isfile(item_path):
            upload_file(item_path, parent_folder_id)

# 主程式
if __name__ == "__main__":
    local_folder = '/app/results'
    root_folder_id = '1ikKOG3n2te6mWZSGdYuB3-ygBmneLuFb'

    if not os.path.exists(local_folder):
        logging.error(f"Local folder {local_folder} does not exist.")
    else:
        logging.info(f"Starting sync for local folder: {local_folder}")
        sync_folder(local_folder, root_folder_id)
        logging.info("Sync complete.")
