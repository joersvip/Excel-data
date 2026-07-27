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

## 💻 Panduan Instalasi & Menjalankan Aplikasi

Aplikasi ini dapat dijalankan langsung menggunakan skrip otomatis yang telah disediakan khusus untuk lingkungan Linux, atau dijalankan secara manual pada sistem operasi lain (Windows/macOS).

### A. Cara Instan di Linux (Direkomendasikan)

Kami telah menyertakan skrip shell (`.sh`) otomatis untuk memudahkan pengaturan lingkungan dan menjalankan aplikasi di sistem Linux Anda tanpa repot.

1. **Jalankan Aplikasi dengan Satu Perintah**:
   Skrip ini akan mendeteksi Python, membuat Virtual Environment (`.venv`) otomatis, menginstal semua pustaka pendukung dari `requirements.txt`, menggenerasi aset grafis, dan langsung meluncurkan aplikasi:
   ```bash
   ./run_linux.sh
   ```

2. **Integrasi ke Menu Aplikasi Desktop Linux (Application Launcher)**:
   Jika Anda ingin aplikasi ini muncul di menu pencarian sistem Linux Anda (seperti GNOME, KDE, XFCE) lengkap dengan logo ikonnya sehingga dapat diklik langsung tanpa membuka terminal:
   ```bash
   ./install_desktop.sh
   ```
   *Setelah skrip dijalankan, Anda dapat menekan tombol `Super/Windows` di keyboard Anda, mengetik **"Excel Data Center"**, dan langsung meluncurkannya dari sana.*

---

### B. Cara Manual (Semua OS: Windows, macOS, Linux)

Jika Anda ingin menjalankan atau mengatur lingkungan secara manual langkah demi langkah:

1. **Buat Virtual Environment**:
   ```bash
   python3 -m venv .venv
   ```

2. **Aktifkan Virtual Environment**:
   - **Windows (PowerShell)**:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - **Windows (CMD)**:
     ```cmd
     .venv\Scripts\activate.bat
     ```
   - **Linux / macOS**:
     ```bash
     source .venv/bin/activate
     ```

3. **Instal Dependensi**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Jalankan Skrip Pembuatan Aset**:
   ```bash
   python3 create_assets.py
   ```

5. **Luncurkan Aplikasi**:
   ```bash
   python3 main.py
   ```

---

## 📦 Panduan Build/Kompilasi Menjadi Aplikasi Standalone

Anda dapat membungkus seluruh aplikasi Python ini beserta semua pustakanya ke dalam sebuah file biner tunggal (*executable*) yang dapat dijalankan secara langsung tanpa perlu menginstal Python di komputer target.

### 🐧 Mengemas di Lingkungan Linux
Jalankan skrip kompilasi otomatis berikut:
```bash
./package_linux.sh
```
Skrip ini akan menggunakan PyInstaller untuk membuat paket biner mandiri. File executable biner Linux Anda akan berada di:
📁 `dist/excel-data-center`

### 🪟 Mengemas di Lingkungan Windows
1. Aktifkan virtual environment Anda.
2. Jalankan perintah kompilasi berikut di Command Prompt / PowerShell:
   ```powershell
   pyinstaller --noconsole --onefile --add-data "assets;assets" --add-data "data;data" --name "ExcelDataCenter" main.py
   ```
3. File executable Windows Anda akan berada di:
   📁 `dist/ExcelDataCenter.exe`

---

## 📖 Panduan Penggunaan Aplikasi (User Guide)

Aplikasi **Excel Data Center** dirancang dengan antarmuka yang sangat intuitif dan terdiri dari 4 menu navigasi utama di bagian samping kiri:

### 1. 📊 Menu Dashboard
Halaman ini memberikan ikhtisar visual instan mengenai berkas Excel yang sedang aktif:
* **Informasi Berkas**: Menampilkan nama berkas, ukuran penyimpanan, total baris data, jumlah kolom, dan waktu terakhir diubah.
* **Statistik Utama**: Menampilkan total nilai keuangan (akumulasi pagu), rata-rata anggaran, serta nilai transaksi tertinggi.
* **Top Categories**: Menampilkan grafik representasi visual interaktif frekuensi data terbanyak berdasarkan jenis pengadaan atau satuan kerja.

### 2. 🗂️ Menu Data Tabel (Pusat Data)
Ini adalah area kerja utama untuk mengelola spreadsheet Anda:
* **Pagination (Pengaturan Halaman)**: Di bagian bawah tabel, terdapat kontrol navigasi halaman. Anda dapat berpindah halaman dengan tombol `<` dan `>`, serta mengatur jumlah baris yang tampil per halaman (10, 25, 50, atau 100 baris) untuk memuat ratusan ribu data dengan sangat lancar.
* **Pencarian Real-Time**: Ketik kata kunci apa saja pada kolom pencarian di bagian atas. Tabel akan menyaring baris secara otomatis saat Anda mengetik (*search-as-you-type*) tanpa memerlukan tombol submit.
* **Filter Kolom & Pengurutan**: 
  - Pilih kolom tertentu dari dropdown, kemudian pilih nilai unik yang ingin disaring. Nilai pada dropdown filter akan menyesuaikan secara dinamis dengan isi berkas Excel Anda.
  - Klik tombol sortir untuk mengurutkan data secara Menaik (*Ascending*) atau Menurun (*Descending*).
* **Impor Excel Baru**: Klik tombol **"Impor Excel"** di sudut kanan atas untuk membuka file browser lokal dan memuat data berkas `.xlsx` lainnya secara instan.
* **Ekspor Data Terfilter**: Semua data yang sedang tampil di layar (sesuai hasil pencarian dan penyaringan Anda) dapat diekspor langsung menjadi file baru berformat **Excel (.xlsx)**, **CSV (.csv)**, atau **Laporan PDF Resmi** berdesain korporat dengan mengklik tombol ekspor yang relevan.

### 3. 🔍 Panel Detail Master-Detail
* Saat Anda mengklik baris mana saja pada tabel di halaman **Data**, sebuah panel rincian interaktif akan meluncur keluar dari sisi kanan layar.
* Panel ini menyajikan rincian data lengkap dari baris yang Anda pilih secara rapi dan terstruktur.
* Jika data Anda memuat kolom path gambar (misal foto pegawai atau foto barang), aplikasi akan memvisualisasikannya secara otomatis di bagian atas panel detail.

### 4. ⚙️ Menu Pengaturan
Sesuaikan aplikasi agar nyaman bagi produktivitas Anda:
* **Skema Tema**: Aktifkan **Tema Gelap (Dark Mode)** untuk kenyamanan mata di malam hari, atau kembalikan ke **Tema Terang (Light Mode)**.
* **Skala Teks (Font Size)**: Ubah ukuran tulisan di aplikasi menjadi Kecil, Sedang, atau Besar sesuai kenyamanan visual Anda.
* **Berkas Default**: Tentukan lokasi file Excel default yang ingin selalu dibuka secara otomatis setiap kali aplikasi baru dijalankan.

---

## 🔒 Catatan Keamanan & Kepatuhan Data

* **100% Offline & Lokal**: Aplikasi ini bekerja secara murni lokal di dalam komputer Anda. Tidak ada data yang diunggah ke internet, sehingga menjamin kerahasiaan data sensitif perusahaan Anda.
* **Penanganan Kesalahan Kokoh**: EDC dilengkapi dengan validasi kolom cerdas. Jika file Excel Anda memiliki struktur kolom yang berantakan atau tidak seragam, aplikasi akan menanganinya secara aman tanpa terjadi *force close* (crash).
