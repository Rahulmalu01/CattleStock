from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import (Farm, CattleProfile)
from hardware.models import SensorReading
from cattlestock.mongodb import alerts_collection

@login_required
def dashboard(request):
    total_cattle = CattleProfile.objects.count()
    healthy = CattleProfile.objects.filter(health_status='healthy').count()
    warning = CattleProfile.objects.filter(health_status='warning').count()
    critical = CattleProfile.objects.filter(health_status='critical').count()
    recent_readings = SensorReading.objects.order_by('-timestamp')[:10]
    alerts = list(
        alerts_collection.find()
        .sort('created_at', -1)
        .limit(10)
    )
    context = {
        'total_cattle': total_cattle,
        'healthy': healthy,
        'warning': warning,
        'critical': critical,
        'recent_readings': recent_readings,
        'alerts': alerts,
    }
    return render(
        request,
        'cattle_manager/dashboard.html',
        context
    )

@login_required
def cattle_list(request):
    cattles = CattleProfile.objects.all()
    return render(
        request,
        'cattle_manager/cattle_list.html',
        {'cattles': cattles}
    )

@login_required
def cattle_detail(request, cattle_id):
    cattle = get_object_or_404(
        CattleProfile,
        cattle_id=cattle_id
    )
    readings = SensorReading.objects.filter(cattle__cattle_id=cattle_id).order_by('-timestamp')[:50]
    alerts = list(
        alerts_collection.find({'cattle_id': cattle_id})
        .sort('created_at', -1)
        .limit(20)
    )
    context = {
        'cattle': cattle,
        'readings': readings,
        'alerts': alerts,
    }
    return render(
        request,
        'cattle_manager/cattle_detail.html',
        context
    )

@login_required
def add_cattle(request):
    farms = Farm.objects.all()
    if request.method == 'POST':
        farm = Farm.objects.get(id=request.POST.get('farm'))
        cattle = CattleProfile.objects.create(
            cattle_id=request.POST.get('cattle_id'),
            name=request.POST.get('name'),
            breed=request.POST.get('breed'),
            age=request.POST.get('age'),
            weight=request.POST.get('weight'),
            gender=request.POST.get('gender'),
            farm=farm,
            image=request.POST.get('image'),
        )
        farm.total_cattle += 1
        farm.save()
        return redirect('cattle_list')
    return render(
        request,
        'cattle_manager/add_cattle.html',
        {'farms': farms}
    )