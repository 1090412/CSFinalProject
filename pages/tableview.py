import flet as ft
import sqlite3
import database.queries as queries
import database.columns as columns

DATABASE = "database/database.db"

names = {
    "athletes":"Athlete",
    "supervisors":"Supervisor",
    "competitions":"Competition",
    "events":"Event",
    "races":"Race",
    "results":"Result",
    "patrolgroups":"PatrolGroup",
    "patrols":"Patrol",
    "volunteering":"VolunteerActivity",
    "qualifications":"QualificationAward",
}

icons = {
    "athletes":ft.Icons.PERSON,
    "supervisors":ft.Icons.SUPERVISOR_ACCOUNT,
    "competitions":ft.Icons.EMOJI_EVENTS,
    "events":ft.Icons.FLAG,
    "races":ft.Icons.DIRECTIONS_RUN,
    "results":ft.Icons.EMOJI_EVENTS,
    "patrolgroups":ft.Icons.GROUPS,
    "patrols":ft.Icons.SAFETY_DIVIDER,
    "volunteering":ft.Icons.VOLUNTEER_ACTIVISM,
    "qualifications":ft.Icons.CARD_MEMBERSHIP,
}



def create_filters(page:ft.Page, route:str, settings:dict, update_func):
    def sort_button(field,dir):
        settings["sort"] = field
        settings["sort_dir"] = dir
        settings["page"] = 1
        update_func()
    def filter_change(event,field,key,type):
        if type=="enum":
            if event.control.value and key not in settings["filters"][field]:
                settings["filters"][field].append(key)
            if not event.control.value and key in settings["filters"][field]:
                settings["filters"][field].remove(key)
        if type=="number":
            settings["filters"][field] = (event.control.start_value,event.control.end_value)
        if type=="text":
            settings["filters"][field] = event.control.value
        if type=="id":
            if event.control.value!="":
                try:
                    settings["filters"][field] = int(event.control.value)
                except:
                    settings["filters"][field] = None
            else:
                settings["filters"][field] = None
    def column_button(event,field_no):
        if event.control.value and field_no not in settings["columns"]:
            settings["columns"].append(field_no)
        if not event.control.value and field_no in settings["columns"]:
            settings["columns"].remove(field_no)
        settings["columns"].sort()
    def date_filter(field):
        def date_change(event):
            if event.control.start_value and event.control.end_value:
                settings["filters"][field] = (
                    event.control.start_value.strftime("%Y-%m-%d"),
                    event.control.end_value.strftime("%Y-%m-%d")
                )
        picker = ft.DateRangePicker(
            on_change=date_change
        )
        return ft.Button(
            icon=ft.Icons.DATE_RANGE,
            content="Pick Date Range",
            on_click=lambda _: page.show_dialog(picker),
            expand=5
        )
    cont = ft.ExpansionPanelList(
        expand=True,
        elevation=0,
        controls=[
            ft.ExpansionPanel(
                bgcolor=ft.Colors.SURFACE_CONTAINER,
                header=ft.Row(
                    spacing=20,
                    controls=[
                        ft.Container(
                            padding=20,
                            expand=1,
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(ft.Icons.SORT, size=20, color=ft.Colors.PRIMARY),
                                    ft.Text("Sort Options", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY)
                                ]
                            )
                        ),
                        ft.Container(
                            padding=20,
                            expand=1,
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(ft.Icons.FILTER, size=20, color=ft.Colors.PRIMARY),
                                    ft.Text("Filter Table", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY)
                                ]
                            )
                        ),
                        ft.Container(
                            padding=20,
                            expand=1,
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(ft.Icons.SELECT_ALL, size=20, color=ft.Colors.PRIMARY),
                                    ft.Text("Choose Columns", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY)
                                ]
                            )
                        ),
                    ]
                ),
                content=ft.Row(
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Container(
                            padding=20,
                            expand=1,
                            content=ft.Column(
                                spacing=10,
                                controls=[
                                    ft.Text(f"Sorted by {settings["sort"].split(".")[-1]} {"Ascending" if settings["sort_dir"] else "Descending"}", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY)
                                ]+[
                                    ft.Row(
                                        controls=[
                                            ft.Text(field[1], size=16, width=200, expand=6),
                                            ft.IconButton(ft.Icons.ARROW_UPWARD_OUTLINED, on_click=lambda _,f=field[0],d=True: sort_button(f,d), icon_size=20, icon_color=ft.Colors.PRIMARY, bgcolor=ft.Colors.PRIMARY_CONTAINER if settings["sort"]==field[0] and settings["sort_dir"] else None, disabled=(settings["sort"]==field[0] and settings["sort_dir"]), expand=1),
                                            ft.IconButton(ft.Icons.ARROW_DOWNWARD, on_click=lambda _,f=field[0],d=False: sort_button(f,d), icon_size=20, icon_color=ft.Colors.PRIMARY, bgcolor=ft.Colors.PRIMARY_CONTAINER if settings["sort"]==field[0] and not settings["sort_dir"] else None, disabled=(settings["sort"]==field[0] and not settings["sort_dir"]), expand=1),
                                        ]
                                    ) for field in columns.columns[route]
                                ]
                            )
                        ),
                        ft.Container(
                            padding=20,
                            expand=1,
                            border=ft.Border(
                                left=ft.BorderSide(width=1,color=ft.Colors.PRIMARY_FIXED_DIM),
                                right=ft.BorderSide(width=1,color=ft.Colors.PRIMARY_FIXED_DIM)
                            ),
                            content=ft.Column(
                                spacing=10,
                                controls=[
                                    ft.Text("Filters", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY, expand=1, no_wrap=False)
                                ]+[
                                    ft.Container(
                                        expand=1,
                                        content=ft.Row(
                                            controls=[
                                                ft.Text(field[1], size=16, width=200, expand=3),
                                                ft.Row(
                                                    alignment=ft.MainAxisAlignment.END,
                                                    expand=5,
                                                    spacing=0,
                                                    controls=[ft.Checkbox(label=short,on_change=lambda e,f=field[0],k=long,t="enum": filter_change(e,f,k,t),value=long in settings["filters"][field[0]]) for long,short in field[3]]
                                                ) if field[2]=="enum" else
                                                ft.RangeSlider(
                                                    start_value=settings["filters"][field[0]][0],
                                                    end_value=settings["filters"][field[0]][1],
                                                    min=field[3][0],
                                                    max=field[3][1],
                                                    divisions=(field[3][1]-field[3][0])//field[3][2],
                                                    on_change=lambda e,f=field[0],k=None,t="number": filter_change(e,f,k,t),
                                                    label="{value}",
                                                    expand=5
                                                ) if field[2]=="number" else
                                                date_filter(field[0]) if field[2]=="date" else
                                                ft.TextField(
                                                    label=f"{field[1]}",
                                                    value=settings["filters"][field[0]],
                                                    on_change=lambda e,f=field[0],k=None,t="text": filter_change(e,f,k,t),
                                                    expand=5
                                                ) if field[2]=="text" else
                                                ft.TextField(
                                                    label=f"{field[1]}",
                                                    value=settings["filters"][field[0]],
                                                    on_change=lambda e,f=field[0],k=None,t="id": filter_change(e,f,k,t),
                                                    expand=5
                                                )
                                            ]
                                        )
                                    ) for field in columns.columns[route]
                                ]
                            )
                        ),
                        ft.Container(
                            padding=20,
                            expand=1,
                            content=ft.Column(
                                spacing=10,
                                controls=[
                                    ft.Text(f"{len(settings["columns"])} Fields Selected (Max 8 will be applied)", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY, no_wrap=False)
                                ]+[
                                    ft.Row(
                                        controls=[
                                            ft.Checkbox(value=(num in settings["columns"]), on_change=lambda e,n=num: column_button(e,n), expand=1),
                                            ft.Text(field[1], size=16, width=200, expand=7),
                                        ]
                                    ) for num,field in enumerate(columns.columns[route])
                                ]
                            )
                        )
                    ]
                )
            )
        ]
    )
    return cont



