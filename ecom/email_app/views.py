

from django.http import JsonResponse
from .tasks import send_email_task

def send_email_api(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        recipient_list = request.POST.getlist('recipients')

        send_email_task(subject, message, recipient_list)

        return JsonResponse({'status': 'Email scheduled to be sent'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
