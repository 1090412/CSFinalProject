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
        value = event.control.value
        field = editables[index]
        if field[3]=="id" and value not in [None,"",0]:
            value = int(value)
        if field[3]=="enum":
            for val,txt in field[4]:
                if str(val) == str(value):
                    value = val
                    break
        editables[index][2] = value
    def find_errors():
        errors = []
        for field in editables:
            if field[3]=="text" and not field[2].strip():
                errors.append(f"{field[1]} is empty.")
            if field[3]=="enum" and field[2] not in [i[0] for i in field[4]]:
                errors.append(f"{field[1]} is an invalid option.")
        if len(errors)==0:
            errors.append(f"Data format is invalid.")
        return errors
    def error_popup():
        page.show_dialog(
            ft.AlertDialog(
                title=ft.Text("Invalid Data"),
                content=ft.Column(
                    controls=[ft.Text(f"{error}") for error in find_errors()],
                    tight=True,
                ),
                actions=[ft.Button("OK",on_click=lambda _: page.pop_dialog())],
            )
        )
    def apply_changes():
        conn = sqlite3.connect(DATABASE)
        try:
            values = [i[2] for i in editables]
            if values[0]>0:
                values = [conn] + values
                queries.edit_athlete(*values)
                page.update()
                page.run_task(page.push_route,f"/{route}/{values[1]}")
            else:
                values = [conn] + values[1:]
                queries.add_athlete(*values)
                page.run_task(page.push_route,f"/{route}/view")
        except sqlite3.IntegrityError as e:
            error_popup()
        conn.close()
    def create_date_picker(value,index):
        def date_change(event,index):
            editables[index][2] = event.control.value.strftime("%Y-%m-%d")
            button.content = date_picker.value.strftime("%Y-%m-%d")
            button.update()
        date_picker = ft.DatePicker(
            value=datetime.datetime.strptime(value,"%Y-%m-%d") if value else datetime.datetime.now(),
            on_change=lambda e: date_change(e,index)
        )
        button = ft.Button(
            expand=1,
            icon=ft.Icons.CALENDAR_MONTH,
            content=date_picker.value.strftime("%Y-%m-%d"),
            on_click=lambda _: page.show_dialog(date_picker)
        )
        return button
    mid = len(editables)//2
    conn = sqlite3.connect(DATABASE)
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
                                    create_date_picker(value,i) if types=="date" else
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


