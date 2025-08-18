import requests, argparse
def app():
    """
    This app performs network requests with akamai debug headers. 
    """

    # create parser
    parser = argparse.ArgumentParser(description="Provide a list of URLs and the domain. Additionally you can provide headers and cookies to the requests. The results will be saved as output.txt by default. You can provide output file name optionally.")

    # add arguments
    parser.add_argument("-d", "--domain" , help="Specify the domain to send HTTPS requests to" )
    parser.add_argument("-f", "--file", default="urls.txt", help="The location of the file with the list of URLs separated by line breaks")
    # append action will create a list with the headers passed in by user
    #parser.add_argument("-H", "--headers", action="append", help= "Any additional header to add to the HTTP request")
    parser.add_argument("-c", "--cookies", help="Add cookie to the request example province=ON")
    
    #read the inputs
    args = parser.parse_args()
    akamai_debug_headers = "akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-true-cache-key, akamai-x-get-extracted-values, akamai-x-get-ssl-client-session-id, akamai-x-serial-no, akamai-x-get-request-id, akamai-x-get-brotli-status"

    print(args.domain, args.cookies, args.file)


    
    

    

if __name__ == "__main__":

    app()