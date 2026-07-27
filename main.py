import os
import flet as ft
from modules.helper import ensure_sample_data
from modules.excel_reader import ExcelReader
from pages.dashboard import DashboardPage
from pages.data_page import DataPage
from pages.statistics import StatisticsPage
from pages.settings import SettingsPage

def main(page: ft.Page):
    # Set window parameters (relevant for local desktop execution)
    page.title = "Excel Data Center"
    page.window_width = 1250
    page.window_height = 800
    page.window_min_width = 900
    page.window_min_height = 650
    
    # Ensure sample data exists on launch
    excel_path = page.client_storage.get("excel_path") or "data/data.xlsx"
    ensure_sample_data(excel_path)
    ExcelReader.set_active_file_path(excel_path)

    # Load initial settings from client storage
    theme_mode = page.client_storage.get("theme_mode") or "dark"
    is_dark_init = theme_mode == "dark"
    page.theme_mode = ft.ThemeMode.DARK if is_dark_init else ft.ThemeMode.LIGHT
    page.bgcolor = "#0f1115" if is_dark_init else ft.Colors.GREY_50
    
    font_size = page.client_storage.get("font_size") or "Sedang"
    if font_size == "Kecil":
        page.text_scale = 0.88
    elif font_size == "Besar":
        page.text_scale = 1.12
    else:
        page.text_scale = 1.00

    # Current view state
    current_view_name = "dashboard"

    # Handler for global UI and theme refresh
    def apply_settings_change():
        t_mode = page.client_storage.get("theme_mode")
        is_dark = (t_mode == "dark")
        page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
        page.bgcolor = "#0f1115" if is_dark else ft.Colors.GREY_50
        
        # Update content area background
        content_area.bgcolor = "#0f1115" if is_dark else ft.Colors.GREY_50
        
        # Update sidebar styles
        sidebar.bgcolor = "#1a1d23" if is_dark else ft.Colors.GREY_100
        sidebar.border = ft.border.only(right=ft.border.BorderSide(1, "#2d3139" if is_dark else ft.Colors.GREY_300))
        
        # Update sidebar header text color
        sidebar_header.content.controls[0].controls[1].color = "#f8fafc" if is_dark else ft.Colors.BLUE_GREY_900
        sidebar_header.content.controls[0].controls[0].color = "#3b82f6" if is_dark else ft.Colors.BLUE_600
        sidebar_header.content.controls[1].color = "#3b82f6" if is_dark else ft.Colors.BLUE_500
        
        # Update about button colors
        about_btn.content.controls[0].color = "#94a3b8" if is_dark else ft.Colors.GREY_700
        about_btn.content.controls[1].color = "#cbd5e1" if is_dark else ft.Colors.GREY_800
        
        f_size = page.client_storage.get("font_size")
        if f_size == "Kecil":
            page.text_scale = 0.88
        elif f_size == "Besar":
            page.text_scale = 1.12
        else:
            page.text_scale = 1.00
            
        page.update()
        
        # Re-build page contents
        navigate_to(current_view_name)

    # 1. Page Instantiations
    dashboard_page = DashboardPage(page, on_page_navigate=lambda dest: navigate_to(dest))
    
    def on_excel_reloaded():
        # Re-instantiate statistics and dashboard to pick up new excel schema
        nonlocal dashboard_page, statistics_page
        dashboard_page = DashboardPage(page, on_page_navigate=lambda dest: navigate_to(dest))
        statistics_page = StatisticsPage(page)

    data_page = DataPage(page, on_data_reloaded=on_excel_reloaded)
    statistics_page = StatisticsPage(page)
    settings_page = SettingsPage(page, on_settings_changed=apply_settings_change)

    # Content wrapper
    content_area = ft.Container(expand=True, bgcolor="#0f1115" if is_dark_init else ft.Colors.GREY_50)

    # Navigate to target view helper
    def navigate_to(view_name: str):
        nonlocal current_view_name
        current_view_name = view_name
        is_dark = page.theme_mode == ft.ThemeMode.DARK
        
        # Reset sidebar highlights
        for key, btn in nav_buttons.items():
            is_active = (key == view_name)
            btn.bgcolor = "#242831" if (is_active and is_dark) else (
                ft.Colors.BLUE_100 if (is_active and not is_dark) else ft.Colors.transparent
            )
            # Accent styling
            btn.content.controls[0].color = "#3b82f6" if (is_active and is_dark) else (
                ft.Colors.BLUE_700 if (is_active and not is_dark) else (
                    "#94a3b8" if is_dark else ft.Colors.GREY_700
                )
            )
            btn.content.controls[1].color = "#3b82f6" if (is_active and is_dark) else (
                ft.Colors.BLUE_900 if (is_active and not is_dark) else (
                    "#cbd5e1" if is_dark else ft.Colors.GREY_800
                )
            )
            btn.update()

        # Mount target content
        if view_name == "dashboard":
            content_area.content = dashboard_page.build()
        elif view_name == "data_page":
            content_area.content = data_page.build()
        elif view_name == "statistics":
            content_area.content = statistics_page.build()
        elif view_name == "settings":
            content_area.content = settings_page.build()
            
        content_area.update()

    # Show About Dialog
    def show_about_dialog(e):
        about_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.INFO_OUTLINE, color=ft.Colors.BLUE_400),
                ft.Text("Tentang Excel Data Center", weight=ft.FontWeight.BOLD)
            ], spacing=10),
            content=ft.Column([
                ft.Text("Excel Data Center adalah aplikasi desktop offline enterprise-grade untuk mengelola, menyaring, mencari, mengekspor, dan menganalisis data lembar kerja Microsoft Excel (.xlsx) Anda secara instan.", size=13),
                ft.Divider(height=10, color=ft.Colors.transparent),
                ft.Text("Spesifikasi Sistem:", weight=ft.FontWeight.BOLD, size=13),
                ft.Text("• Versi Aplikasi: 1.0.0 (Stable)\n• Framework GUI: Flet (Python)\n• Engine Data: Pandas & Openpyxl\n• Pengembang: Senior Python & UI Engineer", size=12, color=ft.Colors.GREY_400 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.GREY_600),
                ft.Divider(height=10, color=ft.Colors.transparent),
                ft.Text("Aplikasi berjalan 100% lokal, aman, tanpa memerlukan koneksi internet maupun server eksternal.", size=12, italic=True, color=ft.Colors.BLUE_400)
            ], tight=True, spacing=5, width=420),
            actions=[
                ft.TextButton("Tutup", on_click=lambda _: close_about_dialog(about_dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(about_dialog)
        about_dialog.open = True
        page.update()

    def close_about_dialog(dialog):
        dialog.open = False
        page.update()

    # Navigation sidebar items definition
    def create_nav_item(key: str, icon: str, label: str):
        is_dark = page.theme_mode == ft.ThemeMode.DARK
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=18, color="#94a3b8" if is_dark else ft.Colors.GREY_700),
                ft.Text(label, size=13, weight=ft.FontWeight.W_500, color="#cbd5e1" if is_dark else ft.Colors.GREY_800)
            ], spacing=12),
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            border_radius=8,
            bgcolor=ft.Colors.transparent,
            on_click=lambda _: navigate_to(key),
            on_hover=lambda e: on_nav_hover(e, key),
            margin=ft.margin.only(bottom=5)
        )

    def on_nav_hover(e, key):
        # Apply hover state if it is not the active button
        if key == current_view_name:
            return
        is_hover = e.data == "true"
        is_dark = page.theme_mode == ft.ThemeMode.DARK
        if is_dark:
            e.control.bgcolor = "#242831" if is_hover else ft.Colors.transparent
        else:
            e.control.bgcolor = ft.Colors.GREY_200 if is_hover else ft.Colors.transparent
        e.control.update()

    nav_buttons = {
        "dashboard": create_nav_item("dashboard", ft.Icons.DASHBOARD_ROUNDED, "Dashboard"),
        "data_page": create_nav_item("data_page", ft.Icons.TABLE_CHART_ROUNDED, "Data Excel"),
        "statistics": create_nav_item("statistics", ft.Icons.BAR_CHART_ROUNDED, "Statistik Data"),
        "settings": create_nav_item("settings", ft.Icons.SETTINGS_ROUNDED, "Pengaturan"),
    }

    # "About" button is unique as it triggers a dialog instead of switching pages
    is_dark_now = page.theme_mode == ft.ThemeMode.DARK
    about_btn = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.INFO_ROUNDED, size=18, color="#94a3b8" if is_dark_now else ft.Colors.GREY_700),
            ft.Text("Tentang Aplikasi", size=13, weight=ft.FontWeight.W_500, color="#cbd5e1" if is_dark_now else ft.Colors.GREY_800)
        ], spacing=12),
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        border_radius=8,
        on_click=show_about_dialog,
        on_hover=lambda e: on_nav_hover(e, "about"),
        margin=ft.margin.only(bottom=15)
    )

    sidebar_bg = "#1a1d23" if is_dark_now else ft.Colors.GREY_100
    sidebar_border_color = "#2d3139" if is_dark_now else ft.Colors.GREY_300

    # Sidebar Header branding block
    sidebar_header = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.LAYERS, size=28, color="#3b82f6" if is_dark_now else ft.Colors.BLUE_600),
                ft.Text("Excel Data Center", size=18, weight=ft.FontWeight.BOLD, color="#f8fafc" if is_dark_now else ft.Colors.BLUE_GREY_900)
            ], spacing=10),
            ft.Text("OFFLINE HUB v1.0", size=11, weight=ft.FontWeight.BOLD, color="#3b82f6" if is_dark_now else ft.Colors.BLUE_500)
        ], spacing=2),
        padding=ft.padding.only(left=8, right=8, top=10, bottom=20),
    )

    # Sidebar container layout
    sidebar = ft.Container(
        width=240,
        bgcolor=sidebar_bg,
        border=ft.border.only(right=ft.border.BorderSide(1, sidebar_border_color)),
        padding=16,
        content=ft.Column([
            sidebar_header,
            ft.Column(list(nav_buttons.values()), expand=True),
            about_btn,
            ft.Text("© 2026 EDC Client", size=10, color=ft.Colors.GREY_500, text_align=ft.TextAlign.CENTER)
        ], spacing=10)
    )

    # Main wrapper container
    main_layout = ft.Row([
        sidebar,
        content_area
    ], spacing=0, expand=True)

    # Initial page loads
    page.add(main_layout)
    navigate_to("dashboard")

if __name__ == "__main__":
    # We bind the Flet server to host '0.0.0.0' and port 3000
    # The uploads folder is specified as "uploads" which handles temporary files for browser picker
    # assets_dir is set to "assets" so static exports and graphics are directly downloadable from /
    ft.app(
        target=main, 
        port=3000, 
        host="0.0.0.0", 
        view=ft.AppView.WEB_BROWSER,
        assets_dir="assets",
        upload_dir="uploads"
    )
