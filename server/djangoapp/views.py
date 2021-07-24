from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealer_by_state_from_cf, get_dealer_reviews_from_cf, get_dealers_from_cf
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
    logger.debug("Logout user `{}`".format(request.user.username))
    # logout using builtin method + redirect to index
    logout(request)
    return redirect('djangoapp:index')


def registration_request(request):
    context = {} # IDK what we're passing yet, if anything
    # Handle GET request -> send to sign up page
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    # Handle POST request -> register user w/ form info
    elif request.method == "POST":
        # Gather user info
        username = request.POST['usr']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']

        user_exist = False # for checking if they already exist
        try:
            User.objects.get(username=username)
            user_exist = True
        except: # user doesn't exist
            logger.debug("{} is a new user".format(username))

        # now determine what to do with this existence info
        if not user_exist:
            # Make a new User obj
            user = User.objects.create_user(username=username, first_name=first_name,
                last_name=last_name, password=password)
            # Log them in and go home
            login(request, user)
            return redirect('djangoapp:index')
        else: # User exists or something went wrong
            context['message'] = "Sign up for a new account or login above."
            return render(request, 'djangoapp/registration.html', context)

# #
# IBM CLOUD FUNCTION API INTERACTIONS
# #

# API URLS - all GET requests return JSON with "entries" key containing list of reviews
REVIEW_API_URL = "https://1984d932.us-south.apigw.appdomain.cloud/api/review" 
    # GET: get-dealer-review (requires param dealerId)
    # POST: save-review
DEALERSHIP_API_URL = "https://1984d932.us-south.apigw.appdomain.cloud/api/dealerships" 
    # GET: get-all-dealers
STATE_DEALERS_API_URL = "https://1984d932.us-south.apigw.appdomain.cloud/api/state-dealers"
    # GET: get-state-dealers (requires param state)


def get_dealerships(request):
    context = {}
    if request.method == "GET":
        # Runs the "get-all-dealers" Function
        url = DEALERSHIP_API_URL
        dealerships = get_dealers_from_cf(url) # should be a list of CarDealer objs.
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships]) # dot-access cuz it should be an object...
        
        context['dealers'] = dealer_names
        return render(request, 'djangoapp/index.html', context)


def get_state_dealers(request, state):
    context = {}
    if request.method == "GET":
        # Run get-state-dealers Function
        url = STATE_DEALERS_API_URL
        dealerships = get_dealer_by_state_from_cf(url, state=state)
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])

        context['dealers'] = dealer_names
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        # API link for the "get-dealer-reviews" Function handling GET requests
        # Requires dealerID as kwarg
        url = REVIEW_API_URL
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)

        #review_IDs = ' '.join([str(review.id) for review in reviews])
        # Verify we do have Review objects
        print(reviews[0].review) # print(reviews[0].review)
        context['reviews'] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

