import pandas as pd
import flet as ft
from modules.excel_reader import ExcelReader
from modules.helper import format_currency

class DashboardPage:
    def __init__(self, page: ft.Page, on_page_navigate):
        self.page = page
        self.on_page_navigate = on_page_navigate

    def build(self) -> ft.Control:
        theme_mode = self.page.client_storage.get("theme_mode")
        is_dark = theme_mode == "dark"
        
        # Color palette based on theme (Elegant Dark vs Light)
        card_bg = "#1e2229" if is_dark else ft.Colors.WHITE
        border_color = "#2d3139" if is_dark else ft.Colors.GREY_300
        text_primary = "#f8fafc" if is_dark else ft.Colors.BLUE_GREY_900
        text_secondary = "#94a3b8" if is_dark else ft.Colors.GREY_600
        card_shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.15 if is_dark else 0.08, ft.Colors.BLACK),
            offset=ft.Offset(0, 4)
        )

        try:
            # Load metadata
            meta = ExcelReader.get_metadata()
            df = ExcelReader.load_data()
        except Exception as e:
            # Fallback metadata if Excel is not loaded or error occurred
            meta = {
                "file_name": "-",
                "file_path": "-",
                "total_rows": 0,
                "total_cols": 0,
                "columns": [],
                "last_updated": "-",
                "file_size": "-"
            }
            df = None

        # Build Stats Cards
        def create_stat_card(title: str, value: str, icon: str, accent_color: str):
            return ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(icon, size=28, color=accent_color),
                        padding=12,
                        bgcolor=ft.Colors.with_opacity(0.12, accent_color),
                        border_radius=10
                    ),
                    ft.Column([
                        ft.Text(title, size=12, color=text_secondary, weight=ft.FontWeight.W_500),
                        ft.Text(value, size=20, color=text_primary, weight=ft.FontWeight.BOLD),
                    ], spacing=2, tight=True, expand=True)
                ], spacing=16, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=card_bg,
                padding=18,
                border_radius=12,
                border=ft.border.all(1, border_color),
                shadow=card_shadow,
                expand=True
            )

        # Create row of key metric cards
        stats_cards = ft.ResponsiveRow([
            ft.col.col(12, sm=6, md=4, lg=2.4, content=create_stat_card("Nama File Aktif", meta["file_name"], ft.Icons.INSERT_DRIVE_FILE, "#3b82f6")),
            ft.col.col(12, sm=6, md=4, lg=2.4, content=create_stat_card("Jumlah Baris", f"{meta['total_rows']:,}".replace(",", "."), ft.Icons.VIEW_LIST, ft.Colors.GREEN_400)),
            ft.col.col(12, sm=6, md=4, lg=2.4, content=create_stat_card("Jumlah Kolom", f"{meta['total_cols']}", ft.Icons.COLUMNS, ft.Colors.ORANGE_400)),
            ft.col.col(12, sm=6, md=4, lg=2.4, content=create_stat_card("Ukuran File", meta["file_size"], ft.Icons.SD_STORAGE, ft.Colors.PURPLE_400)),
            ft.col.col(12, sm=6, md=4, lg=2.4, content=create_stat_card("Update Terakhir", meta["last_updated"], ft.Icons.UPDATE, ft.Colors.RED_400)),
        ], spacing=16)

        # Quick statistics section
        # Calculate some quick statistics if we have a dataframe
        info_widgets = []
        if df is not None and not df.empty:
            # Let's find some columns to show quick insight
            numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and c != "No"]
            categorical_cols = [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c]) and c != "No" and df[c].nunique() < 30]

            insights = []
            
            # Numeric Insight
            if numeric_cols:
                primary_num_col = numeric_cols[0]
                total_val = df[primary_num_col].sum()
                avg_val = df[primary_num_col].mean()
                max_val = df[primary_num_col].max()
                
                is_currency = "Gaji" in primary_num_col or "Penjualan" in primary_num_col or "Pagu" in primary_num_col
                
                if is_currency:
                    total_str = format_currency(total_val)
                    avg_str = format_currency(avg_val)
                    max_str = format_currency(max_val)
                else:
                    total_str = f"{total_val:,.2f}".rstrip('0').rstrip('.')
                    avg_str = f"{avg_val:,.2f}".rstrip('0').rstrip('.')
                    max_str = f"{max_val:,.2f}".rstrip('0').rstrip('.')

                insights.append(
                    ft.Column([
                        ft.Text(f"Ringkasan Numerik: {primary_num_col}", size=15, weight=ft.FontWeight.BOLD, color=text_primary),
                        ft.Row([
                            ft.Column([ft.Text("Total", size=11, color=text_secondary), ft.Text(total_str, size=15, weight=ft.FontWeight.BOLD, color="#3b82f6" if is_dark else ft.Colors.BLUE_700)], spacing=1),
                            ft.VerticalDivider(width=20, color=border_color),
                            ft.Column([ft.Text("Rata-rata", size=11, color=text_secondary), ft.Text(avg_str, size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400 if is_dark else ft.Colors.GREEN_700)], spacing=1),
                            ft.VerticalDivider(width=20, color=border_color),
                            ft.Column([ft.Text("Maksimal", size=11, color=text_secondary), ft.Text(max_str, size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_400 if is_dark else ft.Colors.ORANGE_700)], spacing=1),
                        ], spacing=16, alignment=ft.MainAxisAlignment.START)
                    ], spacing=10)
                )

            # Categorical Insight
            if categorical_cols:
                primary_cat_col = categorical_cols[0]
                top_categories = df[primary_cat_col].value_counts().head(3)
                
                cat_rows = []
                for cat, count in top_categories.items():
                    pct = (count / len(df)) * 100
                    cat_rows.append(
                        ft.Row([
                            ft.Text(f"{cat}", size=13, weight=ft.FontWeight.W_500, expand=True, color=text_primary),
                            ft.Text(f"{count} ({pct:.1f}%)", size=13, weight=ft.FontWeight.BOLD, color="#3b82f6" if is_dark else ft.Colors.BLUE_800),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    )

                insights.append(
                    ft.Column([
                        ft.Text(f"Kategori Teratas: {primary_cat_col}", size=15, weight=ft.FontWeight.BOLD, color=text_primary),
                        ft.Column(cat_rows, spacing=8)
                    ], spacing=10)
                )

            # Put Insights in horizontal or vertical structure
            for ins in insights:
                info_widgets.append(
                    ft.Container(
                        content=ins,
                        bgcolor=card_bg,
                        padding=20,
                        border_radius=12,
                        border=ft.border.all(1, border_color),
                        shadow=card_shadow,
                        expand=True
                    )
                )

        # Layout for lower sections
        lower_row = ft.ResponsiveRow([
            ft.col.col(12, md=6, content=ft.Column([
                ft.Text("Selamat Datang di Excel Data Center", size=18, weight=ft.FontWeight.BOLD, color="#3b82f6" if is_dark else ft.Colors.BLUE_800),
                ft.Text("Aplikasi ini memungkinkan Anda untuk mengimpor spreadsheet Excel, menjelajahi baris data dengan antarmuka tabel modern, memfilter secara instan, melakukan pencarian waktu nyata, dan melihat analitik yang dihasilkan secara otomatis.", size=14, color=text_secondary),
                ft.Row([
                    ft.ElevatedButton(
                        "Eksplor Data Excel",
                        icon=ft.Icons.TABLE_CHART,
                        on_click=lambda _: self.on_page_navigate("data_page"),
                        style=ft.ButtonStyle(
                            background_color=ft.Colors.BLUE_600,
                            color=ft.Colors.WHITE,
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.padding.symmetric(horizontal=16, vertical=12)
                        )
                    ),
                    ft.OutlinedButton(
                        "Analisis Statistik",
                        icon=ft.Icons.BAR_CHART,
                        on_click=lambda _: self.on_page_navigate("statistics"),
                        style=ft.ButtonStyle(
                            color="#3b82f6" if is_dark else ft.Colors.BLUE_800,
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.padding.symmetric(horizontal=16, vertical=12)
                        )
                    )
                ], spacing=10)
            ], spacing=15)),
        ], spacing=20)

        # Combine insights row
        insights_row = ft.ResponsiveRow(
            [ft.col.col(12, md=6, content=w) for w in info_widgets],
            spacing=16
        )

        content = ft.Container(
            padding=30,
            expand=True,
            content=ft.Column([
                ft.Text("Dashboard Utama", size=24, weight=ft.FontWeight.BOLD, color="#3b82f6" if is_dark else ft.Colors.BLUE_800),
                ft.Text("Ikhtisar data dari file Microsoft Excel yang aktif saat ini.", size=14, color=text_secondary),
                ft.Divider(height=10, color=ft.Colors.transparent),
                stats_cards,
                ft.Divider(height=20, color="#2d3139" if is_dark else ft.Colors.GREY_300),
                lower_row,
                ft.Divider(height=10, color=ft.Colors.transparent),
                insights_row
            ], spacing=20, scroll=ft.ScrollMode.ADAPTIVE)
        )

        return content
