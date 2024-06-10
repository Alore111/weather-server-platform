import os
import zipfile

import sys
from datetime import datetime
def create_zip(start_date, end_date, zip_name):
    # 转换日期格式
    start_date = datetime.strptime(start_date, "%Y%m%d")
    end_date = datetime.strptime(end_date, "%Y%m%d")
    # 创建压缩包
    zip_filename = f'{zip_name}.zip'
    root=os.path.dirname(sys.argv[0])+"/files/"
    zip_path=os.path.dirname(sys.argv[0])+"/zip/"+zip_filename
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        # 遍历文件夹，找到符合条件的文件
        for file in os.listdir(os.path.dirname(sys.argv[0])+"/files"):
            if file.endswith('.txt'):
                file_date_str = file.split('.')[0]
                file_date = datetime.strptime(file_date_str, "%Y%m%d")
                if start_date <= file_date <= end_date:
                    file_path = os.path.join(root, file)
                    arcname=os.path.join(root, file).replace(root,"")
                    zipf.write(file_path,arcname=arcname)

    # zipf.close()
    return zip_path

def log_request(zip_name, start_date, end_date, note):
    root = os.path.dirname(sys.argv[0])+'/file.txt'
    start_date_formatted = datetime.strptime(start_date, "%Y%m%d").strftime('%Y-%m-%d')
    end_date_formatted = datetime.strptime(end_date, "%Y%m%d").strftime('%Y-%m-%d')
    with open(root, 'a', encoding='utf-8') as f:
        f.write(f'{zip_name},{start_date_formatted},{end_date_formatted},{note}\n')