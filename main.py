import requests
import time
import json

# initial variables
token = '6108890878:AAFDOGUVkBqFK9nAyyil96EHxd1eWq9NrGk'
base_link = f'https://api.telegram.org/bot{token}/'
file_storage = 'bot_answered_messages.txt'
answered_messages = []

bus_services = {
    "044p": {
        "departure_city": "Kyiv",
        "arrival_city": "Lviv",
        "departure_time": "12:00",
        "arrival_time": "20:00",
        "price": 400,
        "total_number_of_places": 40,
        "free_places": 23,
    },
    "223lk": {
        "departure_city": "Lviv",
        "arrival_city": "Kyiv",
        "departure_time": "14:30",
        "arrival_time": "23:00",
        "price": 500,
        "total_number_of_places": 40,
        "free_places": 35,
    }
}

def read_answered_messages():
    global answered_messages
    f = open(file_storage, 'r')
    answered_messages_string = f.read()

    try:
        answered_messages = json.loads(answered_messages_string)
    except:
        pass

def write_answered_message():
    f = open(file_storage, 'w')
    f.write(json.dumps(answered_messages))

def get_update():
    link = base_link + 'getUpdates?offset=-1'
    response = requests.get(link)
    response_dict = response.json()

    if response_dict['result']:
        result = response_dict['result'][0]
    else:
        result = 'No notifications'

    return result

def get_message_text(update):
    return update['message']['text']

def get_chat_id(update):
    return update['message']['chat']['id']

def get_update_id(update):
    return update['update_id']

def send_message(id, text):
    link = base_link + f'sendMessage?chat_id={id}&text={text}'
    requests.get(link)

while True:
    read_answered_messages()
    update = get_update()

    if update != 'No notifications':
        update_id = get_update_id(update)

        if update_id not in answered_messages:
            answered_messages.append(update_id)
            write_answered_message()
            text = get_message_text(update)
            chat_id = get_chat_id(update)
            result = 'Як не знаю, як відповісти на ваш запит'

            print(f"Last notification: {text} from user (id): {chat_id}")

            if text == 'help' or text == '/help':
                result = '/help - перелік команд\n/schedule - подивитися графік рейсів'

            if text == '/schedule':
                result = 'Графік рейсів\n\n'

                for bus_service_id, bus_service_info in bus_services.items():
                    result += "Рейс № " + bus_service_id + "\n"

                    for key, value in bus_service_info.items():
                        result += key + ': ' + str(value) + '\n'

                    result += '\n'

            send_message(chat_id, result)
    else:
        print('No notifications')

    time.sleep(1)
