# Excel Data Center (EDC)

**Excel Data Center** adalah aplikasi desktop offline *enterprise-grade* modern yang dibangun menggunakan **Python 3.13** dan **Flet UI**. Aplikasi ini dirancang khusus untuk memuat, mencari, memfilter, menganalisis, dan mengekspor data dari file Microsoft Excel (`.xlsx` atau `.xls`) secara instan dan 100% offline (aman tanpa server, tanpa koneksi internet, dan tanpa database online).

---

## 🚀 Fitur Utama

1. **Dashboard Utama Modern**: 
   - Ringkasan metadata berkas aktif (Nama Berkas, Ukuran, Jumlah Kolom & Baris, Tanggal Pembaruan).
   - Analitik deskriptif kilat (Rata-rata, Akumulasi, Kategori Teratas).
   
2. **Eksplorasi Data Berkinerja Tinggi**:
   - Menampilkan data Excel menggunakan `DataTable` interaktif.
   - Menggunakan algoritma **Pagination** cerdas (opsi 10, 25, 50, atau 100 baris per halaman) sehingga mampu memuat lembar kerja berukuran besar (**10.000+, 50.000+, hingga 100.000+ baris**) dengan lancar tanpa lag maupun crash.
   - Penomoran urut otomatis dan bar navigasi halaman yang intuitif.

3. **Pencarian Real-Time (Tanpa Tombol)**:
   - Pencarian instan dan responsif yang memindai semua kolom secara bersamaan saat Anda mengetik.

4. **Penyaringan & Pengurutan Fleksibel**:
   - Penyaringan data dinamis berdasarkan nama kolom pilihan dan nilai kolom unik (Dropdown nilai otomatis terisi berdasarkan data Excel aktual).
   - Pengurutan data tingkat lanjut (A-Z, Z-A, Ascending, Descending) pada kolom apa saja.

5. **Panel Detail Master-Detail**:
   - Memilih baris data akan menampilkan panel detail di sisi kanan secara mulus.
   - Menampilkan seluruh isi rekaman secara terstruktur.
   - Deteksi otomatis kolom "Foto" (mendukung tampilan berkas gambar lokal maupun eksternal).

6. **Impor & Ekspor Mandiri**:
   - Impor berkas `.xlsx` baru secara instan melalui tombol **Impor Excel** dengan dialog File Picker asli.
   - Ekspor data hasil filter/pencarian Anda ke format **Excel (.xlsx)**, **CSV (.csv)**, atau laporan cetak **PDF (.pdf)** dengan tata letak korporat.

7. **Pengaturan Personalisasi**:
   - Mengubah skema tema secara instan antara **Tema Gelap (Dark Mode)** dan **Tema Terang (Light Mode)**.
   - Menentukan lokasi berkas Excel default.
   - Menyesuaikan skala tipografi antarmuka pengguna (Kecil, Sedang, Besar) untuk kemudahan membaca.

---

## 📂 Struktur Proyek

```text
project/
│
├── main.py                 # File entry-point utama aplikasi
│
├── assets/
│      logo.png             # Logo aplikasi (dan folder untuk static files)
│      exports/             # Direktori penyimpanan hasil ekspor data (XLSX, CSV, PDF)
│      avatars/             # Direktori penyimpanan contoh foto avatar data
│
├── data/
│      data.xlsx            # File database Excel default (otomatis dibuat jika kosong)
│
├── modules/
│      excel_reader.py      # Core logic pembacaan dan validasi Excel (Pandas + Openpyxl)
│      search.py            # Mesin pencarian data realtime vektor
│      filter.py            # Operasi penyaringan nilai unik dan pengurutan dataframe
│      statistics.py        # Analisis statistik deskriptif dan kategorikal otomatis
│      export.py            # Modul penulisan output CSV, Excel, dan pembuatan laporan PDF (FPDF2)
│      helper.py            # Fungsi pemformatan mata uang, tanggal, dan generator data sampel
│
├── pages/
│      dashboard.py         # Halaman visualisasi data ringkas utama
│      data_page.py         # Halaman manajemen tabel data, pencarian, dan impor/ekspor
│      detail_page.py       # Panel samping modular penampil detail baris terpilih
│      settings.py          # Halaman konfigurasi tema, font, dan default file
│
├── requirements.txt        # Daftar dependensi modul Python
│
└── README.md               # Dokumentasi panduan operasional proyek
```

---

## 💻 Cara Menjalankan Aplikasi Secara Lokal

### Prasyarat
Pastikan komputer Anda sudah terinstal **Python 3.11 atau versi lebih baru (direkomendasikan Python 3.13)**.

### Langkah-Langkah:

1. **Unduh atau Salin Proyek**:
   Buka terminal/command prompt di direktori proyek ini.

2. **Buat Virtual Environment (Opsional namun Sangat Direkomendasikan)**:
   ```bash
   python -m venv venv
   ```

3. **Aktifkan Virtual Environment**:
   - **Windows (CMD)**:
     ```cmd
     venv\Scripts\activate
     ```
   - **macOS / Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Instal Dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Jalankan Aplikasi**:
   ```bash
   python main.py
   ```
   *(Aplikasi akan otomatis mendeteksi ketiadaan data default dan membuat data dummy sebanyak 1.200 baris lengkap dengan kategori departemen, nominal gaji, penjualan, kota, dan avatar sehingga Anda dapat langsung mencobanya!)*

---

## 📦 Panduan Build Menjadi File Executable (.exe)

Anda dapat mengemas aplikasi Python ini menjadi satu berkas binary `.exe` mandiri yang dapat langsung diklik oleh pengguna akhir di Windows (bahkan tanpa harus menginstal Python di komputer mereka) menggunakan **PyInstaller**.

### Langkah Kompilasi:

1. Pastikan Anda berada dalam lingkungan virtual environment aktif dan semua dependensi terinstal.
2. Jalankan perintah kompilasi PyInstaller berikut:

   ```bash
   pyinstaller --noconsole --onefile --add-data "assets;assets" --add-data "data;data" --name "ExcelDataCenter" main.py
   ```

   **Penjelasan Parameter Perintah:**
   - `--noconsole`: Menyembunyikan jendela hitam terminal (command prompt) saat aplikasi dijalankan, sehingga murni memunculkan antarmuka grafis (GUI).
   - `--onefile`: Membundel seluruh kode, pustaka, dan dependensi ke dalam satu file `.exe` tunggal di direktori `dist/`.
   - `--add-data "assets;assets"`: Memasukkan seluruh aset statis (termasuk folder ekspor dan avatar) ke dalam paket executable.
   - `--add-data "data;data"`: Menyertakan folder data Excel default bawaan ke dalam paket executable.
   - `--name "ExcelDataCenter"`: Menamai file keluaran menjadi `ExcelDataCenter.exe`.

3. Setelah proses kompilasi selesai (sekitar 1-2 menit), silakan temukan file executable Anda di folder hasil keluaran:
   `dist/ExcelDataCenter.exe`

4. Anda dapat membagikan file `.exe` tersebut kepada pengguna lain. Mereka dapat menggunakannya langsung secara instan tanpa perlu koneksi internet.

---

## 🔒 Catatan Keamanan & Kepatuhan Data

- **Keamanan Penuh**: EDC beroperasi sepenuhnya secara lokal di komputer klien. Data Anda tidak pernah diunggah ke internet atau server cloud pihak ketiga mana pun.
- **Validasi Berkas Tangguh**: Aplikasi ini dilengkapi validasi otomatis yang mencegah program terhenti (*force close*) apabila berkas Excel yang dimasukkan rusak, memiliki format kolom tidak seragam, atau kosong.
