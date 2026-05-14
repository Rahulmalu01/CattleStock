from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TeamMember
from .models import Contact

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
