from django.conf.urls import url,include
from .import views


urlpatterns = [
 # url(r'^CM-Tickets/$',views.jira_detailed_view, name='CM-Tickets'),
 url(r'^CM-Tickets$',views.jira_detailed_view, name='CM-Tickets'),
 url(r'^IP-PD-Tickets/$',views.IP_PD_Tickets, name='IP-PD-Tickets'),
 url(r'^Optical-Tickets/$',views.OP_PD_Tickets, name='Optical-Tickets'),
 url(r'^signup/$',views.signup, name='signup'),
 url(r'^$',views.home, name='home'),
 # url(r'^login/$',views.login, name='login'),
 url('accounts/', include('django.contrib.auth.urls')),
 # url(r'^$',views.home, name='Home')
]
