# from rest_framework import permissions

class SendOwnEntries(permissions.BasePermission):
    """Allow users to only send messages as themself"""

    def has_object_permissions(self, request, view, obj):
        """Check the user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            # Won't the request.user.id always be that of
            # AnonymousUser until auth is set up correctly?
            return obj.author.id == request.user.id