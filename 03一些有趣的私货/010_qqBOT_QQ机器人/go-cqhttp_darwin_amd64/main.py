from flask import Flask, request
import requests
app = Flask(__name__)


@app.route('/', methods=["GET","POST"])
def post_data():
        while True: 
            url="http://127.0.0.1:5700/send_private_msg"
            params = {'user_id': 1729655011,
                      'message':"test" }
            requests.get(url,params=params)
            #uid = request.get_json().get('sender').get('user_id') 
            #message = request.get_json().get('message')
            #params["user_id"]=uid
            
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5701)