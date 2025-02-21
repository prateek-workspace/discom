from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer
from base.services.ai_service import get_ai_response
from base.models import Message, AIResponse

@api_view(['GET'],)
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    return Response(routes) 

@api_view(['GET'],)
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'],)
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def generate_ai_response(request):
    message_id = request.data.get('message_id')
    message_text = request.data.get('message')
    
    try:
        # Get AI response
        ai_response = get_ai_response(message_text)
        
        return Response({
            'success': True,
            'response': ai_response,
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=500)