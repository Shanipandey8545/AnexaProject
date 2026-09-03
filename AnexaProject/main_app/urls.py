from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('company-overview/', views.company_overview, name='company_overview'),
    path('vision-mission/', views.vision_mission, name='vision_mission'),
    path('our-solutions/', views.our_solutions, name='our_solutions'),
    path('project-capabilities/', views.project_capabilities, name='project_capabilities'),
    path('quality-safety/', views.quality_safety, name='quality_safety'),
    path('why-anexa/', views.why_anexa, name='why_anexa'),
    path('leadership-contact/', views.leadership_contact, name='leadership_contact'),
]