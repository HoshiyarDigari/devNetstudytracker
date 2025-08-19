import http.client, json
http.client._MAXHEADERS = 200 
import requests, argparse

def send_request(domain:str, url:str, akamai_headers:dict, request_cookies:dict)->str:
        """
        Gets the response headers for HTTP GET request to the domain and url, optionally can be passed additional headers and cookies
        Args:
            domain: the hostname for the web server
            url: the URL along with query strings(if any)
            akamai_headers: list of request headers 
            request_cookies: list of request cookies
        Returns:
            A json string containing response headers with following keys
                - Error details : Details if there was an Error doing the GET request
                - Status Code : HTTP response status code
                - Caching headers: respopnse header about caching behaviour
                - cookie headers: response headers that set cookie
                - Akamai debug information: Akamai specific headers for troubleshooting
                - other headers: rest of the response headers including Akamai debug headers
                
        """
        result=[]
        try:

            response = requests.get(f"{domain}{url}", headers=akamai_headers, cookies=request_cookies,timeout=30)
            status_code= response.status_code
            for key, value in response.headers.items():
                if "cache" in key.lower():
                    result.append(f"{key}:{value}")
                elif "cookie" in key.lower():
                    result.append(f"{key}:{value}")
                elif "x-akamai" in key.lower():
                    result.append(f"{key}:{value}")
                else:
                    result.append(f"{key}:{value}")
                
        except requests.exceptions.Timeout:
            result.append(f"Error:Server took too long to respond, Timed out")
        except requests.exceptions.RequestException as err:
            result.append(f"Error:{err}")

        data = ''.join(result)
        return json.dumps(data)   


def main():
    """
    This app performs network requests with akamai debug headers. 
    """

    # create parser
    parser = argparse.ArgumentParser(description="Provide a list of URLs and the domain. Additionally you can provide headers and cookies to the requests. The results will be saved as output.txt by default. You can provide output file name optionally.")

    # add arguments
    parser.add_argument("-d", "--domain", required=True , help="Specify the domain to send HTTPS requests to" )
    parser.add_argument("-f", "--file", help="The location of the file with the list of URLs separated by line breaks")
    
    # append action will create a list with the headers passed in by user
    parser.add_argument("-H", "--headers", action="append", help= "Any additional header to add to the HTTP request, use it multiple times to add multiple headers")
    parser.add_argument("-c", "--cookies",action = "append", help="Add cookie to the request example province=ON")
    parser.add_argument("-u", "--url", help="url to send HTTP request to")



    #read the inputs
    args = parser.parse_args()

    #enforce either file or url is present
    if not args.url and not args.file:
        parser.error("You must provide either --file or --url")
    if args.url and args.file:
        parser.error("You must provide either a URL or the URL file, but not both")

    # dictionary to hold the headers to send in the HTTP request
    akamai_headers = {"pragma":"akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-true-cache-key,akamai-x-get-extracted-values", "x-akamai-debug":"RogersFidoHeaders"}
    
    if args.headers:
        for h in args.headers:
            name, value = h.split(":", 1)
            akamai_headers[name.strip()] = value.strip()
    
    request_cookies= {}

    if args.cookies:
        for cookie in args.cookies:
            key, value = cookie.split("=",1)
            request_cookies[key.strip()]=value.strip()
    
         
        #print(response.text)
    
    if args.url:

        result = send_request(args.domain, args.url, akamai_headers, request_cookies)
        print(result)
    elif args.file:
        try:
            with open(args.file, 'r') as file:
                for line in file:
                    result = send_request(args.domain, line, akamai_headers, request_cookies)
                    print(result,"\n")
        except FileNotFoundError:
            print(f"File couldn't be found in the current directory. Provide absolute or relative path")
            exit(code=2)
    

if __name__ == "__main__":

    main()