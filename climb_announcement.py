import requests
from datetime import datetime
from bs4 import BeautifulSoup 

# line_token = os.environ['LINE_NOTIFY_TOKEN']

def send_notification_line(unit_from, name, link):
    error_token = []
    new_token = []
    url = 'https://notify-api.line.me/api/notify'
    with open('oauth/token_list', 'r') as token_file:
        all_token = token_file.read()
        all_token = all_token.split('\n')
    for i in range(len(all_token)):

        headers = {
            'Authorization': 'Bearer ' + all_token[i]    
        }
        data = {
            'message': '\n' + unit_from +'\n' + name + '\n' + link + '\n'
        }
        response = requests.post(url, headers=headers, data=data)
        if(response == '401'):
            error_token.append(all_token[i])
        else:
            new_token.append(all_token[i])
    
    if(len(error_token != 0)):
        with open('new_token', 'w') as token_file:
            for i in new_token:
                token_file.write( i + '\n')
        with open('error_token', 'w') as token_file:
            for i in error_token:
                token_file.write( i + '\n')
            



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
    today_date = datetime.strftime(datetime.now(),'%Y/%m/%d')
    # today_date = '2024/01/25'  ## change after complete
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