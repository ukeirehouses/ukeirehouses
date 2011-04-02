from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect
from django.utils.translation import activate
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.contrib.formtools.preview import FormPreview

from google.appengine.ext import db

from ukeirehouses.models import PropertyOffer, PropertyRequest, Message
from ukeirehouses.models import PropertyOfferForm, PropertyRequestForm

from google.appengine.api import images
from django.core.mail import send_mail
from django.contrib.auth.models import User

import logging


def index(request):
    offers_count = PropertyOffer.objects.count()
    offers = PropertyOffer.objects.all().order_by('-created_date')[:10]

    requests_count = PropertyRequest.objects.count()
    return direct_to_template(request, 'ukeirehouses/index.html', {'offers_count':offers_count, 'requests_count':requests_count, 'offers': offers})

@login_required
def offer_property(request):
    form = PropertyOfferForm()
    return direct_to_template(request, 'ukeirehouses/add-property.html', {'form':form})

def offer_property_confirm(request):
    form = PropertyOfferForm(request.POST)

def offer_details(request, id):
    offer = PropertyOffer.objects.get(id=id)
    return direct_to_template(request, 'ukeirehouses/offer-details.html', {'offer':offer})
    
@login_required
def add_property_action(request):
    f = PropertyOfferForm(request.POST, request.FILES)

    if f.is_valid():
        newoffer = f.save(commit=False)
        if request.user.is_authenticated():
            newoffer.user = request.user

        newoffer.save()
        
        return redirect('/')

    return direct_to_template(request, 'ukeirehouses/add-property.html', {'form':f})

def search_offered_property(request):
    if request.method == 'POST':
        place = request.POST['place']
        classfication = request.POST['classfication']
        room_type = request.POST['room_type']
        property_type = request.POST['property_type']
        maximum_number_of_people_stay = request.POST['maximum_number_of_people_stay']
        maximum_number_of_family_group = request.POST['maximum_number_of_family_group']
        possible_move_in_date = request.POST['possible_move_in_date']
        maximum_days_stay = request.POST['maximum_days_stay']
        stayable_person_male = request.POST['stayable_person_male']
        stayable_person_female = request.POST['stayable_person_female']
        stayable_person_baby = request.POST['stayable_person_baby']
        stayable_person_child = request.POST['stayable_person_child']
        stayable_person_student = request.POST['stayable_person_student']
        stayable_person_aged = request.POST['stayable_person_aged']
        stayable_person_family = request.POST['stayable_person_family']
        stayable_person_pet = request.POST['stayable_person_pet']

        offers = PropertyOffer.search(place, classfication, room_type, property_type, maximum_number_of_people_stay, maximum_number_of_family_group, possible_move_in_date, maximum_days_stay, stayable_person_male, stayable_person_female, stayable_person_baby, stayable_person_child, stayable_person_student, stayable_person_aged, stayable_person_family, stayable_person_pet)

    else:
        offers = PropertyOffer.objects.all()

    form = PropertyOfferForm()

    offers.order_by('-created_date')[:10]

    return direct_to_template(request, 'ukeirehouses/search-offered-property.html', {'offers':offers, 'form':form})

@login_required
def request_property(request):
    form = PropertyRequestForm()
    return direct_to_template(request, 'ukeirehouses/request-property.html', {'form':form})

@login_required
def request_property_action(request):
    f = PropertyRequestForm(request.POST)
    if f.is_valid():
        f.save()
        return redirect('/')

def search_requested_property(request):
    requests = PropertyRequest.objects.all().order_by('-created_date')[:10]
    return direct_to_template(request, 'ukeirehouses/search-request-property.html', {'requests':requests})

# message

def send_request_message(request, id):
    offer = PropertyOffer.objects.get(id=id)
    return direct_to_template(request, 'ukeirehouses/send-request-message.html', {'id':id})

    
def send_offer_message(request, id):
    request = PropertyRequest.objects.get(id=id)
    return direct_to_template(request, 'ukeirehouses/send-request-message.html', {'id':id})

def send_message_action(request):
    id = request.POST['id']
    message = request.POST['message']

    offer = PropertyOffer.objects.get(id=id)

    new_message = Message()
    new_message.from_user = request.user
    new_message.to_user = offer.user
    new_message.message = message

    new_message.save()

    offer.user.email_user('Subject', message)

    return redirect('/sent-message/')

def sent_message(request):    
    return direct_to_template(request, 'ukeirehouses/sent-message.html')

# util

def set_lang(request, lang):
    activate(lang)
    return redirect('/')

# image

def get_property_full_image(request, id, index):
    return get_property_image(request, id, index, False)

def get_property_thumb_image(request, id, index):
    return get_property_image(request, id, index, True)

def get_property_image(request, id, index, thumb):
    property_offer = PropertyOffer.objects.get(id=id)
    image = None
    index = int(index)

    logging.info(index)

    if property_offer:
        if index == 1:
            image = property_offer.image1
        elif index == 2:
            image = property_offer.image2
        elif index == 3:
            image = property_offer.image3
        elif index == 4:
            image = property_offer.image4
        elif index == 5:
            image = property_offer.image5

    if image != None:
        if thumb:
            image = images.resize(image, 100) #, output_encoding=images.JPEG)
        response = HttpResponse(image)
        response['Content-Type'] = 'image/jpeg'
    else:
        return HttpResponseRedirect("/static/image_not_found.png")

    return response

#static

def legal_disclaimer(request):
    return direct_to_template(request, 'ukeirehouses/legal-disclaimer.html', {})

def private_policy(request):
    return direct_to_template(request, 'ukeirehouses/private-policy.html', {})
