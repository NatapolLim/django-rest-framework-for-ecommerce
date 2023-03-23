
from rest_framework import viewsets, mixins
from .models import Profile
from .serializers import ProfileSerializer, UserSerializer
from .permissions import IsOwnUser, IsOwnProfile
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsOwnUser,
        ]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return None
        
        queryset = super(UserViewSet, self).get_queryset()
        # user_profile = self.request.user.profile
        # update_queryset = queryset.filter(profile=user_profile)
        return queryset

class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsOwnProfile,
        ]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return None

        queryset = super(ProfileViewSet, self).get_queryset()
        # user = self.request.user
        # update_queryset = queryset.filter(user=user)
        return queryset