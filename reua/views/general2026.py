from django.shortcuts import render

from reua.models import News, Project, Partner


def index2026(request):
    partners = Partner.objects.all().order_by('?')
    middle=   len(partners) // 2
    partners_row1 = partners[:middle]
    partners_row2 = partners[middle:]
    ctx = {
        'news': Project.objects.all()[:4],
        'parnters': {
            'r1': partners_row1,
            'r2': partners_row2
        }
    }
    return render(request, '2026/index/index.html', ctx)