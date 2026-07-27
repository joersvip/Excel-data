import os

def generate_assets():
    print("Memulai pembuatan aset gambar...")
    os.makedirs("assets/avatars", exist_ok=True)
    os.makedirs("assets/exports", exist_ok=True)

    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("Pillow belum terinstal. Membuat file placeholder kosong.")
        # Create empty placeholder files if Pillow is not found
        with open("assets/logo.png", "wb") as f:
            f.write(b"")
        for i in range(1, 6):
            with open(f"assets/avatars/avatar_{i}.png", "wb") as f:
                f.write(b"")
        print("Aset placeholder berhasil dibuat.")
        return

    # Draw beautiful modern logo.png
    # Let's create an elegant 256x256 image with green background and spreadsheet-like graphics
    logo = Image.new("RGBA", (256, 256), (30, 41, 59, 255)) # Dark navy
    draw = ImageDraw.Draw(logo)
    
    # Draw green accent rounded rectangle/box
    draw.rounded_rectangle([40, 40, 216, 216], radius=24, fill=(16, 185, 129, 255)) # Emerald Green
    
    # Draw spreadsheet cells/columns inside
    # Header block
    draw.rounded_rectangle([65, 65, 191, 95], radius=6, fill=(255, 255, 255, 255))
    # 3 columns grids
    draw.rounded_rectangle([65, 110, 100, 145], radius=4, fill=(255, 255, 255, 180))
    draw.rounded_rectangle([110, 110, 145, 145], radius=4, fill=(255, 255, 255, 180))
    draw.rounded_rectangle([155, 110, 191, 145], radius=4, fill=(255, 255, 255, 180))
    
    # 3 columns grids (second row)
    draw.rounded_rectangle([65, 160, 100, 195], radius=4, fill=(255, 255, 255, 180))
    draw.rounded_rectangle([110, 160, 145, 195], radius=4, fill=(255, 255, 255, 180))
    draw.rounded_rectangle([155, 160, 191, 195], radius=4, fill=(255, 255, 255, 180))

    logo.save("assets/logo.png", "PNG")
    print("Logo assets/logo.png berhasil dibuat!")

    # Draw 5 distinct avatars (circle silhouette in pastel background)
    colors = [
        (96, 165, 250, 255),  # Pastel Blue
        (52, 211, 153, 255),  # Pastel Green
        (248, 113, 113, 255), # Pastel Red
        (251, 191, 36, 255),  # Pastel Orange
        (192, 132, 252, 255), # Pastel Purple
    ]

    for idx, bg_col in enumerate(colors, start=1):
        avatar = Image.new("RGBA", (150, 150), (255, 255, 255, 0))
        draw_av = ImageDraw.Draw(avatar)
        
        # Circle background
        draw_av.ellipse([10, 10, 140, 140], fill=bg_col)
        
        # Draw user head
        draw_av.ellipse([50, 35, 100, 85], fill=(255, 255, 255, 255))
        
        # Draw user shoulders
        draw_av.chord([25, 90, 125, 170], start=180, end=0, fill=(255, 255, 255, 255))
        
        avatar.save(f"assets/avatars/avatar_{idx}.png", "PNG")
        print(f"Avatar assets/avatars/avatar_{idx}.png berhasil dibuat!")

if __name__ == "__main__":
    generate_assets()
