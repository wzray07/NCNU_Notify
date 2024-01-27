import uuid
from flask import Flask, render_template, request
from lotify.client import Client
import requests

CLIENT_ID = "Dj1tRApv8HZfBjUWj0dNOe"
SECRET = "EzLJPlSm7wRYzdxHO4FNS8VbkEXANEFCcN3DE58BWgE"
URI = "http://localhost:8080/callback/"
lotify = Client(client_id=CLIENT_ID, client_secret=SECRET, redirect_uri=URI)

app = Flask(__name__)

def store_info(token):
    with open('token_list', 'a') as token_file:
        token_file.write( token + '\n')

def welcome_notification(token):
    # check before send
    with open('token_list', 'r') as token_file:
        all_token = token_file.read()
        all_token = all_token.split('\n')
    if token not in all_token:
        return False
    
    url = 'https://notify-api.line.me/api/notify'
    headers = {
        'Authorization': 'Bearer ' + token    
    }
    data = {
        'message': "已與暨大最新公告 2.0 完成連動，如有任何問題請詢問開發者"+ '\n' + '問題與使用意見回饋: '+ '\n' + 'https://github.com/wzray07/NCNU_Notify/issues'
    }
    response = requests.post(url, headers=headers, data=data)

    if(response.status_code != 200):
        return False
    
    return True

@app.route("/")
def home():
    link = lotify.get_auth_link(state=uuid.uuid4())
    return render_template("index.html", auth_url=link)

@app.route("/callback")
def complete():
    token = lotify.get_access_token(code=request.args.get("code"))
    store_info(token)
    response = welcome_notification(token)
    if(response == False):
        return render_template("error.html")
    
    return render_template("callback.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)