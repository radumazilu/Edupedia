# This file stores our representations of objects which will be stored in our database.

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse

class Topic(models.Model):
    user = models.ForeignKey(User, default=1)
    title = models.CharField(max_length=200, blank=False, null=False)
    content = models.TextField(default="Please add your content here")
    modified_content = models.TextField(default="Please add your content here")

    requirement_for = models.ForeignKey('self',
                                        related_name='is_requirement_for',
                                        null=True,
                                        blank=True,
                                        on_delete=models.CASCADE)

    main_requirement = models.ForeignKey('self',
                                         related_name='has_main_requirement',
                                         null=True,
                                         blank=True,
                                         on_delete=models.CASCADE)

    requirements = models.ManyToManyField('self',
                                          through='Requirement_Relation',
                                          blank=True,
                                          symmetrical=False,
                                          related_name='related_topic+')

    is_basic = models.BooleanField(default=False)
    is_first = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Requirement_Relation(models.Model):
    # ?! you might need to use these the other way around
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, related_name='for_topic')
    requirement = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, related_name='from_topic')

    class Meta:
        unique_together = ('topic', 'requirement')
