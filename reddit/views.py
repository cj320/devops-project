from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.
class GetUsers(TemplateView):
    template_name = 'reddit_home.html'
    def get_context_data(self, *args, **kwargs):
        pass



