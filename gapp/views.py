from django.shortcuts import render, redirect
import datetime
from zoneinfo import ZoneInfo
import random
from decimal import Decimal
from django.contrib import messages

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


def welcome(request):
    return render(request, 'welcome.html')