def create_buttons(page:ft.Page, route:str, settings:dict, update_func):
    def change_page(change):
        max_pages = (settings["num_records"]+49)//50
        new = settings["page"] + change
        if 1<=new<=max_pages:
            settings["page"] = new
            update_func()
    def reset_settings():
        settings["sort"] = columns.columns[route][0][0]
        settings["sort_dir"] = True
        settings["filters"] = {
            field[0]: [i[0] for i in field[3]] if field[2]=="enum" else
                      (field[3][0],field[3][1]) if field[2]=="number" else
                      ("1901-01-01","2050-01-01") if field[2]=="date" else
                      "" if field[2]=="text" else
                      None
            for field in columns.columns[route]
        }
        settings["columns"] = [0,1,2,3,4,5]
        settings["page"] = 1
        update_func()
    def apply_settings():
        if len(settings["columns"])>8:
            settings["columns"].sort()
            settings["columns"] = settings["columns"][:8]
        settings["page"] = 1
        update_func()
    cont = ft.Row(
        expand=True,
        controls=[
            ft.Text(
                expand=8,
                value=f"Showing {settings["page"]*50-49}-{min(settings["page"]*50,settings["num_records"])} of {settings["num_records"]} record(s)",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.PRIMARY,
            ),
            ft.IconButton(
                expand=1,
                on_click=lambda _,c=-1: change_page(c),
                icon=ft.Icons.ARROW_LEFT,
                icon_color=ft.Colors.PRIMARY,
                icon_size=24
            ),
            ft.Text(
                expand=2,
                value=f"Page {settings["page"]}",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.PRIMARY,
                text_align=ft.TextAlign.CENTER
            ),
            ft.IconButton(
                expand=1,
                on_click=lambda _,c=1: change_page(c),
                icon=ft.Icons.ARROW_RIGHT,
                icon_color=ft.Colors.PRIMARY,
                icon_size=24
            ),
            ft.Button(
                expand=4,
                on_click=lambda _: reset_settings(),
                content=ft.Text("Reset",size=16,weight=ft.FontWeight.BOLD),
                icon=ft.Icon(ft.Icons.REDO,size=20),
                style = ft.ButtonStyle(
                    bgcolor=ft.Colors.SURFACE_CONTAINER,
                    color=ft.Colors.PRIMARY,
                    padding=ft.Padding(0,20,0,20),
                    shape=ft.RoundedRectangleBorder(radius=10),
                )
            ),
            ft.Button(
                expand=4,
                on_click=lambda _: apply_settings(),
                content=ft.Text("Apply Filter/Columns",size=16,weight=ft.FontWeight.BOLD),
                icon=ft.Icon(ft.Icons.CHANGE_CIRCLE,size=20),
                style = ft.ButtonStyle(
                    bgcolor=ft.Colors.SURFACE_CONTAINER,
                    color=ft.Colors.PRIMARY,
                    padding=ft.Padding(0,20,0,20),
                    shape=ft.RoundedRectangleBorder(radius=10),
                )
            ),
            ft.Button(
                expand=4,
                content=ft.Text(f"Add {names[route]}",size=16,weight=ft.FontWeight.BOLD),
                icon=ft.Icon(ft.Icons.ADD,size=20),
                on_click=lambda _: page.run_task(page.push_route,f"/{route}/add"),
                style = ft.ButtonStyle(
                    bgcolor=ft.Colors.PRIMARY,
                    color=ft.Colors.ON_PRIMARY,
                    padding=ft.Padding(0,20,0,20),
                    shape=ft.RoundedRectangleBorder(radius=10),
                )
            )
        ]
    )
    return cont



