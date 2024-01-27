import requests
from datetime import datetime
from bs4 import BeautifulSoup 

# line_token = os.environ['LINE_NOTIFY_TOKEN']
line_token = ''

def send_notification_line(unit_from, name, link):
    url = 'https://notify-api.line.me/api/notify'
    headers = {
        'Authorization': 'Bearer ' + line_token    
    }
    data = {
        'message': unit_from +'\n' + name + '\n' + link + '\n'
    }
    data = requests.post(url, headers=headers, data=data)

def check_and_send(name, link, unit_from, record):
    if name in record:
        return
    send_notification_line(unit_from, name, link)
    ## write record
    with open('record_today', 'a') as record_file:
        record_file.write( name + '\n')

def main():
    ## get today record
    with open('record_today', 'r') as record_file:
        record = record_file.read()
        record = record.split('\n')
    data = requests.get('https://www.ncnu.edu.tw/p/422-1000-1.php?Lang=zh-tw', verify=False)
    #today_date = datetime.strftime(datetime.now(),'%Y/%m/%d')
    today_date = '2024/01/25'  ## change after complete
    soup = BeautifulSoup(data.text, "lxml")
    ## listTB table
    findData = soup.find(class_ = 'listTB table')
    ## Date -> name -> from 
    ## get one data -> check date -> check record -> send notification
    step = 0
    for i in findData.find_all(class_ = 'd-txt'):
        if(step % 3 == 0):
            announcement_date = i.text.strip()
        elif(step % 3 == 1):
            link = i.find(class_ = 'mtitle').a['href']
            name = i.find(class_ = 'mtitle').a.text.strip()
        else:
            unit_from = i.text.strip()
            if(announcement_date != today_date):
                break
            check_and_send(name, link, unit_from, record)
        step += 1

if __name__ == '__main__':
    main()