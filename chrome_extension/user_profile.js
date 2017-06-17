function getUserIDfromPage(){
    return $('sup.nfm').text();
}

function renderUserBullettins(bulletinUrls){
    $('dl.uprofile-info:first-child').append('<dt>Другие объявления</dt>');
    bulletinUrls.forEach(function(url){
        $('dl.uprofile-info:first-child').append('<a href="' + url + '">' + url + '</a>')
        $('dl.uprofile-info:first-child').append('<br/>')
    });
}

var userId = getUserIDfromPage();
chrome.runtime.sendMessage({agent: userId}, function(response) {
    $('dl.uprofile-info:first-child').append('<dt>Вероятность, что агент</dt');
    if (response.error || response.is_agent_probability === -1){
        $('dl.uprofile-info:first-child').append('<dd>Неизвестно</dd');
    } else {
        $('dl.uprofile-info:first-child').append('<dd>' + response.is_agent_probability +  '</dd>');
        renderUserBullettins(response.posts);
    }
});
