'use strict';
$(document).ready(function() {

    function getMessages(response) {
        var count = 0;
        for (var i = 0; i < response['data']['result'].length; i++) {
            count += response['data']['result'][i]['values'].length;
        }
        return count;
    }

    function getBytes(response) {
        const size = new TextEncoder().encode(JSON.stringify(response)).length
        const kiloBytes = size / 1024;
        const megaBytes = kiloBytes / 1024;        
        return kiloBytes;
    }

    function getTopics(response) {
        for (var i = 0; i < response['data']['result'].length; i++) {
            return response['data']['result'][i]['metric']['topic'];
        }
    }


    var url = "http://10.0.0.67:9090/api/v1/query_range?query=received_messages&start=1618276878&end=1618335953&step=20s";
    $.getJSON(url, function(response) {
        getMessages(response);
        $("#test").append(getMessages(response));
    });

    $.getJSON(url, function(response) {
        $("#bytes").append(getBytes(response) + " kB");
    });
});
