from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms import ModelForm, Textarea, BooleanField
from django.utils.translation import ugettext_lazy as _
import os
from backend.models import Theme

__author__ = 'sdvoynikov'


class UploadThemeForm(ModelForm):
    class Meta:
        model = Theme
        fields = ('name', 'author', 'website', 'comment', 'archive')
        widgets = {
            'comment': Textarea(attrs={'cols': 80, 'rows': 4}),
        }

    accept = BooleanField(required=True)

    def clean_name(self):
        data = self.cleaned_data['name']
        data = data.strip()
        try:
            theme = Theme.objects.get(name__iexact=data)
        except ObjectDoesNotExist:
            theme = None

        if theme:
            raise ValidationError(_('Theme with name "%(name)s" already exists'),
                                  params={'name': data},
                                  code='name-is-not-unique')

        return data

    def clean_website(self):
        data = self.cleaned_data['website']
        data = data.strip()

        if len(data) > 0 and \
                        data.find('http://') != 0 and \
                        data.find('https://') != 0 and \
                        data.find('mailto:') != 0:
            data = 'http://' + data

        return data

    def clean_archive(self):
        data = self.cleaned_data['archive']

        if not data:
            raise ValidationError(_('Theme file is not specified'))

        name, ext = os.path.splitext(data.name)
        if not ext.lower() in ['.icls', '.xml']:
            raise ValidationError(_('Only ICLS and XML files are supported'))

        return data
