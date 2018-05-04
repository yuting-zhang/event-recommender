from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from django.template import loader
from django.core.files import File
from django.core.files.storage import default_storage, FileSystemStorage
from django.core.files.base import ContentFile


from .models import TestClass

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'test1/index.html'
    context_object_name = 'test_context'

    def get_queryset(self):
    	x = TestClass()
    	x.set_values(1, 12.345, 'testing', False, '05 03 2018')
    	return [x]
