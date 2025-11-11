from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    context= {'variable1':"this is sent",
              'variable2':"this is also sent"}
    return render (request, "index.html", context)
    # return HttpResponse("Hello, welcome to the Home Page!")

def about(request):
    return HttpResponse("Hello, welcome to the About Page!")
def services(request):
    return HttpResponse("Hello, welcome to the Services Page!")
def contact(request):
    return HttpResponse("Hello, welcome to the Contact Page!")