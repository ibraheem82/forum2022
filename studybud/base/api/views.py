# from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
# ===> getting from the models
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def getRoutes(request):
    
    routes = [
        # ===> make a request to us and get this api
        'GET /api/',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    
    
    '''
    # ===> [safe] means that we can use more than one python dictionary inside of this response
    # ===> [safe] is going to allow this list to be turned into a [List]
    # ===> this [Json] response is going to convert the this data into a [Json] data
    '''

    return Response(routes)
    # return JsonResponse(routes, safe=False)
    
    
    
    
    
@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    # ===> [Response] can not return python list of object, we need to [serialise] it
    # ===> we are serializing a queryset, (rooms) is the object that we want to serialize, while (many=True) means that we are serializing many object
    serializer = RoomSerializer(rooms, many=True)
    # ===> we are returning back the data attributes
    return Response(serializer.data)







    
@api_view(['GET'])
# ===> we are getting a single room
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    # ===> [Response] can not return python list of object, we need to [serialise] it
    # ===> we are serializing a queryset, (rooms) is the object that we want to serialize, while (many=False) means that we are serializing and returning one object
    serializer = RoomSerializer(room, many=False)
    # ===> we are returning back the data attributes
    return Response(serializer.data)