import matplotlib.pyplot as plt
import matplotlib.patches as mpt
import numpy as np
from tessellation import Tessellation
from functions import *

#Parameter zur Genauigkeit
num_points = 61
extend = 18
margin = 2.118

#Abfrage nach zu analysierender Parkettierung
print("Auswahl:")
for name in Tessellation.library.keys():
    print(name)
polygon = input("Parkettierung: ")

# Erstellen der Plots für die Parkettierungen
fig, ax = plt.subplots()

#Parkettierungen erstellen und anzeigen
tess = Tessellation(polygon, extend=extend)
tess.show(ax, 'blue', True)

#Duale Parkettierung daraufsetzten
tess.get_dual().show(ax, 'goldenrod')

#Ziele im Kreis um center erstellen
center = tess.center_bridge()
radius = (tess.extend /2 - margin) * tess.spacing
ax.add_patch(plt.Circle(center, radius, color="darkred", fill=False, zorder=6))
circle_points = distribute_points_on_circle(center, radius, num_points, ax)

#Durchschnittsroutenlänge berechnen
medium_length = tess.medium_route(center, circle_points, ax, 5)
print("Durchschnittsroutenlänge für eine Luftlinie von " + str(round(radius,2)) + " Einheiten: " + str(round(medium_length,2)))
print("Das entspricht einer durchschnittlichen Verlängerung von: " + str(round(((medium_length/radius - 1) * 100), 2)) + "%")

#Achsen ausblenden
ax.set_xticks([])
ax.set_yticks([])

#zeigen
plt.tight_layout()
plt.show()
