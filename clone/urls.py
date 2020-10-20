from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import PostListView,PostCreateView,PostUpdateView
urlpatterns=[
    url(r'^$',PostListView.as_view(),name='home'),
    url(r'^post/new/$', PostCreateView.as_view(), name='post-create'),
    url(r'^post/<int:pk>/update$', PostUpdateView.as_view(), name='post-update'),
    url(r'^signout/$', views.signout, name='signout'),
    url(r'^comment/(?P<post_id>\d+)', views.add_comment, name='comment'),
    url(r'^prof/(?P<username>[-_\w.]+)/$', views.profile, name='prof'),
    url(r'^profile/(?P<username>[-_\w.]+)/followers/$', views.followers, name='followers'),
    url(r'^profile/(?P<username>[-_\w.]+)/following/$', views.following, name='following'),
    url(r'^profile/(?P<username>[-_\w.]+)/$', views.profile, name='profile'),
    url(r'^post/(?P<pk>\d+)/$', views.post, name='post'),
    url(r'^profile/(?P<username>[-_\w.]+)/edit/$', views.profile_settings, name='profile_settings'),
    url(r'^search/',views.search_results, name='search_results'),

    url(r'^post/(?P<pk>\d+)/likes/$', views.likes, name='likes'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
