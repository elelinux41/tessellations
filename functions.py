import numpy as np
import matplotlib.pyplot as plt

def closest_intersection(point: tuple[float], lines1: list[tuple[tuple[float]]], lines2: list[tuple[tuple[float]]]) -> tuple | None:
    """
    gibt den nächsten Schnittpunkt von point aus zwischen Strecken aus lines1 und lines2 zurück
    
    point
        von diesem Punkt (x,y) aus wird gesucht
    lines1, lines2
        Listen von Strecken [((x, nx),(y, ny)),...] die sich überschneiden
    """
    def line_intersection(line1: tuple[tuple[float]], line2: tuple[tuple[float]]) -> tuple | None:
        """
        gibt den Schnittpunkt zweier Strecken zurück
        
        line1, line2
            Strecken ((x, xn), (y, yn)), die sich kreuzen sollen
        """
        # Punkte der ersten Linie
        x1, x2 = line1[0]
        y1, y2 = line1[1]
        
        # Punkte der zweiten Linie
        x3, x4 = line2[0]
        y3, y4 = line2[1]

        # Berechnung der Determinanten
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        
        if denominator == 0:
            return None  # Linien sind parallel, kein Schnittpunkt
        
        # Berechnung der Schnittkoordinaten
        intersect_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
        intersect_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator

        # Überprüfen, ob der Schnittpunkt innerhalb beider Liniensegmente liegt
        if (min(x1, x2) <= intersect_x <= max(x1, x2) and min(y1, y2) <= intersect_y <= max(y1, y2) and
            min(x3, x4) <= intersect_x <= max(x3, x4) and min(y3, y4) <= intersect_y <= max(y3, y4)):
            return (intersect_x, intersect_y)
        
        return None  # Der Schnittpunkt liegt nicht auf beiden Liniensegmenten
    min_distance = float('inf')
    nearest_intersection = None
    
    # Alle Paare von Liniensegmenten durchgehen
    for line1 in lines1:
        for line2 in lines2:
            intersection = line_intersection(line1, line2)
            if intersection is not None:
                # Abstand vom gegebenen Punkt zum Schnittpunkt berechnen
                dist = np.hypot(point[0] - intersection[0], point[1] - intersection[1])
                if dist < min_distance:
                    min_distance = dist
                    nearest_intersection = intersection

    return nearest_intersection

# Finde die nächste Strecke und den projizierten Punkt
def closest_waypoint(point: tuple[float], lines: list[tuple[tuple[float]]]) -> tuple:
    '''
    gibt den nächsten Punkt (und dessen Strecke) auf einer Strecke aus lines von point aus zurück

    point
        von diesem Punkt (x,y) aus wird gesucht

    lines
        Liste von Strecken [((x, nx),(y, ny)),...]
    '''
    def project_point_on_line(a, b, p):
        '''
        gibt Pjektioon des Punktes p aus Strecke ab zurück
        a, b
            Punkte (x,y) der Strecke
        p
            zu projektierender Punkt (x,y)
        '''
        ap = np.array([p[0] - a[0], p[1] - a[1]])
        ab = np.array([b[0] - a[0], b[1] - a[1]])
        ab2 = np.dot(ab, ab)
        t = np.dot(ap, ab) / ab2
        t = np.clip(t, 0, 1)  # Begrenze t auf [0, 1], um sicherzustellen, dass die Projektion auf der Strecke liegt
        return a[0] + t * ab[0], a[1] + t * ab[1]
    min_distance = float('inf')
    closest_point = None
    closest_line = None
    
    for line in lines:
        point1 = (line[0][0], line[1][0])
        point2 = (line[0][1], line[1][1])
        
        # Projektion des Punktes auf die Linie
        projected_point = project_point_on_line(point1, point2, point)
        
        # Berechne die Distanz zwischen dem Punkt und der Projektion
        distance = np.hypot(point[0] - projected_point[0], point[1] - projected_point[1])
        
        if distance < min_distance:
            min_distance = distance
            closest_point = projected_point
            closest_line = line
    
    return closest_point, closest_line


def distribute_points_on_circle(center: tuple[float], radius: float, num_points: int, ax: plt.Axes=None, displacement: float=0) -> list:
    """
    gibt gleichmäßig verteilte Punkte um einen Kreis zurück

    center
        Mittelpunkt
    radius
        Radius
    num_points
        Anzahl der Punkte, die auf dem Kreis verteilt werden sollen
    ax
        KOS, in dem die Punkte geplottet werden sollen, wenn gewollt
    displacement
        Verschiebung der Punkte in Bogenmaß um den Mittelpunkt
    """
    # Berechne die Winkel für die Punkte
    angles = [i + displacement for i in np.linspace(0, 2 * np.pi, num_points, endpoint=False)]
    
    # Berechne die x- und y-Koordinaten der Punkte auf dem Kreis
    points = []
    for angle in angles:
        x = center[0] + radius * np.cos(angle)
        y = center[1] + radius * np.sin(angle)
        points.append((x,y))
        if ax is not None:
            ax.scatter(x, y, color='red', zorder=6)
            ax.scatter(center[0], center[1], color="red", zorder=9)

    return points