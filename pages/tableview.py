import flet as ft
import sqlite3
import database.queries as queries
import database.enums as enums

DATABASE = "database/database.db"

names = {
    "athletes":"Athlete",
    "competitions":"Competition",
    "events":"Event",
    "patrols":"Patrol",
    "volunteering":"VolunteerActivity",
    "qualifications":"Qualification",
}

icons = {
    "athletes":ft.Icons.PERSON,
    "competitions":ft.Icons.PERSON,
    "events":ft.Icons.PERSON,
    "patrolgroups":ft.Icons.PERSON,
    "patrols":ft.Icons.PERSON,
    "volunteering":ft.Icons.PERSON,
    "qualifications":ft.Icons.PERSON,
}

columns = {
    "athletes": [
        ("Athlete.AthleteID", "Athlete ID", "id"),
        ("Name", "Name", "text"),
        ("Athlete.FirstName", "First Name", "text"),
        ("Athlete.LastName", "Last Name", "text"),
        ("Athlete.Gender", "Gender", "enum", (("Male","M"),("Female","F"),("Not Specified","-"))),
        ("Athlete.DOB", "Date of Birth", "date"),
        ("Athlete.MainDiscipline", "Main Discipline", "enum", (("Surf","S"),("Beach","Be"),("Boats","Bo"),("Lifesaving","L"),)),
        ("Athlete.PatrolGroupID", "Patrol Group ID", "id"),
        ("Athlete.Phone", "Phone", "text"),
        ("Athlete.Email", "Email", "text"),
        ("Athlete.Active", "Active", "enum", ((1,"Active"),(0,"Inactive"))),
        ("Patrols", "Patrols", "number"),
        ("PatrolHours", "Patrol Hours", "number"),
        ("VolunteerSessions", "Volunteer Sessions", "number"),
        ("VolunteerHours", "Volunteer Hours", "number"),
        ("TotalHours", "Total Hours", "number"),
        ("Competitions", "Competitions", "number"),
        ("Races", "Races", "number"),
        ("Qualifications", "Qualifications", "number"),
        ("PatrolPoints", "Patrol Points", "number"),
        ("VolunteerPoints", "Volunteer Points", "number"),
        ("CompetitionPoints", "Competition Points", "number"),
        ("TotalPoints", "Total Points", "number")
    ],
    "competitions": [
        ("Competition.CompetitionID", "Competition ID", "id"),
        ("Competition.Name", "Name", "text"),
        ("Competition.Season", "Season", "text"),
        ("Competition.Discipline", "Discipline", "enum", (("Surf","S"),("Beach","Be"),("Boats","Bo"),("Lifesaving","L"),)),
        ("Competition.Location", "Location", "text"),
        ("Competition.StartDate", "Start Date", "date"),
        ("Competition.EndDate", "End Date", "date"),
        ("Competition.Importance", "Importance", "number"),
        ("Races", "Races", "number"),
        ("Competitors", "Competitors", "number"),
        ("Results", "Results", "number")
    ],
    "events": [
        ("Event.EventID", "Event ID", "id"),
        ("Event.Name", "Name", "text"),
        ("Event.Discipline", "Discipline", "enum", (("Surf","S"),("Beach","Be"),("Boats","Bo"),("Lifesaving","L"),)),
        ("Event.TeamEvent", "Team Event", "enum", (("Indiv.",0),("Team",1))),
        ("Event.Importance", "Importance", "number")
    ],
    "patrolgroups": [
        ("PatrolGroup.PatrolGroupID", "Patrol Group ID", "id"),
        ("PatrolGroup.Name", "Name", "text"),
        ("PatrolGroup.SupervisorID", "Supervisor ID", "id"),
        ("SupervisorName", "Supervisor Name", "text"),
        ("Patrols", "Patrols", "number"),
        ("AverageAttendance", "Average Attendance", "number"),
        ("UniqueAttendees", "Unique Attendees", "number")
    ],
    "patrols": [
        ("Patrol.PatrolID", "Patrol ID", "id"),
        ("Patrol.PatrolGroupID", "Patrol Group ID", "id"),
        ("PatrolGroupName", "Patrol Group Name", "text"),
        ("SupervisorName", "Supervisor Name", "text"),
        ("Patrol.Date", "Date", "date"),
        ("Patrol.Session", "Session", "enum", (("Morning","AM"),("Afternoon","PM"),("All Day","All"),)),
        ("Patrol.Holiday", "Holiday", "enum", (("Normal",0),("Holiday",1))),
        ("Attendance", "Attendance", "number"),
        ("AverageHoursEarned", "Average Hours Earned", "number"),
        ("TotalHoursEarned", "Total Hours Earned", "number")
    ],
    "volunteering": [
        ("VolunteerActivity.ActivityID", "Activity ID", "id"),
        ("VolunteerActivity.Name", "Name", "text"),
        ("VolunteerActivity.SupervisorID", "Supervisor ID", "id"),
        ("SupervisorName", "Supervisor Name", "text"),
        ("VolunteerActivity.Type", "Type", "enum", (("Course Trainer","CT"),("Water Safety","WS"),("Sunday Program Help","Sun"),("Fundraiser","Fund"),("Club Chore","Club"),)),
        ("VolunteerActivity.Date", "Date", "date"),
        ("VolunteerActivity.FundsRaised", "Funds Raised", "number"),
        ("VolunteerActivity.PercFundsReceived", "Percentage Funds Received", "number"),
        ("AthleteGrantContribution", "Athlete Grant Contribution", "number"),
        ("FundsRaisedPerAthlete", "Funds Raised Per Athlete", "number"),
        ("Attendance", "Attendance", "number"),
        ("AverageHoursEarned", "Average Hours Earned", "number"),
        ("TotalHoursEarned", "Total Hours Earned", "number")
    ],
    "qualifications": [
        ("Qualification.QualificationID", "Qualification ID", "id"),
        ("Qualification.Name", "Name", "text"),
        ("Requals", "Requalifications", "number"),
        ("Athletes", "Athletes", "number")
    ]
}



