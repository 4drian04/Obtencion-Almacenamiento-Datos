import sqlite3


def create_tables():
    conn = sqlite3.connect("soccer.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS league (id INTEGER PRIMARY KEY, name TEXT, year INTEGER)"
    )
    conn.commit()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS teams (id INTEGER PRIMARY KEY, name TEXT, league_id INTEGER, logo TEXT, FOREIGN KEY(league_id) REFERENCES league(id))"
    )
    conn.commit()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, team_id INTEGER, points INTEGER, played INTEGER, goals_against INTEGER, goals_for INTEGER, wins INTEGER, draws INTEGER, losses INTEGER, position TEXT, FOREIGN KEY(team_id) REFERENCES teams(id))"
    )
    conn.commit()
    conn.close()


def insert_leagues(leagues):
    conn = sqlite3.connect("soccer.db")
    cursor = conn.cursor()
    prev_leagues = [
        row[0] for row in cursor.execute("SELECT name FROM league").fetchall()
    ]
    for league in leagues:
        if (league["name"]) not in prev_leagues:
            cursor.execute(
                "INSERT INTO league (name, year) VALUES (?, ?)",
                (league["name"], league["year"]),
            )
        else:
            update_league = cursor.execute(
                "SELECT name, year FROM league WHERE name = ?", (league["name"],)
            ).fetchone()
            if update_league[1] != league["year"]:
                cursor.execute(
                    "UPDATE league SET year = ? WHERE name = ?",
                    (league["year"], league["name"]),
                )
                cursor.execute("DELETE FROM stats")
                cursor.execute("DELETE FROM teams")
    conn.commit()
    conn.close()


def insert_teams(teams):
    conn = sqlite3.connect("soccer.db")
    cursor = conn.cursor()
    prev_teams = cursor.execute("SELECT name FROM teams").fetchall()
    for team in teams:
        team["league"] = cursor.execute(
            "SELECT id FROM league WHERE name = ?", (team["league"],)
        ).fetchone()[0]
        if (team["name"],) not in prev_teams:
            cursor.execute(
                "INSERT INTO teams (name, league_id, logo) VALUES (?, ?, ?)",
                (team["name"], team["league"], team["logo"]),
            )
        else:
            cursor.execute(
                "UPDATE teams SET name = ?, league_id = ?, logo = ? WHERE name = ?",
                (team["name"], team["league"], team["logo"], team["name"]),
            )
    conn.commit()
    conn.close()


def insert_stats(stats):
    conn = sqlite3.connect("soccer.db")
    cursor = conn.cursor()
    prev_stats = cursor.execute("SELECT team_id FROM stats").fetchall()
    for stat in stats:
        if (stat["team_id"],) in prev_stats:
            cursor.execute(
                "UPDATE stats SET position = ?, points = ?, played = ?, goals_against = ?, goals_for = ?, wins = ?, draws = ?, losses = ? WHERE team_id = ?",
                (
                    stat["position"],
                    stat["points"],
                    stat["played"],
                    stat["goals_against"],
                    stat["goals_for"],
                    stat["wins"],
                    stat["draws"],
                    stat["losses"],
                    stat["team_id"],
                ),
            )
        else:
            cursor.execute(
                "INSERT INTO stats (position, team_id, points, played, goals_against, goals_for, wins, draws, losses) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    stat["position"],
                    stat["team_id"],
                    stat["points"],
                    stat["played"],
                    stat["goals_against"],
                    stat["goals_for"],
                    stat["wins"],
                    stat["draws"],
                    stat["losses"],
                ),
            )
    conn.commit()
    conn.close()


create_tables()
insert_leagues(
    [{"name": "Premier League", "year": 2024}, {"name": "La Liga", "year": 2024}]
)
insert_teams(
    [
        {
            "name": "Manchester United",
            "league": "Premier League",
            "logo": "manu_logo.png",
        },
        {"name": "Real Madrid", "league": "La Liga", "logo": "realmadrid_logo.png"},
    ]
)
insert_stats(
    [
        {
            "position": "1",
            "team_id": 1,
            "points": 85,
            "played": 38,
            "goals_against": 30,
            "goals_for": 70,
            "wins": 27,
            "draws": 4,
            "losses": 7,
        },
        {
            "position": "2",
            "team_id": 2,
            "points": 83,
            "played": 38,
            "goals_against": 25,
            "goals_for": 65,
            "wins": 25,
            "draws": 5,
            "losses": 8,
        },
    ]
)
