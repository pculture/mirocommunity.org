from __future__ import with_statement
import os
import subprocess

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from localtv.tiers import Tier


NAME_TO_COST = Tier.NAME_TO_COST()


class SiteCreationForm(forms.ModelForm):
    TIER_CHOICES = (
        ('basic', _('Basic (free of cost)')),
        ('plus', _('Plus ${cost}/mo'.format(cost=NAME_TO_COST['plus']))),
        ('premium', _('Premium ${cost}/mo'.format(cost=NAME_TO_COST['premium']))),
        ('max', _('Max ${cost}/mo'.format(cost=NAME_TO_COST['max'])))
    )
    domain = forms.RegexField(r'^[a-z0-9][a-z0-9-]*$',
                              label=_('Site name'),
                              help_text=_('Letters a-z, numbers, and hyphens only.'))
    tier_name = forms.ChoiceField(label=_('Selected Plan'),
                                  required=True,
                                  choices=TIER_CHOICES)
    first_name = forms.CharField(label=_('First name'))
    last_name = forms.CharField(label=_('Last name'))
    username = forms.RegexField(r'^[\w0-9_]+$',
        label=_('Username'), max_length=30,
        help_text=_('Just letters, digits, and underscores.'))
    email = forms.EmailField()
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Confirm password"), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def validate_unique(self):
        pass

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def clean_domain(self):
        domain = self.cleaned_data['domain']
        if os.path.exists(os.path.join(
            settings.PROJECT_ROOT,
            '{0}_project'.format(domain))):
            raise forms.ValidationError('A site already exists with that name.')
        return domain

    def _log_file(self):
        return open(os.path.join(settings.PROJECT_ROOT,
                                '{domain}.txt'.format(self.cleaned_data)),
                    'a')

    def save(self):
        # For backwards-compatibility, we use the same process as the previous
        # code, with the hope to replace it with something more sane in the
        # future - for example, django 1.4 project templates. -SB
        with self._log_file() as out:
            subprocess.check_call([settings.PROJECT_SCRIPT,
                                   self.cleaned_data['url']],
                                  stdout=out,
                                  stderr=out,
                                  env={
                    'DJANGO_SETTINGS_MODULE':
                        os.environ['DJANGO_SETTINGS_MODULE'],
                    'NEW_TIER_NAME': self.cleaned_data['tier_name'],
                    'NEW_USERNAME': self.cleaned_data['username'],
                    'NEW_PASSWORD': self.cleaned_data['password1'],
                    'NEW_EMAIL': self.cleaned_data['email']})
