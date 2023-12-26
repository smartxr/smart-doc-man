function srchResourceChange(caller) {
    // console.info('item: ', caller.id);
    var selectedResource = $(caller).val();
    var indexSelector = undefined;
    if (caller.id === 'resourceSelector_srch') {
        indexSelector = $('#indexSelector_srch');
    } else {
        indexSelector = $('#indexSelector_chat');
    }
    // Fetch options for index selector based on the selected resource
    $.get('/get_options/' + selectedResource, function(index_list) {
        // Update options in index selector
        indexSelector.empty();
        $.each(index_list, function(indexId, indexLabel) {
            indexSelector.append($('<option>').text(indexLabel).attr('value', indexId));
        });
    });
}

$(document).ready(function() {
    // Event listener for changes in the resource selector
    // $('#resourceSelector_chat').change(function() {
    //     var selectedResource = $(this).val();
    //     // Fetch options for selector 2 based on the selected resource
    //     $.get('/get_options/' + selectedResource, function(index_list) {
    //         // Update options in selector 2
    //         var indexSelector = $('#indexSelector');
    //         indexSelector.empty();
    //         $.each(index_list, function(indexId, indexLabel) {
    //             indexSelector.append($('<option>').text(indexLabel).attr('value', indexId));
    //         });
    //     });

    //     // Automatically set default selection to the first option
    //     // indexSelector.val(options[0]);
    //     // indexSelector.find('option:first').prop('selected', true);
    //     // TODO: ERROR: jQuery.Deferred exception: indexSelector.find
    //     // indexSelector.find('option:eq(1)').prop('selected', true);
    // });

    $('#resourceSelector_srch').change(function() {
        srchResourceChange(this);
    });
    $('#resourceSelector_srch').trigger('change');      
    
    
    // Trigger change event to populate the second selector with default selection
    $('#resourceSelector_chat').trigger('change');

    // Hide spinner
    // $('#PDloader, .PDloading').css('display' , 'none');

    // Event listener for Ctrl+Enter
    // document.getElementById("prompt-textarea").addEventListener("keydown", function(event) {
    //     // if (event.ctrlKey && event.key === "Enter") {
    //     if (event.ctrlKey && event.keyCode === 13) {
    //         sendMessage();
    //     }
    // });

    // Event listener for Ctrl+Enter
    // document.getElementById("historyItem").addEventListener("click", function(event) {
    //     // if (event.ctrlKey && event.key === "Enter") {
    //     console.info('Hitory Clicked');
    //     // var chatThread = document.getElementById("chat-thread");
    //     // chatThread.disabled = true;
    // });

    tabClick('searchItem');
    
});

const blades = {
    searchItem: 'content-area-search',
    chatItem: 'content-area-chat',
    historyItem: 'content-area-history',
    configItem: 'content-area-config',
    deployItem: 'content-area-deploy'
};

function tabClick(caller_id) {
    for (const [key, value] of Object.entries(blades)) {
        // console.info('item: ', key, ' tab:', value);
        // console.error('Unknown tab clicked:', call_id);
        const threadElement = document.getElementById(value);
        threadElement.style.display = key === caller_id ? 'flex' : 'none';
        const menuElement = document.getElementById(key);
        menuElement.style.backgroundColor = key === caller_id ? 'lightgray' : '';
        menuElement.disabled = key === caller_id ? true : false;
    };
}

//once the form has loaded and initial lookups have run, this section will execute
// $(document).on("onloadlookupfinished", function () {
//     // the following line hides the spinner. 
//     $('#PDloader, .PDloading').css('display' , 'none');
// });
