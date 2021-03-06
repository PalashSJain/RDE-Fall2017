"""LibraryOfBooks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf import settings
from django.views.static import serve

from enduser import views

urlpatterns = [
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name="home"),
    url(r'book/(?P<book_id>[0-9]+)/page/(?P<page_number>[\-0-9]+)$', views.show_page, name="show_page"),
    url(r'changePageSize/(?P<book_id>[0-9]+)/(?P<new_page_size>(50|55|60|65|70|75))$', views.change_page_size),
]

handler404 = views.response_code_404
handler500 = views.response_code_500