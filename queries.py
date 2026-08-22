import sqlite3
import enums

def create_tables(conn:sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE Athlete (
        AthleteID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL
            CHECK (
                length(FirstName) > 0
                AND FirstName NOT GLOB '*[^A-Za-z]*'
            ),
        LastName TEXT NOT NULL
            CHECK (
                length(LastName) > 0
                AND LastName NOT GLOB '*[^A-Za-z]*'
            ),
        Gender TEXT NOT NULL
            CHECK (
                Gender IN (
                    'Male',
                    'Female',
                    'Not Specified'
                )
            ),
        DOB TEXT NOT NULL
            CHECK (
                DOB GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
                AND date(DOB) IS NOT NULL
            ),
        MainDiscipline TEXT NOT NULL
            CHECK (
                MainDiscipline IN (
                    'Surf',
                    'Beach',
                    'Boats',
                    'Lifesaving'
                )
            ),
        PatrolGroupID INTEGER,
        Phone TEXT NOT NULL
            CHECK (
                length(Phone) = 10
                AND Phone NOT GLOB '*[^0-9]*'
            ),
        Email TEXT NOT NULL
            CHECK (
                Email LIKE '%@%.%'
            ),
        Active BOOLEAN,
        FOREIGN KEY (PatrolGroupID) REFERENCES PatrolGroup(PatrolGroupID)
    );
    """)
    cursor.execute("""
    CREATE TABLE Supervisor (
        SupervisorID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL
            CHECK (
                length(FirstName) > 0
                AND FirstName NOT GLOB '*[^A-Za-z]*'
            ),
        LastName TEXT NOT NULL
            CHECK (
                length(LastName) > 0
                AND LastName NOT GLOB '*[^A-Za-z]*'
            ),
        Phone TEXT NOT NULL
            CHECK (
                length(Phone) = 10
                AND Phone NOT GLOB '*[^0-9]*'
            ),
        Email TEXT NOT NULL
            CHECK (
                Email LIKE '%@%.%'
            )
    );
    """)
    cursor.execute("""
    CREATE TABLE PatrolGroup (
        PatrolGroupID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL CHECK (length(Name) > 0),
        SupervisorID INTEGER NOT NULL,
        FOREIGN KEY (SupervisorID) REFERENCES Supervisor(SupervisorID)
    );
    """)
    cursor.execute("""
    CREATE TABLE Patrol (
        PatrolID INTEGER PRIMARY KEY AUTOINCREMENT,
        PatrolGroupID INTEGER NOT NULL,
        Date TEXT NOT NULL
            CHECK (
                Date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
                AND date(Date) IS NOT NULL
            ),
        Session TEXT NOT NULL
            CHECK (
                Session IN (
                    'Morning',
                    'Afternoon',
                    'All Day'
                )
            ),
        Holiday BOOLEAN,
        FOREIGN KEY (PatrolGroupID) REFERENCES PatrolGroup(PatrolGroupID)
    );
    """)
    cursor.execute("""
    CREATE TABLE Athlete_Patrol (
        AthleteID INTEGER NOT NULL,
        PatrolID INTEGER NOT NULL,
        Hours NUMERIC NOT NULL
            CHECK (
                Hours >= 0
                AND Hours <= 8
            ),
        PRIMARY KEY (AthleteID, PatrolID),
        FOREIGN KEY (AthleteID) REFERENCES Athlete(AthleteID),
        FOREIGN KEY (PatrolID) REFERENCES Patrol(PatrolID)
    );
    """)
    cursor.execute("""
    CREATE TABLE VolunteerActivity (
        ActivityID INTEGER PRIMARY KEY AUTOINCREMENT,
        SupervisorID INTEGER NOT NULL,
        Name TEXT NOT NULL CHECK (length(Name) > 0),
        Type TEXT NOT NULL
            CHECK (
                Type IN (
                    'Water Safety',
                    'Course Trainer',
                    'Fundraiser',
                    'Sunday Program Help',
                    'Club Chore'
                )
            ),
        Date TEXT NOT NULL
            CHECK (
                Date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
                AND date(Date) IS NOT NULL
            ),
        FundsRaised NUMERIC NOT NULL
            CHECK (
                FundsRaised >= 0
                AND FundsRaised < 10000
            ),
        PercFundsReceived NUMERIC NOT NULL
            CHECK (
                PercFundsReceived >= 0
                AND PercFundsReceived <= 100
            ),
        FOREIGN KEY (SupervisorID) REFERENCES Supervisor(SupervisorID)
    );
    """)
    cursor.execute("""
    CREATE TABLE Athlete_Volunteer (
        AthleteID INTEGER NOT NULL,
        ActivityID INTEGER NOT NULL,
        Hours NUMERIC NOT NULL
            CHECK (
                Hours >= 0
                AND Hours <= 8
            ),
        PRIMARY KEY (AthleteID, ActivityID),
        FOREIGN KEY (AthleteID) REFERENCES Athlete(AthleteID),
        FOREIGN KEY (ActivityID) REFERENCES VolunteerActivity(ActivityID)
    );
    """)
    cursor.execute("""
    CREATE TABLE QualificationAward (
        AwardID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL CHECK (length(Name) > 0)
    );
    """)
    cursor.execute("""
    CREATE TABLE Requalification (
        AthleteID INTEGER NOT NULL,
        AwardID INTEGER NOT NULL,
        SupervisorID INTEGER NOT NULL,
        Date TEXT NOT NULL
            CHECK (
                Date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
                AND date(Date) IS NOT NULL
            ),
        PRIMARY KEY (AthleteID, AwardID),
        FOREIGN KEY (AthleteID) REFERENCES Athlete(AthleteID),
        FOREIGN KEY (AwardID) REFERENCES QualificationAward(AwardID),
        FOREIGN KEY (SupervisorID) REFERENCES Supervisor(SupervisorID)
    );
    """)
    cursor.execute("""
    CREATE TABLE Competition (
        CompetitionID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL CHECK (length(Name) > 0),
        Season INTEGER NOT NULL
            CHECK (
                Season >= 1900
                AND Season <= 2100
            ),
        Discipline TEXT NOT NULL
            CHECK (
                Discipline IN (
                    'Surf',
                    'Beach',
                    'Boats',
                    'Lifesaving'
                )
            ),
        Location TEXT,
        StartDate TEXT NOT NULL
            CHECK (
                StartDate GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
                AND date(StartDate) IS NOT NULL
            ),
        EndDate TEXT
            CHECK (
                EndDate IS NULL
                OR (
                    EndDate GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
                    AND date(EndDate) IS NOT NULL
                )
            ),
        Importance INTEGER NOT NULL CHECK (Importance > 0)
    );
    """)
    cursor.execute("""
    CREATE TABLE Event (
        EventID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL CHECK (length(Name) > 0),
        Discipline TEXT NOT NULL
            CHECK (
                Discipline IN (
                    'Surf',
                    'Beach',
                    'Boats',
                    'Lifesaving'
                )
            ),
        TeamEvent INTEGER NOT NULL CHECK (TeamEvent IN (0, 1)),
        Importance INTEGER NOT NULL CHECK (Importance > 0)
    );
    """)
    cursor.execute("""
    CREATE TABLE Race (
        RaceID INTEGER PRIMARY KEY AUTOINCREMENT,
        CompetitionID INTEGER NOT NULL,
        EventID INTEGER NOT NULL,
        AgeGroup TEXT NOT NULL
            CHECK (
                AgeGroup IN (
                    'Open',
                    'U23',
                    'U19',
                    'U17',
                    'U15',
                    'U14',
                    'U13'
                )
            ),
        Gender TEXT NOT NULL
            CHECK (
                Gender IN (
                    'Male',
                    'Female',
                    'Mixed'
                )
            ),
        FOREIGN KEY (CompetitionID) REFERENCES Competition(CompetitionID),
        FOREIGN KEY (EventID) REFERENCES Event(EventID)
    );
    """)
    cursor.execute("""
    CREATE TABLE Result (
        ResultID INTEGER PRIMARY KEY AUTOINCREMENT,
        RaceID INTEGER NOT NULL,
        Ranking INTEGER NOT NULL CHECK (Ranking >= 1),
        FOREIGN KEY (RaceID) REFERENCES Race(RaceID)
    );
    """)
    cursor.execute("""
    CREATE TABLE Athlete_Result (
        AthleteID INTEGER NOT NULL,
        ResultID INTEGER NOT NULL,
        PRIMARY KEY (AthleteID, ResultID),
        FOREIGN KEY (AthleteID) REFERENCES Athlete(AthleteID),
        FOREIGN KEY (ResultID) REFERENCES Result(ResultID)
    );
    """)
    cursor.execute("PRAGMA foreign_keys = ON")
    conn.commit()



def add_athlete(conn:sqlite3.Connection,
                firstname:str,
                lastname:str,
                gender:int|str,
                dob:str,
                maindiscipline:int|str,
                patrolgroupid:int|None,
                phone:str,
                email:str,
                active:bool):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Athlete (
        FirstName,
        LastName,
        Gender,
        DOB,
        MainDiscipline,
        PatrolGroupID,
        Phone,
        Email,
        Active
    )
    VALUES (
        ?,?,?,?,?,?,?,?,?
    )
    """,
    (
        firstname,
        lastname,
        enums.GENDERS[gender] if isinstance(gender,int) else gender,
        dob,
        enums.DISCIPLINES[maindiscipline] if isinstance(maindiscipline,int) else maindiscipline,
        patrolgroupid,
        phone,
        email,
        active
    ))
    conn.commit()

