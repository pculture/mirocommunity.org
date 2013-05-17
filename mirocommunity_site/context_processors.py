from django.conf import settings


def analytics(request):
    return {
        'GOOGLE_ANALYTICS_UA': getattr(settings,
                                       'GOOGLE_ANALYTICS_UA',
                                       ''),
        'GOOGLE_ANALYTICS_DOMAIN': getattr(settings,
                                           'GOOGLE_ANALYTICS_DOMAIN',
                                           ''),
    }
