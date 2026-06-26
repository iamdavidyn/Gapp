from django.shortcuts import render, redirect
import datetime
from .utils import get_slip_data
from zoneinfo import ZoneInfo
import random
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.contrib.sessions.models import Session


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_approved:
                if user.session_key:
                    Session.objects.filter(session_key=user.session_key).delete()
                login(request, user)
                user.session_key = request.session.session_key
                user.save()
                messages.success(request, 'You have successfully logged in.')
                return redirect('welcome')
            else:
               return redirect('approval')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
        
    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return redirect('signup')

        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return redirect('signup')
        
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')
        
        elif CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'That username is already taken.')
            return redirect('signup')
        else:
            CustomUser.objects.create_user(username=username, password=password, is_approved=False)
            messages.success(request, 'Account created. Please wait for admin approval.')
            return redirect('approval')

    return render(request, 'signup.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('welcome')


def approval_view(request):
    return render(request, 'approval.html')

@login_required
def gcash_form(request):
    if request.method == 'POST':
            # Gets the form data here
            gcname = request.POST.get('gcname')
            gnumber = request.POST.get('gnumber')
            balance = request.POST.get('balance')
            amount = request.POST.get('amount')
            # Store the form data in the session
            request.session['gcname'] = gcname
            request.session['gnumber'] = gnumber
            request.session['balance'] = balance
            request.session['amount'] = amount

            # Masking the name

            part = gcname.split() 
            masked_parts= []

            for i, name in enumerate(part):
                name = name.upper()
                if i == len(part) - 1:
                    masked = name[0]
                else:

                    if len(name) <= 3:
                        masked = name[:1] + "•" * (len(name) - 1)


                    else:
                        masked = name[:2] + "•" * (len(name) - 3) + name[-1]

                masked_parts.append(masked)

            gcname = ' '.join(masked_parts)


        #abbrivate of the name

        
           
            balance = Decimal(balance).quantize(Decimal('0.00'))

            amount = Decimal(amount).quantize(Decimal('0.00'))

            comtext = {
                'abbr': gcname[0] + gcname.split()[-1].upper(),
                'gcname': gcname,
                'gnumber': gnumber[:3] + " " + gnumber[3:6] + " " + gnumber[6:9] + " " + gnumber[9:],
                'balance': balance,
                'amount': amount,
            }




            return render(request, 'index.html', comtext)
    else:

        return render(request, 'form.html', {'form': gcash_form})


@login_required
def screenshot(request):
    # Retrieve the form data from the session
    gcname = request.session.get('gcname')
    gnumber = request.session.get('gnumber')
    balance = request.session.get('balance')
    amount = request.session.get('amount')
    

    if not gcname or not gnumber or not balance or not amount:
        messages.error(request, 'Please fill out the form before accessing the screenshot.')
        return redirect('welcome')

    # Masking the name
    part = gcname.split()
    masked_parts = []

    for i, name in enumerate(part):
        name = name.upper()
        if i == len(part) - 1:
            masked = name[0]
        else:
            if len(name) <= 3:
                masked = name[:1] + "•" * (len(name) - 1)
            else:
                masked = name[:2] + "•" * (len(name) - 3) + name[-1]

        masked_parts.append(masked)

    gcname = ' '.join(masked_parts)

    balance = Decimal(balance).quantize(Decimal('0.00'))
    
    amount = Decimal(amount).quantize(Decimal('0.00'))
    
    data = {
        'gcname': gcname,
        'gnumber': gnumber[:3] + " " + gnumber[3:6] + " " + gnumber[6:9] + " " + gnumber[9:],
        'balance': balance,
        'amount': amount,
    }

    # Get the current time in the Philippines timezone
    philipines_time = datetime.datetime.now(ZoneInfo('Asia/Manila'))
    data['timestamp'] = philipines_time

    # Generate a random reference number in the format "1234 567 890123"
    chunk_length = [4, 3, 6]

    chunks = []
    for length in chunk_length:
        chunk = ''.join(str(random.randint(0, 9)) for _ in range(length))
        chunks.append(chunk)

    data['reff'] = ' '.join(chunks)

    return render(request, 'screenshot.html', data)
@login_required
def slip(request):
     # Retrieve the form data from the session
        gcname = request.session.get('gcname')
        gnumber = request.session.get('gnumber')
        balance = request.session.get('balance')
        amount = request.session.get('amount')
        
    
        if not gcname or not gnumber or not balance or not amount:
            messages.error(request, 'Please fill out the form before accessing the screenshot.')
            return redirect('welcome')
    
        # Masking the name
        part = gcname.split()
        masked_parts = []
    
        for i, name in enumerate(part):
            name = name.upper()
            if i == len(part) - 1:
                masked = name[0]
            else:
                if len(name) <= 3:
                    masked = name[:1] + "•" * (len(name) - 1)
                else:
                    masked = name[:2] + "•" * (len(name) - 3) + name[-1]
    
            masked_parts.append(masked)
    
        gcname = ' '.join(masked_parts)
    
        balance = Decimal(balance).quantize(Decimal('0.00'))
        
        amount = Decimal(amount).quantize(Decimal('0.00'))
        
        data = {
            'gcname': gcname,
            'gnumber': gnumber[:3] + " " + gnumber[3:6] + " " + gnumber[6:9] + " " + gnumber[9:],
            'balance': balance,
            'amount': amount,
        }
    
        # Get the current time in the Philippines timezone
        philipines_time = datetime.datetime.now(ZoneInfo('Asia/Manila'))
        data['timestamp'] = philipines_time
    
        # Generate a random reference number in the format "1234 567 890123"
        chunk_length = [4, 3, 6]
    
        chunks = []
        for length in chunk_length:
            chunk = ''.join(str(random.randint(0, 9)) for _ in range(length))
            chunks.append(chunk)
    
        data['reff'] = ' '.join(chunks)
        
        return render(request, 'slip.html', data)

def payment(request):
    # Retrieve the form data from the session
    gcname = request.session.get('gcname')
    gnumber = request.session.get('gnumber')
    balance = request.session.get('balance')
    amount = request.session.get('amount')
    

    if not gcname or not gnumber or not balance or not amount:
        messages.error(request, 'Please fill out the form before accessing the screenshot.')
        return redirect('welcome')

    # Masking the name
    part = gcname.split()
    masked_parts = []

    for i, name in enumerate(part):
        name = name.upper()
        if i == len(part) - 1:
            masked = name[0]
        else:
            if len(name) <= 3:
                masked = name[:1] + "•" * (len(name) - 1)
            else:
                masked = name[:2] + "•" * (len(name) - 3) + name[-1]

        masked_parts.append(masked)

    gcname = ' '.join(masked_parts)

    balance = Decimal(balance).quantize(Decimal('0.00'))
    
    amount = Decimal(amount).quantize(Decimal('0.00'))
    
    data = {
        'gcname': gcname,
        'gnumber': gnumber[:3] + " " + gnumber[3:6] + " " + gnumber[6:9] + " " + gnumber[9:],
        'balance': balance,
        'amount': amount,
    }

    # Get the current time in the Philippines timezone
    philipines_time = datetime.datetime.now(ZoneInfo('Asia/Manila'))
    data['timestamp'] = philipines_time

    # Generate a random reference number in the format "1234 567 890123"
    chunk_length = [13]

    chunks = []
    for length in chunk_length:
        chunk = ''.join(str(random.randint(0, 9)) for _ in range(length))
        chunks.append(chunk)
    
    data['reff'] = ' '.join(chunks)
    
    return render(request, 'gcash.html', data)


@login_required
def select_page(request):
    return render(request, 'select.html')


def welcome(request):
    return render(request, 'welcome.html')