#----------------------import packages---------------------------------------#
#from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from easykrishi.lsettings.main_pagination import PageNumberPagination
#from rest_framework.pagination import PageNumberPagination
from oauth2_provider.models import Application,AccessToken,RefreshToken
#------------------------------------------------------------------------------#
from django.core.mail import send_mail,send_mass_mail,EmailMessage,EmailMultiAlternatives

from rest_framework import status
import ast
from django.conf import settings
import json
import random
import time
import uuid
from hashlib import sha1
import hmac
import requests
from django.http import HttpResponse,HttpResponseRedirect
from rest_framework.views import APIView

class LinkHeaderPagination(PageNumberPagination):
	def get_paginated_response(self, data):		
		return Response({
			   'next': self.get_next_link(),
			   'previous': self.get_previous_link(),
			'count': self.page.paginator.count,
			'results': data
		})


