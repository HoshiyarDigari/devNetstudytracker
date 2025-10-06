import requests
from flask import render_template, jsonify
from akamai.edgegrid import EdgeGridAuth, EdgeRc


def get_geo_location():
    edgerc = EdgeRc('~/.edgerc')
    section = 'default'
    hostname = edgerc.get(section, 'host')
    url = "https://akab-xlrfq5l7edeuvxbc-bndequkrcni7wk3p.luna.akamaiapis.net/edge-diagnostics/v1/verify-locate-ip"
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
 
    auth = EdgeGridAuth.from_edgerc(edgerc, section)
    payload = {"ipAddress": "192.0.2.12"}
    
    response = requests.post(url, headers=headers, json=payload, auth=auth)
    output = response.json()
    print(response.status_code, output)
    return render_template('geoLocationResponse.html', output=output)