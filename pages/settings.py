import flet as ft
from modules.excel_reader import ExcelReader

class SettingsPage:
    def __init__(self, page: ft.Page, on_settings_changed):
        self.page = page
        self.on_settings_changed = on_settings_changed
        
        # Load existing settings from Client Storage or set defaults
        if not self.page.client_storage.contains("theme_mode"):
            self.page.client_storage.set("theme_mode", "dark")
        if not self.page.client_storage.contains("excel_path"):
            self.page.client_storage.set("excel_path", "data/data.xlsx")
        if not self.page.client_storage.contains("font_size"):
            self.page.client_storage.set("font_size", "Sedang")

    def build(self) -> ft.Control:
        theme_mode = self.page.client_storage.get("theme_mode")
        excel_path = self.page.client_storage.get("excel_path")
        font_size = self.page.client_storage.get("font_size")

        # UI elements
        theme_dropdown = ft.Dropdown(
            label="Tema Tampilan",
            value=theme_mode,
            options=[
                ft.dropdown.Option("dark", "Tema Gelap (Dark)"),
                ft.dropdown.Option("light", "Tema Terang (Light)"),
            ],
            width=400,
            border_radius=8,
            border_color="#3b82f6" if theme_mode == "dark" else ft.Colors.BLUE_700,
        )

        excel_input = ft.TextField(
            label="Lokasi File Excel Default",
            value=excel_path,
            width=400,
            border_radius=8,
            border_color="#3b82f6" if theme_mode == "dark" else ft.Colors.BLUE_700,
        )

        font_dropdown = ft.Dropdown(
            label="Ukuran Font UI",
            value=font_size,
            options=[
                ft.dropdown.Option("Kecil", "Kecil (12px)"),
                ft.dropdown.Option("Sedang", "Sedang (14px)"),
                ft.dropdown.Option("Besar", "Besar (16px)"),
            ],
            width=400,
            border_radius=8,
            border_color="#3b82f6" if theme_mode == "dark" else ft.Colors.BLUE_700,
        )

        def save_settings(e):
            old_path = self.page.client_storage.get("excel_path")
            new_path = excel_input.value.strip()

            self.page.client_storage.set("theme_mode", theme_dropdown.value)
            self.page.client_storage.set("excel_path", new_path)
            self.page.client_storage.set("font_size", font_dropdown.value)

            # If Excel file path changed, reload ExcelReader active file path
            if old_path != new_path:
                ExcelReader.set_active_file_path(new_path)

            # Trigger global update
            self.on_settings_changed()
            
            # Show snackbar notification
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Pengaturan berhasil disimpan!", color=ft.Colors.WHITE),
                background_color=ft.Colors.GREEN_600,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()

        save_btn = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.SAVE, size=18, color=ft.Colors.WHITE),
                ft.Text("Simpan Pengaturan", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
            ], tight=True),
            style=ft.ButtonStyle(
                background_color=ft.Colors.BLUE_600,
                padding=ft.padding.symmetric(horizontal=24, vertical=14),
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=save_settings
        )

        content = ft.Container(
            padding=30,
            expand=True,
            content=ft.Column([
                ft.Text("Pengaturan Aplikasi", size=24, weight=ft.FontWeight.BOLD, 
                        color="#3b82f6" if theme_mode == "dark" else ft.Colors.BLUE_800),
                ft.Text("Konfigurasi preferensi tampilan, font, dan lokasi file data default.", size=14, color=ft.Colors.GREY_500),
                ft.Divider(height=20, color="#2d3139" if theme_mode == "dark" else ft.Colors.GREY_300),
                ft.VerticalDivider(width=10),
                
                ft.Column([
                    ft.Text("Tampilan & Warna", size=16, weight=ft.FontWeight.BOLD),
                    theme_dropdown,
                    ft.Text("Atur skema warna dasar aplikasi.", size=12, color=ft.Colors.GREY_500),
                ], spacing=8),
                
                ft.Divider(height=20, color=ft.Colors.transparent),
                
                ft.Column([
                    ft.Text("Lokasi Data", size=16, weight=ft.FontWeight.BOLD),
                    excel_input,
                    ft.Text("Path file spreadsheet (.xlsx) yang otomatis dimuat saat aplikasi dibuka.", size=12, color=ft.Colors.GREY_500),
                ], spacing=8),
                
                ft.Divider(height=20, color=ft.Colors.transparent),
                
                ft.Column([
                    ft.Text("Tipografi", size=16, weight=ft.FontWeight.BOLD),
                    font_dropdown,
                    ft.Text("Skala ukuran teks pada seluruh antarmuka pengguna.", size=12, color=ft.Colors.GREY_500),
                ], spacing=8),
                
                ft.Divider(height=30, color="#2d3139" if theme_mode == "dark" else ft.Colors.GREY_300),
                save_btn
            ], spacing=20, scroll=ft.ScrollMode.ADAPTIVE)
        )
        
        return content
