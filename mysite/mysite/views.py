from django.http import HttpResponse


def index(request):
    return HttpResponse("You've finished the initial setup for the 'Django: Beyond the Basics' tutorial.")
