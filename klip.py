import os
import time

def delete_folder_contents(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

def delete_folder_contents_periodically(folder_path, interval):
    while True:
        delete_folder_contents(folder_path)
        time.sleep(interval)

backup_folder = '/www/wwwroot/ccgnimex.my.id/backupx'
delete_interval = 3600  # 1 jam

delete_folder_contents_periodically(backup_folder, delete_interval)
