import flet as ft
import random

information_cards = {
    "home":[
        (ft.Icons.PEOPLE, 0, "Registered Athletes"),
        (ft.Icons.LOCK_CLOCK, 0, "Total Patrol Hours"),
        (ft.Icons.FLAG, 0, "Completed Required Patrols"),
        (ft.Icons.EMOJI_EVENTS, 0, "2026 State Medals"),
    ],
    "athletes":[

    ],
    "competitions":[

    ],
    "patrols":[
        
    ],
    "volunteering":[
        
    ],
    "grants":[
        
    ],
}

def create_cards(page:ft.Page, route:str):
    cont = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=50,
        controls=[
            ft.Container(
                width=200,
                height=225,
                border_radius=20,
                bgcolor=ft.Colors.SURFACE_CONTAINER,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    tight=True,
                    spacing=0,
                    controls=[
                        ft.Icon(icon, color=ft.Colors.SURFACE_DIM, size=100),
                        ft.Text(str(number), text_align=ft.TextAlign.CENTER, size=40, weight=ft.FontWeight.BOLD),
                        ft.Text(str(stat), text_align=ft.TextAlign.CENTER, size=14, no_wrap=False)
                    ]
                )
            ) for icon,number,stat in random.sample(information_cards[route],min(5,len(information_cards[route])))
        ]
    )
    return cont



summary_card = {
    "home":[
        "... Overview",
        [
            (True,"Total Athletes",...),
            (False,"Male",...),
            (False,"Female",...),
        ],[
            (True,"Average Age",0),
            (False,"Youth (13-15)",0),
            (False,"U23 (16-22)",0),
            (False,"Open (23-59)",0),
            (False,"Masters (60+)",0),
        ]
    ],
    "athletes":[
        "... Overview"
    ],
    "competitions":[
        "... Overview"
    ],
    "patrols":[
        "... Overview"
    ],
    "volunteering":[
        "... Overview"
    ],
    "grants":[
        "... Overview"
    ],
}

def create_summary(page:ft.Page, route:str):
    cont = ft.Container(
            padding=25,
            border_radius=20,
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                tight=True,
                controls=[
                    ft.Text(summary_card[route][0], text_align=ft.TextAlign.LEFT, size=24, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        spacing=50,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            ft.Column(
                                expand=True,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text(name, size=15, expand=5, text_align=ft.TextAlign.LEFT, weight=ft.FontWeight.BOLD),
                                            ft.Text(str(value), size=15, expand=3, text_align=ft.TextAlign.RIGHT, weight=ft.FontWeight.BOLD),
                                        ] if main else [
                                            ft.Text(expand=1),
                                            ft.Text(name, size=15, expand=4, text_align=ft.TextAlign.LEFT),
                                            ft.Text(str(value), size=15, expand=3, text_align=ft.TextAlign.RIGHT),
                                        ]
                                    ) for main,name,value in col
                                ]
                            ) for col in summary_card[route][1:]
                        ]
                    )
                ]
            )
        )
    return cont



minitables = {
    "home":[
        
    ],
    "athletes":[
        ("Athlete", "/athletes", ft.Icons.PERSON, ("Name","Age","Gender"), (("Perosn 1",23,"M"),("Perosn 2",19,"F"),("Perosn 3",32,"F")), 10)
    ],
    "competitions":[

    ],
    "patrols":[
        
    ],
    "volunteering":[
        
    ],
    "grants":[
        
    ],
}

def create_minitable(page:ft.Page, route:str):
    def buttons(table,link):
        return (
            (ft.Icons.ADD,f"Add {table}",link+"/add"),
            (ft.Icons.UPLOAD,"Export Table",link+"/view"),
            (ft.Icons.SEARCH,f"View {table} Table",link+"/view"),
        )
    cont = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=15,
                controls=[
                    ft.Button(
                        content=ft.Text(text,size=16,weight=ft.FontWeight.BOLD),
                        icon=ft.Icon(icon,size=20),
                        expand=True,
                        on_click=lambda _,dest=dest: page.run_task(page.push_route,dest),
                        style = ft.ButtonStyle(
                            bgcolor=ft.Colors.SURFACE_CONTAINER,
                            color=ft.Colors.PRIMARY,
                            icon_color=ft.Colors.PRIMARY,
                            padding=ft.Padding(0,20,0,20),
                            shape=ft.RoundedRectangleBorder(radius=10),
                        )
                    ) for icon,text,dest in buttons(name,link)
                ]
            ) if i==0 else
            ft.Container(
                padding=25,
                border_radius=20,
                bgcolor=ft.Colors.SURFACE_CONTAINER,
                content=ft.Column(
                    controls=[
                        ft.Text(f"{name} Table", text_align=ft.TextAlign.LEFT, size=24, weight=ft.FontWeight.BOLD),
                    ] + [
                        ft.Row(
                            [ft.Text("", size=15, expand=1)] +
                            [ft.Text(columns[0], size=15, weight=ft.FontWeight.BOLD, expand=5)] +
                            [ft.Text(str(header), text_align=ft.TextAlign.CENTER, size=15, weight=ft.FontWeight.BOLD, expand=3) for header in columns[1:]]
                        )
                    ] + [
                        ft.Row(
                            [ft.Icon(icon, color=ft.Colors.SURFACE_DIM, size=15, expand=1)] +
                            [ft.Text(str(row[0]), size=15, expand=5)] +
                            [ft.Text(str(cell), text_align=ft.TextAlign.CENTER, size=15, expand=3) for cell in row[1:]]
                        ) for row in data
                    ] + [
                        ft.TextButton(f"View All {size} Records", icon=ft.Icons.SEARCH, on_click=lambda _,link=link: page.run_task(page.push_route,link))
                    ]
                )
            ) for name,link,icon,columns,data,size in minitables[route] for i in range(2)
        ]
    )
    return cont



def create_left_cont(page:ft.Page, route:str):
    return [
        create_summary(page,route),
        create_minitable(page,route)
    ]

def create_right_cont(page:ft.Page, route:str):
    return [

    ]

def build_page(page:ft.Page, route:str):
    cont = ft.Column(
        expand=True,
        spacing=30,
        controls=[
            create_cards(page,route),
            ft.Row(
                expand=True,
                spacing=30,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Column(expand=3, spacing=15, controls=create_left_cont(page,route)),
                    ft.Column(expand=2, spacing=15, controls=create_right_cont(page,route)),
                ]
            )
        ]
    )
    return cont