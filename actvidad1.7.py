import requests

r = requests.get("https://site.web.api.espn.com/apis/v2/sports/soccer/esp.1/standings").json()

estadisticas = ["gamesPlayed", "losses", "pointDifferential", "points", "pointsAgainst", "pointsFor", "ties", "rank"]
liga = []
equipos = {"equipos": {}}
liga.append(r["abbreviation"])
liga.append(r["children"][0]["abbreviation"])
for equipo in r["children"][0]["standings"]["entries"]:
    nombreEquipo = equipo["team"]["name"]
    equipos["equipos"][equipo["team"]["name"]] = {}
    equipos["equipos"][equipo["team"]["name"]]["nombre"] = equipo["team"]["name"]
    equipos["equipos"][nombreEquipo]["league"] = liga[0]
    equipos["equipos"][equipo["team"]["name"]]["logo"] = equipo["team"]["logos"][0]["href"]
    equipos["equipos"][equipo["team"]["name"]]["estadisticas"] = {}
    for estadistica in equipo["stats"]:
        if estadistica["name"] in estadisticas:
            equipos["equipos"][nombreEquipo]["estadisticas"][estadistica["name"]] = estadistica["value"]

print(equipos)