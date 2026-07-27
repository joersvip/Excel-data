import os
import pandas as pd
import flet as ft
from modules.helper import format_currency, format_date

class DetailPage:
    @staticmethod
    def build_detail_panel(page: ft.Page, record: dict, on_close) -> ft.Control:
        """Build a highly polished vertical side panel/card displaying full record details."""
        theme_mode = page.client_storage.get("theme_mode")
        is_dark = theme_mode == "dark"
        
        text_color = "#f8fafc" if is_dark else ft.Colors.BLUE_GREY_900
        label_color = "#94a3b8" if is_dark else ft.Colors.GREY_600
        bg_color = "#1e2229" if is_dark else ft.Colors.GREY_100
        border_color = "#2d3139" if is_dark else ft.Colors.GREY_300

        # Title and header row
        header = ft.Row([
            ft.Text("Detail Informasi", size=18, weight=ft.FontWeight.BOLD, color=text_color),
            ft.IconButton(
                icon=ft.Icons.CLOSE, 
                icon_color=ft.Colors.RED_400 if is_dark else ft.Colors.RED_600, 
                tooltip="Tutup Detail",
                on_click=lambda _: on_close()
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # Image preview block (if "Foto" column is present)
        image_control = None
        foto_val = record.get("Foto", None)
        
        if foto_val and isinstance(foto_val, str):
            # Check if image file exists or can be displayed
            # We also provide a nice placeholder avatar if not found
            avatar_path = foto_val
            # Ensure it fits in assets path
            if not avatar_path.startswith("assets/"):
                avatar_path = os.path.join("assets", avatar_path)
            
            # Since Flet serves the assets folder, we can reference /exports/ or /avatars/ directly
            # If the path contains assets/, Flet can serve it under /avatars/ or similar, depending on how assets_dir is configured.
            # Usually, if assets_dir="assets", then "assets/avatars/avatar_1.png" is served at "/avatars/avatar_1.png" (without "assets/").
            # Let's adjust the path for Flet's web server!
            web_img_path = foto_val
            if web_img_path.startswith("assets/"):
                web_img_path = web_img_path[7:]  # Strip "assets/" prefix for serving
                
            image_control = ft.Container(
                content=ft.Image(
                    src=web_img_path,
                    width=110,
                    height=110,
                    fit=ft.ImageFit.COVER,
                    border_radius=12,
                    error_content=ft.Container(
                        content=ft.Icon(ft.Icons.PERSON, size=50, color=ft.Colors.GREY_500),
                        bgcolor=ft.Colors.GREY_800 if is_dark else ft.Colors.GREY_300,
                        border_radius=12,
                        alignment=ft.alignment.center,
                        width=110,
                        height=110,
                    )
                ),
                border=ft.border.all(2, "#3b82f6" if is_dark else ft.Colors.BLUE_600),
                border_radius=14,
                padding=2,
                alignment=ft.alignment.center,
                margin=ft.margin.only(bottom=15)
            )

        # Detail items (rows of key-value pairs)
        detail_items = []
        
        # Display primary identifying info at top if available
        primary_title = record.get("Nama Lengkap", record.get("Nama", ""))
        primary_subtitle = record.get("ID Karyawan", record.get("ID", ""))
        
        if primary_title:
            detail_items.append(
                ft.Column([
                    ft.Text(str(primary_title), size=16, weight=ft.FontWeight.BOLD, color=text_color, text_align=ft.TextAlign.CENTER),
                    ft.Text(str(primary_subtitle), size=12, italic=True, color=label_color, text_align=ft.TextAlign.CENTER) if primary_subtitle else ft.Container()
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2)
            )
            detail_items.append(ft.Divider(height=15, color=border_color))

        # Show other fields
        grid_fields = []
        for col_name, value in record.items():
            if col_name in ["Foto", "Nama Lengkap", "Nama", "ID Karyawan", "ID"]:
                continue  # Already handled or skipped
                
            # Formatting values for beautiful display
            display_val = str(value)
            if "Gaji" in col_name or "Penjualan" in col_name:
                try:
                    display_val = format_currency(float(value))
                except Exception:
                    pass
            elif "Tanggal" in col_name:
                display_val = format_date(value)
            elif pd.isna(value) if hasattr(value, 'isna') else (value is None or value == 'nan'):
                display_val = "-"

            grid_fields.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(col_name, size=11, color=label_color, weight=ft.FontWeight.W_500),
                        ft.Text(display_val, size=13, weight=ft.FontWeight.BOLD, color=text_color, overflow=ft.TextOverflow.ELLIPSIS),
                    ], spacing=2, tight=True),
                    bgcolor=ft.Colors.with_opacity(0.04 if is_dark else 0.5, ft.Colors.BLACK) if not is_dark else "#1a1d23",
                    padding=10,
                    border_radius=8,
                    border=ft.border.all(1, border_color),
                )
            )

        grid_container = ft.Column(grid_fields, spacing=8, scroll=ft.ScrollMode.ADAPTIVE)
        
        panel_content = ft.Container(
            bgcolor=bg_color,
            padding=20,
            border_radius=12,
            border=ft.border.all(1, border_color),
            width=320,
            content=ft.Column([
                header,
                ft.Divider(height=10, color=border_color),
                ft.Column([
                    image_control if image_control else ft.Container(),
                    grid_container
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.ADAPTIVE, expand=True)
            ], spacing=10, expand=True)
        )
        
        return panel_content