def add_supervisor(conn:sqlite3.Connection,
                   firstname:str,
                   lastname:str,
                   phone:str,
                   email:str):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Supervisor (
        FirstName,
        LastName,
        Phone,
        Email
    )
    VALUES (
        ?,?,?,?
    )
    """,
    (
        firstname,
        lastname,
        phone,
        email,
    ))
    conn.commit()

def add_patrolgroup(conn:sqlite3.Connection,
                   name:str,
                   supervisorid:int):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO PatrolGroup (
        Name,
        SupervisorID
    )
    VALUES (
        ?,?
    )
    """,
    (
        name,
        supervisorid,
    ))
    conn.commit()

def add_patrol(conn:sqlite3.Connection,
               patrolgroupid:int,
               date:str,
               session:int|str,
               holiday:bool):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Patrol (
        PatrolGroupID,
        Date,
        Session,
        Holiday
    )
    VALUES (
        ?,?,?,?
    )
    """,
    (
        patrolgroupid,
        date,
        enums.SESSIONS[session] if isinstance(session,int) else session,
        holiday
    ))
    conn.commit()

def add_athlete_patrol(conn:sqlite3.Connection,
                       athleteid:int,
                       patrolid:int,
                       hours:float):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Athlete_Patrol (
        AthleteID,
        PatrolID,
        Hours
    )
    VALUES (
        ?,?,?
    )
    """,
    (
        athleteid,
        patrolid,
        hours
    ))
    conn.commit()

