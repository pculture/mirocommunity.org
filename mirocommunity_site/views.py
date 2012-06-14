from __future__ import with_statement

from django.http import HttpResponseRedirect
from django.views.generic import FormView, TemplateView
from mirocommunity_saas.models import Tier

from mirocommunity_site.forms import SiteCreationForm


class SiteCreationView(FormView):
    form_class = SiteCreationForm

    def get_initial(self):
        initial = super(SiteCreationView, self).get_initial()
        try:
            tier = Tier.objects.get(slug=self.request.GET.get('tier'))
        except Tier.DoesNotExist:
            pass
        else:
            initial.update({'tier': tier})
        return initial

    def form_valid(self, form):
        target_url = form.save()
        return HttpResponseRedirect(target_url)

    #def dispatch(self, request, *args, **kwargs):
    #    if not getattr(settings, 'SITE_CREATION_ROOT', None):
    #        raise Http404
    #    return super(SiteCreationView, self).dispatch(request, *args, **kwargs)


class PricingView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(PricingView, self).get_context_data(**kwargs)
        context['tiers'] = Tier.objects.filter(slug__in=['basic',
                                                         'plus',
                                                         'premium',
                                                         'max']
                                      ).order_by('price')
        return context
