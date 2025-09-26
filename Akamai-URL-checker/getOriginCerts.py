from OpenSSL import SSL, crypto
from flask import render_template
import socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def parse_pem_cert(pem_cert):
    """
    input: pem encoded certificate file
    output: parsed information of the cert as json object
    """
    cert = x509.load_pem_x509_certificate(pem_cert.encode(), default_backend())
    try: 
        san = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
        san_list = [name.value for name in san]
    except Exception:
        san_list=[]
    
    return {
            "subject": cert.subject.rfc4514_string(),
            "issuer": cert.issuer.rfc4514_string(),
            "serial_number": str(cert.serial_number),
            "not_valid_before": cert.not_valid_before.isoformat(),
            "not_valid_after": cert.not_valid_after.isoformat(),
            "signature_algorithm": cert.signature_algorithm_oid._name,
            "san": san_list
        }



def get_origin_cert(origin, host):
    '''
    Returns the certificate on origin for the server name host
    '''
    # context
    context = SSL.Context(SSL.TLS_CLIENT_METHOD)
    # verify
    context.set_verify(SSL.VERIFY_NONE, callback = lambda *args: True)
    # socket
    sock = socket.create_connection((origin, 443))
    # wrap 
    secure_sock = SSL.Connection(context, sock)
    # set the SNI header
    secure_sock.set_tlsext_host_name(host.encode())
    # handshake
    secure_sock.set_connect_state()
    secure_sock.do_handshake()
    # get cert
    certs = secure_sock.get_peer_cert_chain()
    
    #convert the certs to PEM format
    certs_pem =  [crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode() for cert in certs]

    # extract information from the pem certs and create json return object
    cert_details = dict()
   
    for i, pem in enumerate(certs_pem):
        #cert_type = pem._cert_type()
        parsed = parse_pem_cert(pem)
        cert_details[i] = parsed
    cert_details[10] = certs_pem
    return render_template("originCertCheckerResponse.html", output=cert_details)