def create_filters(page:ft.Page, route:str, settings:dict, update_func):
    def sort_button(field,dir):
        settings["sort"] = field
        settings["sort_dir"] = dir
        settings["page"] = 1
        update_func()
    def filter_button(field):
        ...
        update_func()
    def column_button(event,field_no):
        if event.control.value and field_no not in settings["columns"]:
            settings["columns"].append(field_no)
        if not event.control.value and field_no in settings["columns"]:
            settings["columns"].remove(field_no)
        settings["page"] = 1
        update_func()
    cont = ft.Row(
        expand=True,
        controls=[
            ft.ExpansionPanelList(
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
                                            ) for field in columns[route]
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
                                            ft.Text("2 Active Filters", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY, expand=1, no_wrap=False)
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
                                                            controls=[ft.Checkbox(label=short) for long,short in field[3]]
                                                        ) if field[2]=="enum" else
                                                        ft.RangeSlider(start_value=0,end_value=10,min=0,max=10,label="{value}",expand=5) if field[2]=="number" else
                                                        ft.Button(
                                                            icon=ft.Icons.DATE_RANGE,
                                                            content="Pick Date Range",
                                                            on_click=lambda _: page.show_dialog(ft.DateRangePicker()),
                                                            expand=5
                                                        ) if field[2]=="date" else
                                                        ft.TextField(label=f"{field[1]}",expand=5)
                                                    ]
                                                )
                                            ) for field in columns[route]
                                        ]
                                    )
                                ),
                                ft.Container(
                                    padding=20,
                                    expand=1,
                                    content=ft.Column(
                                        spacing=10,
                                        controls=[
                                            ft.Text(f"{len(settings["columns"])} Fields Selected", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY, no_wrap=False)
                                        ]+[
                                            ft.Row(
                                                controls=[
                                                    ft.Checkbox(value=(num in settings["columns"]), on_change=lambda e,n=num: column_button(e,n), expand=1),
                                                    ft.Text(field[1], size=16, width=200, expand=7),
                                                ]
                                            ) for num,field in enumerate(columns[route])
                                        ]
                                    )
                                )
                            ]
                        )
                    )
                ]
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
        settings["sort"] = columns[route][0][0]
        settings["sort_dir"] = True
        settings["filters"] = {}
        settings["columns"] = [0,1,2,3,4,5]
        settings["page"] = 1
        update_func()
    cont = ft.Row(
        expand=True,
        controls=[
            ft.Text(
                expand=12,
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
                content=ft.Text(f"Add {names[route]}",size=16,weight=ft.FontWeight.BOLD),
                icon=ft.Icon(ft.Icons.ADD,size=20),
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
        columns=settings["columns"],
        limit=50,
        offset=50*(settings["page"]-1)
    )
    settings["num_records"] = queries.table_size(
        conn=conn,
        table=names[route],
        column=columns[route][0][0],
        filters=settings["filters"]
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
                        ft.Text(str(columns[route][i][0]),weight=ft.FontWeight.BOLD,text_align=ft.TextAlign.CENTER,expand=10)
                        for i in settings["columns"]
                    ]
                )
            )
        ] + [
            ft.Container(
                bgcolor=ft.Colors.SURFACE_CONTAINER,
                ink=True,
                on_click=lambda _:0,
                border_radius=20,
                padding=10,
                content=ft.Row(
                    controls=[
                        ft.Icon(icon=icons[route],color=ft.Colors.PRIMARY,expand=2)
                    ] + [
                        ft.Text(str(attr),text_align=ft.TextAlign.CENTER,expand=10)
                        for attr in data
                    ]
                )
            ) for data in records
        ]
    )
    conn.close()
    return cont



def build_page(page:ft.Page, route:str):
    table_settings = {
        "sort": columns[route][0][0],
        "sort_dir": True,
        "filters": {},
        "columns": [0,1,2,3,4,5],
        "page": 1,
        "num_records": 0
    }
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