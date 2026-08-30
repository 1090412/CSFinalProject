columns = {
    "athletes": [
        ("Athlete.AthleteID", "Athlete ID", "id"),
        ("Name", "Name", "text"),
        ("Athlete.FirstName", "First Name", "text"),
        ("Athlete.LastName", "Last Name", "text"),
        ("Athlete.Gender", "Gender", "enum", (("Male","M"),("Female","F"),("Not Specified","-"))),
        ("Athlete.DOB", "Date of Birth", "date"),
        ("Athlete.MainDiscipline", "Main Discipline", "enum", (("Surf","S"),("Beach","Be"),("Boats","Bo"),("Lifesaving","L"),)),
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
    "competitions": [
        ("Competition.CompetitionID", "Competition ID", "id"),
        ("Competition.Name", "Name", "text"),
        ("Competition.Season", "Season", "text"),
        ("Competition.Discipline", "Discipline", "enum", (("Surf","S"),("Beach","Be"),("Boats","Bo"),("Lifesaving","L"),)),
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
        ("Event.Discipline", "Discipline", "enum", (("Surf","S"),("Beach","Be"),("Boats","Bo"),("Lifesaving","L"),)),
        ("Event.TeamEvent", "Team Event", "enum", (("Indiv.",0),("Team",1))),
        ("Event.Importance", "Importance", "number", (1,5,1))
    ],
    "patrolgroups": [
        ("PatrolGroup.PatrolGroupID", "Patrol Group ID", "id"),
        ("PatrolGroup.Name", "Name", "text"),
        ("PatrolGroup.SupervisorID", "Supervisor ID", "id"),
        ("SupervisorName", "Supervisor Name", "text"),
        ("Patrols", "Patrols", "number", (0,50,1)),
        ("AverageAttendance", "Average Attendance", "number", (0,30,1)),
        ("UniqueAttendees", "Unique Attendees", "number", (0,50,1))
    ],
    "patrols": [
        ("Patrol.PatrolID", "Patrol ID", "id"),
        ("Patrol.PatrolGroupID", "Patrol Group ID", "id"),
        ("PatrolGroupName", "Patrol Group Name", "text"),
        ("SupervisorName", "Supervisor Name", "text"),
        ("Patrol.Date", "Date", "date"),
        ("Patrol.Session", "Session", "enum", (("Morning","AM"),("Afternoon","PM"),("All Day","All"),)),
        ("Patrol.Holiday", "Holiday", "enum", (("Normal",0),("Holiday",1))),
        ("Attendance", "Attendance", "number", (0,50,1)),
        ("AverageHoursEarned", "Average Hours Earned", "number", (0,10,1)),
        ("TotalHoursEarned", "Total Hours Earned", "number", (0,500,1))
    ],
    "volunteering": [
        ("VolunteerActivity.ActivityID", "Activity ID", "id"),
        ("VolunteerActivity.Name", "Name", "text"),
        ("VolunteerActivity.SupervisorID", "Supervisor ID", "id"),
        ("SupervisorName", "Supervisor Name", "text"),
        ("VolunteerActivity.Type", "Type", "enum", (("Course Trainer","CT"),("Water Safety","WS"),("Sunday Program Help","Sun"),("Fundraiser","Fund"),("Club Chore","Club"),)),
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
        ("Qualification.QualificationID", "Qualification ID", "id"),
        ("Qualification.Name", "Name", "text"),
        ("Requals", "Requalifications", "number", (0,50,1)),
        ("Athletes", "Athletes", "number", (0,100,1))
    ]
}

names = {
    "athletes": lambda cols: f"Athlete #{cols[0]} - {cols[1]}",
    "competitions": lambda cols: f"Competition #{cols[0]} - {cols[2]} {cols[1]}",
    "events": lambda cols: f"Event #{cols[0]} - {cols[1]} ({cols[2]})",
    "patrolgroups": lambda cols: f"Patrol Group #{cols[0]} - {cols[1]}",
    "patrols": lambda cols: f"Patrol #{cols[0]} - {cols[2]} {cols[5]} {cols[6]}",
    "volunteering": lambda cols: f"Volunteer Activity #{cols[0]} - {cols[1]} {cols[5]}",
    "qualifications": lambda cols: f"Qualification #{cols[0]} - {cols[1]}",
}