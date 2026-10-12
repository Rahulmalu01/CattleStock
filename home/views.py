from django.shortcuts import render, redirect
from django.contrib import messages
from home.models import TeamMember
from home.models import Contact
from cattle_manager.models import CattleProfile
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
    total_cattle = CattleProfile.objects.count()
    total_farms = CattleProfile.objects.values('farm').distinct().count()
    # total_farms = 0
    context = {
        'total_cattle': total_cattle,
        'total_farms': total_farms,
    }
    return render(request, 'home/index.html', context)

def about(request):
    team = TeamMember.objects.all()
    context = {
        'team': team,
    }
    return render(request, 'home/about.html', context)

def contact(request):
    if request.method == 'POST':
        messages.success(request, "Thank you for your message! We'll get back to you shortly.")
        return redirect('contact')
    return render(request, 'home/contact.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')
    context = {
        'page_title': 'Contact',
        'current_page': 'contact',
    }
    return render(request, 'home/contact.html', context)

@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '').lower()
        if 'dashboard' in message:
            response = 'You can monitor cattle health and sensor analytics from the dashboard.'
        elif 'alert' in message:
            response = 'Alerts help detect abnormal cattle health conditions in real time.'
        elif 'diagnostic' in message:
            response = 'Device diagnostics show sensor battery, connectivity, and firmware health.'
        elif 'temperature' in message:
            response = 'Normal cattle temperature ranges between 38°C and 39.5°C.'
        elif 'heart' in message:
            response = 'Normal cattle heart rate ranges from 60 to 80 BPM.'
        else:
            response = 'I am here to help with cattle monitoring, analytics, alerts, and smart farming.'
        return JsonResponse({'response': response})

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Here you would typically save the email to your database or mailing list
        messages.success(request, "Thank you for subscribing! You'll receive updates from us.")
        return redirect('home')
    return redirect('home')