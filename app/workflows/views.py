from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'pages/index.html')


def login(request):
    username = request.POST.get('login')
    password = request.POST.get('password')
    print(username)
    print(password)
    # TODO: handle logging(check if user exists etc.)
    context = {
        'is_new_account': False,
        'failed': False,
        'login': None,
        'password': None
    }
    return render(request, 'pages/login.html', context)


def register(request):
    return render(request, 'pages/register.html')
