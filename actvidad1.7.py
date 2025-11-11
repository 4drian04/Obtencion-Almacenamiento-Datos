import requests
import db

r = requests.get("https://site.web.api.espn.com/apis/v2/sports/soccer/esp.1/standings").json()

estadisticas = ["gamesPlayed", "losses", "pointDifferential", "points", "pointsAgainst", "pointsFor", "ties", "rank", "wins"]
liga = []
equipos = {"equipos": {}}
liga.append(r["abbreviation"])
liga.append(r["children"][0]["abbreviation"])
for equipo in r["children"][0]["standings"]["entries"]:
    nombreEquipo = equipo["team"]["name"]
    equipos["equipos"][nombreEquipo] = {}
    equipos["equipos"][nombreEquipo]["nombre"] = equipo["team"]["name"]
    equipos["equipos"][nombreEquipo]["league"] = liga[0]
    equipos["equipos"][nombreEquipo]["logo"] = equipo["team"]["logos"][0]["href"]
    equipos["equipos"][nombreEquipo]["estadisticas"] = {}
    for estadistica in equipo["stats"]:
        if estadistica["name"] in estadisticas:
            equipos["equipos"][nombreEquipo]["estadisticas"][estadistica["name"]] = int(estadistica["value"])

db.create_tables()
db.insert_leagues(liga)
db.insert_teams(list(equipos.values())[0])