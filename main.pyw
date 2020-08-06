import requests
import smtplib, ssl
from bs4 import BeautifulSoup
import re
from email.mime.text import MIMEText
from datetime import date
import calendar

def parser():
    # Returns desired Html content
    content = []
    page = requests.get("https://spaceflightnow.com/launch-schedule/")
    soup = BeautifulSoup(page.text, 'html.parser')
    data_launch_names = soup.find_all('span', attrs={'class': 'mission'})
    data_launch_day = soup.find_all('span', attrs={'class': 'launchdate'})
    data_launch_time = soup.find_all('div', attrs={'class': 'missiondata'})

    month_regex = re.compile(r'\w\w\w\. \d')
    # Get matching value into a list
    for (launch, day, launch_time) in zip(data_launch_names, data_launch_day, data_launch_time):
        
        rocket = launch.contents[0].split("•")
        content.append(rocket[0]) # Rocket Name
        content.append(rocket[1]) # Mission Name
        content.append(day.contents[0]) # Day
        time = re.findall(r'\(.*?\)', ((launch_time.text.strip()).split("\n"))[0]) 
        content.append(time[0].split("EDT")[0][1:]) # Time
        if len(list(filter(month_regex.match, content))) > 0: 
            break
        else:
            content = []
    return content
def content_formatter(content):
    # Returns formatted text to be used at email_sender()
    today = date.today()
    content [0] = " - %s: The Rocket %swill take%s at %s"% (content[2], content[0],content[1],content[3])
    content [1] = 'Rocket Launch - %s'% (today.strftime("%d/%m"))
    return content
def email_sender(content):
    port = 465  # 465 For SSL and 587 for TLS/STARTTLS
    smtp_server = "smtp.gmail.com"
    sender_email = "a_sender_email@gmail.com" 
    receiver_email = "a_receiver_email@gmail.com"
    password = input("Type your password and press enter: ")
    message = MIMEText(content[0])
    message['Subject'] = (content[1])
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
def main():
    today = date.today()
    month = today.strftime("%m")
    text_month = (parser()[2][0:3])
    day = today.strftime("%d")
    months_dict = {a: b for b,a in enumerate(calendar.month_abbr)}
    if ((months_dict.get(text_month) == int(month)) and (int(parser()[2][-1]) == int(day))):
        content = parser()
        email_sender(content_formatter(content))
    else:
        pass
main()
