from django.shortcuts import render,redirect
from django.contrib import messages


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def company_overview(request):
    return render(request, 'company_overview.html')

def vision_mission(request):
    return render(request, 'vision_mission.html')

def our_solutions(request):
    return render(request, 'our_solutions.html')

def project_capabilities(request):
    return render(request, 'project_capabilities.html')

def quality_safety(request):
    return render(request, 'quality_safety.html')

def why_anexa(request):
    return render(request, 'why_anexa.html')

def leadership_contact(request):
    if request.method == "POST":
        # Form data extraction (Baad me model me save karne ke liye)
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        scope = request.POST.get('scope')
        message = request.POST.get('message')
        
        # Abhi ke liye success feedback trigger
        messages.success(request, "Thank you! Your inquiry has been submitted successfully.")
        return redirect('leadership_contact')
        
    return render(request, 'leadership_contact.html')