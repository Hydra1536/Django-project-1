from django.shortcuts import render, HttpResponse
from datetime import datetime
from home.models import Contact
# Create your views here.
def index(request):
    # context= {'variable1':"this is sent",
    #           'variable2':"this is also sent"}
    return render (request, "index.html")
    # return HttpResponse("Hello, welcome to the Home Page!")

def about(request):
        return render (request, "about.html")

    # return HttpResponse("Hello, welcome to the About Page!")
def services(request):
        return render (request, "services.html")
    # return HttpResponse("Hello, welcome to the Services Page!")
def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        comments=request.POST.get('comments')
        contact=Contact(name=name, email=email, phone=phone, comments=comments, date=datetime.today())
        contact.save()
    return render (request, "contact.html")

    # return HttpResponse("Hello, welcome to the Contact Page!")