from rest_framework import permissions

# Create your rest permissions here.


class CustomPostPermission(permissions.IsAuthenticatedOrReadOnly):
    """ Object-level permission to allow like, dislike to anonymous users,
        read only for authenticated users,
        and only allow owners of a post to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Allow POST for likes and dislikes,
        uri = request._request.build_absolute_uri()
        rating = uri.endswith('/like/') or uri.endswith('/dislike/')
        post = request.method == 'POST'
        owner = obj.user == request.user
        if post and rating and not owner:
            return True
        # Deny users to liking/disliking their own posts
        if post and rating and owner:
            return False

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS \
           and request.user.is_authenticated:
            return True

        # Authenticated user must mach instance user to edit
        if owner:
            return True
