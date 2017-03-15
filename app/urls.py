from django.conf.urls import url
from app import views

app_name = 'app'

urlpatterns = [

    # /app/
    url(r'^$', views.index, name = 'index'),

    # /app/<topic_id>/
    url(r'^(?P<topic_id>[0-9]+)/', views.detail, name = 'detail'),

    # /app/create_topic/
    url(r'^create_topic/$', views.create_topic, name = 'create_topic'),

    # /app/<topic_id>/add_requirement/<topic_id>
    url(r'^add_requirement/(?P<to_topic_id>[0-9]+)/(?P<from_topic_id>[0-9]+)/$', views.add_requirement, name = 'add_requirement'),

    # /app/delete_topic/
    url(r'^delete_topic/(?P<topic_id>[0-9]+)/$', views.delete_topic, name = 'delete_topic'),

    # /app/<topic_id>/edit_topic/
    url(r'^edit_topic/(?P<topic_id>[0-9]+)/$', views.edit_topic, name = 'edit_topic'),

    # /app/graph/
    url(r'^graph/$', views.graph, name = 'graph'),

    # /app/api/get_topics_as_json/
    url(r'^graph/api/get_topics_as_json/$', views.get_topics_as_json, name = 'get_topics_as_json'),

]
