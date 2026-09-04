import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import ContactForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q


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


def send_inquiry_emails(contact):
    context = {
        'name': contact.name or 'Client',
        'phone': contact.phone or 'N/A',
        'email': contact.email or 'N/A',
        'required_facade_scope': contact.required_facade_scope or 'Architectural Facade',
        'description': contact.description or 'No details provided',
        'created_at': contact.created_at.strftime("%d %b %Y, %I:%M %p")
    }

    from_sender = getattr(settings, 'DEFAULT_FROM_EMAIL')
    if contact.email:
        try:
            cust_html = render_to_string('EmailFormat/customer_ack.html', context)
            cust_msg = EmailMultiAlternatives(
                subject="Inquiry Received | ANEXA Facade Systems LLP",
                body=strip_tags(cust_html),
                from_email=from_sender,
                to=[contact.email]
            )
            cust_msg.attach_alternative(cust_html, "text/html")
            cust_msg.send(fail_silently=True)
            print("Customer Email send", contact.email)
            
        except Exception as e:
            print("Customer Email Error:", e)

    # 2. Send notification to ANEXA Admin
    try:
        admin_html = render_to_string('EmailFormat/admin_alert.html', context)
        admin_msg = EmailMultiAlternatives(
            subject=f"New Lead: {contact.name} - {contact.required_facade_scope}",
            body=strip_tags(admin_html),
            from_email=from_sender,
            to=['info@anexafacades.com']
        )
        admin_msg.attach_alternative(admin_html, "text/html")
        admin_msg.send(fail_silently=True)
        print("Customer Email send Admin")
        
    except Exception as e:
        print("Admin Email Error:", e)


def fill_contact_form(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        scope = request.POST.get('scope') or request.POST.get('required_facade_scope')
        message = request.POST.get('message') or request.POST.get('description')

        contact = ContactForm.objects.create(name=name,phone=phone,
            email=email,required_facade_scope=scope,
            description=message,status='New'
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
