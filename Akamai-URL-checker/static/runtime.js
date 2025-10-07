function changeVisibility(clickElementId, targetElementId) {
    document.getElementById(clickElementId).addEventListener('click', () => {
        const targetElement = document.getElementById(targetElementId);
        const clickElement = document.getElementById(clickElementId);

        const currentDisplay = window.getComputedStyle(targetElement).display;

        // we store in data-* attribute the original value of the display if it is not none, so we can use it to restore the display
        if (!targetElement.dataset.original_display && currentDisplay!=='none') {
            targetElement.dataset.original_display=window.getComputedStyle(targetElement).display;
            console.log('saved the original display value', targetElement.dataset.original_display);
        }


        if (currentDisplay === 'none') {
            targetElement.style.display= targetElement.dataset.original_display || "flex";
        }
        else {
            targetElement.style.display='none'
        }

    })
}

function submitGeoLocationForm() {
    // ensure that only one of the input forms is filled in, this grays out the host input if ip address input is filled in and vice versa

    const hostInput = document.getElementById('geoByHostInput')
    const ipInput = document.getElementById('geoByIPInput')

    document.getElementById('geoLocationSubmit').addEventListener('click', (event)=>{
        event.preventDefault();
        const form = document.getElementById('geoLocationForm')
        const payload = new FormData(form)
        if (ipInput.value && hostInput.value) {
            alert("You can only check with either the Ip or the Hostname")
            ipInput.value='';
            hostInput.value = '';
        }
        else {
            fetch('/geo-location', {
                method:'POST',
                body: payload

            })
            .then (response => {
                return response.text()
            })
            .then (html => {
                document.getElementById('toolArea').innerHTML= html
            })
            .catch (error => {
                document.getElementById('toolArea').innerHTML=`<h2>error occurred ${error}</h2>`
            })
        }
    })

    
}
function parseRawHeaders(){
    // capture status code
    const statusCode = document.getElementById("status_code").textContent;
    let redirectUrl = '';
    let status = "FAIL";
    if (statusCode >= 200 && statusCode <=299 ){
        status = "Success"
    }
    if (statusCode >=300 && statusCode <=399){
        status = "Redirect" ;
        redirectUrl = document.getElementById("Location").textContent.trim();
    }
    let message = `The request was ${status} with HTTP status code ${statusCode}.<br>`;
    if (status === "Redirect") {
        message+=`The redirect location is ${redirectUrl}<br>`
    };
    const propertyName = document.getElementById("name=AKA_PM_PROPERTY_NAME").textContent.replace("value=", '');
    
    const propertyVersion = document.getElementById("name=AKA_PM_PROPERTY_VERSION").textContent.replace("value=",'');
    let edgeIP = document.getElementById("X-Cache").textContent;
    const ipParts = edgeIP.match(/from\s+([^-]+)-([^-]+)-([^-]+)-([^.]+)/);
    if (ipParts) {
        edgeIP = `${ipParts[1]}.${ipParts[2]}.${ipParts[3]}.${ipParts[4]}`; 
    }
    message += `The request was processed by Akamai edge IP ${edgeIP} using rules from property ${propertyName}, version ${propertyVersion}.<br>`;
    let cache_hit = document.getElementById("X-Cache").textContent.trim();
    // cache hit will be true if "HIT" is found in the string else it will be false
    cache_hit = cache_hit.toLowerCase().includes("hit");
    message+= cache_hit? "The response was served from cache.<br><br>": "The response was not from Akamai cache and came from the origin.<br>";
    // check if there is a server header
    const cache_key = document.getElementById('X-Cache-Key').innerText.trim()
    message+=`The cache key is ${cache_key}<br>`
    const origin = document.getElementById("Server")
    if (origin) {
        message+=`The origin server is ${origin.textContent.trim()}.<br>`
    }
    // select all elements whose id begins with ALB string, which should be just one, we then format it to just get teh alb origin name, because we are looking at a cookie value
    let alb_origin =''
    try {
        alb_origin = document.querySelectorAll('[id^="ALB"]')[0].textContent.split(';',1);
    }
    catch (error) {
        alb_origin='';
    }
        
    if (alb_origin) {
        message+=`The request was assigned an ALB origin: ${alb_origin}`;
    }
    // else {
    //     // check if there is a ALB cookie that begins with akaalb
    //     alb_origin = document.querySelectorAll("[id^='akaalb']")[0].innerHTML
    //     if (alb_origin) [
    //         message+=`The request was assigned the alb cookie ${alb_origin}`
    //     ]


    // }
    
    document.getElementById('summary').innerHTML = `<h3>Summary</h3><p>${message}</p>`;
}

