from django.conf.urls import url
from .views import Register, IndexView, Logout

urlpatterns = [
    url(r'^register/$', Register.as_view(), name='register'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^logout/$', Logout.as_view(), name='logout')
]
