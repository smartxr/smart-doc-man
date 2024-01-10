function publishPaging(page = 1, count = 1) {
    var searchPages = document.getElementById("search_pages");
    searchPages.innerHTML = ``;
    
    if (page !== 1) {
        searchPages.innerHTML += `<a href='javascript:;' onclick='runSearch(${page - 1});'>&laquo;</a>`;
    }

    for (let i = 1; i <= count; i++) {
        if (i === page) {
            searchPages.innerHTML += `<a href='javascript:;' onclick='runSearch(${i});' class="active">${i}</a>`;
        } else {
            searchPages.innerHTML += `<a href='javascript:;' onclick='runSearch(${i});'>${i}</a>`;
        }
    }

    if (page !== count) {
        searchPages.innerHTML += `<a href='javascript:;' onclick='runSearch(${page + 1});'>&raquo;</a>`;
    }
}

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
            var searchPageSize = data.result["page_size"];

            publishPaging(page, data.result["total_pages"]);

            var searchFlow = document.getElementById("search-flow");
            
            // Clear previous Search results
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
            let record_num = (searchPageSize * (page - 1)) + 1;
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
                        captions_html += `<p class="highlight">${ caption }</p>`
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
                            <p class="searchrecordnum"><span>${ record_num++ }</span></p>
                            <p class="searchtitle"><span>${ value.filename }</span></p>
                            <p class="searchurl"><span>${ value.url }</span></p>
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