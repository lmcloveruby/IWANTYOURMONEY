from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, 'labs_index.html')


def resonate_index(request):
    return render(request, 'labs_resonate_index.html')
