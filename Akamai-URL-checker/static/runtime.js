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
                const form = document.getElementById('inputForm');

                
                //POST data from the debug url form
                fetch('/debug-url', {
                    method:"POST",
                    body: new FormData(form)
                })
                .then(response => {return response.text()})
                .then(html => {document.getElementById('toolArea').innerHTML = html})
                .catch(error => {console.log('error', error)});
                
                


            } )
        })
        .catch(error => {
            console.error("Fetch Error", error);
        })
    });

    
})