def add_volunteeractivity(conn:sqlite3.Connection,
                          supervisorid:int,
                          name:str,
                          type:int|str,
                          date:str,
                          fundsraised:float,
                          percfundsreceived:float):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO VolunteerActivity (
        SupervisorID,
        Name,
        Type,
        Date,
        FundsRaised,
        PercFundsReceived
    )
    VALUES (
        ?,?,?,?,?,?
    )
    """,
    (
        supervisorid,
        name,
        enums.VOLUNTEER_TYPES[type] if isinstance(type,int) else type,
        date,
        fundsraised,
        percfundsreceived
    ))
    conn.commit()

def add_athlete_volunteer(conn:sqlite3.Connection,
                          athleteid:int,
                          activityid:int,
                          hours:float):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Athlete_Volunteer (
        AthleteID,
        ActivityID,
        Hours
    )
    VALUES (
        ?,?,?
    )
    """,
    (
        athleteid,
        activityid,
        hours
    ))
    conn.commit()

def add_qualificationaward(conn:sqlite3.Connection,
                           name:str):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO QualificationAward (
        Name
    )
    VALUES (
        ?
    )
    """,
    (
        name
    ))
    conn.commit()

def add_requalification(conn:sqlite3.Connection,
                        athleteid:int,
                        awardid:int,
                        supervisorid:int,
                        date:str):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Requalification (
        AthleteID,
        AwardID,
        SupervisorID,
        Date
    )
    VALUES (
        ?,?,?,?
    )
    """,
    (
        athleteid,
        awardid,
        supervisorid,
        date
    ))
    conn.commit()

