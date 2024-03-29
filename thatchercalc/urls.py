from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^braced', views.braced, name='braced'),
    url(r'^cantilever', views.cantilever, name='cantilever'),
    url(r'^output', views.output, name='output'),
    url(r'^pressure_plot', views.pressure_plot, name='pressure_plot'),
    url(r'^surface', views.surface, name='surface'),
    url(r'^cant_output', views.cant_output, name='cant_output'),
    url(r'^multilayer', views.multilayer, name='multilayer'),
    url(r'^multi_output', views.multi_output, name='multi_output'),
    url(r'^strut_diagram', views.strut_diagram, name='strut_diagram'),
    url(r'^three_layer', views.three_layer, name='three_layer'),
    url(r'^three_output', views.three_output, name='three_output'),
    url(r'^micropile_joint_bending_capacity', views.micropile_joint_bending_capacity, name='micropile_joint_bending_capacity'),
    url(r'^micropile_output', views.micropile_output, name='micropile_output'),
    url(r'^one_layer_optimizer', views.one_layer_optimizer, name='one_layer_optimizer'),
    url(r'^optimizer_output', views.optimizer_output, name='optimizer_output'),
    url(r'^active_passive_plot', views.active_passive_plot, name='active_passive_plot'),
    url(r'^water_pressure_plot', views.water_pressure_plot, name='water_pressure_plot'),
    url(r'^cant_pp', views.cant_pp, name='cant_pp'),
    url(r'^loader', views.loader, name='loader')
]
