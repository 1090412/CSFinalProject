import flet as ft

themes = {
    "index":ft.Theme(color_scheme_seed=ft.Colors.BLUE_GREY),
    "athletes":ft.Theme(color_scheme_seed=ft.Colors.YELLOW),
    "competitions":ft.Theme(color_scheme_seed=ft.Colors.BLUE),
    "patrols":ft.Theme(color_scheme_seed=ft.Colors.RED),
    "volunteering":ft.Theme(color_scheme_seed=ft.Colors.BLUE),
    "grants":ft.Theme(color_scheme_seed=ft.Colors.LIGHT_GREEN),
}

def build(page:ft.Page, focus:str):
    pass