def add_competition(conn:sqlite3.Connection,
                    name:str,
                    season:int,
                    discipline:int|str,
                    location:str|None,
                    startdate:str,
                    enddate:str|None,
                    importance:int):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Competition (
        Name,
        Season,
        Discipline,
        Location,
        StartDate,
        EndDate,
        Importance
    )
    VALUES (
        ?,?,?,?,?,?,?
    )
    """,
    (
        name,
        season,
        enums.DISCIPLINES[discipline] if isinstance(discipline,int) else discipline,
        location,
        startdate,
        enddate,
        importance
    ))
    conn.commit()

def add_event(conn:sqlite3.Connection,
              name:str,
              discipline:int|str,
              teamevent:bool,
              importance:int):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Event (
        Name,
        Discipline,
        TeamEvent,
        Importance
    )
    VALUES (
        ?,?,?,?
    )
    """,
    (
        name,
        enums.DISCIPLINES[discipline] if isinstance(discipline,int) else discipline,
        teamevent,
        importance
    ))
    conn.commit()

def add_race(conn:sqlite3.Connection,
             competitionid:int,
             eventid:int,
             agegroup:int|str,
             gender:int|str):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Race (
        CompetitionID,
        EventID,
        AgeGroup,
        Gender
    )
    VALUES (
        ?,?,?,?
    )
    """,
    (
        competitionid,
        eventid,
        enums.AGE_GROUPS[agegroup] if isinstance(agegroup,int) else agegroup,
        enums.GENDERS[gender] if isinstance(gender,int) else gender
    ))
    conn.commit()

def add_result(conn:sqlite3.Connection,
               raceid:int,
               ranking:int):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Result (
        RaceID,
        Ranking
    )
    VALUES (
        ?,?
    )
    """,
    (
        raceid,
        ranking
    ))
    conn.commit()

