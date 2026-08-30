columns = {
    "athletes": [
        ("Athlete.AthleteID", "Athlete ID", "id"),
        ("Name", "Name", "text"),
        ("Athlete.FirstName", "First Name", "text"),
        ("Athlete.LastName", "Last Name", "text"),
        ("Athlete.Gender", "Gender", "enum", (("Male","M"),("Female","F"),("Not Specified","-"))),
        ("Athlete.DOB", "Date of Birth", "date"),
        ("Athlete.MainDiscipline", "Main Discipline", "enum", (("Surf","S"),("Beach","Be"),("Boats","Bo"),("Lifesaving","L"))),
        ("Athlete.PatrolGroupID", "Patrol Group ID", "id", ("PatrolGroup","patrolgroups")),
        ("Athlete.Phone", "Phone", "text"),
        ("Athlete.Email", "Email", "text"),
        ("Athlete.Active", "Active", "enum", ((1,"Active"),(0,"Inactive"))),
        ("Patrols", "Patrols", "number", (0,20,1)),
        ("PatrolHours", "Patrol Hours", "number", (0,100,1)),
        ("VolunteerSessions", "Volunteer Sessions", "number", (0,20,1)),
        ("VolunteerHours", "Volunteer Hours", "number", (0,100,1)),
        ("TotalHours", "Total Hours", "number", (0,200,1)),
        ("Competitions", "Competitions", "number", (0,20,1)),
        ("Races", "Races", "number", (0,50,1)),
        ("Qualifications", "Qualifications", "number", (0,20,1)),
        ("PatrolPoints", "Patrol Points", "number", (0,1000,1)),
        ("VolunteerPoints", "Volunteer Points", "number", (0,1000,1)),
        ("CompetitionPoints", "Competition Points", "number", (0,1000,1)),
        ("TotalPoints", "Total Points", "number", (0,3000,1))
    ],
    "supervisors": [
        ("Supervisor.SupervisorID", "Supervisor ID", "id"),
        ("Name", "Name", "text"),
        ("Supervisor.FirstName", "First Name", "text"),
        ("Supervisor.LastName", "Last Name", "text"),
        ("Supervisor.Phone", "Phone", "text"),
        ("Supervisor.Email", "Email", "text"),
        ("PatrolGroups", "Patrol Groups", "number", (0,50,1)),
        ("PatrolsSupervised", "Patrols Supervised", "number", (0,100,1)),
        ("VolunteersSupervised", "Volunteers Supervised", "number", (0,100,1)),
        ("Requalifications", "Requalifications", "number", (0,100,1))
    ],
    "patrolgroups": [
        ("PatrolGroup.PatrolGroupID", "Patrol Group ID", "id"),
        ("PatrolGroup.Name", "Name", "text"),
        ("PatrolGroup.SupervisorID", "Supervisor ID", "id", ("Supervisor","supervisors")),
        ("SupervisorName", "Supervisor Name", "text"),
        ("Patrols", "Patrols", "number", (0,50,1)),
        ("AverageAttendance", "Average Attendance", "number", (0,30,1)),
        ("UniqueAttendees", "Unique Attendees", "number", (0,50,1))
    ],
    "patrols": [
        ("Patrol.PatrolID", "Patrol ID", "id"),
        ("Patrol.PatrolGroupID", "Patrol Group ID", "id", ("PatrolGroup","patrolgroups")),
        ("PatrolGroupName", "Patrol Group Name", "text"),
        ("SupervisorName", "Supervisor Name", "text"),
        ("Patrol.Date", "Date", "date"),
        ("Patrol.Session", "Session", "enum", (("Morning","AM"),("Afternoon","PM"),("All Day","All"))),
        ("Patrol.Holiday", "Holiday", "enum", ((0,"Normal"),(1,"Holiday"))),
        ("Attendance", "Attendance", "number", (0,50,1)),
        ("AverageHoursEarned", "Average Hours Earned", "number", (0,10,1)),
        ("TotalHoursEarned", "Total Hours Earned", "number", (0,500,1))
    ],
    "volunteering": [
        ("VolunteerActivity.ActivityID", "Activity ID", "id"),
        ("VolunteerActivity.Name", "Name", "text"),
        ("VolunteerActivity.SupervisorID", "Supervisor ID", "id", ("Supervisor","supervisors")),
        ("SupervisorName", "Supervisor Name", "text"),
        ("VolunteerActivity.Type", "Type", "enum", (("Course Trainer","CT"),("Water Safety","WS"),("Sunday Program Help","Sun"),("Fundraiser","Fund"),("Club Chore","Club"))),
        ("VolunteerActivity.Date", "Date", "date"),
        ("VolunteerActivity.FundsRaised", "Funds Raised", "number", (0,10000,100)),
        ("VolunteerActivity.PercFundsReceived", "Percentage Funds Received", "number", (0,100,1)),
        ("AthleteGrantContribution", "Athlete Grant Contribution", "number", (0,10000,100)),
        ("FundsRaisedPerAthlete", "Funds Raised Per Athlete", "number", (0,1000,10)),
        ("Attendance", "Attendance", "number", (0,100,1)),
        ("AverageHoursEarned", "Average Hours Earned", "number", (0,10,1)),
        ("TotalHoursEarned", "Total Hours Earned", "number", (0,500,1))
    ],
    "qualifications": [
        ("QualificationAward.AwardID", "Award ID", "id"),
        ("QualificationAward.Name", "Name", "text"),
        ("Requals", "Requalifications", "number", (0,50,1)),
        ("Athletes", "Athletes", "number", (0,100,1))
    ],
    "competitions": [
        ("Competition.CompetitionID", "Competition ID", "id"),
        ("Competition.Name", "Name", "text"),
        ("Competition.Season", "Season", "number", (1900,2100,1)),
        ("Competition.Discipline", "Discipline", "enum", (("Surf","S"),("Beach","Be"),("Boats","Bo"),("Lifesaving","L"))),
        ("Competition.Location", "Location", "text"),
        ("Competition.StartDate", "Start Date", "date"),
        ("Competition.EndDate", "End Date", "date"),
        ("Competition.Importance", "Importance", "number", (1,5,1)),
        ("Races", "Races", "number", (0,50,1)),
        ("Competitors", "Competitors", "number", (0,100,1)),
        ("Results", "Results", "number", (0,100,1))
    ],
    "events": [
        ("Event.EventID", "Event ID", "id"),
        ("Event.Name", "Name", "text"),
        ("Event.Discipline", "Discipline", "enum", (("Surf","S"),("Beach","Be"),("Boats","Bo"),("Lifesaving","L"))),
        ("Event.TeamEvent", "Team Event", "enum", ((0,"Indiv."),(1,"Team"))),
        ("Event.Importance", "Importance", "number", (1,5,1))
    ],
    "races": [
        ("Race.RaceID", "Race ID", "id"),
        ("Race.CompetitionID", "Competition ID", "id", ("Competition","competitions")),
        ("CompetitionName", "Competition Name", "text"),
        ("Race.EventID", "Event ID", "id", ("Event","events")),
        ("EventName", "Event Name", "text"),
        ("Race.AgeGroup", "Age Group", "enum", (("Open","Open"),("U23","U23"),("U19","U19"),("U17","U17"),("U15","U15"),("U14","U14"),("U13","U13"))),
        ("Race.Gender", "Gender", "enum", (("Male","M"),("Female","F"),("Mixed","Mix")))
    ],
    "results": [
        ("Result.ResultID", "Result ID", "id"),
        ("Result.RaceID", "Race ID", "id", ("Race","races")),
        ("CompetitionName", "Competition Name", "text"),
        ("EventName", "Event Name", "text"),
        ("Result.Ranking", "Ranking", "number", (1,100,1))
    ]
}

