from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from django.template import loader

from .models import Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        x = Question()
        x.id = 34
        x.question_text = 'Does this work?'
        y = Question()
        y.id = 99
        y.question_text = 'Yes it does'
        rando_list = [x, y]
        return rando_list


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

"""
def index(response):
    template = loader.get_template('polls/index.html')
    x = Question()
    x.id = 34
    x.question_text = 'Does this work?'
    y = Question()
    y.id = 99
    y.question_text = 'Yes it does'
    rando_list = [x, y]
    context = { 'latest_question_list': rando_list }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)
    """

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
