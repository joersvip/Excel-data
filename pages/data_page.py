import os
import math
from datetime import datetime
import pandas as pd
import flet as ft
from modules.excel_reader import ExcelReader
from modules.search import search_data
from modules.filter import get_unique_values, filter_data, sort_data
from modules.export import export_to_csv, export_to_excel, export_to_pdf
from pages.detail_page import DetailPage

class DataPage:
    def __init__(self, page: ft.Page, on_data_reloaded):
        self.page = page
        self.on_data_reloaded = on_data_reloaded
        
        # State variables
        self.current_page = 1
        self.rows_per_page = 25
        self.selected_row_idx = None
        self.selected_record = None
        
        # Search & Filter state
        self.query = ""
        self.filter_col = None
        self.filter_val = None
        self.sort_col = None
        self.sort_dir = "Ascending"

        # File Picker setup
        self.file_picker = ft.FilePicker(
            on_result=self.on_file_selected,
            on_upload_progress=self.on_upload_progress
        )
        self.page.overlay.append(self.file_picker)

    def on_upload_progress(self, e: ft.FilePickerUploadEvent):
        """Handle upload progress and trigger reload when finished."""
        if e.progress == 1.0:
            file_name = e.file_name
            target_path = os.path.join("uploads", file_name)
            try:
                # Set active path and force reload
                self.page.client_storage.set("excel_path", target_path)
                ExcelReader.set_active_file_path(target_path)
                ExcelReader.load_data(force_reload=True)
                
                # Reset filters and trigger refresh
                self.reset_filters()
                self.on_data_reloaded()
                
                # Show success SnackBar
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Berhasil mengimpor {file_name}!", color=ft.Colors.WHITE),
                    background_color=ft.Colors.GREEN_600
                )
                self.page.snack_bar.open = True
                self.refresh_ui()
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Gagal memuat file: {str(ex)}", color=ft.Colors.WHITE),
                    background_color=ft.Colors.RED_600
                )
                self.page.snack_bar.open = True
                self.page.update()

    def on_file_selected(self, e: ft.FilePickerResultEvent):
        """Handle new Excel file selection from FilePicker."""
        if not e.files:
            return

        file = e.files[0]
        
        # Web or Desktop upload routing
        # In web mode, we must upload the file to serve/read it
        if file.path is None:
            # Web mode - upload file
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Mengunggah {file.name}...", color=ft.Colors.WHITE),
                background_color=ft.Colors.BLUE_600
            )
            self.page.snack_bar.open = True
            self.page.update()

            os.makedirs("uploads", exist_ok=True)
            self.file_picker.upload(
                [ft.FilePickerUploadFile(
                    file.name,
                    upload_url=self.page.get_upload_url(file.name, 600)
                )]
            )
        else:
            # Desktop mode - local path is directly accessible
            try:
                self.page.client_storage.set("excel_path", file.path)
                ExcelReader.set_active_file_path(file.path)
                ExcelReader.load_data(force_reload=True)
                
                self.reset_filters()
                self.on_data_reloaded()
                
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Berhasil mengimpor {os.path.basename(file.path)}!", color=ft.Colors.WHITE),
                    background_color=ft.Colors.GREEN_600
                )
                self.page.snack_bar.open = True
                self.refresh_ui()
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Gagal memuat file: {str(ex)}", color=ft.Colors.WHITE),
                    background_color=ft.Colors.RED_600
                )
                self.page.snack_bar.open = True
                self.page.update()

    def reset_filters(self):
        """Reset search and filter selections to defaults."""
        self.query = ""
        self.filter_col = None
        self.filter_val = None
        self.sort_col = None
        self.sort_dir = "Ascending"
        self.current_page = 1
        self.selected_row_idx = None
        self.selected_record = None

    def refresh_ui(self):
        # We replace the body content by rebuilding the container content
        if hasattr(self, "body_container"):
            self.body_container.content = self.get_page_content()
            self.body_container.update()

    def build(self) -> ft.Control:
        self.body_container = ft.Container(
            expand=True,
            content=self.get_page_content()
        )
        return self.body_container

    def get_page_content(self) -> ft.Control:
        theme_mode = self.page.client_storage.get("theme_mode")
        is_dark = theme_mode == "dark"
        
        # Stylings (Elegant Dark vs Light)
        card_bg = "#1e2229" if is_dark else ft.Colors.WHITE
        border_color = "#2d3139" if is_dark else ft.Colors.GREY_300
        text_primary = "#f8fafc" if is_dark else ft.Colors.BLUE_GREY_900
        text_secondary = "#94a3b8" if is_dark else ft.Colors.GREY_600
        
        try:
            # 1. Load active data from reader
            df_raw = ExcelReader.load_data()
            meta = ExcelReader.get_metadata()
            columns = meta["columns"]
        except Exception as e:
            # Show a friendly error container if no excel file is found or file is corrupt
            return ft.Container(
                padding=40,
                alignment=ft.alignment.center,
                content=ft.Column([
                    ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, size=64, color=ft.Colors.ORANGE_400),
                    ft.Text("Gagal Memuat Data Excel", size=20, weight=ft.FontWeight.BOLD, color=text_primary),
                    ft.Text(str(e), size=14, color=text_secondary, text_align=ft.TextAlign.CENTER),
                    ft.Divider(height=20, color=ft.Colors.transparent),
                    ft.Row([
                        ft.ElevatedButton(
                            "Impor File Excel Baru",
                            icon=ft.Icons.UPLOAD_FILE,
                            on_click=lambda _: self.file_picker.pick_files(allowed_extensions=["xlsx", "xls"]),
                            style=ft.ButtonStyle(background_color=ft.Colors.BLUE_600, color=ft.Colors.WHITE)
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
            )

        # 2. Process data: Apply Real-time Search
        df_processed = df_raw.copy()
        if self.query:
            df_processed = search_data(df_processed, self.query)

        # 3. Process data: Apply Filter Column and Value
        if self.filter_col and self.filter_val:
            df_processed = filter_data(df_processed, self.filter_col, self.filter_val)

        # 4. Process data: Apply Sort Column and Direction
        if self.sort_col:
            df_processed = sort_data(df_processed, self.sort_col, self.sort_dir)

        # 5. Process data: Paginate
        total_records = len(df_processed)
        max_page = max(1, math.ceil(total_records / self.rows_per_page))
        if self.current_page > max_page:
            self.current_page = max_page

        start_row = (self.current_page - 1) * self.rows_per_page
        end_row = min(start_row + self.rows_per_page, total_records)
        df_page = df_processed.iloc[start_row:end_row]

        # UI: Define Controls
        search_field = ft.TextField(
            hint_text="Cari data realtime di semua kolom...",
            prefix_icon=ft.Icons.SEARCH,
            value=self.query,
            width=280,
            height=40,
            border_radius=8,
            border_color=border_color,
            text_size=13,
            on_change=self.on_search_change
        )

        # Filter Column Dropdown
        filter_col_dropdown = ft.Dropdown(
            hint_text="Pilih Kolom Filter",
            value=self.filter_col,
            options=[ft.dropdown.Option(col) for col in columns if col != "No" and col != "Foto"],
            width=180,
            height=40,
            border_radius=8,
            border_color=border_color,
            text_size=12,
            on_change=self.on_filter_col_change
        )

        # Filter Value Dropdown
        filter_val_options = []
        if self.filter_col:
            unique_vals = get_unique_values(df_raw, self.filter_col)
            filter_val_options = [ft.dropdown.Option(val) for val in unique_vals[:100]]  # Limit dropdown options to 100 for perf

        filter_val_dropdown = ft.Dropdown(
            hint_text="Pilih Nilai Filter",
            value=self.filter_val,
            options=filter_val_options,
            width=180,
            height=40,
            border_radius=8,
            border_color=border_color,
            text_size=12,
            disabled=not self.filter_col,
            on_change=self.on_filter_val_change
        )

        # Sort Column Dropdown
        sort_col_dropdown = ft.Dropdown(
            hint_text="Urutkan Kolom",
            value=self.sort_col,
            options=[ft.dropdown.Option(col) for col in columns if col != "Foto"],
            width=180,
            height=40,
            border_radius=8,
            border_color=border_color,
            text_size=12,
            on_change=self.on_sort_col_change
        )

        # Sort Direction Toggle Button
        sort_dir_btn = ft.IconButton(
            icon=ft.Icons.ARROW_UPWARD if self.sort_dir == "Ascending" else ft.Icons.ARROW_DOWNWARD,
            icon_size=20,
            tooltip="Balik Urutan" if self.sort_dir == "Ascending" else "Urutkan Normal",
            on_click=self.toggle_sort_direction
        )

        # Reset Filter Button
        reset_btn = ft.IconButton(
            icon=ft.Icons.FILTER_ALT_OFF,
            icon_color=ft.Colors.RED_400 if is_dark else ft.Colors.RED_600,
            tooltip="Reset Filter & Pencarian",
            on_click=self.on_reset_click
        )

        # Export Button Row
        def trigger_export(export_type: str):
            filename_base = f"Ekspor_Data_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            try:
                if export_type == "CSV":
                    filename = f"{filename_base}.csv"
                    export_to_csv(df_processed, filename)
                elif export_type == "Excel":
                    filename = f"{filename_base}.xlsx"
                    export_to_excel(df_processed, filename)
                elif export_type == "PDF":
                    filename = f"{filename_base}.pdf"
                    export_to_pdf(df_processed, filename)

                # Serves downloaded file
                # In Flet web, launching '/exports/filename' lets the user download it!
                self.page.launch_url(f"/exports/{filename}")

                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Berhasil mengekspor ke {export_type}!", color=ft.Colors.WHITE),
                    background_color=ft.Colors.GREEN_600
                )
                self.page.snack_bar.open = True
                self.page.update()
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Gagal mengekspor: {str(ex)}", color=ft.Colors.WHITE),
                    background_color=ft.Colors.RED_600
                )
                self.page.snack_bar.open = True
                self.page.update()

        export_menu = ft.PopupMenuButton(
            content=ft.Row([
                ft.Icon(ft.Icons.DOWNLOAD, size=18, color=ft.Colors.WHITE),
                ft.Text("Ekspor", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, size=13)
            ], tight=True),
            style=ft.ButtonStyle(
                background_color=ft.Colors.GREEN_600,
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.symmetric(horizontal=16, vertical=10)
            ),
            items=[
                ft.PopupMenuItem(text="Ekspor ke Excel (.xlsx)", on_click=lambda _: trigger_export("Excel")),
                ft.PopupMenuItem(text="Ekspor ke CSV (.csv)", on_click=lambda _: trigger_export("CSV")),
                ft.PopupMenuItem(text="Ekspor ke PDF (.pdf)", on_click=lambda _: trigger_export("PDF")),
            ]
        )

        import_btn = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.UPLOAD_FILE, size=18, color=ft.Colors.WHITE),
                ft.Text("Impor Excel", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, size=13)
            ], tight=True),
            style=ft.ButtonStyle(
                background_color=ft.Colors.BLUE_600,
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.symmetric(horizontal=16, vertical=12)
            ),
            on_click=lambda _: self.file_picker.pick_files(allowed_extensions=["xlsx", "xls"])
        )

        refresh_btn = ft.IconButton(
            icon=ft.Icons.REFRESH,
            tooltip="Segarkan Data",
            on_click=self.on_refresh_click
        )

        # Create Table Headers
        table_columns = []
        # We only render the first 8 columns to keep the UI perfectly clean and prevent massive horizontal scrolls
        rendered_cols = [col for col in columns if col != "Foto"][:8]
        
        for col in rendered_cols:
            table_columns.append(
                ft.DataColumn(
                    ft.Text(col, weight=ft.FontWeight.BOLD, color=text_primary, size=13)
                )
            )

        # Create Table Rows
        table_rows = []
        for index, row in df_page.iterrows():
            cells = []
            row_dict = row.to_dict()
            
            # Highlight selected row
            is_selected = (self.selected_row_idx == index)
            row_bg_color = ft.Colors.with_opacity(0.15, "#3b82f6") if is_selected else None

            for col in rendered_cols:
                val = row[col]
                # Format numbers nicely
                if isinstance(val, (int, float)) and ("Gaji" in col or "Penjualan" in col or "Pagu" in col):
                    val_str = f"Rp {val:,.0f}".replace(",", ".")
                elif isinstance(val, (datetime, pd.Timestamp)):
                    val_str = val.strftime("%d-%m-%Y")
                else:
                    val_str = str(val) if not pd.isna(val) else "-"

                # Truncate string cell if too long
                if len(val_str) > 28:
                    val_str = val_str[:25] + "..."

                cells.append(
                    ft.DataCell(
                        ft.Text(val_str, color=text_primary, size=12, overflow=ft.TextOverflow.ELLIPSIS)
                    )
                )

            # Define selection handler
            def make_select_handler(r_idx, r_val):
                return lambda e: self.on_row_select(r_idx, r_val)

            table_rows.append(
                ft.DataRow(
                    cells=cells,
                    selected=is_selected,
                    color=row_bg_color,
                    on_select_changed=make_select_handler(index, row_dict)
                )
            )

        # Assemble the DataTable in a Scrollable container
        data_table_control = ft.DataTable(
            columns=table_columns,
            rows=table_rows,
            column_spacing=24,
            heading_row_height=42,
            data_row_min_height=38,
            data_row_max_height=38,
            show_checkbox_column=False,
            expand=True
        )

        table_scroll_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    data_table_control
                ], scroll=ft.ScrollMode.ADAPTIVE)
            ], scroll=ft.ScrollMode.ADAPTIVE, expand=True),
            border_radius=8,
            border=ft.border.all(1, border_color),
            bgcolor=card_bg,
            padding=10,
            expand=True
        )

        # Pagination controls
        pages_dropdown = ft.Dropdown(
            value=str(self.rows_per_page),
            options=[
                ft.dropdown.Option("10", "10 baris"),
                ft.dropdown.Option("25", "25 baris"),
                ft.dropdown.Option("50", "50 baris"),
                ft.dropdown.Option("100", "100 baris"),
            ],
            width=110,
            height=38,
            border_radius=8,
            border_color=border_color,
            text_size=12,
            on_change=self.on_page_size_change
        )

        pagination_label = ft.Text(
            f"Menampilkan {start_row + 1 if total_records > 0 else 0} - {end_row} dari {total_records:,} data".replace(",", "."),
            size=12,
            color=text_secondary,
            weight=ft.FontWeight.W_500
        )

        pagination_row = ft.Row([
            ft.Row([
                ft.Text("Baris per halaman:", size=12, color=text_secondary),
                pages_dropdown,
            ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            pagination_label,
            ft.Row([
                ft.IconButton(
                    icon=ft.Icons.FIRST_PAGE,
                    disabled=self.current_page == 1,
                    on_click=self.go_to_first_page,
                    icon_size=18,
                ),
                ft.IconButton(
                    icon=ft.Icons.CHEVRON_LEFT,
                    disabled=self.current_page == 1,
                    on_click=self.go_prev_page,
                    icon_size=18,
                ),
                ft.Text(f"Halaman {self.current_page} dari {max_page}", size=12, color=text_primary, weight=ft.FontWeight.BOLD),
                ft.IconButton(
                    icon=ft.Icons.CHEVRON_RIGHT,
                    disabled=self.current_page == max_page,
                    on_click=self.go_next_page,
                    icon_size=18,
                ),
                ft.IconButton(
                    icon=ft.Icons.LAST_PAGE,
                    disabled=self.current_page == max_page,
                    on_click=self.go_to_last_page,
                    icon_size=18,
                ),
            ], spacing=2, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)

        # Re-build details panel if visible
        detail_panel = ft.Container()
        if self.selected_record is not None:
            detail_panel = DetailPage.build_detail_panel(
                self.page, 
                self.selected_record, 
                on_close=self.close_detail_panel
            )

        # Assemble Master-Detail Row
        main_workspace = ft.Row([
            ft.Container(
                content=table_scroll_container,
                expand=True
            ),
            # Sliding animation represented by appending or layout updates
            detail_panel
        ], spacing=16, expand=True)

        # Title/Header Block
        page_header = ft.Row([
            ft.Column([
                ft.Text("Manajemen Data Excel", size=24, weight=ft.FontWeight.BOLD, color="#3b82f6" if is_dark else ft.Colors.BLUE_800),
                ft.Text(f"File aktif: {meta['file_name']} (Total: {meta['total_rows']:,} baris)".replace(",", "."), size=13, color=text_secondary),
            ], spacing=2),
            ft.Row([
                refresh_btn,
                import_btn,
                export_menu,
            ], spacing=8)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # Combined View
        layout = ft.Container(
            padding=24,
            expand=True,
            content=ft.Column([
                page_header,
                ft.Divider(height=10, color=ft.Colors.transparent),
                # Filters row
                ft.Row([
                    search_field,
                    filter_col_dropdown,
                    filter_val_dropdown,
                    sort_col_dropdown,
                    sort_dir_btn,
                    reset_btn
                ], spacing=10, wrap=True, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Divider(height=5, color=ft.Colors.transparent),
                main_workspace,
                pagination_row
            ], spacing=15, expand=True)
        )

        return layout

    # Callbacks
    def on_search_change(self, e):
        self.query = e.control.value
        self.current_page = 1  # Reset to page 1
        self.refresh_ui()

    def on_filter_col_change(self, e):
        self.filter_col = e.control.value
        self.filter_val = None  # Reset value
        self.current_page = 1
        self.refresh_ui()

    def on_filter_val_change(self, e):
        self.filter_val = e.control.value
        self.current_page = 1
        self.refresh_ui()

    def on_sort_col_change(self, e):
        self.sort_col = e.control.value
        self.refresh_ui()

    def toggle_sort_direction(self, e):
        if self.sort_dir == "Ascending":
            self.sort_dir = "Descending"
        else:
            self.sort_dir = "Ascending"
        self.refresh_ui()

    def on_reset_click(self, e):
        self.reset_filters()
        self.refresh_ui()

    def on_refresh_click(self, e):
        try:
            ExcelReader.load_data(force_reload=True)
            self.on_data_reloaded()
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Data Excel berhasil disegarkan!", color=ft.Colors.WHITE),
                background_color=ft.Colors.GREEN_600
            )
            self.page.snack_bar.open = True
            self.refresh_ui()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Gagal memuat ulang: {str(ex)}", color=ft.Colors.WHITE),
                background_color=ft.Colors.RED_600
            )
            self.page.snack_bar.open = True
            self.page.update()

    def on_row_select(self, row_idx, record_dict):
        # Toggle selection
        if self.selected_row_idx == row_idx:
            self.selected_row_idx = None
            self.selected_record = None
        else:
            self.selected_row_idx = row_idx
            self.selected_record = record_dict
        self.refresh_ui()

    def close_detail_panel(self):
        self.selected_row_idx = None
        self.selected_record = None
        self.refresh_ui()

    def on_page_size_change(self, e):
        self.rows_per_page = int(e.control.value)
        self.current_page = 1
        self.refresh_ui()

    def go_to_first_page(self, e):
        self.current_page = 1
        self.refresh_ui()

    def go_prev_page(self, e):
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_ui()

    def go_next_page(self, e):
        self.current_page += 1
        self.refresh_ui()

    def go_to_last_page(self, e):
        try:
            df = ExcelReader.load_data()
            if self.query:
                df = search_data(df, self.query)
            if self.filter_col and self.filter_val:
                df = filter_data(df, self.filter_col, self.filter_val)
            max_page = max(1, math.ceil(len(df) / self.rows_per_page))
            self.current_page = max_page
            self.refresh_ui()
        except Exception:
            pass
