from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render, HttpResponse


def index(request):
    return render(request, 'index.html')
