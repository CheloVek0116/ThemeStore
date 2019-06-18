from django.shortcuts import render
# Create your views here.


def present_page(request):
    return render(request, "Present.html")


