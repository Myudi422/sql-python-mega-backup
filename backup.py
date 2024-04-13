import os
import time
import datetime
import subprocess
from mega import Mega

# Fungsi untuk melakukan backup database MySQL
def backup_database():
    db_user = 'ccgnimex'
    db_password = 'aaaaaaac'
    db_name = 'ccgnimex'
    backup_dir = '/www/wwwroot/ccgnimex.my.id/v2'

    # Generate nama file backup
    current_time = datetime.datetime.now()
    backup_file = f'{db_name}_{current_time.strftime("%Y%m%d_%H%M%S")}.sql'

    # Perintah untuk melakukan backup menggunakan mysqldump
    command = f'mysqldump --user={db_user} --password={db_password} {db_name} > {os.path.join(backup_dir, backup_file)}'

    # Jalankan perintah backup menggunakan subprocess
    subprocess.call(command, shell=True)

    return os.path.join(backup_dir, backup_file)

# Fungsi untuk mengunggah file ke Mega
def upload_to_mega(file_path):
    mega = Mega()
    m = mega.login('myudi422@gmail.com', 'cinangka03')  # Ganti dengan email dan password Mega Anda

    # Cek apakah file sudah ada di Mega
    file_exists = m.find('ccgnimex.sql')

    # Jika file sudah ada, hapus file tersebut
    if file_exists:
        m.delete(file_exists[0])

    # Upload file baru
    m.upload(file_path, dest_filename='ccgnimex.sql')

    print(f'File {os.path.basename(file_path)} berhasil diunggah ke Mega')

# Fungsi untuk menunggu hingga jam 12 siang atau malam
def wait_until_midday_or_midnight():
    now = datetime.datetime.now()
    next_midday = datetime.datetime(now.year, now.month, now.day, 12, 0)
    next_midnight = datetime.datetime(now.year, now.month, now.day, 0, 0) + datetime.timedelta(days=1)
    if now <= next_midday:
        time.sleep((next_midday - now).total_seconds())
    else:
        time.sleep((next_midnight - now).total_seconds())

# Jalankan backup dan upload pada jam 12 siang dan malam
while True:
    wait_until_midday_or_midnight()
    backup_file_path = backup_database()
    upload_to_mega(backup_file_path)
