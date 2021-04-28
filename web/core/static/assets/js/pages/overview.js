'use strict';
$(document).ready(function () {
    setTimeout(function () {
        var ip = document.getElementById('ip_address').textContent;

        function getTemp(response, device) {
            var temp = [];
            for (var j = 0; j < response['data']['result'].length; j++) {
                var topic = response['data']['result'][j]['metric']['topic'];
                if (topic.includes(device) && topic.includes("temp")) {
                    for (var i = 0; i < response['data']['result'][0]['values'].length; i++) {
                        var pair = [];
                        var timestamp = response['data']['result'][j]['values'][i][0];
                        var temperature = response['data']['result'][j]['values'][i][1];
                        pair.push(timestamp);
                        pair.push(temperature);
                        temp.push(pair);
                    }
                }
            }
            return temp;
        } 

        function fill_device(response, device) {
            var device_data = [];
            for (var j = 0; j < response['data']['result'].length; j++) {
                var topic = response['data']['result'][j]['metric']['topic'];
                if (topic.includes(device) && (topic.includes("status") || topic.includes("energy"))) {
                    for (var i = 0; i < response['data']['result'][0]['values'].length; i++) {
                        var data_point = response['data']['result'][j]['values'][i];
                        if (typeof data_point != 'undefined') {
                            device_data.push(response['data']['result'][j]['values'][i]);
                        }
                    }
                }
            }
            if (device.includes("switch")) {
                device_data.push([1618335953, 151]);
            }
            return device_data;
        }

        //Air Controller Temperature Line Chart
        $(function () {
            var url = "http://" + ip + ":9090/api/v1/query_range?query=temperature&start=1618332873&end=1618335953&step=20s";
            $.getJSON(url, function (response) {
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
                        text: 'No Data for Selected Time'
                    },
                    xaxis: {
                        type: 'datetime',
                        categories: [],
                        tickPlacement: 'on',
                        labels: {
                            trim: false,
                            rotate: 0,
                            rotateAlways: true,
                            formatter: function (timestamp) {
                                var date = new Date(timestamp * 1000).toISOString().slice(0, 19).replace('T', ' ');
                                return date;
                            },
                        },
                        offsetX: 50,
                    }
                };

                var chart = new ApexCharts(document.querySelector("#line-chart-1"), options);
                chart.render();
                chart.updateSeries([{
                    name: 'Temperature',
                    data: getTemp(response, "air_controller"),
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
                var startTime = new Date(dateText).getTime() / 1000;
                var endTime = startTime + 21600;
                var url = "http://" + ip + ":9090/api/v1/query_range?query=temperature&start=" + startTime + "&end=" + endTime + "&step=480s";

                $.getJSON(url, function (response) {
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
                            text: 'No Data for Selected Time'
                        },
                        xaxis: {
                            type: 'datetime',
                            categories: [],
                            tickPlacement: 'on',
                            labels: {
                                trim: false,
                                rotate: 0,
                                rotateAlways: true,
                                formatter: function (timestamp) {
                                    var date = new Date(timestamp * 1000).toISOString().slice(0, 19).replace('T', ' ');
                                    return date;
                                },
                            },
                            offsetX: 50,
                        }
                    };

                    var chart = new ApexCharts(document.querySelector("#line-chart-1"), options);
                    chart.render();
                    chart.updateSeries([{
                        name: 'Temperature',
                        data: getTemp(response, "air_controller"),
                    }])
                });
            }
        });

        //Fridge Temperature Line Chart
        $(function () {

            var url = "http://" + ip + ":9090/api/v1/query_range?query=temperature&start=1618332873&end=1618335953&step=20s";
            $.getJSON(url, function (response) {

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
                        text: 'No Data for Selected Time'
                    },
                    xaxis: {
                        type: 'datetime',
                        categories: [],
                        tickPlacement: 'on',
                        labels: {
                            trim: false,
                            rotate: 0,
                            rotateAlways: true,
                            formatter: function (timestamp) {
                                var date = new Date(timestamp * 1000).toISOString().slice(0, 19).replace('T', ' ');
                                return date;
                            },
                        },
                        offsetX: 50,
                    }
                };

                var chart = new ApexCharts(document.querySelector("#line-chart-2"), options);
                chart.render();

                chart.updateSeries([{
                    name: 'Temperature',
                    data: getTemp(response, "fridge")
                }])
            });

            $('#datepicker4').datepicker(
                {
                    onSelect: function () {
                        var currentDate = $("#datepicker4").datepicker("getDate");
                        getTime(currentDate);
                    }
                }
            );
            function getTime(dateText) {
                var startTime = new Date(dateText).getTime() / 1000;
                var endTime = startTime + 7200;
                var url = "http://" + ip + ":9090/api/v1/query_range?query=temperature&start=" + startTime + "&end=" + endTime + "&step=20s";

                $.getJSON(url, function (response) {

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
                            text: 'No Data for Selected Time'
                        },
                        xaxis: {
                            type: 'datetime',
                            categories: [],
                            tickPlacement: 'on',
                            labels: {
                                trim: false,
                                rotate: 0,
                                rotateAlways: true,
                                formatter: function (timestamp) {
                                    var date = new Date(timestamp * 1000).toISOString().slice(0, 19).replace('T', ' ');
                                    return date;
                                },
                            },
                            offsetX: 50,
                        }
                    };

                    var chart = new ApexCharts(document.querySelector("#line-chart-2"), options);
                    chart.render();
                    chart.updateSeries([{
                        name: 'Temperature',
                        data: getTemp(response, "fridge")
                    }])
                });
            }
        });

        //Energy Line Chart
        $(function () {
            var url = 'http://' + ip + ':9090/api/v1/query_range?query=watts&start=1618335123&end=1618335953&step=20s';
            $.getJSON(url, function (response) {
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
                        data: fill_device(response, "fridge")
                    },
                    {
                        name: "Switch 1 Energy",
                        data: fill_device(response, "switch_1")
                    },
                    {
                        name: "Switch 2 Energy",
                        data: fill_device(response, "switch_2")
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
                        categories: [],
                        tickPlacement: 'on',
                        labels: {
                            trim: false,
                            rotate: 0,
                            rotateAlways: true,
                            formatter: function (timestamp) {
                                var date = new Date(timestamp * 1000).toISOString().slice(0, 19).replace('T', ' ');
                                return date;
                            },
                        },
                        offsetX: 50,
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
                var url = "http://" + ip + ":9090/api/v1/query_range?query=watts&start=" + startTime + "&end=" + endTime + "&step=120s";

                $.getJSON(url, function (response) {
                    function fill_chart(response) {
                        fill_device(response, "fridge");
                        fill_device(response, "switch_1");
                        fill_device(response, "switch_2");
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
                            data: fill_device(response, "fridge")

                        },
                        {
                            name: "Switch 1 Energy",
                            data: fill_device(response, "switch_1")
                        },
                        {
                            name: "Switch 2 Energy",
                            data: fill_device(response, "switch_2")
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
                            categories: [],
                            tickPlacement: 'on',
                            labels: {
                                trim: false,
                                rotate: 0,
                                rotateAlways: true,
                                formatter: function (timestamp) {
                                    var date = new Date(timestamp * 1000).toISOString().slice(0, 19).replace('T', ' ');
                                    return date;
                                },
                            },
                            offsetX: 50,
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
                        name: "Energy",
                        data: fill_chart(response),
                    }])
                });
            }
        });

        //Bar Chart
        $(function () {
            var url = "http://" + ip + ":9090/api/v1/query_range?query=received_messages&start=1618190822&end=1618350476&step=20s";
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

    }, 700);
});
