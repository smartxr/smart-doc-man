function runSearch(page = 1) {
    // Get seed message
    var searchPhrase = document.getElementById("srchPhrase").value;
    if (searchPhrase.trim() === "") return;

    // Show spinner
    $('#PDloader, .PDloading').css('display' , 'block');
    // var spinner = document.createElement("div");
    // spinner.className = "spinner";
    // document.body.appendChild(spinner);


    // Send user message to server
    fetch('/run_search'
        + '?search_query=' + encodeURIComponent(searchPhrase)
        + '&search_resource=' + document.getElementById("resourceSelector_srch").value
        + '&search_index=' + document.getElementById("indexSelector_srch").value
        + '&page=' + page,
        {method: 'GET', }
    )
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            var srchCountLabel = document.getElementById("search_count_label");
            srchCountLabel.innerHTML = data.result["count"];


            var searchFlow = document.getElementById("search-flow");
            
            // Update chat history with user message
            searchFlow.innerHTML = ``;
            // searchFlow.innerHTML = `
            //     <div class="user-message">
            //         ${data.result["count"]}
            //     </div>`;

            //data.messages

            // Update chat history with server response
            // for (let message in data.messages) {
            //     chatFlow.innerHTML += `
            //         <div>
            //             <span class="message-timestamp">${message.timestamp}</span><br>
            //             <span class="message-party">${message.role}:</span>
            //             <span>${message.content}</span><br>
            //             <span>${message}</span>
            //         </div>`;
            // }
            
            // Update chat history with server response
            for (let value of data.result["values"]) {

                // Building Highlights section
                let highlights_html = "";
                if (value.highlights !== undefined && Array.isArray(value.highlights) && value.highlights.length > 0) {
                    for (let highlight of value.highlights) {
                        highlights_html += `<p class="highlight">${ highlight }</p>`
                    }
                }
                else {
                    highlights_html = `<span><i>No highlights provided</i></span>`
                }
                
                // Building Captions section
                let captions_html = "";
                if (value.captions !== undefined && Array.isArray(value.captions) && value.captions.length > 0) {
                    for (let caption of value.captions) {
                        captions_html += ` <p class="highlight">${ caption }</p>`
                    }
                }
                else {
                    captions_html = `<span><i>No captions provided</i></span>`
                }

                // Bulding completed chat message
                //<div style="max-width: 98%;">
                //<div class="extended-frame">
                searchFlow.innerHTML += `
                    <div style="max-width: 98%;">
                        <div>
                            <p>
                                <span class="searchtitle">${ value.filename }</span><br>
                                <span class="searchurl">${ value.url }:</span>
                            </p>
                        </div>
                        <div class="searchresults">
                            <p><b>Highlights:</b></p>
                            ${ highlights_html }
                            <p><b>Captions:</b></p>
                            ${ captions_html }
                        </div>
                    </div>`;
            }

            
            // chatFlow.innerHTML += `
            //     <div>
            //         <span>${data.messages}</span>
            //     </div>`;

            // conversationHistory = data.chathistory

            // Push scrolling to the bottom of chat-flow
            // var chatThread = document.getElementById("chat-thread");
            // chatThread.scrollTop = chatThread.scrollHeight;

            // Enable send button and remove spinner
            // document.getElementById("send-button").disabled = false;
            // document.body.removeChild(spinner);
            $('#PDloader, .PDloading').css('display' , 'none');
            
            // Clear user input
            // document.getElementById("prompt-textarea").value = "";
        } else {
            console.error('Error in sending message:', data.message);
            $('#PDloader, .PDloading').css('display' , 'none');
            
            alert('Error: ' + data.message);
        }
    });

    // Clear user input
    // document.getElementById("prompt-textarea").value = "";
}