from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import RawProblem
from .serializers import RawProblemSerializer

from server.permissions import OnlyCurator, OnlyNaturalPerson, NaturalOrCurator

from Notis.models import Noti
    
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
        }

        # Iterate over the dictionary and filter the queryset
        for param, field in and_filter_params.items():
            value = self.request.query_params.get(param, None)
            if value is not None:
                kwargs = {field: value}
                queryset = queryset.filter(**kwargs)

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
            self.permission_classes = [OnlyNaturalPerson]
        else:
            self.permission_classes = [NaturalOrCurator]
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
        if self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [OnlyNaturalPerson]
        if self.request.method in ['DELETE']:
            self.permission_classes = [OnlyCurator]
        else:
            self.permission_classes = [NaturalOrCurator]
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
