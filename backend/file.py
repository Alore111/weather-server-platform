import os
import zipfile
from wv_sql import *
import sys
from datetime import datetime
from io import BytesIO
import json
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

insert_data_query = '''
INSERT INTO WeatherData (
    Station_Id_d, Year, Mon, Day, Lat, Lon, Alti, PRS_Sea_Avg, WIN_S_Max,
    WIN_S_2mi_Avg, TEM_Avg, TEM_Max, TEM_Min, GST_Avg, PRE_Time_2020,
    SSH, CLO_Cov_Avg, CLO_Cov_Low_Avg, VIS_Min, Date
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
'''

def process_file(file_path, db):
    with open(file_path, 'r') as file:
        next(file)  # 跳过标题行
        for line in file:
            fields = line.split()
            if len(fields) == 19:
                Station_Id_d, Year, Mon, Day, Lat, Lon, Alti, PRS_Sea_Avg, WIN_S_Max, WIN_S_2mi_Avg, TEM_Avg, TEM_Max, TEM_Min, GST_Avg, PRE_Time_2020, SSH, CLO_Cov_Avg, CLO_Cov_Low_Avg, VIS_Min = fields
                Date = os.path.basename(file_path).split('.')[0]
                cursor.execute(insert_data_query, (
                    Station_Id_d, Year, Mon, Day, Lat, Lon, Alti, PRS_Sea_Avg, WIN_S_Max,
                    WIN_S_2mi_Avg, TEM_Avg, TEM_Max, TEM_Min, GST_Avg, PRE_Time_2020,
                    SSH, CLO_Cov_Avg, CLO_Cov_Low_Avg, VIS_Min, Date
                ))


if __name__ == '__main__':
    db = Database()
    connection = db.connect()
    cursor = connection.cursor()
    # 处理文件
    directory = os.path.dirname(sys.argv[0])+"/files/"
    for filename in os.listdir(directory):
        if filename.startswith('2016') and filename.endswith('.txt'):
            process_file(os.path.join(directory, filename), db)
            connection.commit()

    cursor.close()
    connection.close()


def fetch_data(db, start_date, end_date, options):
    # 构造查询字段
    fields = [key for key, value in options.items() if value]
    if 'Date' not in fields:
        fields.append('Date')  # 确保 Date 字段被包括在内
    fields_str = ", ".join(fields)

    query = f'''
    SELECT {fields_str} FROM WeatherData
    WHERE Date BETWEEN %s AND %s
    ORDER BY Date
    '''
    connection = db.connect()
    cursor = connection.cursor()
    cursor.execute(query, (start_date, end_date))
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data, fields


def write_txt_files(data, fields):
    date_dict = {}
    for row in data:
        date = row['Date']
        if date not in date_dict:
            date_dict[date] = []
        date_dict[date].append(row)

    file_names = []
    for date, rows in date_dict.items():
        filename = f"{date}.txt"
        file_names.append(filename)
        with open(filename, 'w') as file:
            # 写入属性名（不包括Date）
            fields_without_date = [field for field in fields if field != 'Date']
            file.write(" ".join(fields_without_date) + "\n")
            for row in rows:
                file.write(" ".join(str(row[field]) for field in fields_without_date) + "\n")
    return file_names


def create_zip_file(file_names, zip_name):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_name in file_names:
            zipf.write(file_name)
            os.remove(file_name)  # 删除已添加到zip的txt文件
    zip_buffer.seek(0)
    return zip_buffer


def log_download(db, zip_name, start_date, end_date, note, options):
    start_date_formatted = datetime.strptime(start_date, "%Y%m%d").strftime('%Y-%m-%d')
    end_date_formatted = datetime.strptime(end_date, "%Y%m%d").strftime('%Y-%m-%d')
    # 英文标签到中文标签的映射
    label_mapping = {
        "Station_Id_d": "站点",
        "Lat": "纬度",
        "Lon": "经度",
        "Alti": "海拔",
        "PRS_Sea_Avg": "压强",
        "WIN_S_Max": "最大风速",
        "WIN_S_2mi_Avg": "2m平均风速",
        "TEM_Avg": "平均温度",
        "TEM_Max": "最高温度",
        "TEM_Min": "最低温度",
        "GST_Avg": "地表平均温度",
        "PRE_Time_2020": "降水量",
        "SSH": "海平面高度",
        "CLO_Cov_Avg": "云平均覆盖度",
        "CLO_Cov_Low_Avg": "低云平均覆盖度",
        "VIS_Min": "最小能见度"
    }

    converted_options = [label_mapping[key] for key, value in options.items() if value and key in label_mapping]
    options_str = ", ".join(converted_options)
    query = '''
    INSERT INTO download_log (zip_name, start_date, end_date, note, options)
    VALUES (%s, %s, %s, %s, %s)
    '''
    connection = db.connect()
    cursor = connection.cursor()

    cursor.execute(query, (zip_name, start_date, end_date, note,options_str))
    connection.commit()
    cursor.close()
    connection.close()