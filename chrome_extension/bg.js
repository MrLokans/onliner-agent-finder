chrome.runtime.onMessage.addListener(getAgentData);


function getAgentData(request, sender, sendResponse){

    var getAgentSuccess = function(resp){
        sendResponse(resp);
    };

    var getAgentError = function(resp){
        sendResponse({'error': 'Status is unknown'});
    };

    $.get(config.SERVER_HOST + config.SERVER_API_URL + request.agent)
        .then(getAgentSuccess, getAgentError);
    return true;
}