names = {
    "athletes": lambda cols: f"Athlete #{cols[0]} - {cols[1]}",
    "supervisors": lambda cols: f"Supervisor #{cols[0]} - {cols[1]}",
    "competitions": lambda cols: f"Competition #{cols[0]} - {cols[2]} {cols[1]}",
    "events": lambda cols: f"Event #{cols[0]} - {cols[1]} ({cols[2]})",
    "patrolgroups": lambda cols: f"Patrol Group #{cols[0]} - {cols[1]}",
    "patrols": lambda cols: f"Patrol #{cols[0]} - {cols[2]} {cols[5]} {cols[4]}",
    "volunteering": lambda cols: f"Volunteer Activity #{cols[0]} - {cols[1]} {cols[5]}",
    "qualifications": lambda cols: f"Qualification #{cols[0]} - {cols[1]}",
    "races": lambda cols: f"Race #{cols[0]} - {cols[2]} {cols[4]} {cols[5]} {cols[6]}",
    "results": lambda cols: f"Result #{cols[0]} - {cols[2]} {cols[3]} - #{cols[4]}",
}

relations = {
    "athletes":{
        "patrols":[
            "Patrols",
            ("Athlete","Patrol","Athlete_Patrol","AthleteID","PatrolID"),
            True,
            [
                ("Hours","number",(0,8,1))
            ]
        ],
        "volunteering":[
            "Volunteering",
            ("Athlete","VolunteerActivity","Athlete_Volunteer","AthleteID","ActivityID"),
            True,
            [
                ("Hours","number",(0,8,1))
            ]
        ],
        "qualifications":[
            "Requalifications",
            ("Athlete","QualificationAward","Requalification","AthleteID","AwardID"),
            True,
            [
                ("SupervisorID","id",("Supervisor","supervisors")),
                ("Date","date")
            ]
        ],
        "results":[
            "Results",
            ("Athlete","Result","Athlete_Result","AthleteID","ResultID"),
            True,
            []
        ]
    },
    "supervisors":{
        "patrolgroups":[
            "Patrol Groups",
            ("Supervisor","PatrolGroup","PatrolGroup","PatrolGroupID","SupervisorID"),
            False,
            []
        ],
        "volunteering":[
            "Volunteer Activities",
            ("Supervisor","VolunteerActivity","VolunteerActivity","ActivityID","SupervisorID"),
            False,
            []
        ]
    },
    "competitions":{
        "races":[
            "Races",
            ("Competition","Race","Race","RaceID","CompetitionID"),
            False,
            []
        ]
    },
    "events":{
        "races":[
            "Races",
            ("Event","Race","Race","RaceID","EventID"),
            False,
            []
        ]
    },
    "patrolgroups":{
        "athletes":[
            "Athletes",
            ("PatrolGroup","Athlete","Athlete","AthleteID","PatrolGroupID"),
            False,
            []
        ],
        "patrols":[
            "Patrols",
            ("PatrolGroup","Patrol","Patrol","PatrolID","PatrolGroupID"),
            False,
            []
        ]
    },
    "patrols":{
        "athletes":[
            "Athletes",
            ("Patrol","Athlete","Athlete_Patrol","PatrolID","AthleteID"),
            True,
            [
                ("Hours","number",(0,8,1))
            ]
        ]
    },
    "volunteering":{
        "athletes":[
            "Athletes",
            ("VolunteerActivity","Athlete","Athlete_Volunteer","ActivityID","AthleteID"),
            True,
            [
                ("Hours","number",(0,8,1))
            ]
        ]
    },
    "races":{
        "results":[
            "Results",
            ("Race","Result","Result","ResultID","RaceID"),
            False,
            []
        ]
    },
    "results":{
        "athletes":[
            "Athletes",
            ("Result","Athlete","Athlete_Result","ResultID","AthleteID"),
            True,
            []
        ]
    },
    "qualifications":{}
}