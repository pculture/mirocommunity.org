# Copyright 2009 - Participatory Culture Foundation
# 
# This file is part of Miro Community.
# 
# Miro Community is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
# 
# Miro Community is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with Miro Community.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls.defaults import url, patterns
from django.template import TemplateDoesNotExist
from django.views.generic import TemplateView
from django.http import Http404

from mirocommunity_site.views import (NAME_TO_COST, SiteCreationView)


urlpatterns = patterns("",
    url(r'^$',
        TemplateView.as_view(template_name='mirocommunity_site/index.html'),
        name='mirocommunity_site_index'),
    url(r'^create/?$',
        SiteCreationView.as_view(template_name='mirocommunity_site/create_site.html'),
        name='mirocommunity_site_create'),
    url(r'^pricing/?$',
        TemplateView.as_view(template_name='mirocommunity_site/pricing.html'),
        {'NAME_TO_COST': NAME_TO_COST},
        'mirocommunity_site_pricing'),

    url(r'^local-media/$',
        TemplateView.as_view(template_name='mirocommunity_site/local-media.html')),
    url(r'^features/$',
        TemplateView.as_view(template_name='mirocommunity_site/features.html')),
    url(r'^college/$',
        TemplateView.as_view(template_name='mirocommunity_site/college.html')),
    url(r'^enterprise/$',
        TemplateView.as_view(template_name='mirocommunity_site/enterprise.html')),
    url(r'^terms/$',
        TemplateView.as_view(template_name='mirocommunity_site/terms.html')),
    url(r'^about/$',
        TemplateView.as_view(template_name='mirocommunity_site/about.html')),
)
