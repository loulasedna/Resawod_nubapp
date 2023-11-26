#!/usr/bin/env python3

import requests
import time
import optparse
import datetime
import json

# Variables
application_id = '36307036' # Replace by your id_application

with open('personal_data/users.json') as json_file:
	data = json.load(json_file)


def get_session_id(session, id_application):
	headers = {
		'authority': 'sport.nubapp.com',
		'pragma': 'no-cache',
		'cache-control': 'no-cache',
		'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
		'sec-ch-ua-mobile': '?0',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'sec-fetch-site': 'same-origin',
		'sec-fetch-mode': 'navigate',
		'sec-fetch-dest': 'document',
		'referer': f'https://sport.nubapp.com/web/setApplication.php?id_application={id_application}',
		'accept-language': 'fr-FR,fr;q=0.9',
		'cookie': f'applicationId={id_application}',
	}

	params = (
		('id_application', id_application),
		('isIframe', 'false'),
	)
	return session.get('https://sport.nubapp.com/web/cookieChecker.php', headers=headers, params=params)


def login(session, account, password):

	headers = {
		'authority': 'sport.nubapp.com',
		'pragma': 'no-cache',
		'cache-control': 'no-cache',
		'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
		'sec-ch-ua-mobile': '?0',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36',
		'content-type': 'application/x-www-form-urlencoded',
		'origin': 'https://sport.nubapp.com',
		'sec-fetch-site': 'same-origin',
		'sec-fetch-mode': 'cors',
		'sec-fetch-dest': 'empty',
		'referer': 'https://sport.nubapp.com/web/index.php',
		'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
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


def get_slots(session, start_timestamp, end_timestamp, now_timestamp, id_application):
	headers = {
		'authority': 'sport.nubapp.com',
		'pragma': 'no-cache',
		'cache-control': 'no-cache',
		'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
		'sec-ch-ua-mobile': '?0',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36',
		'sec-fetch-site': 'same-origin',
		'sec-fetch-mode': 'cors',
		'sec-fetch-dest': 'empty',
		'referer': 'https://sport.nubapp.com/web/index.php',
		'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
	}

	params = (		
		('id_category_activity', '2179'), # id of the activity
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
		'formIntoNotes': ''
	}
	ret = session.post(
		'https://sport.nubapp.com/web/ajax/bookings/bookBookings.php', headers=headers, data=data)
	return ret


def main(user):
	print("=" * 100)
	print(f"[{user['name']}] Running script on {str(datetime.datetime.now())}")

	d = datetime.datetime.today()

	session = requests.Session()

	# Login
	sess_id = get_session_id(session, application_id)
	res_login = login(session, user['login'], user['password']).json()

	if options.verbose:
		print("Response from login:")
		print(res_login)

	# id_application = res_login.get('resasocialAccountData').get('boundApplicationData').get('id_application')
	id_application = None
	if options.verbose:
		resasocial_account_data = res_login.get('resasocialAccountData')
		if resasocial_account_data is not None:
			bound_application_data = resasocial_account_data.get(
				'boundApplicationData')
			if bound_application_data:
				id_application = bound_application_data.get('id_application')
				if id_application:
					print(id_application)
				else:
					print("Erreur: id_application non trouvé dans la réponse.")
			else:
				print("Erreur: boundApplicationData non trouvé dans la réponse.")
		else:
			print("Erreur: resasocialAccountData est None dans la réponse.")

	# Build slots
	start_h, start_min, end_h, end_min = 00, 00, 22, 00

	calendar = dict()
	days = [('monday', 0), ('tuesday', 1), ('wednesday', 2), ('thursday', 3), ('friday', 4), ('saturday', 5), ('sunday', 6)]
	# days = [('monday', 0)]
	for t in user['slots']:
		weekday = next_weekday(d, t[1])
		search_start = datetime.datetime(
			weekday.year, weekday.month, weekday.day, start_h, start_min)
		search_end = datetime.datetime(
			weekday.year, weekday.month, weekday.day, end_h, end_min)

		slots = get_slots(session, search_start.timestamp(), search_end.timestamp(
		), datetime.datetime.now().timestamp(), id_application)
		eligible_slots = [s for s in slots if '18:30:00' in s['start']]

		if len(eligible_slots) == 1:
			assert len(eligible_slots) == 1
			slot = eligible_slots[0]

			calendar[t[0]] = {
				'start': slot['start'],
				'end': slot['end'],
				'slot_id': slot['id_activity_calendar']
			}

	for k, v in calendar.items():
		print(
			f"Booking for {k}, {v['start']} and {v['end']} and id {v['slot_id']} ")
		book_res = book(session, v['slot_id'])
		book_res = json.loads(book_res.content)
		if options.verbose:
			print(json.dumps(book_res, indent=4, sort_keys=True))

if __name__ == "__main__":

	parser = optparse.OptionParser()

	parser.add_option('-m', '--multi-users', action="store_true", dest="multi_users", default=False, help="Run the script for all users in the json file")
	parser.add_option('-u', '--user', action="store", dest="account", help="Login of the user for mono user mode")
	parser.add_option('-p', '--password', action="store", dest="password", help="Password of the user for mono user mode")
	parser.add_option('-f', '--first-connexion', action="store_true", dest="first_connexion", default=False, help="If it's the first connexion of the user, the script will show your id_application & id_category_activity. Better to use this mode in mono user mode")
	parser.add_option('-v', '--verbose', action="store_true", dest="verbose", default=False, help="Verbose mode")
	parser.add_option('-d', '--debug', action="store_true", dest="debug", default=False, help="Debug mode")

	options, _ = parser.parse_args()

	if options.debug:
		print("Debug mode")
		print(get_session_id(session, id_application))

	if options.first_connexion:
		print("First connexion mode : WIP")
		exit(0)

	if options.multi_users:
		print("Multi users mode")
		for user in data['users']:
			main(user)
			time.sleep(5)
	else:
		print("Mono user mode")
		main(options.account, options.password)

# TODO : clean up the code with a common_headers' dict
