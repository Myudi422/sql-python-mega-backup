import os
import time
import datetime
from mega import Mega
import shutil

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
def upload_to_mega(file_path):
    mega = Mega()
    m = mega.login('myudi422@gmail.com', 'cinangka03')  # Ganti dengan email dan password Mega Anda

    # Dapatkan daftar file di direktori root Mega
    files = m.get_files()

    # Filter file zip yang relevan
    backup_files = [file for file in files.values() if file['a']['n'].endswith('.zip')]

    # Jika ada lebih dari 1 file, hapus file backup tertua
    if len(backup_files) > 1:
        # Urutkan file berdasarkan waktu pembuatan
        backup_files.sort(key=lambda x: x['ts'])
        oldest_file = backup_files[0]
        m.delete(oldest_file['h'])

    # Upload file baru
    m.upload(file_path)

    print(f'File {os.path.basename(file_path)} berhasil diunggah ke Mega')

# Atur jadwal eksekusi sekali sehari
schedule_time = datetime.time(0, 0)  # Atur waktu eksekusi ke tengah malam (00:00)

while True:
    # Dapatkan waktu saat ini
    current_time = datetime.datetime.now().time()

    # Periksa apakah waktu saat ini sama dengan waktu jadwal
    if current_time.hour == schedule_time.hour and current_time.minute == schedule_time.minute:
        backup_file_path = backup_directory()
        upload_to_mega(backup_file_path)
        time.sleep(86400)  # Tunggu 1 hari (86400 detik)
    else:
        # Tunggu 10 detik sebelum memeriksa kembali
        time.sleep(10)
