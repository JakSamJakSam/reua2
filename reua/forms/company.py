import datetime

from django.core.exceptions import ValidationError
from django.db.models import Max
from django.forms import ModelForm, CharField, BooleanField, ModelChoiceField, ImageField

from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

from reua.models import Company, SiteSettings, CompanyCategory, InvestitionCompany
from reua.models.compaies import InvestitionCategory


class AddCompanyForm(ModelForm):
    def __init__(self, *args, site_id=None, **kwargs):
        self.site_id = site_id
        super().__init__(*args, **kwargs)

    form_code = CharField(required=True, label=_("Код запрошення до групи компаній"))
    phone = PhoneNumberField(label=Company.phone.field.verbose_name, required=False)
    repr_phone = PhoneNumberField(label=Company.repr_phone.field.verbose_name, required=False)
    logotype = ImageField(allow_empty_file=True, label=Company.logotype.field.verbose_name, required=False)
    i_agree = BooleanField(
        required=False,
        label=_('Даю згоду на обробку персональних даних'),
        help_text=_(
            "Група компаній REUA Building Group є публічною компанією з відкритими даними про учасників групи. Ваша компанія відображатиметься у розділі \"Група компаній\" з відображенням статусу.")
    )
    
    def save(self, commit=True):
        max_order = self._meta.model.objects.aggregate(max_order=Max('order'))['max_order']
        max_order = max_order if max_order is not None else 0
        self.instance.order = max_order + 1
        return super().save(commit=commit)

    def clean_i_agree(self):
        if not self.cleaned_data['i_agree']:
            raise ValidationError(_("Ваша згода обов'язкова"))


class AddCompanyG(AddCompanyForm):
    category = ModelChoiceField(CompanyCategory.objects.all(), label=Company.category.field.verbose_name,
                                required=True, empty_label=_('Оберіть категорію'))
    def clean_form_code(self):
        try:
            setts = SiteSettings.objects.get(site_id=self.site_id)
        except SiteSettings.DoesNotExist:
            raise ValidationError(_('Невірний код'))
        if self.cleaned_data['form_code'] != setts.company_add_code:
            raise ValidationError(_('Невірний код'))

    class Meta:
        model = Company
        exclude = ('order',)
        empty_labels = {'category': _('Select Category'), }


class AddCompanyI(AddCompanyForm):
    category = ModelChoiceField(InvestitionCategory.objects.all(), label=InvestitionCompany.category.field.verbose_name,
                                required=True, empty_label=_('Оберіть категорію'))

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        current_year = datetime.date.today().year
        self.fields['turnover_1'].label = _(f'Оборот за {current_year-1} р.')
        self.fields['turnover_2'].label = _(f'Оборот за {current_year-2} р.')
        self.fields['turnover_3'].label = _(f'Оборот за {current_year-3} р.')

    def clean_form_code(self):
        try:
            setts = SiteSettings.objects.get(site_id=self.site_id)
        except SiteSettings.DoesNotExist:
            raise ValidationError(_('Невірний код'))
        if self.cleaned_data['form_code'] != setts.invest_add_code:
            raise ValidationError(_('Невірний код'))

    class Meta:
        model = InvestitionCompany
        exclude = ('order',)
        empty_labels = {'category': _('Select Category'), }
