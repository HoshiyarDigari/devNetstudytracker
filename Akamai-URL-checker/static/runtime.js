// We only invoke the JS functions once the page is fully loaded
window.addEventListener("DOMContentLoaded", ()=>{
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
            // function to POST form data
            document.getElementById('debugUrlFormSubmit').addEventListener('click',(event)=>{
                // stop default action of submit to POST data
                event.preventDefault();
                // capture the form values
                const form = document.getElementById('inputForm');

                
                //POST data
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