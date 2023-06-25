import math
from datetime import timedelta

from helpers.decorators import cache_result, calculate_execution_time


COURIERS_AVG_SPEED = 30     # km/h
EARTH_MEAN_RADIUS = 6371.0  # km


#@calculate_execution_time
@cache_result
async def estimate_travel_time(src_lat, src_lon, dst_lat, dst_lon) -> timedelta:
    """
    Takes the geographical coordinates of two points in WGS84 (EPSG:4326),
    calculates the Great Circle Distance between them using Haversine formula,
    and estimates the travel time based on the couriers average speed.
    """
    # convert decimal degrees to radians
    src_lat = math.radians(src_lat)
    src_lon = math.radians(src_lon)
    dst_lat = math.radians(dst_lat)
    dst_lon = math.radians(dst_lon)

    # calculate haversine distance
    dlat = dst_lat - src_lat
    dlon = dst_lon - src_lon
    # a is the square of the half-chord length between the points, or (sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2)).
    a = math.sin(dlat / 2)**2 + math.cos(src_lat) * math.cos(dst_lat) * math.sin(dlon / 2)**2
    # c is the angular distance in radians between the points, or 2 * atan2( √a, √(1−a) ).
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance_km = EARTH_MEAN_RADIUS * c

    # calculate average travel time for a courier
    travel_time_hours = distance_km / COURIERS_AVG_SPEED

    # convert travel time to minutes and round to nearest minute
    travel_time_minutes = round(travel_time_hours * 60)

    return timedelta(minutes=travel_time_minutes)