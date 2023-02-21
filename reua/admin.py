from django.contrib import admin

from reua.models import TopMenu, Partner, FoundingDocument

admin.site.register(TopMenu, admin.ModelAdmin)

admin.site.register(Partner, admin.ModelAdmin)

admin.site.register(FoundingDocument, admin.ModelAdmin)
