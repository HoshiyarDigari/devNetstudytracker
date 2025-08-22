from flask import Flask, render_template, request
from getResponse import get_response
import json


# The app is an instance of the Flask class
app = Flask(__name__)




@app.route('/')
def homepage():
    return render_template('index.html', output='')

@app.route('/akamai-curl', methods=["POST"])
def form_handler():
    domain = request.form.get('hostname')
    path = request.form.get('path')
    akamai_headers = {"pragma":"akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-true-cache-key,akamai-x-get-extracted-values", "x-akamai-debug":"RogersFidoHeaders"}
    user_headers = request.form.get('request_headers')
    if user_headers:
        user_headers_list = user_headers.split() #splits at each space in the user headers string from the form
        for h in user_headers_list:
            name, value = h.split(':',1)
            akamai_headers[name.strip()] = value.strip() # strip removes whitespaces from the strings
    request_cookies={}
    user_cookies= request.form.get('request_cookies')
    if user_cookies:
        user_cookies_list = user_cookies.split("\n")
        for cookie in user_cookies_list:
            name, value = cookie.split("=",1)
            request_cookies[name.strip()]=value.strip()
    network = request.form.get('network')

    result= get_response(domain, path, akamai_headers, request_cookies,network)
    output = json.loads(result.get_data(as_text=True))
    return render_template('index.html', output=output)

# this ensures that this code is running directly and not as a imported module
if __name__ == "__main__":
    app.run( port=13001, debug=True)