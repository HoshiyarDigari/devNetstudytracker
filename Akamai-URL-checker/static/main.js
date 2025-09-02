function toggleVisiblity (elementID) {
    const element = document.getElementById(elementID)
    if (element.style.display=="none"){
        element.style.display="block"
    }
    else {
        element.style.display="none"
    }
    
} 

document.getElementById("rawButton").addEventListener(onclick, toggleVisiblity(rawButton))
