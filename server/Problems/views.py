from rest_framework.response import Response
from rest_framework import authentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import RawProblem, CleanProblem
from .serializers import RawProblemSerializer, CleanProblemSerializer

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
            self.permission_classes = [NaturalOrCurator]
        if self.request.method in ['DELETE']:
            self.permission_classes = [OnlyCurator]
        else:
            self.permission_classes = [NaturalOrCurator]
        return super(RawProblemDetail, self).get_permissions()

    def update(self, request, *args, **kwargs):
        problem = self.get_object()
       # se quito esta funcion para la autenticacion de la funcion actualizada
       # if request.user != problem.applicant:
          #  return Response(status=403)
        ###
        serializer = self.get_serializer(problem, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Si se proporciona el ID del CleanProblem en la solicitud, actualizamos soluc_resuelt
        clean_problem_id = request.data.get('soluc_resuelt')
        if clean_problem_id:
            problem.soluc_resuelt = clean_problem_id
            problem.save()
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        problem = self.get_object()
        if request.user != problem.applicant:
            return Response(status=403)
        return super().delete(request, *args, **kwargs)
#---------------------------- CLEAN PROBLEMS ------------------------------
class CleanProblemList(ProblemList):
    queryset = CleanProblem.objects.all()
    serializer_class = CleanProblemSerializer

    def get_permissions(self):
        if self.request.method in ['POST']:
            self.permission_classes = [OnlyCurator]
        else:
            self.permission_classes = [NaturalOrCurator]
        return super(CleanProblemList, self).get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()

        if getattr(self.request.user, 'role', None) != 'admin':
            queryset = queryset.filter(creator=self.request.user)
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        
class CleanProblemDetail(ProblemDetail):
    queryset = CleanProblem.objects.all()
    serializer_class = CleanProblemSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [OnlyCurator]
        if self.request.method in ['DELETE']:
            self.permission_classes = [OnlyCurator]
        else:
            self.permission_classes = [NaturalOrCurator]
        return super(CleanProblemDetail, self).get_permissions()

    def update(self, request, *args, **kwargs):
        problem = self.get_object()
        if request.user != problem.creator:
            return Response(status=403)
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        problem = self.get_object()
        if request.user != problem.creator:
            return Response(status=403)
        return super().delete(request, *args, **kwargs)