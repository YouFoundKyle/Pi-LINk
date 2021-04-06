'use strict';
$(document).ready(function() {
    var url = "http://10.0.0.67:9090/api/v1/query_range?query=received_messages&start=1616993300&end=1617166100&step=20s";
    $.getJSON(url, function(response) {
        $("#test").append(response['data']['result'][0]['values'].length);
	console.log(response['data']['result'][0]['values'].length);
    });
});
