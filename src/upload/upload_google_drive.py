from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import os

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
        # 文件夾已存在
        return files[0]['id']
    else:
        # 創建文件夾
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
        }
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]
        folder = service.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id')

# 上傳文件到指定文件夾
def upload_file(file_path, folder_id):
    try:
        file_metadata = {'name': os.path.basename(file_path), 'parents': [folder_id]}
        media = MediaFileUpload(file_path, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"Uploaded {file_path} to Google Drive with ID: {file.get('id')}")
    except Exception as e:
        print(f"Failed to upload {file_path}: {e}")

# 遞迴同步文件夾及文件
def sync_folder(local_folder, parent_folder_id):
    for item in os.listdir(local_folder):
        item_path = os.path.join(local_folder, item)
        if os.path.isdir(item_path):
            # 如果是文件夾，先創建對應的 Google Drive 文件夾
            folder_id = create_folder(item, parent_folder_id)
            print(f"Created/Found folder '{item}' with ID: {folder_id}")
            # 遞迴同步子文件夾
            sync_folder(item_path, folder_id)
        elif os.path.isfile(item_path):
            # 如果是文件，直接上傳到當前 Google Drive 文件夾
            upload_file(item_path, parent_folder_id)

# 主程式
if __name__ == "__main__":
    # 本地主文件夾
    local_folder = '/app/results'
    # Google Drive 主文件夾 ID
    root_folder_id = '1ikKOG3n2te6mWZSGdYuB3-ygBmneLuFb'

    # 確保本地文件夾存在
    if not os.path.exists(local_folder):
        print(f"Local folder {local_folder} does not exist.")
    else:
        # 開始同步
        sync_folder(local_folder, root_folder_id)