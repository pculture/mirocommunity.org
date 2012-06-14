from __future__ import with_statement
import os
import subprocess

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from mirocommunity_saas.models import Tier

from mirocommunity_site.utils.projects import (create_project,
                                               _project_name,
                                               _mysql_database_name,
                                               create_mysql_database,
                                               syncdb,
                                               initialize)
from mirocommunity_site.signals import post_creation


class TierChoiceField(forms.models.ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.price == 0:
            return "{name} (free of cost)".format(name=obj.name)
        return "{name} ${price}/mo".format(name=obj.name, price=obj.price)


class SiteCreationForm(forms.ModelForm):
    site_name = forms.RegexField(r'^[a-z0-9][a-z0-9-]*$',
                                 max_length=20,
                                 label=_('Site name'),
                                 help_text=_('Letters a-z, numbers, and '
                                             'hyphens only.'))
    tier = TierChoiceField(queryset=Tier.objects.filter(slug__in=['basic',
                                                                  'plus',
                                                                  'premium',
                                                                  'max']
                                               ).order_by('price'),
                           label=_('Selected Plan'),
                           required=True)
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

    def clean_site_name(self):
        site_name = self.cleaned_data['site_name']
        if os.path.exists(os.path.join(
            settings.SITE_CREATION_ROOT,
            _project_name(site_name))):
            raise forms.ValidationError('A site already exists with that name.')
        return site_name

    def save(self):
        site_name = self.cleaned_data['site_name']
        create_project(site_name)

        default_db = settings.DATABASES['default']
        if default_db['ENGINE'] == 'django.db.backends.sqlite3':
            pass
        elif default_db['ENGINE'] == 'django.db.backends.mysql':
            database_name = _mysql_database_name(site_name)
            create_mysql_database(database_name)
        else:
            raise ValueError("Unhandled database.")

        syncdb(site_name)

        redirect = initialize(site_name,
                              username=self.cleaned_data['username'],
                              email=self.cleaned_data['email'],
                              password=self.cleaned_data['password1'],
                              tier=self.cleaned_data['tier'].slug)

        # At this point, the site is initialized; we send a post-creation
        # signal so that you can hook into this process.
        post_creation.send(sender=self, site_name=site_name)

        return redirect
