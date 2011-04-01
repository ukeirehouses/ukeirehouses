import datetime

from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms

#from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _

import djangotoolbox
from form_utils.forms import BetterModelForm

import logging

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)

    first_name = models.CharField(_('First Name'), max_length=200)
    last_name = models.CharField(_('Last Name'), max_length=200)
    address = models.CharField(_('Address'), max_length=200)
    tel = models.CharField(_('Tel'), max_length=200)

    @property
    def as_ul(self):
        html = "<ul>"
        html += "<li>" + self.first_name + "</li>"
        html += "<li>" + self.last_name + "</li>"
        html += "<li>" + self.tel + "</li>"
        html += "<li>" + self.address + "</li>"
        html += "</ul>"

        return html

class PropertyRequest(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(_('Title'), max_length=200)
    current_address = models.CharField(_('Current Address'), max_length=200)
    looking_address = models.CharField(_('Looking Address'), max_length=200)
    number_of_family_group = models.IntegerField(_('Number of family group'), default=0)
    number_of_people = models.IntegerField(_('Number of people'), default=0)
    has_male = models.BooleanField(_('Male'))
    has_female = models.BooleanField(_('Female'))
    has_baby = models.BooleanField(_('Baby'))
    has_child = models.BooleanField(_('Child'))
    has_student = models.BooleanField(_('Student'))
    has_aged = models.BooleanField(_('Aged'))
    has_family = models.BooleanField(_('Family'))
    has_pet = models.BooleanField(_('Pet'))
    description = models.TextField(_('Description'))
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super(PropertyRequest, self).__init__(*args, **kwargs)

        for name in self._meta.get_all_field_names():
            method_name = 'get_' + name + '_verbose_name'
            setattr(self, method_name, self.get_model_name(name))
        
    def get_model_name(self, field_name):
        return self._meta.get_field_by_name(field_name)[0].verbose_name

class PropertyOffer(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(_('Title'), max_length=200, help_text='help text', default="")
    CLASSIFICATION_CHOICES = ((1, _("Indivisual")), (2, _("NPO")), (3, _("Governmental")), (4, _("Company")))
    classfication = models.IntegerField(_('Classification'), choices=CLASSIFICATION_CHOICES)
    ROOM_TYPE_CHOICES = ((1, _("Shared Room")), (2, _("Private Room")), (3, _("Entire Home")))
    room_type = models.IntegerField(_('Room Type'), choices=ROOM_TYPE_CHOICES)
    PROPERTY_TYPE_CHOICES = ((1, _("Apartment")), (2, _("House")), (3, _("Hotel")), (4, "Dorm"))
    property_type = models.IntegerField(_('Room Type'), choices=PROPERTY_TYPE_CHOICES)
    maximum_number_of_people_stay = models.IntegerField(_('Maximum people can stay'))
    maximum_number_of_family_group = models.IntegerField(_('Maximum family can stay'))
    possible_move_in_date = models.DateField(_('Possible move in date'), default=datetime.datetime.today().strftime("%Y/%m/%d"))
    maximum_days_stay = models.IntegerField(_('Maxmum days can stay'), default=365)
    price_per_day = models.FloatField(_('Price per Day'), default=0)
    stayable_person_male = models.BooleanField(_('Male Stayable'), default=True)
    stayable_person_female = models.BooleanField(_('Female Stayable'), default=True)
    stayable_person_baby = models.BooleanField(_('Baby Stayable'), default=True)
    stayable_person_child = models.BooleanField(_('Child Stayable'), default=True)
    stayable_person_student = models.BooleanField(_('Student Stayable'), default=True)
    stayable_person_aged = models.BooleanField(_('Aged Stayable'), default=True)
    stayable_person_family = models.BooleanField(_('Family Stayable'), default=True)
    stayable_person_pet = models.BooleanField(_('With Pet Stayable'), default=True)
    FACIRITY_TYPE_CHOICES = ((1, _("Available")), (2, _("Shared")), (3, _("Not Available")))
    FACIRITY_TYPE_CHOICES2 = ((1, _("Available")), (2, _("Not Available")))
    facility_toilet = models.IntegerField(_('Toilet'), choices=FACIRITY_TYPE_CHOICES, blank=True, null=True)
    facility_bath = models.IntegerField(_('Bath'), choices=FACIRITY_TYPE_CHOICES, blank=True, null=True)
    facility_airconditioning = models.IntegerField(_('Air-conditioning'), choices=FACIRITY_TYPE_CHOICES2, blank=True, null=True)
    facility_parking = models.IntegerField(_('Parking'), choices=FACIRITY_TYPE_CHOICES2, blank=True, null=True)
    facility_kitchen = models.IntegerField(_('Kitchen'), choices=FACIRITY_TYPE_CHOICES2, blank=True, null=True)
    facility_sleeping_gear = models.IntegerField(_('Sleeping Gear'), choices=FACIRITY_TYPE_CHOICES2, blank=True, null=True)

    details = models.TextField(_('Details'), default='')
    zipcode = models.CharField(_('Zipcode'), max_length=15, default='')
    address = models.CharField(_('Address'), max_length=200, default='')
    location = models.CharField(_('Location'), max_length=100, blank=True)

    url = models.CharField(max_length=200, blank=True)
    STATUS_CHOICES = ((1, _("Vacancy")), (2, _("Talking")), (3, _("Decited")), (4, _("Canceled")))
    status = models.IntegerField(_('Status'), choices=STATUS_CHOICES, default=1)
    image1 = djangotoolbox.fields.BlobField(_('Image1'), blank=True)
    image2 = djangotoolbox.fields.BlobField(_('Image2'), blank=True)
    image3 = djangotoolbox.fields.BlobField(_('Image3'), blank=True)
    image4 = djangotoolbox.fields.BlobField(_('Image4'), blank=True)
    image5 = djangotoolbox.fields.BlobField(_('Image5'), blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super(PropertyOffer, self).__init__(*args, **kwargs)

        for name in self._meta.get_all_field_names():
            method_name = 'get_' + name + '_verbose_name'
            setattr(self, method_name, self.get_model_name(name))
        
    def get_model_name(self, field_name):
        return self._meta.get_field_by_name(field_name)[0].verbose_name

    @classmethod
    def search(self, place, classfication, room_type, property_type, max_people, max_family, move_in_date, max_days, male, female, baby, child, student,aged, family, pet):
        offers = self.objects.all()
        if classfication:
            offers = offers.filter(classfication = classfication)
        if room_type:
            offers = offers.filter(room_type = room_type)
        if property_type:
            offers = offers.filter(property_type = property_type)
        if max_people:
            offers = offers.filter(maximum_number_of_people_stay = max_people)
        if max_family:
            offers = offers.filter(maximum_number_of_family_group = max_family)
#        if move_in_date:
#            offers = offers.filter(possible_move_in_date = move_in_date)
        if max_days:
            offers = offers.filter(maximum_days_stay = max_days)
        if male:
            offers = offers.filter(stayable_person_male = male)
        if female:
            offers = offers.filter(stayable_person_female = female)
        if baby:
            offers = offers.filter(stayable_person_baby = baby)
        if child:
            offers = offers.filter(stayable_person_child = child)
        if student:
            offers = offers.filter(stayable_person_student = student)
        if aged:
            offers = offers.filter(stayable_person_aged = aged)
        if family:
            offers = offers.filter(stayable_person_family = family)
        if pet:
            offers = offers.filter(stayable_person_pet = pet)

        return offers
        

#Model Forms

#class PropertyOfferForm(ModelForm):
class PropertyOfferForm(BetterModelForm):
    possible_move_in_date = forms.DateField(('%Y/%m/%d',), required=False, label=_('Possible move in date'),
        widget=forms.DateTimeInput(format='%Y/%m/%d', attrs={}),
        initial=datetime.datetime.today()
    )
#    logging.info(datetime.datetime.today().strftime("%Y/%m/%d"))
    class Meta:
        model = PropertyOffer
        fieldsets = [(_('main'), {'fields': ['title', 'details', 'classfication', 'room_type', 'property_type', 'maximum_number_of_people_stay', 'maximum_number_of_family_group', 'possible_move_in_date', 'maximum_days_stay', 'price_per_day', 'status']}),
                     (_('stayable'), {'fields': ['stayable_person_male', 'stayable_person_female', 'stayable_person_baby', 'stayable_person_child', 'stayable_person_student', 'stayable_person_aged', 'stayable_person_family', 'stayable_person_pet']}),
                     (_('facility'), {'fields': ['facility_toilet', 'facility_bath', 'facility_airconditioning', 'facility_parking', 'facility_kitchen', 'facility_sleeping_gear']}),
                     (_('images'), {'fields': ['image1', 'image2', 'image3', 'image4', 'image5']}),
                     (_('location'), {'fields': ['zipcode', 'address', 'url', 'location']}),
                     ]
        row_attrs = {'location': {'style': 'display: none'}}




class PropertyRequestForm(BetterModelForm):
    class Meta:
        model = PropertyRequest
        fieldsets = [(_('main'), {'fields':['title', 'description']}),
                     (_('address'), {'fields':['current_address', 'looking_address']}),
                     (_('our details'), {'fields':['number_of_family_group', 'number_of_people', 'has_male', 'has_female', 'has_baby', 'has_child', 'has_student', 'has_aged', 'has_family', 'has_pet']}),
                     ]
