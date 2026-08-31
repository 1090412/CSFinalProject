import flet as ft

themes = {
    "home":ft.Theme(color_scheme_seed=ft.Colors.GREY),
    "athletes":ft.Theme(color_scheme_seed=ft.Colors.YELLOW),
    "supervisors":ft.Theme(color_scheme_seed=ft.Colors.PURPLE),
    "competitions":ft.Theme(color_scheme_seed=ft.Colors.BLUE),
    "events":ft.Theme(color_scheme_seed=ft.Colors.BLUE),
    "races":ft.Theme(color_scheme_seed=ft.Colors.BLUE),
    "results":ft.Theme(color_scheme_seed=ft.Colors.BLUE),
    "patrolgroups":ft.Theme(color_scheme_seed=ft.Colors.RED),
    "patrols":ft.Theme(color_scheme_seed=ft.Colors.RED),
    "volunteering":ft.Theme(color_scheme_seed=ft.Colors.LIGHT_GREEN),
    "qualifications":ft.Theme(color_scheme_seed=ft.Colors.PURPLE),
}

pages = {
    "home":[
        "Dashboard",
        ft.Icons.HOME,
        ft.Icons.HOME_OUTLINED
    ],
    "athletes":[
        "Athletes",
        ft.Icons.PERSON,
        ft.Icons.PERSON_OUTLINED
    ],
    "competitions":[
        "Competitions",
        ft.Icons.SURFING,
        ft.Icons.SURFING_OUTLINED
    ],
    "patrols":[
        "Patrols",
        ft.Icons.FLAG,
        ft.Icons.FLAG_OUTLINED
    ],
    "volunteering":[
        "Volunteering",
        ft.Icons.VOLUNTEER_ACTIVISM,
        ft.Icons.VOLUNTEER_ACTIVISM_OUTLINED
    ],
    "qualifications":[
        "Qualifications",
        ft.Icons.CARD_MEMBERSHIP,
        ft.Icons.CARD_MEMBERSHIP_OUTLINED,
    ],
}

links = [
    "/",
    "/athletes",
    "/competitions",
    "/patrols",
    "/volunteering",
    "/qualifications",
]

def create_appbar(page:ft.Page, route:str):
    appbar = ft.AppBar(
        toolbar_height=80,
        leading=ft.Icon(ft.Icons.WAVES,size=30),
        leading_width=100,
        title=ft.Text("AthleteTracker",size=30),
        color=ft.Colors.ON_PRIMARY,
        bgcolor=ft.Colors.PRIMARY,
        actions_padding=15,
        actions = [
            ft.SearchBar(bar_hint_text="Search..."),
            ft.VerticalDivider(width=20),
            ft.IconButton(ft.Icons.SETTINGS,icon_size=30)
        ]
    )
    return appbar

def create_sidemenu(page:ft.Page, route:str):
    async def handle_change(event:ft.Event):
        if event.control.selected_index is not None:
            await page.push_route(f"/{links[event.control.selected_index]}")
    navigation_rail = ft.NavigationRail(
        selected_index=list(pages).index(route) if route in pages else None,
        width=100,
        on_change=handle_change,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icon(comp[1],size=30),
                selected_icon=ft.Icon(comp[2],size=30),
                label=comp[0],
                padding=10,
            ) for name,comp in pages.items()
        ]
    )
    return navigation_rail