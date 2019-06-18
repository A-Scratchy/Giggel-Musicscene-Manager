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
from django.urls import path, include
from main import views as main_views
from user import views as user_views
from artist import views as artist_views

urlpatterns = [
    path('blankPage/', main_views.blankPage, name='blankPage'),
    path('admin/', admin.site.urls),
    path('', main_views.home, name='home'),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', user_views.profile, name='profile'),
    path('profile/update', user_views.updateProfile, name='updateProfile'),
    path('artist/create', artist_views.ArtistCreate.as_view(), name='artist_create'),
    path('artist/detail/<slug:slug>/',
         artist_views.ArtistDetail.as_view(), name='artist_detail'),
    path('artist/update/<slug:slug>/',
         artist_views.ArtistUpdate.as_view(), name='artist_update'),
    path('artist/delete/<slug:slug>/', artist_views.ArtistDelte.as_view(), name='artist_delete'),
    path('artist/dashboard', artist_views.ArtistDashboard.as_view(),
         name='artist_dashboard'),
]
