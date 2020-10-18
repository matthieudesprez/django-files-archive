# -*- coding: utf-8 -*-
from django.conf.urls import url

from django_files_archive.components import archive

app_name = "django_files_archive"
urlpatterns = [
    url(r'^test_archive/$', archive.test_archive, name="test_archive"),
    url(r'^archive/$', archive.post_zip_and_serve, name="post_zip_and_serve"),
]
