from rest_framework import permissions

class SendOwnMessages(permissions.BasePermission):
    """Allow users to only send messages as themself"""

    def has_object_permissions(self, request, view, obj):
        """Check the user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True
        else: 
            return obj.user_profile.id == request.user.id