import requests
import time
import optparse
import datetime
import json
import copy


def login(session, account, password):

    headers = {
   'authority': 'sport.nubapp.com' ,
   'accept': 'application/json, text/plain, */*' ,
   'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6' ,
   'content-type': 'application/x-www-form-urlencoded' ,
   'cookie': 'applicationId=21891030; PHPSESSID-FRONT=d4a351m2127qbm7u69oa39vr59' ,
   'origin': 'https://sport.nubapp.com' ,
   'referer': 'https://sport.nubapp.com/web/index.php' ,
   'sec-ch-ua': '"Google Chrome";v="111",  "Chromium";v="111"' ,
   'sec-ch-ua-mobile': '?1' ,
   'sec-ch-ua-platform': '"Android"' ,
   'sec-fetch-dest': 'empty' ,
   'sec-fetch-mode': 'cors' ,
   'sec-fetch-site': 'same-origin' ,
   'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36' ,
   'x-kl-ajax-request': 'Ajax_Request'
    }

    data = {
        'username': account,
        'password': password
    }
    return session.post('https://sport.nubapp.com/web/ajax/users/checkUser.php', headers=headers, data=data)

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def get_slots(session, start_timestamp, end_timestamp, now_timestamp,id_application):
    headers = {
        'authority': 'sport.nubapp.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://sport.nubapp.com/web/index.php',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    params = (
        ('id_category_activity', '176'),
        ('offset', '-120'),
        ('start', start_timestamp),
        ('end', end_timestamp),
        ('_', now_timestamp),
    )
    return session.get('https://sport.nubapp.com/web/ajax/activities/getActivitiesCalendar.php', headers=headers, params=params).json()

def book(session, id_activity_calendar):

    headers = {
        'authority': 'sport.nubapp.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': 'Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://sport.nubapp.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'x-kl-ajax-request': 'Ajax_Request',
        'referer': 'https://sport.nubapp.com/web/index.php',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = {
        'items[activities][0][id_activity_calendar]': id_activity_calendar,
        'items[activities][0][unit_price]': '0',
        'items[activities][0][n_guests]': '0',
        'items[activities][0][id_resource]': 'false',
        'discount_code': 'false',
        'form': '',
        'formIntoNotes':''
    }
    ret = session.post('https://sport.nubapp.com/web/ajax/bookings/bookBookings.php', headers=headers, data=data)
    return ret

def main(account, password):
    
    print(f"\n")
    print("=" * 100)
    print(f"[{account}] Running script on {str(datetime.datetime.now())}")

    d = datetime.datetime.today()
  
    session = requests.Session()
    
    ## Login
    res_login = login(session, account, password).json()
    id_application = res_login.get('resasocialAccountData').get('boundApplicationData').get('id_application')

    # Build slots
    start_h, start_min, end_h, end_min = 00, 00, 22, 00 

    calendar = dict()
    # days = [('monday', 0), ('tuesday', 1), ('wednesday', 2), ('thursday', 3), ('friday', 4)]
    # days = [ ('tuesday', 1), ('wednesday', 2), ('thursday', 3)]
    days = [('saturday', 5)]
    for t in days:
        weekday = next_weekday(d, t[1])
        search_start = datetime.datetime(weekday.year, weekday.month, weekday.day, start_h, start_min)
        search_end = datetime.datetime(weekday.year, weekday.month, weekday.day, end_h, end_min)

        slots = get_slots(session, search_start.timestamp(),search_end.timestamp(), datetime.datetime.now().timestamp(),id_application)
        eligible_slots= [s for s in slots if '18:30:00' in s['start']]

        if len(eligible_slots) == 1:
            assert len(eligible_slots) == 1
            slot = eligible_slots[0]

            calendar[t[0]] = {
                'start' : slot['start'],
                'end' : slot['end'],
                'slot_id' : slot['id_activity_calendar']
            }

    for k, v in calendar.items():
        print(f"Booking for {k}, {v['start']} and {v['end']} and id {v['slot_id']} ")
        book_res = book(session, v['slot_id'])
        book_res = json.loads(book_res.content) 
        print(json.dumps(book_res, indent=4, sort_keys=True))
    

if __name__ == "__main__":
  
    parser = optparse.OptionParser()

    parser.add_option('-e', '--account', action="store", dest="account")
    parser.add_option('-p', '--password', action="store", dest="password")
   
    options, _ = parser.parse_args()

    main(options.account, options.password)