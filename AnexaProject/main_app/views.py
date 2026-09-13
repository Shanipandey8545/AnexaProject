from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .utils import *
import cloudinary.uploader


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

# def upload_file_view(request):
#     if request.method == 'POST':
#         title = request.POST.get('title', '').strip()
#         uploaded_file = request.FILES.get('file')

#         if not title or not uploaded_file:
#             messages.error(request, "Kripya File Name aur File dono provide karein!")
#             return redirect('upload_file')
#         MAX_UPLOAD_SIZE = 10 * 1024 * 1024
#         if uploaded_file.size > MAX_UPLOAD_SIZE:
#             size_in_mb = round(uploaded_file.size / (1024 * 1024), 2)
#             messages.error(request, f"File size ({size_in_mb} MB) 10 MB se badi hai! Kripya 10 MB se chhoti file upload karein.")
#             return redirect('upload_file')
#         asset = UploadedAsset(title=title, file=uploaded_file)
#         asset.save()
#         messages.success(request, f"'{title}' Cloudinary par successfully upload ho gaya!")
#         return redirect('upload_file')



def upload_file_view(request):
    if request.method == 'POST':
        base_title = request.POST.get('title', '').strip()
        uploaded_files = request.FILES.getlist('files')  # 'files' input name HTML me use karein

        if not uploaded_files:
            messages.error(request, "Kripya kam se kam ek file select karein!")
            return redirect('upload_file')

        MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB limit per file
        oversized_files = []
        valid_files = []

        # Pehle sabhi files ka size check karein
        for file in uploaded_files:
            if file.size > MAX_UPLOAD_SIZE:
                size_in_mb = round(file.size / (1024 * 1024), 2)
                oversized_files.append(f"{file.name} ({size_in_mb} MB)")
            else:
                valid_files.append(file)

        # Agar koi file size limit cross kare toh error dikhayein
        if oversized_files:
            messages.error(
                request, 
                f"Ye files 10 MB se badi hain: {', '.join(oversized_files)}. Kripya chhoti files upload karein."
            )
            return redirect('upload_file')

        for index, file in enumerate(valid_files, start=1):
            final_title = f"{base_title} - {file.name}" if base_title else file.name

            asset = UploadedAsset(title=final_title, file=file)
            asset.save()

        messages.success(request, f"{len(valid_files)} files Cloudinary par successfully upload ho gayi hain!")
        return redirect('upload_file')

    search_query = request.GET.get('q', '').strip()
    assets_queryset = UploadedAsset.objects.all().order_by('title')
    if search_query:
        assets_queryset = assets_queryset.filter(title__icontains=search_query)

    paginator = Paginator(assets_queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'upload_file.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_count': assets_queryset.count()
    })
    

def upload_file_delete_view(request, pk):
    asset = get_object_or_404(UploadedAsset, pk=pk)
    
    if request.method == 'POST':
        try:
            public_id = None
            if hasattr(asset.file, 'public_id'):
                public_id = asset.file.public_id
            else:
                url_str = str(asset.file_url)
                if 'upload/' in url_str:
                    path_after_upload = url_str.split('upload/')[-1]
                    parts = path_after_upload.split('/')
                    if parts[0].startswith('v') and parts[0][1:].isdigit():
                        parts = parts[1:]
                    file_with_ext = '/'.join(parts)
                    public_id = file_with_ext.rsplit('.', 1)[0]

            if public_id:
                r_type = 'raw' if asset.file_type.lower() in ['pdf', 'doc', 'docx', 'zip'] else 'image'
                result = cloudinary.uploader.destroy(public_id, resource_type=r_type, invalidate=True)
                if result.get('result') != 'ok' and r_type == 'raw':
                    cloudinary.uploader.destroy(public_id, resource_type='image', invalidate=True)
            asset_title = asset.title
            asset.delete()
            messages.success(request, f"'{asset_title}' Cloudinary aur Database dono se successfully delete ho gaya!")

        except Exception as e:
            asset.delete()
            messages.warning(request, f"File database se delete ho gayi, par Cloudinary sync warning: {str(e)}")

    return redirect('upload_file')