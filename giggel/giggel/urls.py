"""giggel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from main import views as main_views
from user import views as user_views
from artist import views as artist_views
from venue import views as venue_views
from gig import views as gig_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.home, name='home'),
    path('new', main_views.HomeNew.as_view(), name='home_new'),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', user_views.profile.as_view(), name='profile'),
    path('profile/update/<slug:pk>/', user_views.updateProfile.as_view(), name='updateProfile'),
    #artist
    path('artist/create', artist_views.ArtistCreate.as_view(), name='artist_create'),
    path('artist/detail/<slug:slug>/',
         artist_views.ArtistDetail.as_view(), name='artist_detail'),
    path('artist/update/<slug:slug>/',
         artist_views.ArtistUpdate.as_view(), name='artist_update'),
    path('artist/delete/<slug:slug>/', artist_views.ArtistDelete.as_view(), name='artist_delete'),
    path('artist/dashboard', artist_views.ArtistDashboard.as_view(),
         name='artist_dashboard'),
    path('profile/artven', user_views.ArtVenCreate.as_view(), name='artven'),
    path('artist/directory', artist_views.ArtistDirectory.as_view(), name='artist_directory'),
    #venue
    path('venue/create', venue_views.VenueCreate.as_view(), name='venue_create'),
    path('venue/detail/<slug:slug>/',
         venue_views.VenueDetail.as_view(), name='venue_detail'),
    path('venue/update/<slug:slug>/',
         venue_views.VenueUpdate.as_view(), name='venue_update'),
    path('venue/delete/<slug:slug>/', venue_views.VenueDelete.as_view(), name='venue_delete'),
    path('venue/dashboard', venue_views.VenueDashboard.as_view(),
         name='venue_dashboard'),
    path('venue/directory', venue_views.VenueDirectory.as_view(), name='venue_directory'),
    #gigs
    path('gig/create', gig_views.GigCreate.as_view(), name='gig_create'),
    path('gig/detail/<slug:slug>/',
         gig_views.GigDetail.as_view(), name='gig_detail'),
    path('gig/update/<slug:slug>/',
         gig_views.GigUpdate.as_view(), name='gig_update'),
    path('gig/delete/<slug:slug>/', gig_views.GigDelete.as_view(), name='gig_delete'),
    path('gig/directory', gig_views.GigDirectory.as_view(), name='gig_directory'),
    path('my_gigs', gig_views.MyGigs.as_view(), name='my_gigs'),
    #gig_request
    path('gig_request_at_venue/create', gig_views.GigRequestAtVenueCreate.as_view(), name='gig_request_at_venue'),
    path('gig_request_to_artist/create', gig_views.GigRequestToArtistCreate.as_view(), name='gig_request_to_artist'),
    path('gig_request/detail/<slug:slug>/',
         gig_views.GigRequestDetail.as_view(), name='gig_request_detail'),
    path('gig_request/update/<slug:slug>/',
         gig_views.GigRequestUpdate.as_view(), name='gig_request_update'),
    path('gig_request/delete/<slug:slug>/', gig_views.GigRequestDelete.as_view(), name='gig_request_delete'),
    path('my_gig_requests', gig_views.MyGigRequests.as_view(), name='my_gig_requests'),
    path('my_gig_requests/confirm/<slug:slug>/', gig_views.GigRequestConfirm.as_view(), name='gig_request_confirm'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