function fetchCertCheckForm() {
    document.getElementById('originCertCheck').addEventListener('click', ()=>{
        fetch('/origin-cert-checker')
        .then (response => {
            if (!response.ok) {
                throw new error (`HTTP ERROR; ${response.status}`)
            }
            return response.text()
        })
        .then (html => {
            document.getElementById('toolArea').innerHTML=html;
            submitCertCheckForm()
        })
        .catch ( error =>{
            document.getElementById('toolArea').innerHTML = `<h2>Fetch error ${error}</h2`
        })
    })
}

function submitCertCheckForm(){
    // check if submit button is loaded
    submitAvailable = document.getElementById('originCertCheckerSubmit')
    if (submitAvailable) {
        document.getElementById('originCertCheckerSubmit').addEventListener('click', (event) => {
            event.preventDefault();
            const form = document.getElementById('certCheckForm');
            fetch('/origin-cert-checker', {
                method:'POST',
                body: new FormData(form)
            })
            .then (response => {
                return response.text()
             })
            .then (html => {
                document.getElementById('toolArea').innerHTML = html;
            })
            .catch (error => {
                document.getElementById('toolArea').innerHTML = `<h2>HTTP ERROR: ${error}</h2>`;
            })
    })

    }
}

function fetchGeoLocationForm(){
    document.getElementById('geo-location-finder').addEventListener('click', ()=> {
        fetch('/geo-location')
        .then (response => {
            return response.text();
        })
        .then (html => {
            document.getElementById('toolArea').innerHTML = html;
            changeVisibility("geoByHost", "geoByHostInput");
            changeVisibility("geoByIP", "geoByIPInput");
            submitGeoLocationForm();
        })
        .catch (error => {
            document.getElementById('toolArea').innerHTML = `<pre>error ${error} occured </pre>`
        })
    })
    
}
// We only invoke the JS functions once the page is fully loaded
window.addEventListener("DOMContentLoaded", ()=>{

    // function to toggle menu bar with hamburger menu
    changeVisibility('menuImage','leftMenu')
    // function to get the form for debug url
    document.getElementById('debugUrl').addEventListener('click', ()=>{
        fetch ("/debug-url")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP Error! Status:${response.status} `);
            }
            return response.text()
        })
        .then (html => {
            document.getElementById('toolArea').innerHTML=html;
            // function to toggle the add request headers textarea
            changeVisibility('addReqHeadersButton', 'request_headers')
            // function to toggle the add request cookies textarea
            changeVisibility('addReqCookiesButton','request_cookies')
            
            // function to POST form data
            document.getElementById('debugUrlFormSubmit').addEventListener('click',(event)=>{
                // stop default action of submit to POST data
                event.preventDefault();
                // capture the form values
                const form = document.getElementById('debugUrlForm');

                
                //POST data from the debug url form
                fetch('/debug-url', {
                    method:"POST",
                    body: new FormData(form)
                })
                .then(response => {return response.text()})
                .then(html => {document.getElementById('toolArea').innerHTML = html;
                    parseRawHeaders();
                })
                .catch(error => {console.log('error', error)});
                
                


            } )
        })
        .catch(error => {
            console.error("Fetch Error", error);
        })
    });
    
    // function to fetch the origin Cert checker Input form
    fetchCertCheckForm()
    // function to fetch the geo location form
    fetchGeoLocationForm()

    
})