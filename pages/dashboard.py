import flet as ft
import random
import sqlite3
import database.queries as queries

DATABASE = "database/database.db"

def get_info_cards(route:str):
    conn = sqlite3.connect(DATABASE)
    information_cards = {
        "home":[
            (ft.Icons.PERSON, queries.view_aggregate(conn,"Athlete","AthleteID","COUNT",distinct=True), "Registered Athletes"),
            (ft.Icons.SUPERVISOR_ACCOUNT, queries.view_aggregate(conn,"Supervisor","SupervisorID","COUNT",distinct=True), "Registered Supervisors"),
            (ft.Icons.SAFETY_DIVIDER, queries.view_aggregate(conn,"Patrol","PatrolID","COUNT",distinct=True), "Completed Patrols"),
            (ft.Icons.LOCK_CLOCK, queries.view_aggregate(conn,"Athlete_Patrol","Hours","SUM")+queries.view_aggregate(conn,"Athlete_Volunteer","Hours","SUM"), "Total Hours"),
        ],
        "athletes":[
            (ft.Icons.PERSON, queries.view_aggregate(conn,"Athlete","AthleteID","COUNT",distinct=True), "Registered Athletes"),
            (ft.Icons.SAFETY_DIVIDER, queries.view_aggregate(conn,"Athlete_Patrol","AthleteID","COUNT",distinct=True), "Patroling Athletes"),
            (ft.Icons.VOLUNTEER_ACTIVISM, queries.view_aggregate(conn,"Athlete_Volunteer","AthleteID","COUNT",distinct=True), "Volunteering Athletes"),
            (ft.Icons.EMOJI_EVENTS, queries.view_aggregate(conn,"Athlete_Result","AthleteID","COUNT",distinct=True), "Competing Athletes"),
        ],
        "competitions":[
            (ft.Icons.EMOJI_EVENTS, queries.view_aggregate(conn,"Competition","CompetitionID","COUNT",distinct=True), "Competitions"),
            (ft.Icons.DIRECTIONS_RUN, queries.view_aggregate(conn,"Result","ResultID","COUNT",distinct=True), "Results"),
            (ft.Icons.PERSON, queries.view_aggregate(conn,"Athlete_Result","AthleteID","COUNT",distinct=True), "Competing Athletes"),
        ],
        "patrols":[
            (ft.Icons.GROUPS, queries.view_aggregate(conn,"PatrolGroup","PatrolGroupID","COUNT",distinct=True), "Patrol Groups"),
            (ft.Icons.SAFETY_DIVIDER, queries.view_aggregate(conn,"Patrol","PatrolID","COUNT",distinct=True), "Patrol Sessions"),
            (ft.Icons.LOCK_CLOCK, queries.view_aggregate(conn,"Athlete_Patrol","Hours","SUM"), "Total Patrol Hours"),
            (ft.Icons.LOCK_CLOCK_OUTLINED, round(queries.view_aggregate(conn,"Athlete_Patrol","Hours","AVG"),2), "Average Hours per Patrol"),
        ],
        "volunteering":[
            (ft.Icons.VOLUNTEER_ACTIVISM, queries.view_aggregate(conn,"VolunteerActivity","ActivityID","COUNT",distinct=True), "Volunteer Sessions"),
            (ft.Icons.LOCK_CLOCK, queries.view_aggregate(conn,"Athlete_Volunteer","Hours","SUM"), "Total Volunteer Hours"),
            (ft.Icons.LOCK_CLOCK_OUTLINED, round(queries.view_aggregate(conn,"Athlete_Volunteer","Hours","AVG"),2), "Average Hours per Session"),
            (ft.Icons.MONEY, "$"+str(round(queries.view_aggregate(conn,"VolunteerActivity","FundsRaised","SUM"))), "Money Raised"),
        ],
        "qualifications":[
            (ft.Icons.CARD_MEMBERSHIP, queries.view_aggregate(conn,"QualificationAward","AwardID","COUNT",distinct=True), "Qualification Awards"),
            (ft.Icons.REFRESH, queries.view_aggregate(conn,"Requalification","AthleteID","COUNT"), "Requalifications"),
            (ft.Icons.PERSON, queries.view_aggregate(conn,"Requalification","AthleteID","COUNT",distinct=True), "Qualified Athletes"),
        ],
    }
    conn.close()
    return information_cards[route]

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
            ) for icon,number,stat in get_info_cards(route)
        ]
    )
    return cont



summary_card = {
    "home":[
        "Database Overview"
    ],
    "athletes":[
        "Athlete Overview"
    ],
    "competitions":[
        "Competitions Overview"
    ],
    "patrols":[
        "Patrol Overview"
    ],
    "volunteering":[
        "Volunteering Overview"
    ],
    "qualifications":[
        "Qualifications Overview"
    ],
}

# The majority of the function was unused/not completed
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



