from django.shortcuts import HttpResponse, render


def hello_world(request):
    # return HttpResponse("Hello World!")
    return render(request, 'home.html')