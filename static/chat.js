let conversationHistory = [];
        
function sendMessage() {
    // Get seed message
    var seedMessage = document.getElementById("chatseed-textarea").value;
    if ((seedMessage.trim() !== "") && (conversationHistory.length === 0))
        conversationHistory.push({ role: 'system', content: seedMessage });

    // Get user message
    var userMessage = document.getElementById("prompt-textarea").value;
    if (userMessage.trim() === "") return;

    // conversationHistory = document.getElementById("chat-history").innerHTML;
    // conversationHistory += userMessage;
    conversationHistory.push({ role: 'user', content: userMessage });

    // Disable send button
    document.getElementById("send-button").disabled = true;

    // Show spinner
    $('#PDloader, .PDloading').css('display' , 'block');
    // var spinner = document.createElement("div");
    // spinner.className = "spinner";
    // document.body.appendChild(spinner);


    // Send user message to server
    fetch('/send_message', {
        method: 'POST',
        headers: {
            // 'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Type': 'application/json',
        },
        // body: 'user_message=' + encodeURIComponent(userMessage),
        // body: 'user_message=' + encodeURIComponent(userMessage) + '&ref_id=xyz',
        // body: {user_message: encodeURIComponent(userMessage), conversation_history: conversationHistory}
        body: JSON.stringify({
            user_message: userMessage,
            search_resource: document.getElementById("resourceSelector_chat").value,
            search_index: document.getElementById("indexSelector_chat").value,
            chat_seed: seedMessage,
            chat_history: conversationHistory
        }),
    })            
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            var chatFlow = document.getElementById("chat-flow");
            
            // Update chat history with user message
            chatFlow.innerHTML += `
                <div class="user-message">
                    ${userMessage}
                </div>`;

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
            for (let chat_msg of data.messages) {

                // Building citations section
                let citations_html = "";

                if (chat_msg.context.citations !== undefined && Array.isArray(chat_msg.context.citations) && chat_msg.context.citations.length > 0) {
                    for (let citation of chat_msg.context.citations) {
                        citations_html += `<span><b>${citation.ref_no}</b>: ${citation.filepath} - (${citation.chunk_id})</span><br>
                        <span class="citation-url">${citation.url}</span><br>`
                    }
                }
                else {
                    citations_html += `<span><i>No citations provided</i></span><br>`
                }
                
                // Building intents section
                let intents_html = "";
                if (chat_msg.context.intents !== undefined && Array.isArray(chat_msg.context.intents) && chat_msg.context.intents.length > 0) {
                    for (let intent of chat_msg.context.intents) {
                        intents_html += `<span>${intent}</span><br>`
                    }
                }
                else {
                    intents_html += `<span><i>No intentions provided</i></span><br>`
                }

                // Bulding completed chat message
                chatFlow.innerHTML += `
                    <div>
                        <p>
                            <span class="message-timestamp">${chat_msg.timestamp}</span><br>
                            <span class="message-party">${chat_msg.role}:</span>
                            <span>${chat_msg.content}</span><br>
                        </p>
                        <details>
                            <summary><i>Expend additional context provided by</i> <b>${chat_msg.context.role}</b></summary>
                            <p>
                                <span><i>Citations</i>:</span><br>${citations_html}<br>
                            </p>
                            <p>
                                <span><i>Intents</i>:</span><br>${intents_html}<br>
                            </p>
                        </details>
                    </div>`;
            }

            
            // chatFlow.innerHTML += `
            //     <div>
            //         <span>${data.messages}</span>
            //     </div>`;

            conversationHistory = data.chathistory

            // Push scrolling to the bottom of chat-flow
            var chatThread = document.getElementById("chat-thread");
            chatThread.scrollTop = chatThread.scrollHeight;

            // Enable send button and remove spinner
            document.getElementById("send-button").disabled = false;
            // document.body.removeChild(spinner);
            $('#PDloader, .PDloading').css('display' , 'none');

            // Clear user input
            document.getElementById("prompt-textarea").value = "";
        } else {
            console.error('Error in sending message:', data.message);
        }
    });

    // Clear user input
    // document.getElementById("prompt-textarea").value = "";
}

function clearChat() {
    document.getElementById("chat-flow").innerHTML = "";
    conversationHistory = [];
    // var seedMessage = document.getElementById("chatseed-textarea").value;
    // if (seedMessage.trim() !== "")
    //     conversationHistory.push({ role: 'system', content: seedMessage });
    // Clear chat history on the server
    // fetch('/clear_chat', {
    //     method: 'POST',
    // })
    // .then(response => response.json())
    // .then(data => {
    //     if (data.status === 'success') {
    //         // Clear chat history on the client side
    //         document.getElementById("chat-flow").innerHTML = "";
    //         conversationHistory = [];
    //     } else {
    //         console.error('Error in clearing chat:', data.message);
    //     }
    // });
}
