from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import authentication

from .models import *
from .serializers import *

from django.db.models import Q

from Notis.models import Noti

from server.permissions import OnlyCurator, TesistaOrCurator, OnlyCoordinador, TesistaOrCoordinador, OnlyTesista
    
# ---------------------------- PROPUESTAS DE TESIS ------------------------------
class PropuestaTesisList(ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = PropuestaTesisSerializer
    queryset = PropuestaTesis.objects.all()

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return [OnlyCurator()]
        elif self.request.method in ['DELETE']:
            return [OnlyCoordinador()]
        return [TesistaOrCurator()]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Define a dictionary to map query parameters to model fields
        and_filter_params = {
            'propuesta_title': 'propuesta_title__icontains',
        }

        or_filter_params = {
            'insvestigation_type': 'insvestigation_type',
            'level': 'level',
            'design': 'design',
            'status': 'status',
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
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        try:
            coordinators = Usuario.objects.filter(role='coordinador', career=self.request.user.career)
            for coordinator in coordinators:
                Noti.objects.create(
                subject='Propuesta de Tesis Creada',
                sent_by=self.request.user,
                sent_to=coordinator,
                message='Se ha creado una propuesta de tesis',
                )
        except:
            pass
    
class PropuestaTesisDetail(RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = PropuestaTesisSerializer

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PUT', 'PATCH', 'POST']:
            return [OnlyCoordinador()]
        return [TesistaOrCoordinador()]

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj
    
    def perform_destroy(self, instance):
        try:
            Noti.objects.create(
                subject='Propuesta de Tesis Eliminada',
                sent_by=self.request.user,
                sent_to=instance.tesista,
                message='Tu propuesta de tesis ha sido eliminada',
            )
        except:
            pass
        instance.delete()

# ---------------------------------------- POSTULACIONES ---------------------------------------------
class PostulacionesList(ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = PostulacionesSerializer
    queryset = Postulaciones.objects.all()

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [TesistaOrCoordinador()]
        elif self.request.method in ['PUT', 'PATCH']:
            return [OnlyCoordinador()]
        return [OnlyTesista()]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Define a dictionary to map query parameters to model fields
        and_filter_params = {
            'status': 'status',
        }

        or_filter_params = {
            'student_code': 'tesista__code__icontains',
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

        if self.request.user.role == 'tesista':
            queryset = queryset.filter(tesista=self.request.user)

        return queryset
    
    def perform_create(self, serializer):
        serializer.save(tesista=self.request.user)
        try:
            coordinators = Usuario.objects.filter(role='coordinador', career=self.request.user.career)
            for coordinator in coordinators:
                Noti.objects.create(
                subject='Postulacion a Tesis',
                sent_by=self.request.user,
                sent_to=coordinator,
                message='Se ha postulado a una tesis',
                )
        except:
            pass

class PostulacionesDetail(RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]

    def get_permissions(self):
        if self.request.method in ['GET', 'DELETE']:
            return [TesistaOrCoordinador()]
        return [OnlyCoordinador()]

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj
    
    def perform_update(self, serializer):
        serializer.save()
        if self.request.data['status'] == 'aceptado':
            try: 
                Noti.objects.create(
                    subject='Postulacion a Tesis',
                    sent_by=self.request.user,
                    sent_to=self.get_object().tesista,
                    message='Tu postulacion ha sido aceptada',
                )
            except:
                pass

    def perform_destroy(self, instance):
        try: 
            Noti.objects.create(
                subject='Postulacion a Tesis',
                sent_by=self.request.user,
                sent_to=instance.tesista,
                message='Tu postulacion ha sido rechazada',
            )
        except:
            pass
        instance.delete()

# ---------------------------------------- PARA LA TESIS ---------------------------------------------
class TesisList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [OnlyCoordinador()]

    def get(self, request, format=None):
        tesis = Tesis.objects.all()
        serializer = TesisSerializer(tesis, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TesisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class TesisDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [TesistaOrCoordinador()]

    def get_object(self, pk):
        try:
            return Tesis.objects.get(pk=pk)
        except Tesis.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        tesis = self.get_object(pk)
        serializer = TesisSerializer(tesis)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        tesis = self.get_object(pk)
        serializer = TesisSerializer(tesis, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        tesis = self.get_object(pk)
        tesis.delete()
        return Response(status=204)