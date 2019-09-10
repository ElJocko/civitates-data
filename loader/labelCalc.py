import math
from collections import namedtuple

SIZE_WORLD = 268435456.0

Coordinate = namedtuple("Coordinate", "latitude longitude")
MapPoint = namedtuple("MapPoint", "x y")
ScreenPoint = namedtuple("ScreenPoint", "x y")
ScreenRect = namedtuple("ScreenRect", "x y width height")


def zoom_scale_for_zoom_level(zoom_level):
    return pow(2.0, (zoom_level - 20.0))


def map_point_for_coordinate(coordinate: Coordinate):
    x = (float(coordinate.longitude) + 180.0) * (SIZE_WORLD / 360.0)
    siny = math.sin(float(coordinate.latitude) * (math.pi / 180.0))
    y = (0.5 - (math.log((1.0 + siny) / (1.0 - siny)) / (4.0 * math.pi))) * SIZE_WORLD
    return MapPoint(x, y)


def screen_point_for_map_point(map_point: MapPoint, zoom_level):
    zoom_scale = zoom_scale_for_zoom_level(zoom_level)
    return ScreenPoint(map_point.x * zoom_scale, map_point.y * zoom_scale)


def screen_rects_overlap(screen_rect_1: ScreenRect, screen_rect_2: ScreenRect):
    sr1_x1 = screen_rect_1.x
    sr1_x2 = screen_rect_1.x + screen_rect_1.width
    sr2_x1 = screen_rect_2.x
    sr2_x2 = screen_rect_2.x + screen_rect_2.width

    sr1_y1 = screen_rect_1.y
    sr1_y2 = screen_rect_1.y + screen_rect_1.height
    sr2_y1 = screen_rect_2.y
    sr2_y2 = screen_rect_2.y + screen_rect_2.height

    return sr1_x1 < sr2_x2 and sr1_x2 > sr2_x1 and sr1_y1 < sr2_y2 and sr1_y2 > sr2_y1


def marker_screen_rect_for_map_point(map_point: MapPoint, zoom_level):
    marker_diameter = 10
    marker_radius = marker_diameter / 2

    # Convert from map points to screen points
    screen_point = screen_point_for_map_point(map_point, zoom_level)

    screen_rect = ScreenRect((screen_point.x - marker_radius), (screen_point.y - marker_radius), marker_diameter, marker_diameter)

    return screen_rect


def tag_screen_rect_for_map_point(map_point: MapPoint, tag_position, zoom_level):
    # Size of the tag on the screen
    rect_width= 40
    rect_height = 10

    marker_radius = 5

    # Convert from map points to screen points
    screen_point = screen_point_for_map_point(map_point, zoom_level)

    # Calculate the screen_rect
    x = 0
    y = 0
    if tag_position == 4:
        # Top Center
        x = screen_point.x - (rect_width / 2)
        y = screen_point.y - rect_height - marker_radius
    elif tag_position == 0:
        # Top Right
        x = screen_point.x + marker_radius
        y = screen_point.y - rect_height - marker_radius
    elif tag_position == 6:
        # Right
        x = screen_point.x + marker_radius
        y = screen_point.y - (rect_height / 2)
    elif tag_position == 1:
        # Bottom Right
        x = screen_point.x + marker_radius
        y = screen_point.y - (rect_height / 2) + marker_radius
    elif tag_position == 5:
        # Bottom Center
        x = screen_point.x - (rect_width / 2)
        y = screen_point.y - (rect_height / 2) + marker_radius
    elif tag_position == 3:
        # Bottom Left
        x = screen_point.x - rect_width - marker_radius
        y = screen_point.y - (rect_height / 2) + marker_radius
    elif tag_position == 7:
        # Left
        x = screen_point.x - rect_width - marker_radius
        y = screen_point.y - (rect_height / 2)
    elif tag_position == 2:
        # Top Left
        x = screen_point.x - rect_width - marker_radius
        y = screen_point.y - rect_height - marker_radius

    return ScreenRect(x, y, rect_width, rect_height)
