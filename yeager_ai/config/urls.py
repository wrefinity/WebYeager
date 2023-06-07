from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    #login redirect
    path("", include("yeager_ai.login_redirect.urls")),
    
    # errors
    path('403', TemplateView.as_view(template_name='403.html'), name='403'),
    path('500', TemplateView.as_view(template_name='500.html'), name='500'),
    
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("yeager_ai.users.urls", namespace="users")),
    # User' Profiles management
    path("profiles/", include("yeager_ai.user_profile.urls", namespace="users_profiles")),

    # Referrals
    path("referrals/", include("yeager_ai.referal.urls")),
    # account authentications
    path("accounts/", include("allauth.urls")),
    # payment route
    path("payment/", include("yeager_ai.payment.urls")),
    # payment route
    path("agents/", include("yeager_ai.agent.urls")),
    
    # world path
    path("worlds/", include("yeager_ai.world.urls")),
    # stripe path
    path("stripe/", include("djstripe.urls", namespace="djstripe")),    
    # must be the last url, to avoid 404 error on other pages
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path('<path:path>', TemplateView.as_view(template_name='404.html'), name='404'),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
