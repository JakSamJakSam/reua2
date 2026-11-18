from django.db.models import Count
from django.shortcuts import render

from reua.models import MapPoint, Project, Partner


def index2026(request):
    partners = Partner.objects.all().order_by('?')
    middle=   len(partners) // 2
    partners_row1 = partners[:middle]
    partners_row2 = partners[middle:]
    points = MapPoint.objects.all().annotate(
        stations_count = Count('stations')
    )
    regions = {point.region for point in points}
    stations_count = sum(point.stations_count for point in points)
    points = [
        {
            'lon': point.lon,
            'lat': point.lat,
            'title': point.localized_title,
            'stations_count': point.stations_count,
        }
        for point in points
    ]
    ctx = {
        'news': Project.objects.all()[:4],
        'parnters': {
            'r1': partners_row1,
            'r2': partners_row2
        },
        'stations_count': stations_count,
        'liters': stations_count * 100000,
        'regions_count': len(regions),
        'points': points,
    }
    return render(request, '2026/index/index.html', ctx)

def water2026(request):
    ctx = {
    }
    return render(request, '2026/index/water.html', ctx)
