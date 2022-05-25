from bs4 import BeautifulSoup
import requests, time
from plyer import notification

def tube_status():
    page = requests.get('https://tfl.gov.uk/tube-dlr-overground/status')
    soup = BeautifulSoup(page.content, 'html.parser')

    tube_list = ['bakerloo', 'jubilee', 'metropolitan', 'central', 'victoria', 'elizabeth-line']
    tube_dictionary = {}
    soupBase = soup.find("div", {"class": "service-status-rainbow-board board-wrapper"})
    message = ''

    for tube in tube_list:
        soup = soupBase.find("li", {"class": f"rainbow-list-item {tube}"}) or soupBase.find(
                "li", {"class": f"rainbow-list-item {tube} disrupted expandable"}) 
        soup = soup.find("span", {"class": "disruption-summary"})
        soup = soup.find("span").get_text().strip()

        if soup == 'Good service':
            tube_dictionary[tube] = soup
        elif soup == 'Minor delays':
            tube_dictionary[tube] = soup     

    message = tube_status_summary('Good service', 'Good service on the ', message, tube_dictionary)
    message = tube_status_summary('Minor delays', ' Minor delays on the ', message, tube_dictionary)

    print(message)
    #desktop_notification('Service status', message)
            

def tube_status_summary(summary_status, summary_message, message, tube_dictionary):
    if summary_status in tube_dictionary.values():
        message += summary_message
        for key, value in tube_dictionary.items():
            if value == summary_status:
                if key != '':
                    message += f'{key.title()}, '
        message = message[:-2]
        message += f' line.'
    return message


def desktop_notification(title, message):
    notification.notify(title= title,
                    message= message,
                    app_icon = r'TFL_Logo.ico',
                    timeout= 10,
                    toast=False)

def main():
    while 0 < 1:
        tube_status()
        time.sleep(30)

if __name__ == '__main__':
    main()




"""
    if 'Good service' in tube_dictionary.values():
        message += 'Good service on the '
        for key, value in tube_dictionary.items():
            if value == 'Good service':
                message += f'{key.title()}, '
        message = message[:-2]
        message += f' line.'

    if 'Minor delay' in tube_dictionary.values():
        message += ' \nMinor delays on the '
    for key, value in tube_dictionary.items():
        if value == 'Minor delays':
            if key != '':
                message += f'{key.title()}, '
    message = message[:-2]
    message += f' line.'
"""