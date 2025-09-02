from flask import Flask, render_template, request
from getResponse import get_response
import json
import dns.resolver
import re



# The app is an instance of the Flask class
app = Flask(__name__)




@app.route('/')
def homepage():
    return render_template('index.html', output='')

@app.route('/akamai-curl', methods=["POST"])
def form_handler():
    akamai_headers = {"pragma":"akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-true-cache-key,akamai-x-get-extracted-values", "x-akamai-debug":"RogersFidoHeaders"}
    domain = request.form.get('hostname')
    # if staging is selected, we need to find the staging CNAME
    def get_staging_cname(edgehost):
        try:
            return re.sub(r'(edgesuite|akamaiedge|edgekey)(\.net)',r'\1-staging\2',edgehost)
        except Exception as e:
            return render_template('errors.html', errors=str(e))
    if request.form.get('network') == "staging":
        akamai_headers["host"] = domain
        try:
            answers=dns.resolver.resolve(domain, 'CNAME')
            edgehost=str(answers[0].target)
            domain=get_staging_cname(edgehost)
        except dns.resolver.NoAnswer:
            return render_template("errors.html", errors=f"NO CNAME record found for {domain}")   
        except dns.resolver.NXDOMAIN:
            return render_template('errors.html', errors=f"NO DNS record for {domain}")
        except Exception as e:
            return render_template('errors.html', errors=f"Unexpected error")

    path = request.form.get('path')
    user_headers = request.form.get('request_headers')
    if user_headers:
        user_headers_list = user_headers.split("\n") #splits at each new line in the user headers string from the form
        for h in user_headers_list:
            try:
                name, value = h.split(':',1)
                akamai_headers[name.strip()] = value.strip() # strip removes whitespaces from the strings
            except ValueError as e:
                return render_template('errors.html', error=f"The request header line {h} is not valid format")
    request_cookies={}
    user_cookies= request.form.get('request_cookies')
    if user_cookies:
        user_cookies_list = user_cookies.split("\n")
        for cookie in user_cookies_list:
            try:
                name, value = cookie.split("=",1)
                request_cookies[name.strip()]=value.strip()
            except ValueError as e:
                return render_template('errors.html', error=f"The request cookie {cookie} is not valid format")
    network = request.form.get('network')

    result= get_response(domain, path, akamai_headers, request_cookies,network)
    #output = json.loads(result.get_data(as_text=True))
    return result

# this ensures that this code is running directly and not as a imported module
if __name__ == "__main__":
    app.run( port=13001, debug=True)