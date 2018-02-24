from django.db import models
from groups.models import Productbuyingdetails,Productsellingdetails
# Create your models here.

class OrderedProducts(Productbuyingdetails):
	"""		
	"""
	class Meta:
		proxy=True

class SellProducts(Productsellingdetails):
	"""		
	"""
	class Meta:
		proxy=True
