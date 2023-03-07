from django.contrib.sites.shortcuts import get_current_site

from reua.models import TopMenu, FoundingDocument, SiteSettings


def top_menus(request):
    site = get_current_site(request)
    return {
        'top_menu_items': TopMenu.objects.filter(disabled=False).order_by('order'),
        'founding_documents': FoundingDocument.objects.all(),
        'site_settings': SiteSettings.objects.get(site=site)
    }
