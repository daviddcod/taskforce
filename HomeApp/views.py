from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def beats(request):
    return render(request, 'HomeApp/beats.html' )

def welcome(request):
    return render(request, 'HomeApp/welcome.html' )

def home(request):
    cookies_accepted = request.session.get('cookie_consent', False)
    return render(request, 'wdm_home.html', {'cookies_accepted': cookies_accepted})

@csrf_exempt
def set_cookie(request):
    if request.method == 'POST':
        request.session['cookie_consent'] = True
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)