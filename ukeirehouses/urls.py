from django.conf.urls.defaults import *
#from ukeirehouses.views import RequestOfferFormPreview
#from ukeirehouses.models import PropertyOfferForm

urlpatterns = patterns('ukeirehouses.views',
                       (r'^$', 'index'),
                       (r'^offer-property/$', 'offer_property'),
                       (r'^add-property-action/$', 'add_property_action'),
                       (r'^search-offered-property/$', 'search_offered_property'),
                       (r'^request-property/$', 'request_property'),

                       (r'^request-property-action/$', 'request_property_action'),

                       (r'^offer-details/(?P<id>\d+)/$', 'offer_details'),

                       (r'^search-requested-property/$', 'search_requested_property'),
                       (r'^property-image/(?P<id>\d+)/(?P<index>\d+)/', 'get_property_full_image'),
                       (r'^property-thumb-image/(?P<id>\d+)/(?P<index>\d+)/', 'get_property_thumb_image'),

                       (r'^send-message/request/(?P<id>\d+)/', 'send_request_message'),
                       (r'^send-message/offer/(?P<id>\d+)/', 'send_offer_message'),
                       (r'^send-message-action/', 'send_message_action'),

                       (r'^lang/(?P<lang>.+)/', 'set_lang'),
                       
                       (r'legal-disclaimer/', 'legal_disclaimer'),
                       (r'private-policy/', 'private_policy'),
)
