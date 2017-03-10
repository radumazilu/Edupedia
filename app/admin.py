# This file allows us to register our models to view on the Django Admin Site.

from django.contrib import admin
from models import Topic, Requirement_Relation

admin.site.register(Topic)
admin.site.register(Requirement_Relation)
