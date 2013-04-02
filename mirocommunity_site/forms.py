from __future__ import with_statement
import os

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from mirocommunity_hosting.projects import Project
from mirocommunity_saas.models import Tier


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
            self._project_name(site_name))):
            raise forms.ValidationError('A site already exists with that name.')
        return site_name

    def _project_name(self, site_name):
        return site_name.replace('-', '_') + '_project'

    def save(self):
        site_name = self.cleaned_data['site_name']
        project_name = self._project_name(site_name)
        namespace = getattr(settings, 'MC_NAMESPACE', None)
        domain = "{site_name}.{namespace}{dot}mirocommunity.org".format(
                 site_name=site_name, namespace=namespace,
                 dot='.' if namespace else '')
        project = Project.create(project_name, domain,
                                 'project_base_1_10_project',
                                 settings.SITE_CREATION_ROOT,
                                 settings.SYMLINK_ROOT)

        output = project.manage('initialize', site_name, domain,
                                '--username=' + self.cleaned_data['username'],
                                '--email=' + self.cleaned_data['email'],
                                '--password=' + self.cleaned_data['password1'],
                                '--tier=' + self.cleaned_data['tier'].slug)
        redirect = output.rsplit('\n', 1)[-1]

        return redirect
