import threading
from time import sleep
from threading import Thread

from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail


send_email_errors = []


def _send_email():
    sleep(5)
    try:
        send_mail('Enviando emails','Testando o envio de emails',  from_email=['src@email.com'], recipient_list=['dst@email.com'])
    except ConnectionRefusedError as e:
        send_email_errors.append(str(e))


def send_email_thread():
    Thread(target=_send_email).start()


def send_email(request):
    _send_email()
    print(threading.active_count())
    return HttpResponse("Email enviando")



def send_email_th(request):
    send_email_thread()
    return HttpResponse("Assim que possivel o email será enviado")


def email_status(request):
    return JsonResponse({'list' : send_email_errors})
