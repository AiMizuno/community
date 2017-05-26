"""community URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Control import views as control_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', control_views.welcome, name="welcome"),
    url(r'^logout/$', control_views.logout, name='logout'),
    url(r'^register/$', control_views.register, name="register"),

    url(r'^home/info/$', control_views.selfinfo, name="self_info"),
    url(r'^home/user/$', control_views.get_user, name="get_user"),
    url(r'^home/message/$', control_views.get_message, name="get_message"),
    url(r'^home/activity/$', control_views.get_activity, name="get_activity"),
    url(r'^home/community/$', control_views.get_community, name="get_community"),
    url(r'^home/$', control_views.home, name="home"),

    url(r'^homepage/(?P<Community_name>\w+)/$', control_views.Communityhomepage, name="homepage"),
    url(r'^console/(?P<Community_name>\w+)/$', control_views.Community_console, name="community_console"),
    url(r'^console/activity/(?P<Community_name>\w+)/$', control_views.Community_activity, name="community_activity"),
    url(r'^console/article/(?P<Community_name>\w+)/$', control_views.Community_blog, name="community_blog"),
    url(r'^console/short_article/(?P<Community_name>\w+)/$', control_views.Community_twit, name="community_twit"),
    url(r'^console/member/(?P<Community_name>\w+)/$', control_views.Community_member, name="community_member"),

    #租户界面
    url(r'tenant/$', control_views.Tenant_welcome, name="tenant_welcome"),
    url(r'^tenant/overview/(?P<Community_name>\w+)/$', control_views.Tenant_home, name="tenant_overview"),
    url(r'^tenant/feature/(?P<Community_name>\w+)/$', control_views.Tenant_feature, name="tenant_feature"),
]
