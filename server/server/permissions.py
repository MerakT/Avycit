from rest_framework import permissions

#---------------------- BASE ----------------------
class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

#---------------------- PROBLEMS RELATED ----------------------
class OnlyCurator(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'admin'

class OnlyNaturalPerson(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view) and obj.applicant == request.user

class NaturalOrCurator(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view) and (request.user.role == 'admin' or obj.applicant == request.user)

#---------------------- BOTH RELATED ----------------------
class OnlyTesista(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'tesista'

class TesistaOrCurator(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role in ['tesista', 'admin']
   
#---------------------- TESIS RELATED ----------------------
class OnlyCoordinador(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'coordinador'

class TesistaOrCoordinador(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role in ['tesista', 'coordinador'] 
