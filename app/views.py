# All of our views will live here, which are mapped to URLs.

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
import datetime
from .models import Topic, Requirement_Relation
from .forms import TopicForm
from django.core import serializers


def index(request):
    print "Hello"
    nav_bar = 'app/base_visitor.html'
    topics = Topic.objects.all()
    return render(request, 'app/index.html', {'topics': topics, 'nav_bar': nav_bar})

def detail(request, topic_id):
    topics = Topic.objects.all()
    user = request.user
    topic = get_object_or_404(Topic, pk=topic_id)
    return render(request, 'app/detail.html', {'topic': topic, 'topics': topics, 'user': user})

def change_requirements(topic):
    # if this is a requirement for something, put it into the main_requirement of that
    if topic.requirement_for:

        Topic.objects.filter(pk=topic.requirement_for.id).update(main_requirement=topic)

        # While the upper topic is not first, add this topic in upper topic's requirements
        up_topic = topic
        while up_topic.is_first == False:
            rel = Requirement_Relation(topic=up_topic.requirement_for, requirement=topic)
            rel.save()
            up_topic = up_topic.requirement_for

    # if this has a main_requirement, put it into the requirement_for of that
    if topic.main_requirement:

        Topic.objects.filter(pk=topic.main_requirement.id).update(requirement_for=topic)

        # add the requirement in the requirements of the topic
        rel = Requirement_Relation(topic=topic, requirement=topic.main_requirement)
        rel.save()

def create_topic(request):
    # if not request.user.is_authenticated():
    #     return render(request, 'app/login.html')
    # else:
    form = TopicForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        topic = form.save(commit=False)
        topic.user = request.user
        topic.save()

        change_requirements(topic)

        return render(request, 'app/detail.html', {'topic': topic, 'topic_id': topic.pk})

    context = {
        "form": form,
    }
    return render(request, 'app/create_topic.html', context)

def add_requirement(request, to_topic_id, from_topic_id):
    user = request.user
    nav_bar = 'app/base_visitor.html'
    topics = Topic.objects.all()

    to_topic = get_object_or_404(Topic, pk=to_topic_id)
    from_topic = get_object_or_404(Topic, pk=from_topic_id)

    if Requirement_Relation.objects.filter(requirement=from_topic, topic=to_topic):
        error_message = "Requirement already exists."
        return render(request, 'app/detail.html', {'topic': to_topic, 'topics': topics, 'user': user, 'error_message': error_message})

    relation = Requirement_Relation(topic=to_topic, requirement=from_topic)
    relation.save()

    return render(request, 'app/detail.html', {'topic': to_topic, 'topics': topics, 'user': user})

def delete_topic(request, topic_id):
    nav_bar = "app/base_visitor.html"
    topic = Topic.objects.get(pk=topic_id)

    # Update the topics above and below the topic you want to delete
    Topic.objects.filter(main_requirement=topic).update(main_requirement=topic.main_requirement)
    Topic.objects.filter(requirement_for=topic).update(requirement_for=topic.requirement_for)

    # Set main_requirement and requirement_for to null, to avoid deleting multiple objects
    Topic.objects.filter(pk=topic_id).update(main_requirement=None, requirement_for=None)

    # Delete the relationships this object has to any other
    Requirement_Relation.objects.filter(topic=topic).delete() # Check if this works!
    Requirement_Relation.objects.filter(requirement=topic).delete() # Check if this works!

    topic.delete()
    topics = Topic.objects.filter(user=request.user)
    return render(request, 'app/index.html', {'topics': topics, 'nav_bar': nav_bar})

def edit_topic(request, topic_id):
    user = request.user
    topics = Topic.objects.all()
    topic = get_object_or_404(Topic, pk=topic_id)
    form = TopicForm(request.POST or None, instance=topic)

    if form.is_valid():
        topic = form.save(commit=False)
        topic.user = request.user
        topic.save()
        form.save_m2m()
        # change_requirements(topic)
        return render(request, 'app/detail.html', {'topic': topic, 'topics': topics, 'user': user})
        return HttpResponse('Topic was edited')

    context = {
        "form": form
    }
    return render(request, 'app/edit_topic.html', context)

def graph(request):
    nav_bar = 'app/base_visitor.html'
    return render(request, 'app/graph.html', {'nav_bar': nav_bar})

def get_topics_as_json(request):
    data = serializers.serialize('json', Topic.objects.all().order_by('id'))
    return HttpResponse(JsonResponse(data, safe=False), content_type="application/json")
