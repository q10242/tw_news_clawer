from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

# 認證憑證
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = service_account.Credentials.from_service_account_file('/home/kyjita/codebase/tw_news_clawer/credentials.json', scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

# 上傳文件
def upload_file(file_path, folder_id):
    file_metadata = {'name': file_path.split('/')[-1], 'parents': [folder_id]}
    media = MediaFileUpload(file_path, resumable=True)
    service.files().create(body=file_metadata, media_body=media).execute()

# 本地文件夾路徑
local_folder = '/home/kyjita/codebase/tw_news_clawer/results'
folder_id = '1ikKOG3n2te6mWZSGdYuB3-ygBmneLuFb'

import os
for filename in os.listdir(local_folder):
    file_path = os.path.join(local_folder, filename)
    if os.path.isfile(file_path):
        upload_file(file_path, folder_id)

