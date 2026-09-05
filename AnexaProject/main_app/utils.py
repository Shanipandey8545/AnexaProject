from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import threading




def _email_worker(contact):
    """Background me email bhejne ke liye worker function"""
    context = {
        'name': contact.name or 'Client',
        'phone': contact.phone or 'N/A',
        'email': contact.email or 'N/A',
        'required_facade_scope': contact.required_facade_scope or 'Architectural Facade',
        'description': contact.description or 'No details provided',
        'created_at': contact.created_at.strftime("%d %b %Y, %I:%M %p")
    }

    from_sender = getattr(settings, 'DEFAULT_FROM_EMAIL')

    # 1. Customer Email
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
            cust_msg.send(fail_silently=False)
            print("Customer Email sent to:", contact.email)
        except Exception as e:
            print("Customer Email Error:", e)

    # 2. Admin Email
    try:
        admin_html = render_to_string('EmailFormat/admin_alert.html', context)
        admin_msg = EmailMultiAlternatives(
            subject=f"New Lead: {contact.name} - {contact.required_facade_scope}",
            body=strip_tags(admin_html),
            from_email=from_sender,
            to=['dharmendra@anexafacade.com']
        )
        admin_msg.attach_alternative(admin_html, "text/html")
        admin_msg.send(fail_silently=False)
        print("Admin Email sent successfully")
    except Exception as e:
        print("Admin Email Error:", e)


def send_inquiry_emails(contact):
    """Email ko alag background thread me start karega"""
    thread = threading.Thread(target=_email_worker, args=(contact,))
    thread.daemon = True
    thread.start()

