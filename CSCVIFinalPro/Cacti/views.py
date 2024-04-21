from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .forms import ProfileForm
from .models import Profile
from .models import Cactus
from .forms import CactusForm
from .forms import PaymentForm
from django.http import JsonResponse
import stripe
from django.conf import settings




from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
import stripe

class PaymentTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('stripe.Charge.create')
    def test_successful_payment(self, mock_charge_create):
        # Mock the Stripe API call to simulate a successful payment
        mock_charge_create.return_value = {'status': 'succeeded'}

        # Make a POST request to the view that handles payment processing
        response = self.client.post(reverse('process_payment'), {
            'stripeToken': 'tok_visa',  # Use a test token from Stripe
            'amount': 1000,  # Example amount in cents
        })

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the response content indicates a successful payment
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'success': True})



#####################################################################



def home(request):
    return render(request, "home.html")

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        # address = request.POST['address']
        # address_2 = request.POST['address_2']
        # city = request.POST['city']
        # state = request.POST['state']
        # zip = request.POST['zip']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists ')
                return redirect(register)
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name) #, address=address, city=city, state=state, zip=zip
                #user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, address=address, city=city, state=state, zip=zip)
                user.set_password(password)
                user.is_staff=True
                user.save()
                print("Success")
                return redirect('login_user')

    else:
        print("this is not post method")
        return render(request, "register.html")

def login_user(request):
    if request.method == 'POST':
        username =request.POST['username']
        password =request.POST['password']

        user = auth.authenticate(username=username, password=password)
        #user = CustomUser.objects.get(username=username)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid Username of Password')
            return redirect('login_user')

    else:
        return render(request,"login.html")

def logout_user(request):
    auth.logout(request)
    return redirect('home') #Redirect to the home page
    
#_________________________________________________________________________________________

def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form without committing to get an instance
            profile = form.save(commit=False)
            # Assign the user instance to the profile
            profile.user = request.user
            # Save the profile
            profile.save()
            return redirect('profile_detail')
    else:
        form = ProfileForm()
    return render(request, 'create_profile.html', {'form': form})

def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

def profile_detail(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile_detail.html', {'profile': profile})

#_______________________________________________________________________________________

def cactus_list(request):
    cacti = Cactus.objects.all()
    return render(request, 'cactus_list.html', {'cacti': cacti})

def cactus_detail(request, pk):
    cactus = get_object_or_404(Cactus, pk=pk)
    return render(request, 'cactus_detail.html', {'cactus': cactus})

def cactus_create(request):
    if request.method == 'POST':
        form = CactusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cactus_list')
    else:
        form = CactusForm()
    return render(request, 'cactus_form.html', {'form': form})

def cactus_update(request, pk):
    cactus = get_object_or_404(Cactus, pk=pk)
    if request.method == 'POST':
        form = CactusForm(request.POST, instance=cactus)
        if form.is_valid():
            form.save()
            return redirect('cactus_list')
    else:
        form = CactusForm(instance=cactus)
    return render(request, 'cactus_form.html', {'form': form})

def cactus_delete(request, pk):
    cactus = get_object_or_404(Cactus, pk=pk)
    if request.method == 'POST':
        cactus.delete()
        return redirect('cactus_list')
    return render(request, 'cactus_confirm_delete.html', {'cactus': cactus})

#__________________________________________________________________________________________

def payment_view(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Process payment (to be implemented)
            return render(request, 'payment_success.html')
    else:
        form = PaymentForm()
    return render(request, 'payment_form.html', {'form': form})


#_______________________________________________________________________________________

stripe.api_key = 'sk_test_51P0FreP88EmJMNLRSEzStmgN5opBuPtfcWUakliG1hAtCBk12N6QXcuCRS1cXQpYUg3Q2mwQQrrqT7v1315BWZtC00toP8ZqPd' 

def process_payment(request):
    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        amount = request.POST.get('amount')  # Amount in cents

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                description='Cactus purchase',
                source=token,
            )
            # Handle successful payment (e.g., update database, send confirmation email)
            return JsonResponse({'success': True})
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body['error']
            return JsonResponse({'error': err['message']}, status=403)
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            return JsonResponse({'error': 'An error occurred'}, status=500)