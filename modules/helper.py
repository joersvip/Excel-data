import os
import random
from datetime import datetime, timedelta
import pandas as pd

def format_currency(val: float) -> str:
    """Format numeric value as Indonesian Rupiah (IDR)."""
    try:
        return f"Rp {val:,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return str(val)

def format_date(val) -> str:
    """Format date to DD-MM-YYYY."""
    if pd.isna(val):
        return "-"
    if isinstance(val, (datetime, pd.Timestamp)):
        return val.strftime("%d-%m-%Y")
    try:
        dt = pd.to_datetime(val)
        return dt.strftime("%d-%m-%Y")
    except Exception:
        return str(val)

def ensure_sample_data(file_path: str) -> None:
    """Ensure that a sample Excel file exists at the given path with 1000+ realistic records."""
    if os.path.exists(file_path):
        return

    # Ensure parent directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Try to build from the 4 CSV parts first (the user's actual dataset)
    part1_path = "data/part1.csv"
    if os.path.exists(part1_path):
        try:
            df1 = pd.read_csv(part1_path)
            dfs = [df1]
            for i in range(2, 5):
                part_path = f"data/part{i}.csv"
                if os.path.exists(part_path):
                    df_part = pd.read_csv(part_path, header=None, names=df1.columns)
                    dfs.append(df_part)
            
            df_merged = pd.concat(dfs, ignore_index=True)
            df_merged['Pagu (Rp)'] = pd.to_numeric(df_merged['Pagu (Rp)'], errors='coerce')
            df_merged['ID'] = pd.to_numeric(df_merged['ID'], errors='coerce')
            df_merged['No'] = range(1, len(df_merged) + 1)
            
            df_merged.to_excel(file_path, index=False, engine='openpyxl')
            return
        except Exception as e:
            print(f"Error rebuilding Excel from CSV parts: {str(e)}")

    # Fallback: Generate 1000+ realistic procurement/RUP rows if CSVs are not found
    pakets = [
        "Pengadaan Alat Tulis Kantor", "Belanja Alat Listrik dan Elektronik",
        "Pemeliharaan AC Ruang Kantor", "Belanja Bahan Komputer",
        "Pengadaan Pakaian Dinas Harian", "Pembangunan Gedung Kantor",
        "Sewa Kendaraan Operasional", "Belanja Jasa Kebersihan",
        "Belanja Jasa Keamanan", "Sewa Mesin Fotokopi",
        "Belanja Makanan dan Minuman Kegiatan", "Pengadaan Suku Cadang Kendaraan",
        "Rehabilitasi Jalan Lingkungan", "Penyusunan Rencana Tata Ruang",
        "Pengadaan Server Core IT", "Sewa Lisensi Cloud Antivirus"
    ]
    jenis_pengadaans = ["Barang", "Pekerjaan Konstruksi", "Jasa Lainnya", "Jasa Konsultansi"]
    metodes = ["E-Purchasing", "Pengadaan Langsung", "Tender", "Penunjukan Langsung", "Tender Cepat"]
    pdn_status = ["Produk Dalam Negeri", "Impor"]
    usaha_kecil = ["Usaha Kecil/Koperasi", "Bukan Usaha Kecil"]
    klpd_list = ["Kab. Barru", "Kementerian Kehakiman", "Mahkamah Agung", "Kementerian Keuangan", "Provinsi Sulawesi Selatan"]
    satkers = ["BAGIAN UMUM", "DINAS KESEHATAN", "PENGADILAN NEGERI BARRU", "DINAS PENDIDIKAN", "BADAN KEUANGAN DAERAH"]
    lokasis = ["Sulawesi Selatan, Barru (Kab.)", "Sulawesi Selatan, Makassar (Kota)", "DKI Jakarta, Jakarta Pusat"]

    data = []
    for i in range(1, 1051):
        paket_base = random.choice(pakets)
        paket = f"{paket_base} - Paket {i}"
        pagu = random.randint(1000000, 500000000)
        jenis = random.choice(jenis_pengadaans)
        pdn = random.choice(pdn_status)
        uk = random.choice(usaha_kecil)
        metode = random.choice(metodes)
        waktu = f"January 2026"
        klpd = random.choice(klpd_list)
        satker = random.choice(satkers)
        lokasi = random.choice(lokasis)
        id_rup = random.randint(60000000, 69000000)

        data.append({
            "No": i,
            "Paket": paket,
            "Pagu (Rp)": pagu,
            "Jenis Pengadaan": jenis,
            "Produk Dalam Negeri": pdn,
            "Usaha Kecil/Koperasi": uk,
            "Metode": metode,
            "Pemilihan": waktu,
            "K/L/PD": klpd,
            "Satuan Kerja": satker,
            "Lokasi": lokasi,
            "ID": id_rup
        })

    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False, engine='openpyxl')

