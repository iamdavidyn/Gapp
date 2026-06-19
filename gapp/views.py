from django.shortcuts import render
import datetime
from zoneinfo import ZoneInfo
import random

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
            
            comtext = {
                'abbr': gcname[0] + gcname.split()[-1].upper(),
                'gcname': gcname,
                'gnumber': gnumber[:3] + " " + gnumber[4:7] + " " + gnumber[7:10] + " " + gnumber[10:],
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

    data = {
        'gcname': gcname,
        'gnumber': gnumber[:3] + " " + gnumber[4:7] + " " + gnumber[7:10] + " " + gnumber[10:],
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