from datetime import datetime, timedelta


def birthdays():
    today = datetime.now()
    # contact = Contact.objects.get(id='')
    print(today.month - 2)
    # return render(request, 'addressbookapp/birthdays.html', contact)


birthdays()