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
    backup_dir = '/www/wwwroot/ccgnimex.my.id/backupx'

    # Generate nama file backup
    backup_file = f'{db_name}.sql'

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

# Jalankan backup dan upload setiap 1 menit
while True:
    backup_file_path = backup_database()
    upload_to_mega(backup_file_path)
    time.sleep(60)  # Tunggu selama 1 menit
