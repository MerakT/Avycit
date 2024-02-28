from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import RawProblem, CleanProblem
from .serializers import RawProblemSerializer, CleanProblemSerializer


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
        if getattr(self.request.user, 'role', None) == 'admin':
            return self.queryset
        return self.queryset.filter(applicant=self.request.user)

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
    
class CleanProblemDetail(ProblemDetail):
    queryset = CleanProblem.objects.all()
    serializer_class = CleanProblemSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [permissions.IsAuthenticated, OnlyAdmin]
        else:
            self.permission_classes = [permissions.IsAuthenticated, IsTesistaOrIsAdmin]
        return super(CleanProblemDetail, self).get_permissions()
