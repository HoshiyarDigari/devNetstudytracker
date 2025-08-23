import requests
from flask import render_template
import http.client
http.client._MAXHEADERS = 200 # Akamai Debug returns more than 100 headers , this increases the value beyond the 100 limit by default

def get_response(domain, path, request_headers, request_cookies,network):
    """
        Gets the response headers for HTTP GET request to the domain and path, optionally can be passed additional headers and cookies
        Args:
            domain: the hostname for the web server
            path: the path along with query strings(if any)
            akamai_headers: list of request headers 
            request_cookies: list of request cookies
        Returns:
            index.html with output area populated with data from response of the http request
    """
    caching_headers=[]
    cookie_headers=[]
    akamai_debug_headers=[]
    other_headers=[]
    processing_errors=[]
    status_code = []
    body =[]
    try:

        response = requests.get(f"https://{domain}{path}", headers=request_headers, cookies=request_cookies,timeout=30)
        status_code.append(f"status_code:{response.status_code}")
        body.append(f"Response: {response._content}")
        for key, value in response.headers.items():
            if "cache" in key.lower():
                caching_headers.append(f"{key}:{value}")
            elif "cookie" in key.lower():
                cookie_headers.append(f"{key}:{value}")
            elif "x-akamai" in key.lower():
                akamai_debug_headers.append(f"{key}:{value}")
            else:
                other_headers.append(f"{key}:{value}")
            
    except requests.exceptions.Timeout:
        processing_errors.append(f"Error:Server took too long to respond, Timed out")
    except requests.exceptions.RequestException as err:
        processing_errors.append(f"Error:{err}")

    response_headers = { "status_code":status_code,"caching_headers":caching_headers, "cookie_headers":cookie_headers, "akamai_debug_headers":akamai_debug_headers, "other_headers":other_headers, "Errors":processing_errors, "Text":body}
    return render_template("index.html", output=response_headers)