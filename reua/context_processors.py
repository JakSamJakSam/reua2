from reua.forms.feedback import FeedbackForm
from reua.models import TopMenu, FoundingDocument


def top_menus(request):
    return {
        'top_menu_items': TopMenu.objects.filter(disabled=False).order_by('order'),
        'founding_documents': FoundingDocument.objects.all(),
    }