def add_athlete_result(conn:sqlite3.Connection,
                       athleteid:int,
                       resultid:int):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Athlete_Result (
        AthleteID,
        ResultID
    )
    VALUES (
        ?,?
    )
    """,
    (
        athleteid,
        resultid
    ))
    conn.commit()



def view_athletes(conn:sqlite3.Connection,
                  sort_attr:str,
                  sort_dir:bool,
                  filters:dict,
                  columns:list[int],
                  limit:int|None=None):
    cursor = conn.cursor()
    values = []
    sort_query = f"ORDER BY {sort_attr} {'ASC' if sort_dir else 'DESC'}"
    filter_queries = []
    for attribute,restriction in filters.items():
        query = None
        if isinstance(restriction,str):
            query = f"{attribute} LIKE ?"
            values.append(f"%{restriction}%")
        if isinstance(restriction,tuple) and len(restriction)==2:
            query = f"{attribute} BETWEEN ? AND ?"
            values.extend(restriction)
        if isinstance(restriction,list):
            query = f"{attribute} IN ({",".join("?" for _ in restriction)})"
            values.extend(restriction)
        if query:
            filter_queries.append(query)
    if len(filter_queries)>0:
        filter_query = "WHERE " + " AND ".join(filter_queries)
    else:
        filter_query = ""
    if limit:
        limit_query = f"LIMIT ?"
        values.append(limit)
    else:
        limit_query = ""
    cursor.execute(f"""
    SELECT
        AthleteID,
        FirstName||" "||LastName AS Name,
        FirstName,
        LastName,
        Gender,
        DOB,
        MainDiscipline,
        PatrolGroupID,
        Phone,
        Email,
        Active,
        COALESCE(p.Number,0) AS Patrols,
        COALESCE(p.Total,0) AS PatrolHours,
        COALESCE(v.Number,0) AS VolunteerSessions,
        COALESCE(v.Total,0) AS VolunteerHours,
        COALESCE(p.Total,0) + COALESCE(v.Total,0) AS TotalHours,
        COALESCE(c.NumCompetitions,0) AS Competitions,
        COALESCE(c.NumRaces,0) AS Races,
        COALESCE(q.Number,0) AS Qualifications,
        0 AS PatrolPoints,
        0 AS VolunteerPoints,
        0 AS CompetitionPoints,
        0 AS TotalPoints
    FROM Athlete
    LEFT JOIN (
        SELECT
            AthleteID,
            COUNT(PatrolID) AS Number,
            SUM(Hours) AS Total
        FROM Athlete_Patrol
        GROUP BY AthleteID
    ) AS p ON Athlete.AthleteID = p.AthleteID
    LEFT JOIN (
        SELECT
            AthleteID,
            COUNT(ActivityID) AS Number,
            SUM(Hours) AS Total
        FROM Athlete_Volunteer
        GROUP BY AthleteID
    ) AS v ON Athlete.AthleteID = v.AthleteID
    LEFT JOIN (
        SELECT
            AthleteID,
            COUNT(DISTINCT Race.CompetitionID) AS NumCompetitions,
            COUNT(DISTINCT Race.RaceID) AS NumRaces
        FROM Athlete_Result
        LEFT JOIN Result ON Athlete_Result.ResultID = Result.ResultID
        LEFT JOIN Race ON Result.RaceID = Race.RaceID
        GROUP BY AthleteID
    ) AS c ON Athlete.AthleteID = c.AthleteID
    LEFT JOIN (
        SELECT
            AthleteID,
            COUNT(DISTINCT AwardID) AS Number
        FROM Requalification
        GROUP BY AthleteID
    ) AS q ON Athlete.AthleteID = q.AthleteID
    {filter_query}
    {sort_query}
    {limit_query}
    """, values)
    records = [[attr for i,attr in enumerate(row) if i in columns] for row in cursor.fetchall()]
    return records

def view_supervisors(conn:sqlite3.Connection,
                     sort_attr:str,
                     sort_dir:bool,
                     filters:dict,
                     columns:list[int],
                     limit:int|None=None):
    cursor = conn.cursor()
    values = []
    sort_query = f"ORDER BY {sort_attr} {'ASC' if sort_dir else 'DESC'}"
    filter_queries = []
    for attribute,restriction in filters.items():
        query = None
        if isinstance(restriction,str):
            query = f"{attribute} LIKE ?"
            values.append(f"%{restriction}%")
        if isinstance(restriction,tuple) and len(restriction)==2:
            query = f"{attribute} BETWEEN ? AND ?"
            values.extend(restriction)
        if isinstance(restriction,list):
            query = f"{attribute} IN ({",".join("?" for _ in restriction)})"
            values.extend(restriction)
        if query:
            filter_queries.append(query)
    if len(filter_queries)>0:
        filter_query = "WHERE " + " AND ".join(filter_queries)
    else:
        filter_query = ""
    if limit:
        limit_query = f"LIMIT ?"
        values.append(limit)
    else:
        limit_query = ""
    cursor.execute(f"""
    SELECT
        SupervisorID,
        FirstName||" "||LastName AS Name,
        FirstName,
        LastName,
        Phone,
        Email,
        COALESCE(p.NumGroups,0) AS PatrolGroups,
        COALESCE(p.NumPatrols,0) AS PatrolsSupervised,
        COALESCE(v.Number,0) AS VolunteersSupervised,
        COALESCE(q.Number,0) AS Requalifications
    FROM Supervisor
    LEFT JOIN (
        SELECT
            SupervisorID,
            COUNT(PatrolGroupID) AS NumGroups,
            COUNT(Patrol.PatrolID) AS NumPatrols
        FROM PatrolGroup
        LEFT JOIN Patrol ON PatrolGroup.PatrolGroupID = Patrol.PatrolGroupID
        GROUP BY SupervisorID
    ) AS p ON Supervisor.SupervisorID = p.SupervisorID
    LEFT JOIN (
        SELECT
            SupervisorID,
            COUNT(ActivityID) AS Number
        FROM VolunteerActivity
        GROUP BY SupervisorID
    ) AS v ON Supervisor.SupervisorID = v.SupervisorID
    LEFT JOIN (
        SELECT
            SupervisorID,
            COUNT(AthleteID) AS Number
        FROM Requalification
        GROUP BY SupervisorID
    ) AS q ON Supervisor.SupervisorID = q.SupervisorID
    {filter_query}
    {sort_query}
    {limit_query}
    """, values)
    records = [[attr for i,attr in enumerate(row) if i in columns] for row in cursor.fetchall()]
    return records

def view_patrolgroups(conn:sqlite3.Connection,
                      sort_attr:str,
                      sort_dir:bool,
                      filters:dict,
                      columns:list[int],
                      limit:int|None=None):
    cursor = conn.cursor()
    values = []
    sort_query = f"ORDER BY {sort_attr} {'ASC' if sort_dir else 'DESC'}"
    filter_queries = []
    for attribute,restriction in filters.items():
        query = None
        if isinstance(restriction,str):
            query = f"{attribute} LIKE ?"
            values.append(f"%{restriction}%")
        if isinstance(restriction,tuple) and len(restriction)==2:
            query = f"{attribute} BETWEEN ? AND ?"
            values.extend(restriction)
        if isinstance(restriction,list):
            query = f"{attribute} IN ({",".join("?" for _ in restriction)})"
            values.extend(restriction)
        if query:
            filter_queries.append(query)
    if len(filter_queries)>0:
        filter_query = "WHERE " + " AND ".join(filter_queries)
    else:
        filter_query = ""
    if limit:
        limit_query = f"LIMIT ?"
        values.append(limit)
    else:
        limit_query = ""
    cursor.execute(f"""
    SELECT
        PatrolGroupID,
        Name,
        SupervisorID,
        s.FirstName||" "||s.LastName AS SupervisorName,
        COALESCE(p.NumPatrols,0) AS Patrols,
        COALESCE(p.AvgAthletes,0) AS AverageAttendance,
        COALESCE(p.NumAthletes,0) AS UniqueAttendees
    FROM PatrolGroup
    LEFT JOIN Supervisor AS s ON PatrolGroup.SupervisorID = s.SupervisorID
    LEFT JOIN (
        SELECT
            PatrolGroupID,
            COUNT(PatrolID) AS NumPatrols,
            AVG(a.Attendance) AS AvgAthletes,
            COUNT(DISTINCT Athlete_Patrol.AthleteID) AS NumAthletes
        FROM Patrol
        LEFT JOIN (
            SELECT COUNT(AthleteID) AS Attendance FROM Athlete_Patrol GROUP BY PatrolID
        ) AS a ON Patrol.PatrolID = a.PatrolID
        LEFT JOIN Athlete_Patrol ON Patrol.PatrolID = Athlete_Patrol.PatrolID
        GROUP BY PatrolGroupID
    ) AS p ON PatrolGroup.PatrolGroupID = p.PatrolGroupID
    {filter_query}
    {sort_query}
    {limit_query}
    """, values)
    records = [[attr for i,attr in enumerate(row) if i in columns] for row in cursor.fetchall()]
    return records

def view_patrols(conn:sqlite3.Connection,
                 sort_attr:str,
                 sort_dir:bool,
                 filters:dict,
                 columns:list[int],
                 limit:int|None=None):
    cursor = conn.cursor()
    values = []
    sort_query = f"ORDER BY {sort_attr} {'ASC' if sort_dir else 'DESC'}"
    filter_queries = []
    for attribute,restriction in filters.items():
        query = None
        if isinstance(restriction,str):
            query = f"{attribute} LIKE ?"
            values.append(f"%{restriction}%")
        if isinstance(restriction,tuple) and len(restriction)==2:
            query = f"{attribute} BETWEEN ? AND ?"
            values.extend(restriction)
        if isinstance(restriction,list):
            query = f"{attribute} IN ({",".join("?" for _ in restriction)})"
            values.extend(restriction)
        if query:
            filter_queries.append(query)
    if len(filter_queries)>0:
        filter_query = "WHERE " + " AND ".join(filter_queries)
    else:
        filter_query = ""
    if limit:
        limit_query = f"LIMIT ?"
        values.append(limit)
    else:
        limit_query = ""
    cursor.execute(f"""
    SELECT
        PatrolID,
        PatrolGroupID,
        g.Name AS PatrolGroupName,
        s.FirstName||" "||s.LastName AS SupervisorName,
        Date,
        Session,
        Holiday,
        COALESCE(p.Attendace,0) AS Attendance,
        COALESCE(p.AvgHours,0) AS AverageHoursEarned,
        COALESCE(p.TotalHours,0) AS TotalHoursEarned
    FROM Patrol
    LEFT JOIN PatrolGroup AS g ON Patrol.PatrolGroupID = g.PatrolGroupID
    LEFT JOIN Supervisor AS s ON g.SupervisorID = s.SupervisorID
    LEFT JOIN (
        SELECT
            PatrolID,
            COUNT(AthleteID) AS Attendance,
            AVG(Hours) AS AvgHours,
            SUM(Hours) AS TotalHours
        FROM Athlete_Patrol
        GROUP BY PatrolID
    ) AS p ON Patrol.PatrolID = p.PatrolID
    {filter_query}
    {sort_query}
    {limit_query}
    """, values)
    records = [[attr for i,attr in enumerate(row) if i in columns] for row in cursor.fetchall()]
    return records

def view_volunteeractivities(conn:sqlite3.Connection,
                             sort_attr:str,
                             sort_dir:bool,
                             filters:dict,
                             columns:list[int],
                             limit:int|None=None):
    cursor = conn.cursor()
    values = []
    sort_query = f"ORDER BY {sort_attr} {'ASC' if sort_dir else 'DESC'}"
    filter_queries = []
    for attribute,restriction in filters.items():
        query = None
        if isinstance(restriction,str):
            query = f"{attribute} LIKE ?"
            values.append(f"%{restriction}%")
        if isinstance(restriction,tuple) and len(restriction)==2:
            query = f"{attribute} BETWEEN ? AND ?"
            values.extend(restriction)
        if isinstance(restriction,list):
            query = f"{attribute} IN ({",".join("?" for _ in restriction)})"
            values.extend(restriction)
        if query:
            filter_queries.append(query)
    if len(filter_queries)>0:
        filter_query = "WHERE " + " AND ".join(filter_queries)
    else:
        filter_query = ""
    if limit:
        limit_query = f"LIMIT ?"
        values.append(limit)
    else:
        limit_query = ""
    cursor.execute(f"""
    SELECT
        ActivityID,
        Name,
        SupervisorID,
        s.FirstName||" "||s.LastName AS SupervisorName,
        Type,
        Date,
        FundsRaised,
        PercFundsRaised,
        FundsRaised*PercFundsRaised/100 AS AthleteGrantContribution,
        FundsRaised/COALESCE(v.Attendance,1) AS FundsRaisedPerAthlete,
        COALESCE(v.Attendace,0) AS Attendance,
        COALESCE(v.AvgHours,0) AS AverageHoursEarned,
        COALESCE(v.TotalHours,0) AS TotalHoursEarned
    FROM VolunteerActivity
    LEFT JOIN Supervisor AS s ON VolunteerActivity.SupervisorID = s.SupervisorID
    LEFT JOIN (
        SELECT
            ActivityID,
            COUNT(AthleteID) AS Attendance,
            AVG(Hours) AS AvgHours,
            SUM(Hours) AS TotalHours
        FROM Athlete_Volunteer
        GROUP BY ActivityID
    ) AS v ON VolunteerActivity.ActivityID = v.ActivityID
    {filter_query}
    {sort_query}
    {limit_query}
    """, values)
    records = [[attr for i,attr in enumerate(row) if i in columns] for row in cursor.fetchall()]
    return records

def view_competitions(conn:sqlite3.Connection,
                      sort_attr:str,
                      sort_dir:bool,
                      filters:dict,
                      columns:list[int],
                      limit:int|None=None):
    cursor = conn.cursor()
    values = []
    sort_query = f"ORDER BY {sort_attr} {'ASC' if sort_dir else 'DESC'}"
    filter_queries = []
    for attribute,restriction in filters.items():
        query = None
        if isinstance(restriction,str):
            query = f"{attribute} LIKE ?"
            values.append(f"%{restriction}%")
        if isinstance(restriction,tuple) and len(restriction)==2:
            query = f"{attribute} BETWEEN ? AND ?"
            values.extend(restriction)
        if isinstance(restriction,list):
            query = f"{attribute} IN ({",".join("?" for _ in restriction)})"
            values.extend(restriction)
        if query:
            filter_queries.append(query)
    if len(filter_queries)>0:
        filter_query = "WHERE " + " AND ".join(filter_queries)
    else:
        filter_query = ""
    if limit:
        limit_query = f"LIMIT ?"
        values.append(limit)
    else:
        limit_query = ""
    cursor.execute(f"""
    SELECT
        CompetitionID,
        Name,
        Season,
        Discipline,
        Location,
        StartDate,
        EndDate,
        Importance,
        COALESCE(c.Races,0) AS Races,
        COALESCE(c.Competitors,0) AS Competitors,
        COALESCE(c.Results,0) AS Results
    FROM Competition
    LEFT JOIN (
        SELECT
            CompetitionID,
            COUNT(DISTINCT RaceID) AS Races,
            COUNT(DISTINCT Athlete_Result.AthleteID) AS Competitors,
            COUNT(DISTINCT ResultID) AS Results
        FROM Race
        LEFT JOIN Result ON Race.RaceID = Result.RaceID
        LEFT JOIN Athlete_Result ON Result.ResultID = Athlete_Result.ResultID
        GROUP BY CompetitionID
    ) as c ON Competition.CompetitionID = c.CompetitionID
    {filter_query}
    {sort_query}
    {limit_query}
    """, values)
    records = [[attr for i,attr in enumerate(row) if i in columns] for row in cursor.fetchall()]
    return records

def view_events(conn:sqlite3.Connection,
                             sort_attr:str,
                             sort_dir:bool,
                             filters:dict,
                             columns:list[int],
                             limit:int|None=None):
    cursor = conn.cursor()
    values = []
    sort_query = f"ORDER BY {sort_attr} {'ASC' if sort_dir else 'DESC'}"
    filter_queries = []
    for attribute,restriction in filters.items():
        query = None
        if isinstance(restriction,str):
            query = f"{attribute} LIKE ?"
            values.append(f"%{restriction}%")
        if isinstance(restriction,tuple) and len(restriction)==2:
            query = f"{attribute} BETWEEN ? AND ?"
            values.extend(restriction)
        if isinstance(restriction,list):
            query = f"{attribute} IN ({",".join("?" for _ in restriction)})"
            values.extend(restriction)
        if query:
            filter_queries.append(query)
    if len(filter_queries)>0:
        filter_query = "WHERE " + " AND ".join(filter_queries)
    else:
        filter_query = ""
    if limit:
        limit_query = f"LIMIT ?"
        values.append(limit)
    else:
        limit_query = ""
    cursor.execute(f"""
    SELECT
        EventID,
        Name,
        Discipline,
        TeamEvent,
        Importance
    FROM Event
    {filter_query}
    {sort_query}
    {limit_query}
    """, values)
    records = [[attr for i,attr in enumerate(row) if i in columns] for row in cursor.fetchall()]
    return records

if __name__=="__main__":
    conn = sqlite3.connect("database.db")
    conn.commit()
    conn.close()