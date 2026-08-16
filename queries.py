import sqlite3

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



if __name__=="__main__":
    conn = sqlite3.connect("database.db")
    create_tables(conn)