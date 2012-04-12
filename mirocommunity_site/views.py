from __future__ import with_statement

from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from django.views.generic import FormView

from mirocommunity_site.forms import NAME_TO_COST, SiteCreationForm
from mirocommunity_site.utils.shell import check_output


class SiteCreationView(FormView):
    form_class = SiteCreationForm

    def form_valid(self, form):
        form.save()

        # If that worked, then find out what URL to redirect to.
        with form._log_file() as out:
            target_url = check_output(
                [settings.PROJECT_REDIRECT_SCRIPT,
                 form.cleaned_data['url']],
                stderr=out,
                env={
                    'DJANGO_SETTINGS_MODULE':
                        form.cleaned_data['url'] + '_project.settings',
                    'NEW_TIER_NAME': form.cleaned_data['tier_name'],
                    'NEW_USERNAME': form.cleaned_data['username'],
                    'NEW_PASSWORD': form.cleaned_data['password1'],
                    'NEW_EMAIL': form.cleaned_data['email']}).strip()

        return HttpResponseRedirect(target_url)

    def dispatch(self, request, *args, **kwargs):
        #if not (getattr(settings, 'PROJECT_ROOT', None) and
        #        getattr(settings, 'PROJECT_SCRIPT', None) and
        #        getattr(settings, 'PROJECT_REDIRECT_SCRIPT', None)):
        #    raise Http404
        kwargs['tier_name'] = kwargs.get('tier_name', 'basic')
        if not kwargs['tier_name'] in NAME_TO_COST:
            raise Http404("Unknown tier.")
        return super(SiteCreationView, self).dispatch(request, *args, **kwargs)
