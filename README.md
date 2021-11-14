# Tugas Besar 2 IF2123 Aljabar Linear dan Geometri 

## Deskripsi Program
Program ini dibuat untuk memenuhi Tugas Besar 2 IF2123 Aljabar Linear dan Geometri. Program ini dibuat dengan modul Flask pada Python untuk pembuatan backend dan kombinasi HTML, CSS, dan Javascript untuk membuat tampilan depan dari website. 

Fitur yang terdapat di dalam website :
1. Kompresi gambar dengan presentase antara 1 hingga 100 persen
2. Menampilkan lama waktu kompresi gambar dan presentase pixel yang dikompresi.
3. Gambar hasil kompresi dapat diunduh.

Folder yang terdapat di dalam program:
1. `docs` berisi laporan Tugas Besar.
2. `src` berisi source code program, baik backend maupun frontend.
3. `test` berisi file gambar untuk pengetesan program.

## Cara Instalasi dan Penggunaan Website
1. Clone repository
    ```bash
    git clone https://github.com/geraldabrhm/Algeo02-20116.git
    ```
2. Masuk ke dalam folder `src`
    ```bash
    cd src
    ```
3. Aktifkan virtual environtment
    ```bash
    env\Scripts\activate
    ```
4. Jalankan file `server.py`
    ```bash
    py server.py
    ```
5. Website akan berjalan pada `http://127.0.0.1:5000/`
![hompage](./src/static/Image/landingpage.jpg?raw=true)
6. Masukkan nilai `k` dan upload gambar yang akan dikompresi
![uploadImage](./src/static/Image/uploadImage.jpg?raw=true)
7. Tekan tombol `COMPRESS` dan tunggu beberapa saat
8. Gambar berhasil dikompresi dan dapat didownload
![hasilKompresi](./src/static/Image/hasilKompresi.jpg?raw=true)

## Anggota Kelompok
Program ini dibuat oleh Kelompok 3Maskethir yang beranggotakan:
1. Mahesa Lizardy (13520116)
2. Hafidz Nur Rahman Ghozali (13520117)
3. Gerald Abraham Sianturi (13520138)