def get_minitable(route:str):
    conn = sqlite3.connect(DATABASE)
    minitables = {
        "home":[
            (
                "Athlete",
                "/athletes",
                ft.Icons.PERSON,
                ("Name","Patrols","Total Hours","Competitions",),
                queries.view_table(
                    conn=conn,
                    table="Athlete",
                    sort_attr="TotalHours",
                    sort_dir=False,
                    filters={},
                    columns=[1,11,15,16],
                    limit=10
                )
            ),
        ],
        "athletes":[
            (
                "Athlete",
                "/athletes",
                ft.Icons.PERSON,
                ("Name","Gender","DOB"),
                queries.view_table(
                    conn=conn,
                    table="Athlete",
                    sort_attr="Name",
                    sort_dir=True,
                    filters={},
                    columns=[1,4,5],
                    limit=10
                )
            ),
            (
                "Supervisors",
                "/supervisors",
                ft.Icons.SUPERVISOR_ACCOUNT,
                ("Name","Phone","Email"),
                queries.view_table(
                    conn=conn,
                    table="Supervisor",
                    sort_attr="Name",
                    sort_dir=True,
                    filters={},
                    columns=[1,4,5],
                    limit=10
                )
            ),
        ],
        "competitions":[
            (
                "Competition",
                "/competitions",
                ft.Icons.EMOJI_EVENTS,
                ("Name","Discipline","Date","Competitiors"),
                queries.view_table(
                    conn=conn,
                    table="Competition",
                    sort_attr="Competition.StartDate",
                    sort_dir=False,
                    filters={},
                    columns=[1,3,5,9],
                    limit=10
                )
            ),
            (
                "Event",
                "/events",
                ft.Icons.FLAG,
                ("Name","Discipline","Team Event"),
                queries.view_table(
                    conn=conn,
                    table="Event",
                    sort_attr="Event.Name",
                    sort_dir=True,
                    filters={},
                    columns=[1,2,3],
                    limit=10
                )
            ),
            (
                "Race",
                "/races",
                ft.Icons.DIRECTIONS_RUN,
                ("Competition","Event","Age Group","Gender"),
                queries.view_table(
                    conn=conn,
                    table="Race",
                    sort_attr="Race.RaceID",
                    sort_dir=True,
                    filters={},
                    columns=[2,4,5,6],
                    limit=10
                )
            ),
            (
                "Result",
                "/results",
                ft.Icons.EMOJI_EVENTS,
                ("Competition","Event","Age Group","Gender","Ranking"),
                queries.view_table(
                    conn=conn,
                    table="Result",
                    sort_attr="Result.ResultID",
                    sort_dir=True,
                    filters={},
                    columns=[2,3,4,5,6],
                    limit=10
                )
            ),
        ],
        "patrols":[
            (
                "Athlete",
                "/athletes",
                ft.Icons.PERSON,
                ("Name","Patrols","Patrol Hours","Patrol Pts"),
                queries.view_table(
                    conn=conn,
                    table="Athlete",
                    sort_attr="PatrolHours",
                    sort_dir=False,
                    filters={},
                    columns=[1,11,12,19],
                    limit=10
                )
            ),
            (
                "Patrol Group",
                "/patrolgroups",
                ft.Icons.GROUPS,
                ("Name","Captain","Patrols","Avg. Attendance"),
                queries.view_table(
                    conn=conn,
                    table="PatrolGroup",
                    sort_attr="PatrolGroup.Name",
                    sort_dir=True,
                    filters={},
                    columns=[1,3,4,5],
                    limit=10
                )
            ),
            (
                "Patrol",
                "/patrols",
                ft.Icons.SAFETY_DIVIDER,
                ("Patrol Group","Date","Session","Attendance"),
                queries.view_table(
                    conn=conn,
                    table="Patrol",
                    sort_attr="Patrol.Date",
                    sort_dir=False,
                    filters={},
                    columns=[2,4,5,7],
                    limit=10
                )
            ),
        ],
        "volunteering":[
            (
                "Athlete",
                "/athletes",
                ft.Icons.PERSON,
                ("Name","Vol. Sessions","Vol. Hours","Volunteering Pts"),
                queries.view_table(
                    conn=conn,
                    table="Athlete",
                    sort_attr="VolunteerHours",
                    sort_dir=False,
                    filters={},
                    columns=[1,13,14,20],
                    limit=10
                )
            ),
            (
                "Volunteer Activity",
                "/volunteering",
                ft.Icons.SAFETY_DIVIDER,
                ("Name","Date","Funds Raised","Attendance"),
                queries.view_table(
                    conn=conn,
                    table="VolunteerActivity",
                    sort_attr="VolunteerActivity.Date",
                    sort_dir=False,
                    filters={},
                    columns=[1,5,6,10],
                    limit=10
                )
            ),
        ],
        "qualifications":[
            (
                "Qualification Award",
                "/qualifications",
                ft.Icons.CARD_MEMBERSHIP,
                ("Name","Requalifications","Unique Athletes"),
                queries.view_table(
                    conn=conn,
                    table="QualificationAward",
                    sort_attr="QualificationAward.Name",
                    sort_dir=True,
                    filters={},
                    columns=[1,2,3],
                    limit=10
                )
            ),
            (
                "Supervisors",
                "/supervisors",
                ft.Icons.SUPERVISOR_ACCOUNT,
                ("Name","Requalifications"),
                queries.view_table(
                    conn=conn,
                    table="Supervisor",
                    sort_attr="Name",
                    sort_dir=True,
                    filters={},
                    columns=[1,9],
                    limit=10
                )
            ),
        ],
    }
    conn.close()
    return minitables[route]

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
                        ft.TextButton(f"View All Records", icon=ft.Icons.SEARCH, on_click=lambda _,link=link: page.run_task(page.push_route,link+"/view"))
                    ]
                )
            ) for name,link,icon,columns,data in get_minitable(route) for i in range(2)
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
        ft.Container(
            expand=True,
            padding=25,
            border_radius=20,
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            content=ft.Text("Graphs are coming soon!",text_align=ft.TextAlign.CENTER)
        )
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
                    ft.Column(expand=4, spacing=15, controls=create_left_cont(page,route)),
                    ft.Column(expand=2, spacing=15, controls=create_right_cont(page,route)),
                ]
            )
        ]
    )
    return cont