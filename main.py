import os
import time
import datetime
import subprocess
from mega import Mega
import shutil

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

# Fungsi untuk melakukan backup directory ccgnimex.my.id dan mengompresnya menjadi file zip
def backup_directory():
    source_dir = '/www/wwwroot/ccgnimex.my.id'
    backup_dir = '/www/wwwroot'  # Direktori untuk menyimpan file backup zip

    # Generate nama file backup dengan format timestamp
    backup_file_name = datetime.datetime.now().strftime("%Y-%m-%d") + '.zip'
    backup_file_path = os.path.join(backup_dir, backup_file_name)

    # Kompres direktori ccgnimex.my.id menjadi file zip
    shutil.make_archive(backup_file_path[:-4], 'zip', source_dir)

    return backup_file_path

# Fungsi untuk mengunggah file ke Mega
def upload_to_mega(file_path, file_type):
    mega = Mega()
    m = mega.login('myudi422@gmail.com', 'cinangka03')  # Ganti dengan email dan password Mega Anda

    # Dapatkan daftar file di direktori root Mega
    files = m.get_files()

    # Filter file zip atau sql yang relevan
    if file_type == 'zip':
        backup_files = [file for file in files.values() if file['a']['n'].endswith('.zip')]
    else:
        backup_files = [file for file in files.values() if file['a']['n'].endswith('.sql')]

    # Jika ada lebih dari 1 file, hapus file backup tertua
    if len(backup_files) > 1:
        # Urutkan file berdasarkan waktu pembuatan
        backup_files.sort(key=lambda x: x['ts'])
        oldest_file = backup_files[0]
        m.delete(oldest_file['h'])

    # Upload file baru
    m.upload(file_path)

    print(f'File {os.path.basename(file_path)} berhasil diunggah ke Mega')

# Fungsi untuk menunggu hingga salah satu dari empat waktu yang ditentukan
def wait_until_next_backup_time():
    now = datetime.datetime.now()
    next_times = [
        datetime.datetime(now.year, now.month, now.day, 0, 0),
        datetime.datetime(now.year, now.month, now.day, 6, 0),
        datetime.datetime(now.year, now.month, now.day, 12, 0),
        datetime.datetime(now.year, now.month, now.day, 18, 0)
    ]

    # Jika sekarang sudah melewati waktu-waktu tersebut, pindahkan ke hari berikutnya
    next_times = [time if time > now else time + datetime.timedelta(days=1) for time in next_times]

    # Dapatkan waktu berikutnya yang terdekat
    next_backup_time = min(next_times)
    time_to_wait = (next_backup_time - now).total_seconds()
    print(f'Menunggu hingga {next_backup_time}')
    time.sleep(time_to_wait)

# Jalankan backup dan upload empat kali sehari
while True:
    wait_until_next_backup_time()
    backup_file_path = backup_database()
    upload_to_mega(backup_file_path, file_type='sql')
    backup_file_path = backup_directory()
    upload_to_mega(backup_file_path, file_type='zip')
