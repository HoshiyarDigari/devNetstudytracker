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
    let message = `The request was ${status} with ${statusCode}<br>`;
    if (status === "Redirect") {
        message+=`The redirect location is ${redirectUrl}<br>`
    };
    let propertyName = document.getElementById("name=AKA_PM_PROPERTY_NAME").textContent;
    propertyName = propertyName.replace("value=",'');
    let propertyVersion = document.getElementById("name=AKA_PM_PROPERTY_VERSION").textContent;
    propertyVersion = propertyVersion.replace("value=",'');
    let edgeIP = document.getElementById("X-Cache").textContent;
    const match = edgeIP.match(/from\s+([^-]+)-([^-]+)-([^-]+)-([^.]+)/);
    if (match) {
        edgeIP = `${match[1]}.${match[2]}.${match[3]}.${match[4]}`; 
    }
    message += `The request was processed by Akamai edge IP ${edgeIP} using rules from property ${propertyName}, version ${propertyVersion}.<br><br>`;
    let cache_hit = document.getElementById("X-Cache").textContent.trim();
    // cache hit will be true if "HIT" is found in the string else it will be false
    cache_hit = cache_hit.toLowerCase().includes("hit");
    message+= cache_hit? "The response was served from cache.<br>": "The response was fetched from origin.<br>";
    document.getElementById('parsedMessage').innerHTML = message;
}

window.addEventListener("DOMContentLoaded", ()=> {
    const currentPath=window.location.pathname;
    if (currentPath==="/akamai-curl"){
        parseRawHeaders();
        toggleVisibility("inputFormArea");
    }
});