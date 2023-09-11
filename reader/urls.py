from django.template.defaulttags import url

from reader.views import Article

urlpatterns = [
    url("(.+)", Article.as_view(), name="article"),
]
