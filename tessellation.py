import matplotlib.pyplot as plt
import numpy as np
from functions import *

class Tessellation:
    """
    Parkettierung samt Pfaden und Kreuzungen
    """
    library = { #Parkettierung: ((Verzerrung_x, Verzerrung_y), üblicher Name)
        "3-3-3-3-3-3": ((1, 2 / (3**.5)), "regelmäßige Dreiecksparkettierung"),
        "4-4-4-4": ((1,1), "Quadratparkettierung"),
        "6-6-6": ((1, 2 / (3**.5)), "regelmäßige Sechsecksparkettierung"),
        "4-8-8": ((4-2**1.5,4-2**1.5), None),
        "3-6-3-6": ((1, 2 / (3**.5)), None),
        "4-8-8-dual": ((1,1), "rechtwinklige gleichschenklige Dreiecksparkettierung"),
        "3-6-3-6-dual": ((2/(3**.5), 1), "Rautenparkettierung"),
        "4-6-12": ((1/(4+3**.5), 2 / (3**.5)/(4+3**.5)), None),
        "4-6-12-dual": ((1/(4+3**.5), 2 / (3**.5)/(4+3**.5)), None),
        "3-3-4-3-4": (((2 + 3**.5)**-.5, (2 + 3**.5)**-.5), None),
        "3-3-4-3-4-dual": ((6**-.5, 2 * 6**-.5), "katalanische Parkettierung"),
        #"3-4-6": ((1/(1+3**.5), 2 / (3+3**.5)), None),
        "3-3-3-3-6": ((1/7, 2/ 3**.5), None),
        "3-3-3-3-6-dual": ((1/7, 2/ 3**.5), "Floretparkettierung"),
        "5-5-10": ((1 / (2+5**.5), 1/((5+2*5**.5)**.5 + np.sin(.6*np.pi))), "Sonnenblumenparkettierung"),
        "5-5-10-dual": ((1 / (2+5**.5), 1/((5+2*5**.5)**.5 + np.sin(.6*np.pi))), None)
    }

    def __init__(self, type: str, extend: int = 12, spacing: float = 1, origin: tuple[float]=(0,0), rotation90: bool = False):
        '''
        type
            Parkettierungstyp, Auswahl aus self.stretch_factors.keys()
        extend
            Größe (Wiederholungen) der Parkettierung an
        spacing
            Länge einer Standardstrecke
        origin
            verschiebt die Parkettierung zu (x,y)
        rotation90
            spiegelt die Parkettierung an y=x
        '''
        if self.type not in self.library.keys():
            raise ValueError("Parkettierung nicht bekannt")
        self.type = type
        self.extend = extend
        self.spacing = spacing
        if rotation90:
            self.origin = (origin[1],origin[0])
        else:
            self.origin = origin
        self.rotation90 = rotation90
        self._dual = None

        #Parkettierung aufbauen
        self.points = []
        self.lines = []
        process = "points"
        while process != "done":
            for col in range(round(self.extend * self.library[self.type][0][0]+1.5)):
                for row in range(round(self.extend * self.library[self.type][0][1]+1.5)):
                    to_append = [] #diese Punkte werden self.points hinzugefügt, wenn process == "points"
                    #Punktgenerierung
                    if self.type == "3-3-3-3-3-3":
                        x = col * self.spacing + self.origin[0]
                        y = row * self.spacing * (3**.5) / 2 + self.origin[1]
                        if row % 2 == 1:
                            x += self.spacing / 2
                        to_append.append((x,y))
                        
                    elif self.type == "4-4-4-4" \
                    or self.type == "4-8-8-dual":
                        x = col * self.spacing + self.origin[0]
                        y = row * self.spacing + self.origin[1]
                        to_append.append((x,y))
                    
                    elif self.type == "6-6-6":
                        if not (row % 2 == 1 and col % 3 == 2) \
                        and not (row % 2 == 0 and col % 3 == 1):
                            x = col * self.spacing + self.origin[0]
                            y = row * self.spacing * (3**.5) / 2 + self.origin[1]
                            if row % 2 == 1:
                                x += self.spacing / 2
                            to_append.append((x,y))
                    
                    elif self.type == "4-8-8":
                        if col % 4 in (1,2) and row % 4 in (1,2) \
                        or col % 4 in (0,3) and row % 4 in (0,3):
                            x = col * self.spacing * (2 + 2**.5)/4 + self.origin[0]
                            y = row * self.spacing * (2 + 2**.5)/4 + self.origin[1]
                            if col % 2 == 1:
                                x -= self.spacing * (.5 - 2 ** (-1.5))
                            if row % 2 == 1:
                                y -= self.spacing * (.5 - 2 ** (-1.5))
                            to_append.append((x,y))
                    
                    elif self.type == "3-6-3-6":
                        if row % 2 == 0 \
                        or (row % 4 == 1 and col % 2 == 0) \
                        or (row % 4 == 3 and col % 2 == 1):
                            x = col * self.spacing + self.origin[0]
                            y = row * self.spacing * (3**.5) / 2 + self.origin[1]
                            if row % 2 == 1:
                                x += self.spacing / 2
                            to_append.append((x,y))
                    
                    elif self.type == "3-6-3-6-dual":
                        x = col * self.spacing * (3**.5) / 2 + self.origin[0]
                        y = row * self.spacing + self.origin[1]
                        if col % 2 == 1:
                            y += self.spacing / 2
                        to_append.append((x,y))
                    
                    elif self.type == "4-6-12":
                        x = col * self.spacing * (3 + 3**.5) + self.origin[0]
                        y = row * self.spacing * (3**.5) / 2 * (3 + 3**.5) + self.origin[1]
                        if row % 2 == 1:
                            x += self.spacing* (3 + 3**.5) / 2
                        to_append += distribute_points_on_circle((x,y), self.spacing * (2 + 3**.5)**.5, 12, displacement=np.pi/12)
                    
                    elif self.type == "4-6-12-dual":
                        #Anomalie! Strecken werden hier schon bei der Punktgenerierung gezeichnet
                        x = col * self.spacing * (3 + 3**.5) + self.origin[0]
                        y = row * self.spacing * (3**.5) / 2 * (3 + 3**.5) + self.origin[1]
                        if row % 2 == 1:
                            x += self.spacing* (3 + 3**.5) / 2
                        points_a = distribute_points_on_circle((x,y), self.spacing * (1+3**.5), 6, displacement=np.pi/6)
                        points_b = distribute_points_on_circle((x,y), self.spacing * (3 + 3**.5)/2, 6)
                        
                        for point_a in points_a:
                            for point in self.points:
                                if np.allclose(point_a, point):
                                    point_a = point
                                    break
                            else:
                                to_append.append(point_a)
                            self.lines.append(((x, point_a[0]),(y, point_a[1])))

                        for point_b in points_b:
                            for point in self.points:
                                if np.allclose(point_b, point):
                                    point_b = point
                                    break
                            else:
                                to_append.append(point_b)
                                for point in self.points + to_append:
                                    if np.isclose(np.hypot(point_b[0] - point[0], point_b[1] - point[1]), self.spacing * (1+3**.5)/2):
                                        self.lines.append(((point_b[0], point[0]),(point_b[1], point[1])))
                            self.lines.append(((x, point_b[0]),(y, point_b[1])))
                        to_append.append((x,y))

                    elif self.type == "3-3-4-3-4":
                        x = col * self.spacing * (2 + 3**.5)**.5 + self.origin[0]
                        y = row * self.spacing * (2 + 3**.5)**.5 + self.origin[1]
                        to_append = distribute_points_on_circle((x,y), self.spacing * 2**(-.5), 4, displacement=-np.pi/3)

                    elif self.type == "3-3-4-3-4-dual":
                        x = col * self.spacing * (2 + 3**.5)**.5 * (3-3**.5) + self.origin[0]
                        y = row * self.spacing * (2 + 3**.5)**.5 * (3-3**.5) / 2 + self.origin[1]
                        if row % 2 == 1:
                            x += self.spacing * (2 + 3**.5)**.5 * (3-3**.5) / 2
                            to_append = distribute_points_on_circle((x,y), self.spacing, 4, displacement=np.pi/12)
                        to_append.append((x,y))
                    
                    #noch nicht dual versehen
                    elif self.type == "3-4-6":
                        x = col * self.spacing * (1+3**.5) + self.origin[0]
                        y = row * self.spacing * (3+3**.5)/2 + self.origin[1]
                        if row % 2 == 1:
                            x += self.spacing * (1+3**.5)/2
                        to_append += distribute_points_on_circle((x,y), self.spacing, 6, displacement=np.pi/6)
                    
                    elif self.type == "3-3-3-3-6":
                        x = col * self.spacing * 7 + self.origin[0]
                        y = row * self.spacing * 3**.5 / 2 + self.origin[1]
                        x += (row % 3) * self.spacing * 2.5
                        x += (row//3) * self.spacing * .5
                        to_append += distribute_points_on_circle((x,y), self.spacing, 6)
                    
                    elif self.type == "3-3-3-3-6-dual":
                        #Anomalie! Strecken werden hier schon zum Teil bei der Punktgenerierung gezeichnet
                        x = col * self.spacing * 7 + self.origin[0]
                        y = row * self.spacing * 3**.5 / 2 + self.origin[1]
                        x += (row % 3) * self.spacing * 2.5
                        x += (row//3) * self.spacing * .5
                        to_append += distribute_points_on_circle((x,y), self.spacing * 2 /3**.5, 6, displacement=np.pi/6)
                        for point in to_append:
                            self.lines.append(((x, point[0]),(y,point[1])))
                        to_append.append((x,y))
                        to_append += [(x+self.spacing*1.5,y - self.spacing/(2*3**.5)),(x-self.spacing*1.5,y + self.spacing/(2*3**.5))]
                    
                    elif self.type == "5-5-10":
                        x = col * self.spacing * (2+5**.5) + self.origin[0]
                        y = row * self.spacing * ((5+2*5**.5)**.5 + np.sin(.6*np.pi)) + self.origin[1]
                        if row % 2 == 1:
                            x += self.spacing * (.5*(1+5**.5) + np.cos(.6*np.pi))
                        to_append += distribute_points_on_circle((x,y), self.spacing * .5*(1+5**.5), 10)
                        to_append.append((x + (.5 + .5*(1+5**.5)) * self.spacing, y + .5 * (5+2*5**.5)**.5) * self.spacing)
                        to_append.append((x + (.5 + .5*(1+5**.5)) * self.spacing, y - .5 * (5+2*5**.5)**.5) * self.spacing)
                    
                    elif self.type == "5-5-10-dual":
                        x = col * self.spacing * (2+5**.5) + self.origin[0]
                        y = row * self.spacing * ((5+2*5**.5)**.5 + np.sin(.6*np.pi)) + self.origin[1]
                        if row % 2 == 1:
                            x += self.spacing * (.5*(1+5**.5) + np.cos(.6*np.pi))
                            to_append += distribute_points_on_circle((x,y), self.spacing * .5 * ((5+2*5**.5)**.5 + (1+2*5**-.5)**.5), 10, displacement=-3*np.pi/10)[:4]
                        else:
                            to_append += distribute_points_on_circle((x,y), self.spacing * .5 * ((5+2*5**.5)**.5 + (1+2*5**-.5)**.5), 10, displacement=-np.pi/10)[2:]
                        to_append.append((x,y))
                    
                    if process == "points":
                        print(to_append)
                        self.points += to_append
                    else:
                        #Streckengenerierung für duale Parkettierungen
                        for (nx, ny) in self.points:
                            if self.type == "4-8-8-dual":
                                if col % 2 == 1 and row % 2 == 0:
                                    if np.isclose(np.hypot(x - nx, y - ny), self.spacing) \
                                    or np.isclose(np.hypot(x - nx, y - ny), self.spacing * (2**.5)):
                                        self.lines.append(((x, nx),(y, ny)))
                                if col % 2 == 0 and row % 2 == 1:
                                    if np.isclose(np.hypot(x - nx, y - ny), self.spacing):
                                        self.lines.append(((x, nx),(y, ny)))

                            elif self.type == "3-6-3-6-dual":
                                if row % 3 == col % 2:
                                    if np.isclose(np.hypot(x - nx, y - ny), self.spacing):
                                        self.lines.append(((x, nx),(y, ny)))
                                
                            elif self.type == "3-3-4-3-4-dual":
                                if np.isclose(np.hypot(x - nx, y - ny), self.spacing):
                                    self.lines.append(((x, nx),(y, ny)))
                                if row % 2 == 1:
                                    for point in to_append[:-1]:
                                        if np.isclose(np.hypot(point[0] - nx, point[1] - ny), self.spacing* (3**.5 -1)):
                                            self.lines.append(((point[0], nx),(point[1], ny)))
                            
                            elif self.type == "3-3-3-3-6-dual":
                                #Strecken werden hier schon zum Teil bei der Punktgenerierung gezeichnet
                                if np.isclose(np.hypot(to_append[-2][0] - nx, to_append[-2][1] - ny), self.spacing/3**.5):
                                    self.lines.append(((to_append[-2][0], nx),(to_append[-2][1], ny)))
                                for point in to_append[:5:2]:
                                    if np.isclose(np.hypot(point[0] - nx, point[1] - ny), self.spacing/3**.5):
                                        self.lines.append(((point[0], nx),(point[1], ny)))
                            
                            elif self.type == "5-5-10-dual":
                                #Strecken werden hier schon zum Teil bei der Punktgenerierung gezeichnet
                                if np.isclose(np.hypot(to_append[-1][0] - nx, to_append[-1][1] - ny), self.spacing * .5 * ((5+2*5**.5)**.5 + (1+2*5**-.5)**.5)):
                                    self.lines.append(((to_append[-1][0], nx),(to_append[-1][1], ny)))
                                if row % 2 == 0:
                                    for point in to_append[1:-1:2]:
                                        if np.isclose(np.hypot(point[0] - nx, point[1] - ny), self.spacing * (1+2/5**.5)**.5):
                                            self.lines.append(((point[0], nx),(point[1], ny)))
                                else:
                                    for point in to_append[:3:2]:
                                        if np.isclose(np.hypot(point[0] - nx, point[1] - ny), self.spacing * (1+2/5**.5)**.5):
                                            self.lines.append(((point[0], nx),(point[1], ny)))
                                    for point in to_append[:4:3]:
                                        if np.isclose(np.hypot(point[0] - nx, point[1] - ny), self.spacing * (2*np.sin(.6*np.pi) - (1+2/5**.5)**.5)):
                                            self.lines.append(((point[0], nx),(point[1], ny)))

                            elif self.type == "4-6-12-dual":
                                #Anomalie! Strecken werden hier schon bei der Punktgenerierung gezeichnet
                                break

            if self.type[-4:] == "dual" and process == "points":
                #nur duale Parkettierungen benötigen Schritt der Streckengenerierung in dieser While-Schleife,
                #da es für archmedische einfachere Methoden gibt (s. u.)
                process = "lines"
            else:
                process = "done"

        #Streckengenerierung für platonische und archmedische Parkettierungen
        if self.type[-4:] != "dual":
            for i, (x, y) in enumerate(self.points):
                # Verbinden mit Nachbarn
                for j, (nx, ny) in enumerate(self.points[i+1:], i+1):
                    if np.isclose(np.hypot(x - nx, y - ny), self.spacing):
                        self.lines.append(((x, nx),(y, ny)))
        
        if rotation90:
            #Spiegeln an x=y
            for i, point in enumerate(self.points):
                self.points[i] = (point[1], point[0])
            for i, line in enumerate(self.lines):
                self.lines[i] = (line[1],line[0])
        

    def show(self, ax: plt.Axes, color: str, titeling=False):
        '''
        zeigt die Parkettierung in einem Plot
        
        ax
            in diesem KOS wird die Parkettierung angezeigt
        color
            in dieser Farbe wird die Parkettierung angezeigt
            muss eine CSS-Farbe sein, die es auch mit dem Präfix "dark-" gibt
        titeling
            soll das KOS nach der Parkettierung benannt werden
        '''
        ax.set_aspect('equal')

        for i in self.points:
            ax.scatter(i[0], i[1], color=color, zorder=5)
        for i in self.lines:
            ax.plot(i[0], i[1], color='dark'+color)
        
        if titeling:
            ax.set_title(self.type + "-Parkettierung" if self.library[self.type][1] == None else self.library[self.type][1])
    
    def get_dual(self) -> "Tessellation":
        '''
        gibt die zu self gehörige duale Parkettierung zurück
        '''
        if self._dual == None:
            if self.type == "3-3-3-3-3-3":
                self._dual = Tessellation(
                    "6-6-6",
                    origin=(self.origin[1] + self.spacing / 2, self.origin[0] + self.spacing * (3**.5)/6),
                    spacing=self.spacing /(3**.5),
                    rotation90=not self.rotation90,
                    extend=round(self.extend * (3**.5) - 2)
                )
            elif self.type == "4-4-4-4":
                self._dual = Tessellation(
                    "4-4-4-4",
                    origin=(self.origin[0] + self.spacing / 2, self.origin[1] + self.spacing / 2),
                    spacing=self.spacing,
                    extend=self.extend-1
                )
            elif self.type == "6-6-6":
                self._dual = Tessellation(
                    "3-3-3-3-3-3",
                    origin=(self.origin[0] + self.spacing, self.origin[1]),
                    spacing=self.spacing*(3**.5),
                    rotation90=not self.rotation90,
                    extend=round(self.extend/(3**.5))
                )
            elif self.type == "4-8-8":
                self._dual = Tessellation(
                    "4-8-8-dual",
                    origin=(self.origin[0] + self.spacing * (.5 + 2**(-.5)), self.origin[1] + self.spacing * (.5 + 2**(-.5))),
                    spacing=self.spacing * (1+2**(-.5)),
                    extend=self.extend/(1+2**(-.5))-1
                )
            elif self.type == "4-8-8-dual":
                self._dual = Tessellation(
                    "4-8-8",
                    origin=(self.origin[0] + self.spacing / (2+2**.5), self.origin[1] + self.spacing / (2+2**.5)),
                    spacing=self.spacing / (1+2**(-.5)),
                    extend=self.extend*(1+2**(-.5))-1
                )
            elif self.type == "3-6-3-6":
                self._dual = Tessellation(
                    "3-6-3-6-dual",
                    origin=(self.origin[0] + self.spacing / 2, self.origin[1] - self.spacing * (3**.5) / 2),
                    spacing=self.spacing * (2/3**.5),
                    extend=self.extend/(2/(3**.5)),
                    rotation90=self.rotation90
                )
            elif self.type == "3-6-3-6-dual":
                self._dual = Tessellation(
                    "3-6-3-6",
                    origin=(self.origin[0] + self.spacing * (3**1.5/4), self.origin[1] + self.spacing * 3 / 4),
                    spacing=self.spacing * (3**.5/2),
                    extend=self.extend*(2/(3**.5))-1,
                    rotation90=self.rotation90
                )
            elif self.type == "4-6-12":
                self._dual = Tessellation(
                    "4-6-12-dual",
                    origin=self.origin,
                    spacing=self.spacing,
                    extend=self.extend,
                    rotation90=self.rotation90
                )
            elif self.type == "4-6-12-dual":
                self._dual = Tessellation(
                    "4-6-12",
                    origin=self.origin,
                    spacing=self.spacing,
                    extend=self.extend,
                    rotation90=self.rotation90
                )
            elif self.type == "3-3-4-3-4":
                self._dual = Tessellation(
                    "3-3-4-3-4-dual",
                    origin=self.origin,
                    spacing=self.spacing/(3-3**.5),
                    extend=self.extend+2,
                    rotation90=self.rotation90
                )
            elif self.type == "3-3-4-3-4-dual":
                self._dual = Tessellation(
                    "3-3-4-3-4",
                    origin=self.origin,
                    spacing=self.spacing*(3-3**.5),
                    extend=self.extend-2,
                    rotation90=self.rotation90
                )
            elif self.type == "3-3-3-3-6":
                self._dual = Tessellation(
                    "3-3-3-3-6-dual",
                    origin=self.origin,
                    spacing=self.spacing,
                    extend=self.extend,
                    rotation90=self.rotation90
                )
            elif self.type == "3-3-3-3-6-dual":
                self._dual = Tessellation(
                    "3-3-3-3-6",
                    origin=self.origin,
                    spacing=self.spacing,
                    extend=self.extend,
                    rotation90=self.rotation90
                )
            elif self.type == "5-5-10":
                self._dual = Tessellation(
                    "5-5-10-dual",
                    origin=self.origin,
                    spacing=self.spacing,
                    extend=self.extend,
                    rotation90=self.rotation90
                )
            elif self.type == "5-5-10-dual":
                self._dual = Tessellation(
                    "5-5-10",
                    origin=self.origin,
                    spacing=self.spacing,
                    extend=self.extend,
                    rotation90=self.rotation90
                )
        return self._dual

    def center_bridge(self) -> tuple:
        '''
        gibt die nächste Überschneidung von dualer und Parkettierung vom Mittelpunkt als Koordinaten zurück
        '''
        return closest_intersection(
            (self.extend/2,self.extend/2),
            self.lines,
            self.get_dual().lines
        )
    
    def medium_route(self, point1: tuple[float], points: list[tuple[float]], ax: plt.Axes=None, show: bool=None) -> float:
        '''
        gibt den Durchschnitt der Längen aller kürzesten Routen von point1 zu points zurück,
        wenn len(points) == 1, gibt es die Länge der kürzesten Route zurück

        point1
            Punkt (x,y) von dem alle Routen ausgehen
        points
            Punkte [(x,y),...] zu denen kürzeste Routen berechnet werden
        ax
            in diesem KOS werden die closest_waypoints zu points geplottet
        show
            plottet den Pfad zu points[show] in ax
        '''
        waypoint1, line1 = closest_waypoint(point1, self.lines)
        waypoints = [] #nächster Punkt auf einer Strecke für point in points
        end_points = [] #Alle Enden der waypoint-Strecken
        respective_end_points = [] #Streckenenden für Strecke auf point in points
        for point in points:
            i = closest_waypoint(point, self.lines)
            ax.scatter(i[0][0], i[0][1], color='green', zorder=9)
            waypoints += [i[0]]
            if (i[1][0][0], i[1][1][0]) not in end_points:
                end_points.append((i[1][0][0], i[1][1][0]))
            if (i[1][0][1], i[1][1][1]) not in end_points:
                end_points.append((i[1][0][1], i[1][1][1]))
            respective_end_points.append(((i[1][0][0], i[1][1][0]),(i[1][0][1], i[1][1][1])))
        start_points = ((line1[0][0], line1[1][0]),(line1[0][1], line1[1][1]))

        #Adjazenzliste erstellen
        graph = {point: [] for point in self.points}
        for line in self.lines:
            point1 = (line[0][0], line[1][0])
            point2 = (line[0][1], line[1][1])

            distance = np.hypot(point1[0]-point2[0], point1[1]-point2[1])

            if point2 not in start_points:
                graph[point1].append((point2, distance))
            if point1 not in start_points:
                graph[point2].append((point1, distance))
        

        # Dijkstra-Algorithmus implementieren
        unvisited = {point: float('inf') for point in self.points}
        unvisited[start_points[0]] = np.hypot(waypoint1[0]-start_points[0][0], waypoint1[1]-start_points[0][1])
        unvisited[start_points[1]] = np.hypot(waypoint1[0]-start_points[1][0], waypoint1[1]-start_points[1][1])
        previous_nodes = {point: None for point in self.points}

        # Dijkstra-Suche
        end_point_distances = {}
        while len(end_point_distances) < len(end_points):
            # Wähle den Knoten mit der kleinsten Distanz
            current_point = min(unvisited, key=unvisited.get)
            current_distance = unvisited[current_point]
            if current_point in end_points:
                end_point_distances[end_points.index(current_point)] = current_distance
            
            # Gehe alle Nachbarn des aktuellen Punktes durch
            for neighbor, weight in graph[current_point]:
                if neighbor in unvisited:
                    distance = current_distance + weight
                    if distance < unvisited.get(neighbor, float('inf')):
                        unvisited[neighbor] = distance
                        previous_nodes[neighbor] = current_point
            
            # Entferne den aktuellen Punkt aus den unbesuchten Knoten
            del unvisited[current_point]

        distances = []
        for i, waypoint in enumerate(waypoints):
            #küresten der beiden Pfade heraussuchen
            distance1 = end_point_distances[end_points.index(respective_end_points[i][0])] + np.hypot(waypoint[0]-respective_end_points[i][0][0], waypoint[1]-respective_end_points[i][0][1])
            distance2 = end_point_distances[end_points.index(respective_end_points[i][1])] + np.hypot(waypoint[0]-respective_end_points[i][1][0], waypoint[1]-respective_end_points[i][1][1])
            distances.append(min([distance1, distance2]))

            if show == i and ax != None:
                # Den kürzesten Pfad rekonstruieren
                if distance1 < distance2:
                    current_point = respective_end_points[i][0]
                else:
                    current_point = respective_end_points[i][1]
                
                path = []
                next_point = waypoints[i]
                while current_point is not None:
                    path.append(current_point)
                    ax.plot((next_point[0], current_point[0]), (next_point[1], current_point[1]), color="darkmagenta",zorder=8)
                    ax.scatter(current_point[0], current_point[1], color="magenta", zorder=9)
                    next_point = current_point
                    current_point = previous_nodes[current_point]
                ax.plot((next_point[0], waypoint1[0]), (next_point[1], waypoint1[1]), color="darkmagenta",zorder=8)
                path.reverse()
        
        return sum(distances)/len(distances)