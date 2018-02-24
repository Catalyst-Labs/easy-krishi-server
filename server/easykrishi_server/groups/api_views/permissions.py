from rest_framework import permissions
from django.contrib.auth.models import Group,User
import pdb

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
		# Get a mapping of methods -> required group.
		required_groups_mapping = getattr(view, 'required_groups', {})

		# Determine the required groups for this particular request method.
		required_groups = required_groups_mapping.get(request.method, [])
		
		# Return True if the user has all the required groups.
		return any([is_in_group(request.user, group_name) for group_name in required_groups])