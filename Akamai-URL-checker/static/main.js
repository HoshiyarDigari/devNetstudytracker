function toggleVisibility (elementID) {
    const element = document.getElementById(elementID)
    if (element.style.display==="none"){
        element.style.display="block"
    }
    else {
        element.style.display="none"
    }
    
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
    message+= cache_hit? "The response was served from cache.<br><br>": "The response was fetched from origin.<br>";
    // check if there is a server header
    const origin = document.getElementById("Server")
    if (origin) {
        message+=`The origin server is ${origin.textContent.trim()}.<br>`
    }
    document.getElementById('summary').innerHTML = `<h3>Summary</h3><p>${message}</p>`;
}

window.addEventListener("DOMContentLoaded", ()=> {
    const currentPath=window.location.pathname;
    if (currentPath==="/akamai-curl"){
        parseRawHeaders();
        toggleVisibility("inputFormArea");
    }
});