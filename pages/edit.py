import flet as ft
import sqlite3
import datetime
import database.queries as queries
import database.columns as columns

DATABASE = "database/database.db"

names = {
    "athletes":"Athlete",
    "competitions":"Competition",
    "events":"Event",
    "patrols":"Patrol",
    "volunteering":"VolunteerActivity",
    "qualifications":"Qualification",
}



def top_content(page:ft.Page, route:str, editables):
    def on_change(event,index):
        editables[index][2] = event.control.value
    def apply_changes():
        values = [i[2] for i in editables]
        conn = sqlite3.connect(DATABASE)
        if values[0]>0:
            values = [conn] + values
            queries.edit_athlete(*values)
            page.run_task(page.push_route,f"/{route}/{values[1]}")
        else:
            values = [conn] + values[1:]
            queries.add_athlete(*values)
            page.run_task(page.push_route,f"/{route}/view")
        conn.close()
    mid = len(editables)//2
    conn = sqlite3.connect(DATABASE)
    date_picker = ft.DatePicker(
        value=datetime.datetime(1900,1,1)
    )
    cont = ft.Column(
        spacing=10,
        controls=[
            ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.END,
                expand=True,
                controls=[
                    ft.Column(
                        expand=3,
                        controls=[
                            ft.Text(
                                value=f"Edit {names[route]}",
                                size=32,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                value=f"{names[route]} {f"#{editables[0][2]}" if editables[0][2]>0 else "New"}",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ]
                    ),
                    ft.Button(
                        expand=1,
                        height=50,
                        content=ft.Text(f"Back to Table",size=16,weight=ft.FontWeight.BOLD),
                        icon=ft.Icon(ft.Icons.TABLE_VIEW,size=20),
                        on_click=lambda _: page.run_task(page.push_route,f"/{route}/view"),
                        style = ft.ButtonStyle(
                            bgcolor=ft.Colors.SURFACE_CONTAINER,
                            color=ft.Colors.PRIMARY,
                            padding=ft.Padding(0,20,0,20),
                            shape=ft.RoundedRectangleBorder(radius=10),
                        )
                    ),
                    ft.Button(
                        expand=1,
                        height=50,
                        content=ft.Text(f"Apply Changes",size=16,weight=ft.FontWeight.BOLD),
                        icon=ft.Icon(ft.Icons.EDIT,size=20),
                        on_click=apply_changes,
                        style = ft.ButtonStyle(
                            bgcolor=ft.Colors.PRIMARY,
                            color=ft.Colors.ON_PRIMARY,
                            padding=ft.Padding(0,20,0,20),
                            shape=ft.RoundedRectangleBorder(radius=10),
                        )
                    )
                    
                ]
            ),   
            ft.Divider(height=10),
            ft.Row(
                spacing=100,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Column(
                        spacing=10,
                        expand=True,
                        controls=[
                            ft.Row(
                                expand=1,
                                controls=[
                                    ft.Text(name,weight=ft.FontWeight.BOLD,expand=1),
                                    ft.Dropdown(
                                        expand=1,
                                        label=name,
                                        value=value,
                                        on_select=lambda e,i=i: on_change(e,i),
                                        options=[
                                            ft.DropdownOption(
                                                key=long,
                                                text=short if isinstance(long,int) else long,
                                            ) for long,short in info
                                        ]
                                    ) if types=="enum" else
                                    ft.Slider(
                                        expand=1,
                                        value=value,
                                        on_change=lambda e,i=i: on_change(e,i),
                                        label="{value} hours",
                                        min=info[0],
                                        max=info[1],
                                        divisions=info[2]
                                    ) if types=="number" else
                                    ft.Button(
                                        expand=1,
                                        icon=ft.Icons.DATE_RANGE,
                                        content="Pick Date",
                                        on_click=lambda _: page.show_dialog(date_picker)
                                    ) if types=="date" else
                                    ft.TextField(expand=1,value=value,label=f"{name}",on_change=lambda e,i=i: on_change(e,i)) if types=="text" else
                                    ft.Dropdown(
                                        expand=1,
                                        value=value,
                                        on_select=lambda e,i=i: on_change(e,i),
                                        label=name,
                                        editable=True,
                                        menu_height=300,
                                        options=[
                                            ft.DropdownOption(
                                                key=values[0],
                                                text=columns.names[info[1]](values),
                                            ) for values in queries.view_table(conn,info[0],columns.columns[info[1]][0][0],True,{},list(range(len(columns.columns[info[1]]))))
                                        ]
                                    )
                                ]
                            ) for name_long,name,value,types,info,i in fields
                        ]
                    ) for fields in (editables[1:mid+1], editables[mid+1:])
                ]
            )
        ]
    )
    conn.close()
    return cont



def build_page(page:ft.Page, route:str, id:int):
    conn = sqlite3.connect(DATABASE)
    editable_cols = [i for i,field in enumerate(columns.columns[route]) if field[0].split(".")[0]==names[route]]
    if id>0:
        values = queries.view_table(
            conn=conn,
            table=names[route],
            sort_attr=columns.columns[route][0][0],
            sort_dir=True,
            filters={
                columns.columns[route][0][0]:id
            },
            columns=editable_cols
        )[0]
    editables = [
        [
            columns.columns[route][n][0],
            columns.columns[route][n][1],
            values[i] if id>0 else
            0 if columns.columns[route][n][2] in ["number","id"] else "",
            columns.columns[route][n][2],
            columns.columns[route][n][3] if len(columns.columns[route][n])>3 else None,
            i
        ] for i,n in enumerate(editable_cols)
    ]
    cont = ft.Column(
        expand=True,
        spacing=30,
        controls=[
            top_content(page,route,editables)
        ]
    )
    conn.close()
    return cont