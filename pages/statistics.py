import flet as ft
import random
from modules.excel_reader import ExcelReader
from modules.statistics import analyze_columns, get_categorical_stats, get_numeric_stats
from modules.helper import format_currency

class StatisticsPage:
    def __init__(self, page: ft.Page):
        self.page = page
        
        # UI State
        self.selected_cat_col = None
        self.selected_num_col = None

    def build(self) -> ft.Control:
        self.body_container = ft.Container(
            expand=True,
            content=self.get_page_content()
        )
        return self.body_container

    def refresh_ui(self):
        if hasattr(self, "body_container"):
            self.body_container.content = self.get_page_content()
            self.body_container.update()

    def get_page_content(self) -> ft.Control:
        theme_mode = self.page.client_storage.get("theme_mode")
        is_dark = theme_mode == "dark"
        
        # Theme stylings (Elegant Dark vs Light)
        card_bg = "#1e2229" if is_dark else ft.Colors.WHITE
        border_color = "#2d3139" if is_dark else ft.Colors.GREY_300
        text_primary = "#f8fafc" if is_dark else ft.Colors.BLUE_GREY_900
        text_secondary = "#94a3b8" if is_dark else ft.Colors.GREY_600
        card_shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.12 if is_dark else 0.06, ft.Colors.BLACK),
            offset=ft.Offset(0, 4)
        )

        try:
            df = ExcelReader.load_data()
            cols_analysis = analyze_columns(df)
            cat_cols = cols_analysis["categorical"]
            num_cols = cols_analysis["numeric"]
        except Exception as e:
            # Fallback if no Excel loaded
            return ft.Container(
                padding=40,
                alignment=ft.alignment.center,
                content=ft.Column([
                    ft.Icon(ft.Icons.ANALYTICS_OUTLINED, size=64, color=ft.Colors.GREY_600),
                    ft.Text("Statistik Belum Tersedia", size=20, weight=ft.FontWeight.BOLD, color=text_primary),
                    ft.Text("Harap muat file Excel yang valid di Halaman Data terlebih dahulu.", size=14, color=text_secondary)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )

        # Set default selections if not already set
        if not self.selected_cat_col and cat_cols:
            self.selected_cat_col = cat_cols[0]
        if not self.selected_num_col and num_cols:
            self.selected_num_col = num_cols[0]

        # ---------------- CATEGORICAL SECTION ----------------
        categorical_view = ft.Container()
        if self.selected_cat_col and self.selected_cat_col in df.columns:
            stats = get_categorical_stats(df, self.selected_cat_col)
            
            # Palette for chart colors
            chart_colors = [
                "#3b82f6", ft.Colors.GREEN_400, ft.Colors.ORANGE_400, 
                ft.Colors.PURPLE_400, ft.Colors.RED_400, ft.Colors.TEAL_400, 
                ft.Colors.PINK_400, ft.Colors.AMBER_400, ft.Colors.INDIGO_400, 
                ft.Colors.CYAN_400
            ]
            
            # Build PieChart slices & BarChart rods
            pie_slices = []
            bar_groups = []
            legend_items = []
            table_rows = []
            
            for i, (val, count, pct) in enumerate(stats):
                color = chart_colors[i % len(chart_colors)]
                
                # Pie slice
                pie_slices.append(
                    ft.PieChartEventSection(
                        value=count,
                        title=f"{pct:.1f}%",
                        color=color,
                        radius=50,
                        title_style=ft.TextStyle(size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                    )
                )
                
                # Bar rod
                bar_groups.append(
                    ft.BarChartGroup(
                        x=i,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=count,
                                color=color,
                                width=24,
                                border_radius=4,
                            )
                        ]
                    )
                )

                # Legend item
                legend_items.append(
                    ft.Row([
                        ft.Container(width=12, height=12, bgcolor=color, border_radius=3),
                        ft.Text(f"{val} ({count} data)", size=12, color=text_primary, weight=ft.FontWeight.W_500)
                    ], spacing=8, tight=True)
                )
                
                # Table Row
                table_rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(val, size=12, color=text_primary)),
                            ft.DataCell(ft.Text(f"{count:,}".replace(",", "."), size=12, color=text_primary)),
                            ft.DataCell(ft.Text(f"{pct:.2f}%", size=12, color=text_primary)),
                        ]
                    )
                )

            pie_chart = ft.PieChart(
                sections=pie_slices,
                sections_space=2,
                center_space_radius=40,
                expand=True
            )

            bar_chart = ft.BarChart(
                bar_groups=bar_groups,
                bottom_axis=ft.ChartAxis(
                    labels=[
                        ft.ChartAxisLabel(
                            value=i, 
                            label=ft.Container(
                                content=ft.Text(stats[i][0][:6] + ".." if len(stats[i][0]) > 7 else stats[i][0], size=9, color=text_secondary),
                                margin=ft.margin.only(top=5)
                            )
                        ) for i in range(len(stats))
                    ],
                    labels_size=20,
                ),
                left_axis=ft.ChartAxis(
                    labels_size=30,
                ),
                horizontal_grid_lines=ft.ChartGridLines(
                    color=ft.Colors.with_opacity(0.1, text_secondary),
                    width=1,
                    dash_pattern=[3, 3]
                ),
                expand=True
            )

            stats_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Kategori / Nilai", weight=ft.FontWeight.BOLD, color=text_primary, size=12)),
                    ft.DataColumn(ft.Text("Frekuensi", weight=ft.FontWeight.BOLD, color=text_primary, size=12)),
                    ft.DataColumn(ft.Text("Persentase", weight=ft.FontWeight.BOLD, color=text_primary, size=12)),
                ],
                rows=table_rows,
                column_spacing=20,
                heading_row_height=36,
                data_row_min_height=32,
                data_row_max_height=32,
            )

            categorical_view = ft.ResponsiveRow([
                # Left side: Charts
                ft.col.col(12, lg=7, content=ft.Container(
                    bgcolor=card_bg,
                    padding=20,
                    border_radius=12,
                    border=ft.border.all(1, border_color),
                    shadow=card_shadow,
                    content=ft.Column([
                        ft.Row([
                            ft.Text("Visualisasi Distribusi", size=16, weight=ft.FontWeight.BOLD, color=text_primary),
                        ]),
                        ft.ResponsiveRow([
                            ft.col.col(12, md=6, content=ft.Container(
                                height=220,
                                padding=10,
                                content=pie_chart,
                                alignment=ft.alignment.center
                            )),
                            ft.col.col(12, md=6, content=ft.Container(
                                height=220,
                                padding=10,
                                content=bar_chart
                            )),
                        ], spacing=16),
                        ft.Divider(height=10, color=border_color),
                        # Legend items wrap
                        ft.Row(legend_items, wrap=True, spacing=14, alignment=ft.MainAxisAlignment.CENTER)
                    ], spacing=12)
                )),
                
                # Right side: Summary table
                ft.col.col(12, lg=5, content=ft.Container(
                    bgcolor=card_bg,
                    padding=20,
                    border_radius=12,
                    border=ft.border.all(1, border_color),
                    shadow=card_shadow,
                    content=ft.Column([
                        ft.Text("Tabel Frekuensi", size=16, weight=ft.FontWeight.BOLD, color=text_primary),
                        ft.Container(
                            content=ft.Column([stats_table], scroll=ft.ScrollMode.ADAPTIVE),
                            height=250
                        )
                    ], spacing=12)
                ))
            ], spacing=20)

        # ---------------- NUMERIC SECTION ----------------
        numeric_view = ft.Container()
        if self.selected_num_col and self.selected_num_col in df.columns:
            n_stats = get_numeric_stats(df, self.selected_num_col)
            
            is_currency = "Gaji" in self.selected_num_col or "Penjualan" in self.selected_num_col or "Pagu" in self.selected_num_col
            
            def render_val(val):
                return format_currency(val) if is_currency else f"{val:,.2f}".rstrip('0').rstrip('.')

            def create_metric_card(title, value, color_accent):
                return ft.Container(
                    bgcolor=card_bg,
                    padding=20,
                    border_radius=12,
                    border=ft.border.all(1, border_color),
                    shadow=card_shadow,
                    content=ft.Column([
                        ft.Text(title, size=11, color=text_secondary, weight=ft.FontWeight.W_500),
                        ft.Text(value, size=18, color=color_accent, weight=ft.FontWeight.BOLD),
                    ], spacing=5),
                    expand=True
                )

            numeric_view = ft.ResponsiveRow([
                ft.col.col(12, sm=6, md=4, lg=2.4, content=create_metric_card("Total Akumulasi (Sum)", render_val(n_stats["sum"]), "#3b82f6")),
                ft.col.col(12, sm=6, md=4, lg=2.4, content=create_metric_card("Rata-rata (Mean)", render_val(n_stats["mean"]), ft.Colors.GREEN_400)),
                ft.col.col(12, sm=6, md=4, lg=2.4, content=create_metric_card("Nilai Tengah (Median)", render_val(n_stats["median"]), ft.Colors.ORANGE_400)),
                ft.col.col(12, sm=6, md=4, lg=2.4, content=create_metric_card("Nilai Terendah (Min)", render_val(n_stats["min"]), ft.Colors.RED_400)),
                ft.col.col(12, sm=6, md=4, lg=2.4, content=create_metric_card("Nilai Tertinggi (Max)", render_val(n_stats["max"]), ft.Colors.PURPLE_400)),
            ], spacing=16)

        # Dropdowns block for controlling statistics
        control_panel = ft.Container(
            bgcolor=card_bg,
            padding=18,
            border_radius=12,
            border=ft.border.all(1, border_color),
            shadow=card_shadow,
            content=ft.Row([
                # Categorical picker
                ft.Row([
                    ft.Text("Analisis Kategori:", size=13, weight=ft.FontWeight.BOLD),
                    ft.Dropdown(
                        value=self.selected_cat_col,
                        options=[ft.dropdown.Option(col) for col in cat_cols],
                        width=180,
                        height=38,
                        border_radius=8,
                        border_color=border_color,
                        text_size=12,
                        on_change=self.on_cat_change
                    )
                ], spacing=10),
                
                ft.VerticalDivider(width=20, color=border_color),
                
                # Numeric picker
                ft.Row([
                    ft.Text("Analisis Angka:", size=13, weight=ft.FontWeight.BOLD),
                    ft.Dropdown(
                        value=self.selected_num_col,
                        options=[ft.dropdown.Option(col) for col in num_cols],
                        width=180,
                        height=38,
                        border_radius=8,
                        border_color=border_color,
                        text_size=12,
                        on_change=self.on_num_change
                    )
                ], spacing=10)
            ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER, wrap=True)
        )

        # Page Header
        header = ft.Column([
            ft.Text("Analisis Statistik Otomatis", size=24, weight=ft.FontWeight.BOLD, 
                    color="#3b82f6" if is_dark else ft.Colors.BLUE_800),
            ft.Text("Hasil analitik deskriptif dan grafik visualisasi data yang dimuat saat ini.", size=14, color=text_secondary),
        ], spacing=2)

        # Combined layout
        layout = ft.Container(
            padding=30,
            expand=True,
            content=ft.Column([
                header,
                ft.Divider(height=10, color=ft.Colors.transparent),
                control_panel,
                ft.Divider(height=10, color=ft.Colors.transparent),
                ft.Text("Statistik Kolom Angka (Descriptive)", size=16, weight=ft.FontWeight.BOLD, color=text_primary),
                numeric_view,
                ft.Divider(height=20, color=border_color),
                ft.Text("Statistik Kolom Kategori (Distribution)", size=16, weight=ft.FontWeight.BOLD, color=text_primary),
                categorical_view
            ], spacing=15, scroll=ft.ScrollMode.ADAPTIVE)
        )

        return layout

    def on_cat_change(self, e):
        self.selected_cat_col = e.control.value
        self.refresh_ui()

    def on_num_change(self, e):
        self.selected_num_col = e.control.value
        self.refresh_ui()
