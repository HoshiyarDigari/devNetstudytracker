function toggleVisibility (elementID) {
    const element = document.getElementById(elementID)
    if (element.style.display==="none"){
        element.style.display="block"
    }
    else {
        element.style.display="none"
    }
    
} 
// function to toggle between raw Headers output or the Parsed Headers output
function toggleDisplay(elementID){
    const element = document.getElementById(elementID);
    if (element.textContent === "Raw Headers") {
        element.textContent = "Parsed Information";
        parseRawHeaders()
        
    }
    else {
        element.textContent = "Raw Headers"
    }
    toggleVisibility("rawHeaders");
    toggleVisibility("parsedHeaders")
}
// onclick handler for the output type button
document.getElementById("displayTypeButton").addEventListener("click", () => { toggleDisplay("displayTypeButton");});

// function to extract values for displaying in parsed output.

function parseRawHeaders(){
    let propertyName = document.getElementById("name=AKA_PM_PROPERTY_NAME").textContent;
    propertyName = propertyName.replace("value=",'');
    let propertyVersion = document.getElementById("name=AKA_PM_PROPERTY_VERSION").textContent;
    propertyVersion = propertyVersion.replace("value=",'');
    let edgeIP = document.getElementById("X-Cache").textContent;
    const match = edgeIP.match(/from\s+([^-]+)-([^-]+)-([^-]+)-([^.]+)/);
    if (match) {
        edgeIP = `${match[1]}.${match[2]}.${match[3]}.${match[4]}`; 
    }
    let message = `The request was processed by Akamai edge IP ${edgeIP} using rules from property ${propertyName}, version ${propertyVersion}.\n`;
    let cache_hit = document.getElementById("X-Cache").textContent.trim();
    // cache hit will be true if "HIT" is found in the string else it will be false
    cache_hit = cache_hit.toLowerCase().includes("hit");
    message+= cache_hit? "The response was served from cache": "The response was fetched from origin";
    document.getElementById('parsedMessage').textContent = message;
}