def relational_content(page:ft.Page, route:str, link, info, id):
    conn = sqlite3.connect(DATABASE)
    records = queries.get_relations(
        conn=conn,
        table=info[1][2],
        pk_field=info[1][3],
        parent_id=id,
        fields=[info[1][4]]+[i[0] for i in info[3]]
    )
    records = [list(record) for record in records]
    def create_date_picker(rec,index):
        def date_change(event,r,i):
            records[r][i+1] = event.control.value.strftime("%Y-%m-%d")
            button.content = date_picker.value.strftime("%Y-%m-%d")
            button.update()
        date_picker = ft.DatePicker(
            value=datetime.datetime.strptime(records[rec][index+1],"%Y-%m-%d") if records[rec][index+1] else datetime.datetime.now(),
            on_change=lambda e: date_change(e,rec,index)
        )
        button = ft.Button(
            expand=int(12/len(info[3])),
            icon=ft.Icons.CALENDAR_MONTH,
            content=date_picker.value.strftime("%Y-%m-%d"),
            on_click=lambda _: page.show_dialog(date_picker)
        )
        return button
    def on_change(event,rec,index):
        value = event.control.value
        field = info[3][index]
        if field[1]=="id" and value not in [None,"",0]:
            value = int(value)
        if field[1]=="enum":
            for val,txt in field[2]:
                if str(val) == str(value):
                    value = val
                    break
        records[rec][index+1] = value
        apply_changes()
    def apply_changes():
        conn = sqlite3.connect(DATABASE)
        for record in records:
            queries.update_relation(
                conn=conn,
                table=info[1][2],
                pk1_field=info[1][3],
                pk1_id=id,
                pk2_field=info[1][4],
                pk2_id=record[0],
                fields=[i[0] for i in info[3]],
                values=record[1:]
            )
        conn.close()
    def delete_record(rec):
        conn = sqlite3.connect(DATABASE)
        queries.delete_relation(
            conn=conn,
            table=info[1][2],
            pk1_field=info[1][3],
            pk1_id=id,
            pk2_field=info[1][4],
            pk2_id=records[rec][0]
        )
        records.pop(rec)
        refresh_rows()
        conn.close()
    rows = ft.Column(
        spacing=10,
        expand=True,
        controls=[]
    )
    def refresh_rows():
        conn = sqlite3.connect(DATABASE)
        rows.controls = [
            ft.Row(
                expand=True,
                controls=[
                    ft.Text(expand=1),
                    ft.Text(
                        columns.names[link](
                            queries.view_table(conn,info[1][1],columns.columns[link][0][0],True,{columns.columns[link][0][0]:record[0]},list(range(len(columns.columns[link]))))[0]
                        ),
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        expand=8
                    )
                ] + [
                    ft.Dropdown(
                        expand=int(12/len(info[3])),
                        label=field[0],
                        value=record[i+1],
                        on_select=lambda e,r=r,i=i:on_change(e,r,i),
                        options=[
                            ft.DropdownOption(
                                key=long,
                                text=short if isinstance(long,int) else long,
                            ) for long,short in field[2]
                        ]
                    ) if field[1]=="enum" else
                    ft.Slider(
                        expand=int(12/len(info[3])),
                        on_change=lambda e,r=r,i=i:on_change(e,r,i),
                        value=record[i+1],
                        label="{value} hours",
                        min=field[2][0],
                        max=field[2][1],
                        divisions=8
                    ) if field[1]=="number" else
                    create_date_picker(r,i) if field[1]=="date" else
                    ft.TextField(
                        expand=int(12/len(info[3])),
                        value=record[i+1],
                        label=field[0],
                        on_change=lambda e,r=r,i=i:on_change(e,r,i)
                    ) if field[1]=="text" else
                    ft.Dropdown(
                        expand=int(12/len(info[3])),
                        value=record[i+1],
                        on_select=lambda e,r=r,i=i:on_change(e,r,i),
                        label=field[0],
                        editable=True,
                        menu_height=300,
                        options=[
                            ft.DropdownOption(
                                key=values[0],
                                text=columns.names[field[2][1]](values),
                            ) for values in queries.view_table(conn,field[2][0],columns.columns[field[2][1]][0][0],True,{},list(range(len(columns.columns[field[2][1]]))))
                        ]
                    )
                    for i,field in enumerate(info[3])
                ] + [
                    ft.IconButton(
                        expand=1,
                        icon=ft.Icons.DELETE,
                        icon_color=ft.Colors.ERROR,
                        bgcolor=ft.Colors.ERROR_CONTAINER,
                        on_click=lambda _,r=r: delete_record(r)
                    )
                ]
            ) for r,record in enumerate(records)
        ]
        conn.close()
    refresh_rows()
    cont = ft.Column(
        expand=True,
        spacing=10,
        controls=[
            ft.Divider(height=5),
            ft.Text(
                value=info[0],
                size=20,
                weight=ft.FontWeight.BOLD,
            ),
            rows,
            ft.TextButton(
                content=f"Add {info[1][1]} Relation",
                icon=ft.Icons.ADD
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
    if id>0:
        relations = [relational_content(page,route,link,info,id) for link,info in columns.relations[route].items()]
    else:
        relations = []
    cont = ft.Column(
        expand=True,
        spacing=10,
        controls=[
            top_content(page,route,editables)
        ] + relations
    )
    conn.close()
    return cont