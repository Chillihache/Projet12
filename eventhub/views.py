from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_endpoint(request):
    """
    Endpoint de test qui renvoie des informations sur l'utilisateur connecté.
    """
    user = request.user
    return Response({
        "message": "Vous êtes authentifié avec succès !",
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "password": user.password,
        }
    })

