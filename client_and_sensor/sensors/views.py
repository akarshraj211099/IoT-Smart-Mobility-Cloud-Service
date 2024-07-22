from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Sensor
from django.contrib.auth.decorators import login_required

# Create your views here.
def sensor_detail(request, qr_code):
    try:
        sensor = Sensor.objects.get(qr_code=qr_code)
        data = {
            "name": sensor.name,
            "location": sensor.location,
            "status": sensor.status,
        }
        return JsonResponse(data)
    except Sensor.DoesNotExist:
        return JsonResponse({"error": "Sensor not found"}, status=404)
    

def qr_scan(request):
    return render(request, 'sensors/qr_scan.html')

@login_required
def options(request):
    return render(request, 'sensors/options.html')

def sensor_id(request):
    if request.method == 'POST':
        sensor_id = request.POST.get('sensor_id')
        return redirect('sensor_detail', qr_code=sensor_id)
    return render(request, 'sensors/options.html')