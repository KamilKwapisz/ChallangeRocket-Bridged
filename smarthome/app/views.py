from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def index(request):
    return render(request, "app/index.html", {})


def ajax(request):
    data = request.GET.dict()
    return JsonResponse(True, safe=False)
