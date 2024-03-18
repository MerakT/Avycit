from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import RawProblem, CleanProblem
from .serializers import RawProblemSerializer, CleanProblemSerializer

from django.db.models import Q

#---------------------------- PERMISSIONS ------------------------------
class IsTesistaOrIsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow only users with the role 'admin' and the creator to delete problems
        return request.user.role == 'admin' or request.user.role == "tesista"

class IsApplicantOrIsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow only users with the role 'admin' and the creator to delete problems
        return request.user.role == 'admin' or obj.applicant == request.user

class OnlyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow only users with the role 'admin' to create problems
        return request.user.role == 'admin'
    
class OnlyApplicant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow only the creator to delete problems
        return obj.applicant == request.user
    
#---------------------------- BASE ------------------------------
class ProblemList(ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Define a dictionary to map query parameters to model fields
        and_filter_params = {
            # For Raw Problems
            'title': 'title__icontains',
            'sector': 'sector',
            'institution_type': 'institution_type',
            'status': 'raw_status',
            'is_supported': 'is_supported',
            # For Clean Problems
            'clean_title': 'clean_title__icontains',
            'clean_sector': 'clean_sector',
            'economic_support': 'economic_support',
            'social_support': 'social_support',
            'enviromental_support': 'enviromental_support',
            'importancy': 'importancy'
        }

        or_filter_params = {
            'career_1': 'career_1',
            'career_2': 'career_2',
            'career_3': 'career_3',
        }

        # Iterate over the dictionary and filter the queryset
        for param, field in and_filter_params.items():
            value = self.request.query_params.get(param, None)
            if value is not None:
                kwargs = {field: value}
                queryset = queryset.filter(**kwargs)

        # Initialize an empty Q object
        q_object = Q()

        for param, field in or_filter_params.items():
            value = self.request.query_params.get(param, None)
            if value is not None:
                # Update the Q object for each OR filter
                q_object |= Q(**{field: value})

        # Apply the combined Q object to the queryset
        queryset = queryset.filter(q_object)

        return queryset

class ProblemDetail(RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj

#---------------------------- RAW PROBLEMS ------------------------------
class RawProblemList(ProblemList):
    queryset = RawProblem.objects.all()
    serializer_class = RawProblemSerializer

    def get_permissions(self):
        if self.request.method in ['POST']:
            self.permission_classes = [permissions.IsAuthenticated, OnlyApplicant]
        else:
            self.permission_classes = [permissions.IsAuthenticated, IsApplicantOrIsAdmin]
        return super(RawProblemList, self).get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()

        if getattr(self.request.user, 'role', None) != 'admin':
            queryset = queryset.filter(applicant=self.request.user)
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)
    
class RawProblemDetail(ProblemDetail):
    queryset = RawProblem.objects.all()
    serializer_class = RawProblemSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [permissions.IsAuthenticated, OnlyApplicant]
        else:
            self.permission_classes = [permissions.IsAuthenticated, IsApplicantOrIsAdmin]
        return super(RawProblemDetail, self).get_permissions()

    def update(self, request, *args, **kwargs):
        problem = self.get_object()
        if request.user != problem.applicant:
            return Response(status=403)
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        problem = self.get_object()
        if request.user != problem.applicant:
            return Response(status=403)
        return super().delete(request, *args, **kwargs)

#------------------------------------------- CLEAN PROBLEMS -------------------------------------------
class CleanProblemList(ProblemList):
    queryset = CleanProblem.objects.all()
    serializer_class = CleanProblemSerializer

    def get_permissions(self):
        if self.request.method in ['POST']:
            self.permission_classes = [permissions.IsAuthenticated, OnlyAdmin]
        else:
            self.permission_classes = [permissions.IsAuthenticated, IsTesistaOrIsAdmin]
        return super(CleanProblemList, self).get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
    
    def perform_create(self, serializer):
        if getattr(self.request.user, 'role', None) != 'admin':
            raise PermissionError("Only admins can create clean problems")
        serializer.save(applicant=self.request.user)
    
class CleanProblemDetail(ProblemDetail):
    queryset = CleanProblem.objects.all()
    serializer_class = CleanProblemSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [permissions.IsAuthenticated, OnlyAdmin]
        else:
            self.permission_classes = [permissions.IsAuthenticated, IsTesistaOrIsAdmin]
        return super(CleanProblemDetail, self).get_permissions()
