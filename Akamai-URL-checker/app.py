from flask import Flask, render_template, request
from getResponseHeaders import get_response_headers



# The app is an instance of the Flask class
app = Flask(__name__)




@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/akamai-curl', methods=["POST"])
def form_handler():
    domain = request.form.get('hostname')
    url = request.form.get('url')
    akamai_headers = {"pragma":"akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-true-cache-key,akamai-x-get-extracted-values", "x-akamai-debug":"RogersFidoHeaders"}
    if not request.form.get('request_headers'):
        request_headers=akamai_headers
    request_cookies= request.form.get('request_cookies')
    network = request.form.get('network')

    result= get_response_headers(domain, url, request_headers, request_cookies,network)
    return result

# this ensures that this code is running directly and not as a imported module
if __name__ == "__main__":
    app.run(debug=True)