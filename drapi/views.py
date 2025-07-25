from django.shortcuts import render 
from .models import Aiquest
from .serializer import AiquestSerializer 
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse  
from django.views.decorators.csrf import csrf_exempt 
import io 
from rest_framework.parsers import JSONParser


# ✅ GET all Aiquest data
def aiquest_info(request): 
    ai = Aiquest.objects.all()
    serializer = AiquestSerializer(ai, many=True)
    json_data = JSONRenderer().render(serializer.data)
    return HttpResponse(json_data, content_type='application/json')


# ✅ GET or DELETE single Aiquest by ID
@csrf_exempt
def aiquest_ins(request, pk): 
    try:
        ai = Aiquest.objects.get(id=pk)
    except Aiquest.DoesNotExist:
        error_data = JSONRenderer().render({'error': 'Data not found'})
        return HttpResponse(error_data, content_type='application/json', status=404)

    if request.method == 'GET':
        serializer = AiquestSerializer(ai)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

    elif request.method == 'DELETE':
        ai.delete()
        res = {'msg': 'Deleted successfully'}
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json', status=200)

    else:
        return HttpResponse("This endpoint only accepts GET or DELETE requests.", status=405)


# ✅ POST to create or PUT to update Aiquest
@csrf_exempt
def aiquest_create(request): 
    if request.method == 'POST': 
        json_data = request.body    
        stream = io.BytesIO(json_data)  
        pythondata = JSONParser().parse(stream)  
        serializer = AiquestSerializer(data=pythondata) 

        if serializer.is_valid(): 
            serializer.save() 
            res = {'msg': 'Successfully inserted data'} 
            json_data = JSONRenderer().render(res) 
            return HttpResponse(json_data, content_type='application/json')
        
        json_data = JSONRenderer().render(serializer.errors) 
        return HttpResponse(json_data, content_type='application/json', status=400)
    
    elif request.method == 'PUT': 
        json_data = request.body 
        stream = io.BytesIO(json_data) 
        pythondata = JSONParser().parse(stream) 
        id = pythondata.get('id')  

        try:
            aiq = Aiquest.objects.get(id=id) 
        except Aiquest.DoesNotExist:
            return HttpResponse(JSONRenderer().render({'error': 'Data not found'}), content_type='application/json', status=404)

        serializer = AiquestSerializer(aiq, data=pythondata, partial=True)
        if serializer.is_valid(): 
            serializer.save() 
            res = {'msg': 'Successfully updated data'} 
            json_data = JSONRenderer().render(res) 
            return HttpResponse(json_data, content_type='application/json')
        
        json_data = JSONRenderer().render(serializer.errors) 
        return HttpResponse(json_data, content_type='application/json', status=400)

    else:
        return HttpResponse("This endpoint only accepts POST or PUT requests.", status=405)
