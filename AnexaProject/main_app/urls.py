from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('adminlogin/', views.login_admin, name='adminlogin'),
    path('adminlogout/', views.logout_admin, name='adminlogout'),
    path('about/', views.about, name='about'),
    path('company-overview/', views.company_overview, name='company_overview'),
    path('vision-mission/', views.vision_mission, name='vision_mission'),
    path('our-solutions/', views.our_solutions, name='our_solutions'),
    path('project-capabilities/', views.project_capabilities, name='project_capabilities'),
    path('quality-safety/', views.quality_safety, name='quality_safety'),
    path('why-anexa/', views.why_anexa, name='why_anexa'),
    path('leadership-contact/', views.fill_contact_form, name='leadership_contact'),
    path('contact-list/', views.contact_list, name='contact_list'),
    path('management/contacts/<int:pk>/status/', views.update_contact_status, name='update_contact_status'),
    path('management/contacts/<int:pk>/delete/', views.delete_contact, name='delete_contact'),

    path('services/facade-cladding/', views.service_facade_cladding, name='service_facade_cladding'),
    path('services/glazing-systems/', views.service_glazing_systems, name='service_glazing_systems'),
    path('services/aluminium-works/', views.service_aluminium_works, name='service_aluminium_works'),
    path('services/glass-works/', views.service_glass_works, name='service_glass_works'),
    path('services/special-facade-works/', views.service_special_facade_works, name='service_special_facade_works'),
    path('services/facade-engineering-execution/', views.service_engineering_execution, name='service_engineering_execution'),

    
]