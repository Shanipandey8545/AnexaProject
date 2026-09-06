from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ContactForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .utils import *
from django.http import HttpResponse


def login_admin(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me')

        user = authenticate(request, username=username, password=password)
        print(user,'hjdsfhjdsh')
        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'login.html')

def logout_admin(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')


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




def fill_contact_form(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        scope = request.POST.get('scope') or request.POST.get('required_facade_scope')
        message = request.POST.get('message') or request.POST.get('description')

        contact = ContactForm.objects.create(
            name=name,
            phone=phone,
            email=email,
            required_facade_scope=scope,
            description=message,
            status='New'
        )
        send_inquiry_emails(contact)

        messages.success(request, "Thank you! Your inquiry has been submitted successfully.")
        return redirect('leadership_contact')

    return render(request, 'leadership_contact.html')


@login_required(login_url='login')
def contact_list(request):
    search_query = request.GET.get('q', '').strip()
    contacts_list = ContactForm.objects.all().order_by('-created_at')
    
    status_filter = request.GET.get('status')
    if status_filter:
        contacts_list = contacts_list.filter(status=status_filter)
    if search_query:
        contacts_list = contacts_list.filter(
            Q(name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    paginator = Paginator(contacts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'contact_list.html', {"contact": page_obj})


@login_required(login_url='login')
def update_contact_status(request, pk):
    if request.method == "POST":
        contact = get_object_or_404(ContactForm, pk=pk)
        new_status = request.POST.get('status')

        valid_statuses = [choice[0] for choice in ContactForm.STATUS_CHOICES]
        if new_status in valid_statuses:
            contact.status = new_status
            contact.save()
            messages.success(request, f"Lead #{pk} ({contact.name}) status changed to {new_status}.")
        else:
            messages.error(request, "Invalid status selected.")

    referer = request.META.get('HTTP_REFERER')
    return redirect(referer if referer else 'contact_list')


@login_required(login_url='login')
def delete_contact(request, pk):
    if request.method == "POST":
        contact = get_object_or_404(ContactForm, pk=pk)
        name = contact.name or f"#{pk}"
        contact.delete()
        messages.success(request, f"Lead for {name} has been successfully deleted.")

    referer = request.META.get('HTTP_REFERER')
    return redirect(referer if referer else 'contact_list')





def service_facade_cladding(request):
    return render(request, 'service_facade_cladding.html')

def service_glazing_systems(request):
    return render(request, 'service_glazing_systems.html')

def service_aluminium_works(request):
    return render(request, 'service_aluminium_works.html')

def service_glass_works(request):
    return render(request, 'service_glass_works.html')

def service_special_facade_works(request):
    return render(request, 'service_special_facade_works.html')

def service_engineering_execution(request):
    return render(request, 'service_engineering_execution.html')

