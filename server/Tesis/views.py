from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .models import *
from .serializers import *

ALL_ACCESS = ['coordinador', 'sec_prog']

class AllAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role in ALL_ACCESS
    
class AllAccessOrInternal(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.role in ALL_ACCESS:
            return True
        tesis = Tesis.objects.get(pk=view.kwargs['pk'])
        return request.user and (request.user.id == tesis.tesista.id or request.user.id == tesis.advisor.id)

class TesisList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [AllAccess]

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
    permission_classes = [AllAccessOrInternal]

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