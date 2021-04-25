'use strict';
$(document).ready(function () {
    setTimeout(function () {
        //Air Controller Temperature Line Chart
        $(function () {
            var ip = document.getElementById('ip_address').textContent;
            var url = "http://" + ip + ":9090/api/v1/query_range?query=temperature&start=1618332873&end=1618335953&step=20s";
            $.getJSON(url, function (response) {

                function getACTemp(response) {
                    var AC = [];
                    for (var j = 0; j < response['data']['result'].length; j++) {
                        var topic = response['data']['result'][j]['metric']['topic'];
                        if (topic == "iot/air_controller/temp") {
                            for (var i = 0; i < response['data']['result'][0]['values'].length; i++) {
                                var pair = [];
                                var timestamp = response['data']['result'][j]['values'][i][0];
                                var temperature = response['data']['result'][j]['values'][i][1];
                                pair.push(timestamp);
                                pair.push(temperature);
                                AC.push(pair);
                            }
                        }
                    }
                    return AC;
                }

                var options = {
                    series: [],
                    chart: {
                        height: 350,
                        width: '100%',
                        type: 'line',
                        toolbar: {
                            show: true,
                            tools: {
                                download: true,
                                selection: true,
                                zoom: true,
                                zoomin: true,
                                zoomout: true,
                                pan: true,
                            },
                        },
                    },
                    dataLabels: {
                        enabled: false
                    },
                    title: {
                        text: 'Temperature Trends',
                    },
                    noData: {
                        text: 'Loading...'
                    },
                    xaxis: {
                        type: 'datetime',
                        tickPlacement: 'on',
                        labels: {
                            rotate: -45,
                            rotateAlways: true,
                            formatter: function (value, timestamp) {
                                return new Date(timestamp * 1000).toISOString().slice(0, 19).replace('T', ' ')
                            },
                        },
                    }
                };

                var chart = new ApexCharts(document.querySelector("#line-chart-1"), options);
                chart.render();
                chart.updateSeries([{
                    name: 'Temperature',
                    data: getACTemp(response),
                }])
            });

            $.noConflict();
            $('#datepicker3').datepicker(
                {
                    onSelect: function () {
                        var currentDate = $("#datepicker3").datepicker("getDate");
                        getTime(currentDate);
                    }
                }
            );
            function getTime(dateText) {
                var ip = document.getElementById('ip_address').textContent;
                var startTime = new Date(dateText).getTime() / 1000;
                var endTime = 1618335953;
                var url = "http://" + ip + ":9090/api/v1/query_range?query=temperature&start=" + startTime + "&end=" + endTime + "&step=120s";
                console.log(url);

                $.getJSON(url, function (response) {

                    function getACTemp(response) {
                        var AC = [];
                        for (var j = 0; j < response['data']['result'].length; j++) {
                            var topic = response['data']['result'][j]['metric']['topic'];
                            if (topic == "iot/air_controller/temp") {
                                for (var i = 0; i < response['data']['result'][0]['values'].length; i++) {
                                    var pair = [];
                                    var timestamp = response['data']['result'][j]['values'][i][0];
                                    var temperature = response['data']['result'][j]['values'][i][1];
                                    pair.push(timestamp);
                                    pair.push(temperature);
                                    AC.push(pair);
                                }
                            }
                        }
                        return AC;
                    }

                    var options = {
                        series: [],
                        chart: {
                            height: 350,
                            width: '100%',
                            type: 'line',
                            toolbar: {
                                show: true,
                                tools: {
                                    download: true,
                                    selection: true,
                                    zoom: true,
                                    zoomin: true,
                                    zoomout: true,
                                    pan: true,
                                },
                            },
                        },
                        dataLabels: {
                            enabled: false
                        },
                        title: {
                            text: 'Temperature Trends',
                        },
                        noData: {
                            text: 'Loading...'
                        },
                        xaxis: {
                            type: 'datetime',
                            tickPlacement: 'on',
                            labels: {
                                rotate: -45,
                                rotateAlways: true,
                                formatter: function (value, timestamp) {
                                    return new Date(timestamp * 1000).toISOString().slice(0, 19).replace('T', ' ')
                                },
                            },
                        }
                    };

                    var chart = new ApexCharts(document.querySelector("#line-chart-1"), options);
                    chart.render();
                    chart.updateSeries([{
                        name: 'Temperature',
                        data: getACTemp(response),
                    }])
                });
            }
        });

        //Fridge Temperature Line Chart
        $(function () {
            var url = "http://10.0.0.67:9090/api/v1/query_range?query=temperature&start=1618332873&end=1618335953&step=20s";
            $.getJSON(url, function (response) {

                function getFridgeTemp(response) {
                    var fridge = [];
                    for (var j = 0; j < response['data']['result'].length; j++) {
                        var topic = response['data']['result'][j]['metric']['topic'];
                        if (topic == "iot/fridge/temp") {
                            for (var i = 0; i < response['data']['result'][0]['values'].length; i++) {
                                var pair = [];
                                var timestamp = response['data']['result'][j]['values'][i][0];
                                var temperature = response['data']['result'][j]['values'][i][1];
                                pair.push(timestamp);
                                pair.push(temperature);
                                fridge.push(pair);
                            }
                        }
                    }
                    return fridge;
                }

                var options = {
                    series: [],
                    chart: {
                        height: 350,
                        width: '100%',
                        type: 'line',
                        toolbar: {
                            show: true,
                            tools: {
                                download: true,
                                selection: true,
                                zoom: true,
                                zoomin: true,
                                zoomout: true,
                                pan: true,
                            },
                        },
                    },
                    colors: ["#FFB64D"],
                    dataLabels: {
                        enabled: false
                    },
                    title: {
                        text: 'Temperature Trends',
                    },
                    noData: {
                        text: 'Loading...'
                    },
                    xaxis: {
                        type: 'datetime',
                        tickPlacement: 'on',
                        labels: {
                            rotate: -45,
                            rotateAlways: true,
                            formatter: function (value, timestamp) {
                                return new Date(timestamp * 1000).toISOString().slice(0, 19).replace('T', ' ')
                            },
                        },
                    }
                };

                var chart = new ApexCharts(document.querySelector("#line-chart-2"), options);
                chart.render();

                chart.updateSeries([{
                    name: 'Temperature',
                    data: getFridgeTemp(response)
                }])
            });
        });

        //Energy Line Chart
        $(function () {
                var url = 'http://10.0.0.67:9090/api/v1/query_range?query=watts&start=1618335123&end=1618335953&step=20s';
                $.getJSON(url, function (response) {
                    function fill_fridge(response) {
                        var fridge = [];
                        for (var j = 0; j < response['data']['result'].length; j++) {
                            var topic = response['data']['result'][j]['metric']['topic'];
                            if (topic == "iot/fridge/energy") {
                                for (var i = 0; i < response['data']['result'][0]['values'].length; i++) {
                                    var pair = [];
                                    var timestamp = response['data']['result'][j]['values'][i][0];
                                    var temperature = response['data']['result'][j]['values'][i][1];
                                    pair.push(timestamp);
                                    pair.push(temperature);
                                    fridge.push(pair);
                                }
                            }
                        }
                        return fridge;
                    }

                    function fill_switch_1(response) {
                        var switch_1 = [];
                        for (var j = 0; j < response['data']['result'].length; j++) {
                            var topic = response['data']['result'][j]['metric']['topic'];
                            if (topic == "iot/switch_2/status") {
                                for (var i = 0; i < response['data']['result'][0]['values'].length; i++) {
                                    var pair = [];
                                    var timestamp = response['data']['result'][j]['values'][i][0];
                                    var temperature = response['data']['result'][j]['values'][i][1];
                                    pair.push(timestamp);
                                    pair.push(temperature);
                                    switch_1.push(pair);
                                }
                            }
                        }
                        switch_1.push([1618335953, 151]);
                        return switch_1;
                    }

                    function fill_switch_2(response) {
                        var switch_2 = [];
                        for (var j = 0; j < response['data']['result'].length; j++) {
                            var topic = response['data']['result'][j]['metric']['topic'];
                            if (topic == "iot/switch_2/status") {
                                for (var i = 0; i < response['data']['result'][0]['values'].length; i++) {
                                    var pair = [];
                                    var timestamp = response['data']['result'][j]['values'][i][0];
                                    var temperature = response['data']['result'][j]['values'][i][1];
                                    pair.push(timestamp);
                                    pair.push(temperature);
                                    switch_2.push(pair);
                                }
                            }
                        }
                        switch_2.push([1618335953, 151]);
                        return switch_2;
                    }

                    function fill_chart(response) {
                        fill_fridge(response);
                        fill_switch_1(response);
                        fill_switch_2(response);
                    }

                    var options = {
                        chart: {
                            height: 300,
                            type: 'line',
                            zoom: {
                                enabled: true
                            },
                        },
                        dataLabels: {
                            enabled: false
                        },
                        stroke: {
                            width: [5, 7, 5],
                            curve: 'straight',
                            dashArray: [0, 8, 5]
                        },
                        colors: ["#0e9e4a", "#FFB64D", "#FF5370"],
                        fill: {
                            type: "gradient",
                            gradient: {
                                shade: 'light'
                            },
                        },
                        series: [{
                            name: "Fridge Energy",
                            data: fill_fridge(response)
                        },
                        {
                            name: "Switch 1 Energy",
                            data: fill_switch_1(response)
                        },
                        {
                            name: "Switch 2 Energy",
                            data: fill_switch_2(response)
                        }
                        ],
                        title: {
                            text: 'Energy Usage (watts)',
                            align: 'left'
                        },
                        markers: {
                            size: 0,
                            hover: {
                                sizeOffset: 6
                            }
                        },
                        xaxis: {
                            type: 'datetime',
                            tickPlacement: 'on',
                            labels: {
                                rotate: -45,
                                rotateAlways: true,
                                formatter: function (value, timestamp) {
                                    return new Date(timestamp * 1000).toISOString().slice(0, 19).replace('T', ' ')
                                },
                            },
                        },
                        tooltip: {
                            y: [{
                                title: {
                                    formatter: function (val) {
                                        return val + " watts"
                                    }
                                }
                            }, {
                                title: {
                                    formatter: function (val) {
                                        return val + " watts"
                                    }
                                }
                            }, {
                                title: {
                                    formatter: function (val) {
                                        return val + " watts"
                                    }
                                }
                            }]
                        },
                        grid: {
                            borderColor: '#f1f1f1',
                        }
                    }
                    var chart = new ApexCharts(
                        document.querySelector("#line-chart-3"),
                        options
                    );
                    chart.render();

                    chart.updateSeries([{
                        data: fill_chart(response),
                    }])
                });
            $('#datepicker').datepicker(
                {
                    onSelect: function () {
                        var currentDate = $("#datepicker").datepicker("getDate");
                        getTime(currentDate);
                    }
                }
            );
            function getTime(dateText) {
                var startTime = new Date(dateText).getTime() / 1000;
                var endTime = startTime + 50000;
                var url = "http://10.0.0.67:9090/api/v1/query_range?query=watts&start=" + startTime + "&end=" + endTime + "&step=120s";
                console.log(url);

                //var url = 'http://10.0.0.67:9090/api/v1/query_range?query=watts&start=1618335123&end=1618335953&step=20s';
                $.getJSON(url, function (response) {
                    function fill_fridge(response) {
                        var fridge = [];
                        for (var j = 0; j < response['data']['result'].length; j++) {
                            var topic = response['data']['result'][j]['metric']['topic'];
                            if (topic == "iot/fridge/energy") {
                                for (var i = 0; i < response['data']['result'][0]['values'].length; i++) {
                                    var pair = [];
                                    var timestamp = response['data']['result'][j]['values'][i][0];
                                    var temperature = response['data']['result'][j]['values'][i][1];
                                    pair.push(timestamp);
                                    pair.push(temperature);
                                    fridge.push(pair);
                                }
                            }
                        }
                        return fridge;
                    }

                    function fill_switch_1(response) {
                        var switch_1 = [];
                        for (var j = 0; j < response['data']['result'].length; j++) {
                            var topic = response['data']['result'][j]['metric']['topic'];
                            if (topic == "iot/switch_2/status") {
                                for (var i = 0; i < response['data']['result'][0]['values'].length; i++) {
                                    var pair = [];
                                    var timestamp = response['data']['result'][j]['values'][i][0];
                                    var temperature = response['data']['result'][j]['values'][i][1];
                                    pair.push(timestamp);
                                    pair.push(temperature);
                                    switch_1.push(pair);
                                }
                            }
                        }
                        switch_1.push([1618335953, 151]);
                        return switch_1;
                    }

                    function fill_switch_2(response) {
                        var switch_2 = [];
                        for (var j = 0; j < response['data']['result'].length; j++) {
                            var topic = response['data']['result'][j]['metric']['topic'];
                            if (topic == "iot/switch_2/status") {
                                for (var i = 0; i < response['data']['result'][0]['values'].length; i++) {
                                    var pair = [];
                                    var timestamp = response['data']['result'][j]['values'][i][0];
                                    var temperature = response['data']['result'][j]['values'][i][1];
                                    pair.push(timestamp);
                                    pair.push(temperature);
                                    switch_2.push(pair);
                                }
                            }
                        }
                        switch_2.push([1618335953, 151]);
                        return switch_2;
                    }

                    function fill_chart(response) {
                        fill_fridge(response);
                        fill_switch_1(response);
                        fill_switch_2(response);
                    }

                    var options = {
                        chart: {
                            height: 300,
                            type: 'line',
                            zoom: {
                                enabled: true
                            },
                        },
                        dataLabels: {
                            enabled: false
                        },
                        stroke: {
                            width: [5, 7, 5],
                            curve: 'straight',
                            dashArray: [0, 8, 5]
                        },
                        colors: ["#0e9e4a", "#FFB64D", "#FF5370"],
                        fill: {
                            type: "gradient",
                            gradient: {
                                shade: 'light'
                            },
                        },
                        series: [{
                            name: "Fridge Energy",
                            data: fill_fridge(response)
                        },
                        {
                            name: "Switch 1 Energy",
                            data: fill_switch_1(response)
                        },
                        {
                            name: "Switch 2 Energy",
                            data: fill_switch_2(response)
                        }
                        ],
                        title: {
                            text: 'Energy Usage (watts)',
                            align: 'left'
                        },
                        markers: {
                            size: 0,
                            hover: {
                                sizeOffset: 6
                            }
                        },
                        xaxis: {
                            type: 'datetime',
                            tickPlacement: 'on',
                            labels: {
                                rotate: -45,
                                rotateAlways: true,
                                formatter: function (value, timestamp) {
                                    return new Date(timestamp * 1000).toISOString().slice(0, 19).replace('T', ' ')
                                },
                            },
                        },
                        tooltip: {
                            y: [{
                                title: {
                                    formatter: function (val) {
                                        return val + " watts"
                                    }
                                }
                            }, {
                                title: {
                                    formatter: function (val) {
                                        return val + " watts"
                                    }
                                }
                            }, {
                                title: {
                                    formatter: function (val) {
                                        return val + " watts"
                                    }
                                }
                            }]
                        },
                        grid: {
                            borderColor: '#f1f1f1',
                        }
                    }
                    var chart = new ApexCharts(
                        document.querySelector("#line-chart-3"),
                        options
                    );
                    chart.render();

                    chart.updateSeries([{
                        data: fill_chart(response),
                    }])
                });
            }
        });

        //Bar Chart
        $(function () {
            var url = "http://10.0.0.67:9090/api/v1/query_range?query=received_messages&start=1618190822&end=1618350476&step=20s";
            $.getJSON(url, function (response) {

                function getTopics(response) {
                    var topics = [];
                    for (var i = 0; i < response['data']['result'].length; i++) {
                        var topic = response['data']['result'][i]['metric']['topic'];
                        if (!topics.includes(topic)) {
                            topics.push(topic);
                        }
                    }
                    return topics;
                }

                function getTopicMessages(response) {
                    var messages = [];
                    for (var i = 0; i < response['data']['result'].length; i++) {
                        messages.push(response['data']['result'][i]['values'].length);
                    }
                    return messages;
                }

                var options = {
                    chart: {
                        height: 350,
                        type: 'bar',
                    },
                    plotOptions: {
                        bar: {
                            horizontal: false,
                            columnWidth: '55%',
                            endingShape: 'rounded'
                        },
                    },
                    dataLabels: {
                        enabled: false
                    },
                    colors: ["#0e9e4a", "#4099ff", "#FF5370"],
                    stroke: {
                        show: true,
                        width: 2,
                        colors: ['transparent']
                    },
                    fill: {
                        type: 'gradient',
                        gradient: {
                            shade: 'light',
                            type: "vertical",
                            shadeIntensity: 0.25,
                            inverseColors: true,
                            opacityFrom: 1,
                            opacityTo: 0.7,
                            stops: [50, 100]
                        },
                    },
                    series: [{
                        name: 'Messages Per Topic',
                        data: getTopicMessages(response)
                    }],
                    xaxis: {
                        categories: getTopics(response),
                    },
                    yaxis: {
                        title: {
                            text: 'Messages'
                        }
                    },
                    tooltip: {
                        y: {
                            formatter: function (val) {
                                return val + " messages"
                            }
                        }
                    }
                }
                var chart = new ApexCharts(
                    document.querySelector("#bar-chart-1"),
                    options
                );
                chart.render();
            });
        });

        //Status Pie Chart
        $(function () {
            var url = "http://10.0.0.67:9090/api/v1/query_range?query=received_messages&start=1618164093&end=1618345294&step=20s";
            $.getJSON(url, function (response) {
                function fill_labels(response) {
                    var labels = [];
                    for (var i = 0; i < response['data']['result'].length; i++) {
                        var status = response['data']['result'][i]['metric']['status'];
                        if (!(labels.includes(status))) {
                            labels.push(status);
                        }
                    }
                    return labels;
                }

                function fill_series(response) {
                    var series = [];
                    var storeError = 0;
                    var success = 0;
                    for (var i = 0; i < response['data']['result'].length; i++) {
                        var status = response['data']['result'][i]['metric']['status'];
                        if (status == 'storeError') {
                            storeError++;
                        }
                        else {
                            success++;
                        }
                    }
                    series.push(storeError);
                    series.push(success);
                    return series;
                }

                var options = {
                    chart: {
                        height: 320,
                        type: 'pie',
                    },

                    labels: fill_labels(response),
                    series: fill_series(response),
                    colors: ["#4099ff", "#0e9e4a"],

                    legend: {
                        show: true,
                        position: 'bottom',
                    },
                    fill: {
                        type: 'gradient',
                        gradient: {
                            shade: 'light',
                            inverseColors: true,
                        }
                    },
                    dataLabels: {
                        enabled: true,
                        dropShadow: {
                            enabled: false,
                        }
                    },
                    responsive: [{
                        breakpoint: 480,
                        options: {
                            legend: {
                                position: 'bottom'
                            }
                        }
                    }]
                }

                var chart = new ApexCharts(
                    document.querySelector("#pie-chart-1"),
                    options
                );
                chart.render();
            });
        });
    }, 700);
});
