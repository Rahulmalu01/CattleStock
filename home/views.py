from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TeamMember
from .models import Contact
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
    context = {}
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
    