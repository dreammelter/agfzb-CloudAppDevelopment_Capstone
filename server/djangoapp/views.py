from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.generic.base import TemplateView
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# #
# Static Template Renderers
# #

# ...i can't believe it just needed... the namespace.
class AboutPageView(TemplateView):
    template_name = 'djangoapp/about.html'

class ContactPageView(TemplateView):
    template_name = 'djangoapp/contact.html'


# #
# Account Login and Registration
# #
def login_request(request):
    context = {} # useful for passing login feedback over
    # Login is a POST request (dictionary with key names from the form fields)
    if request.method == "POST":
        # Can get login details from the dictionary
        username = request.POST['usr']
        password = request.POST['psw']
        # Validate for existing creds
        user = authenticate(username=username, password=password)

        if user is not None:
            # Valid Login: log them in and redirect to home page
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # Invalid login: return failure message and point to full login page
            context['message'] = 'Invalid username or password.'
            return render(request, 'djangoapp/login.html', context)
    else:
        # whatever else it is, go to full login page
        context['message'] = 'Please login.'
        return render(request, 'djangoapp/login.html', context)

def logout_request(request):
    # Log to console for ref - get user obj from request
    print("Logout user `{}`".format(request.user.username))
    # logout using builtin method + redirect to index
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

