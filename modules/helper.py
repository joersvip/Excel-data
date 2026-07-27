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

    # Lists for random generation
    first_names = ["Budi", "Andi", "Siti", "Dewi", "Rian", "Eko", "Joko", "Sari", "Laras", "Hendra", 
                   "Aris", "Mega", "Dian", "Putri", "Rudi", "Ahmad", "Taufik", "Ina", "Yudi", "Rina"]
    last_names = ["Santoso", "Wijaya", "Kusuma", "Pratama", "Hidayat", "Saputra", "Lestari", "Wulandari", 
                  "Gunawan", "Setiawan", "Purnama", "Siregar", "Nasution", "Hadi", "Utomo", "Kartika"]
    departments = ["Sales & Marketing", "Information Technology", "Human Resources", "Finance & Accounting", "Operations", "Legal"]
    cities = ["Jakarta", "Surabaya", "Bandung", "Medan", "Semarang", "Makassar", "Yogyakarta", "Balikpapan", "Denpasar", "Palembang"]
    statuses = ["Aktif", "Cuti", "Resign"]

    data = []
    start_date = datetime(2018, 1, 1)

    for i in range(1, 1201):  # Generate 1200 rows of data
        emp_id = f"EMP-{1000 + i}"
        nama = f"{random.choice(first_names)} {random.choice(last_names)}"
        dept = random.choice(departments)
        gaji = random.randint(5000000, 25000000)
        penjualan = random.randint(10000000, 150000000) if dept == "Sales & Marketing" else 0
        tanggal = start_date + timedelta(days=random.randint(0, 2500))
        status = random.choices(statuses, weights=[0.85, 0.10, 0.05])[0]
        kota = random.choice(cities)
        email = f"{nama.lower().replace(' ', '.')}@perusahaan.co.id"
        
        # We can put a path or URL for image
        foto = f"assets/avatars/avatar_{(i % 5) + 1}.png"

        data.append({
            "No": i,
            "ID Karyawan": emp_id,
            "Nama Lengkap": nama,
            "Departemen": dept,
            "Gaji (Rp)": gaji,
            "Total Penjualan (Rp)": penjualan,
            "Tanggal Masuk": tanggal.strftime("%Y-%m-%d"),
            "Status Kerja": status,
            "Email": email,
            "Kota": kota,
            "Foto": foto
        })

    df = pd.DataFrame(data)
    
    # Save to Excel
    df.to_excel(file_path, index=False, engine='openpyxl')
