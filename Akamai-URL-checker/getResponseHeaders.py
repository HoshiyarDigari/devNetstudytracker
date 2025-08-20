import requests
from flask import jsonify
import http.client
http.client._MAXHEADERS = 200 # Akamai Debug returns more than 100 headers , this increases the value beyond the 100 limit by default

def get_response_headers(domain, url, request_headers, request_cookies,network):
    """
        Gets the response headers for HTTP GET request to the domain and url, optionally can be passed additional headers and cookies
        Args:
            domain: the hostname for the web server
            url: the URL along with query strings(if any)
            akamai_headers: list of request headers 
            request_cookies: list of request cookies
        Returns:
            A JSON string containing response headers with following keys
                - processing_errors : Details if there was an Error doing the GET request
                - Status Code : HTTP response status code
                - Caching headers: respopnse header about caching behaviour
                - cookie headers: response headers that set cookie
                - Akamai debug information: Akamai specific headers for troubleshooting
                - other headers: rest of the response headers including Akamai debug headers
                
    """
    caching_headers=[]
    cookie_headers=[]
    akamai_debug_headers=[]
    other_headers=[]
    processing_errors=[]
    status_code = str()
    try:

        response = requests.get(f"https://{domain}{url}", headers=request_headers, cookies=request_cookies,timeout=30)
        status_code = response.status_code
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

    response_headers = { "status_code":status_code,"caching_headers":caching_headers, "cookie_headers":cookie_headers, "akamai_debug_headers":akamai_debug_headers, "other_headers":other_headers, "processing errors":processing_errors}
    return jsonify(response_headers)