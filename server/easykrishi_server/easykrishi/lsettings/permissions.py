from rest_framework import permissions
from django.contrib.auth.models import Group,User
from django.core.exceptions import ImproperlyConfigured
import logging

import pdb

log = logging.getLogger('oauth2_provider')
class IsAuthenticatedOrCreate(permissions.IsAuthenticated):

	def has_permission(self, request, view):
		if request.method == 'POST':
			return True
		if request.method == 'GET':			
			return True
		if request.method == 'PUT':			
			return True
		return super(IsAuthenticatedOrCreate, self).has_permission(request, view)

def is_in_group(user, group_name):
	"""
	Takes a user and a group name, and returns `True` if the user is in that group.
	"""	
	return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()

class HasGroupPermission(permissions.BasePermission):
	"""
	Ensure user is in required groups.
	"""

	def has_permission(self, request, view):		
		
		if request.method in getattr(view, 'actions', {}):
			return True
		else:
			return False

		# # Get a mapping of methods -> required group.
		# required_groups_mapping = getattr(view, 'actions', {})

		# # Determine the required groups for this particular request method.
		# required_groups = required_groups_mapping.get(request.method, [])	
		
		# # Return True if the user has all the required groups		
		# return any([is_in_group(request.user, group_name) for group_name in required_groups])


class TokenHasScope(permissions.BasePermission):
	"""
	The request is authenticated as a user and the token used has the right scope
	"""

	def has_permission(self, request, view):
		
		token = request.auth
		if not token:
			return False		

		if hasattr(token, 'scope'):  # OAuth 2
			required_scopes = self.get_scopes(request, view)
			log.debug("Required scopes to access resource: {0}".format(required_scopes))

			return token.is_valid()

		assert False, ('TokenHasScope requires either the'
					   '`oauth2_provider.rest_framework.OAuth2Authentication` authentication '
					   'class to be used.')

	def get_scopes(self, request, view):		
		try:
			return getattr(view, 'required_scopes')
		except AttributeError:
			raise ImproperlyConfigured(
				'TokenHasScope requires the view to define the required_scopes attribute')