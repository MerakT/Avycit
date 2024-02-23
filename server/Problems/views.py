from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .models import RawProblem, CleanProblem
from .serializers import RawProblemSerializer, CleanProblemSerializer

#---------------------------- RAW PROBLEMS ------------------------------
class RawProblemList(APIView):
    """
    List all problems, or create a new problem.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        problems = RawProblem.objects.all()
        serializer = RawProblemSerializer(problems, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RawProblemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(applicant=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class RawProblemDetail(APIView):
    """
    Retrieve, update or delete a problem instance.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        problem = self.get_object(pk)
        serializer = RawProblemSerializer(problem)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        problem = self.get_object(pk)
        serializer = RawProblemSerializer(problem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        problem = self.get_object(pk)
        problem.delete()
        return Response(status=204)

#------------------------------------------- CLEAN PROBLEMS -------------------------------------------
class CleanProblemList(APIView):
    """
    List all problems, or create a new problem.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        problems = CleanProblem.objects.all()
        serializer = CleanProblemSerializer(problems, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CleanProblemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(applicant=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