def create_table(page:ft.Page, route:str, settings:dict, update_func):
    conn = sqlite3.connect(DATABASE)
    records = queries.view_table(
        conn=conn,
        table=names[route],
        sort_attr=settings["sort"],
        sort_dir=settings["sort_dir"],
        filters=settings["filters"],
        columns=[0]+settings["columns"],
        limit=50,
        offset=50*(settings["page"]-1)
    )
    settings["num_records"] = len(
        queries.view_table(
            conn=conn,
            table=names[route],
            sort_attr=settings["sort"],
            sort_dir=settings["sort_dir"],
            filters=settings["filters"],
            columns=[0]
        )
    )
    cont = ft.Column(
        spacing=5,
        controls=[
            ft.Container(
                padding=10,
                content=ft.Row(
                    controls=[
                        ft.Text(expand=2)
                    ] + [
                        ft.Text(str(columns.columns[route][i][1]),weight=ft.FontWeight.BOLD,text_align=ft.TextAlign.CENTER,expand=10)
                        for i in settings["columns"]
                    ]
                )
            )
        ] + [
            ft.Container(
                bgcolor=ft.Colors.SURFACE_CONTAINER,
                ink=True,
                on_click=lambda _,id=data[0]: page.run_task(page.push_route,f"/{route}/{id}"),
                border_radius=20,
                padding=10,
                content=ft.Row(
                    controls=[
                        ft.Icon(icon=icons[route],color=ft.Colors.PRIMARY,expand=2)
                    ] + [
                        ft.Text(str(attr),text_align=ft.TextAlign.CENTER,expand=10)
                        for attr in (data[1:] if 0 not in settings["columns"] else data)
                    ]
                )
            ) for data in records
        ]
    )
    conn.close()
    return cont



def build_page(page:ft.Page, route:str):
    conn = sqlite3.connect(DATABASE)
    table_settings = {
        "sort": columns.columns[route][0][0],
        "sort_dir": True,
        "filters": {
            field[0]: [i[0] for i in field[3]] if field[2]=="enum" else
                      (field[3][0],field[3][1]) if field[2]=="number" else
                      ("1901-01-01","2050-01-01") if field[2]=="date" else
                      "" if field[2]=="text" else
                      None
            for field in columns.columns[route]
        },
        "columns": list(range(min(8, len(columns.columns[route])))),
        "page": 1,
        "num_records": 0
    }
    table_settings["num_records"] = len(
        queries.view_table(
            conn=conn,
            table=names[route],
            sort_attr=table_settings["sort"],
            sort_dir=table_settings["sort_dir"],
            filters=table_settings["filters"],
            columns=[0]
        )
    )
    conn.close()
    page_container = ft.Container()
    def page_content():
        return ft.Column(
            expand=True,
            spacing=30,
            controls=[
                ft.Column(
                    spacing=10,
                    controls=[
                        ft.Text(
                            value=f"{names[route]} Table",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                        ),
                        create_filters(page,route,table_settings,update_page),
                        create_buttons(page,route,table_settings,update_page)
                    ]
                ),
                create_table(page,route,table_settings,update_page)
            ]
        )
    def update_page():
        page_container.content = page_content()
        page_container.update()
    page_container.content = page_content()
    return page_container