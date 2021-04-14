'use strict';
$(document).ready(function () {
    setTimeout(function () {

        //Air Controller Temperature Line Chart
        $(function () {
            var url = "http://10.0.0.67:9090/api/v1/query_range?query=temperature&start=1618332873&end=1618335953&step=20s";
            $.getJSON(url, function (response) {

                function getACTemp(response) {
                    var AC = [];
                    for (var j = 0; j < response['data']['result'].length; j++) {
                        var topic = response['data']['result'][j]['metric']['topic'];
                        if (topic == "iot/air_controller/temp") {
                            for (var i = 0; i < response['data']['result'][0]['values'].length; i++) {
                                AC.push(response['data']['result'][j]['values'][i][1]);
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
                    type: 'category',
                    tickPlacement: 'on',
                    labels: {
                        rotate: -45,
                        rotateAlways: true
                    },
                    datetimeFormatter: {
                        year: 'yyyy',
                        month: 'MMM \'yy',
                        day: 'dd MMM',
                        hour: 'HH:mm'
                    }
                }
            };

            var chart = new ApexCharts(document.querySelector("#line-chart-1"), options);
            chart.render();
/*
            var metric = "temperature";
            var startTime = "1618332873";
            var endTime = "1618335953";

                var metric_pairs = response['data']['result'][0]['values'];
                if (response['data']['result'][0]['metric']['topic'] == 'iot/air_controller/temp') {
                    for (var i = 0; i < metric_pairs.length; i++) {
                        var timestamp = metric_pairs[i][0] * 1000;
                        //metric_pairs[i][0] = new Date(timestamp).toISOString();
                    }
                }*/
                chart.updateSeries([{
                    name: 'Temperature',
                    data: getACTemp(response)
                }])
            });
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
                                fridge.push(response['data']['result'][j]['values'][i][1]);
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
                    type: 'category',
                    tickPlacement: 'on',
                    labels: {
                        rotate: -45,
                        rotateAlways: true
                    },
                    datetimeFormatter: {
                        year: 'yyyy',
                        month: 'MMM \'yy',
                        day: 'dd MMM',
                        hour: 'HH:mm'
                    }
                }
            };

            var chart = new ApexCharts(document.querySelector("#line-chart-2"), options);
            chart.render();
/*
            var metric = "temperature";
            var startTime = "1618332873";
            var endTime = "1618335953";

                var metric_pairs = response['data']['result'][0]['values'];
                if (response['data']['result'][0]['metric']['topic'] == 'iot/air_controller/temp') {
                    for (var i = 0; i < metric_pairs.length; i++) {
                        var timestamp = metric_pairs[i][0] * 1000;
                        //metric_pairs[i][0] = new Date(timestamp).toISOString();
                    }
                }*/
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
                for (var i = 0; i < response['data']['result'].length; i++) {
                    var topic = response['data']['result'][i]['metric']['topic'];
                    if (topic == "iot/fridge/energy") {
                        for (var i = 0; i < response['data']['result'][0]['values'].length; i++) {
                            fridge.push(response['data']['result'][0]['values'][i][1]);
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
                            switch_1.push(response['data']['result'][j]['values'][i][1]);
                        }
                    }
                }
                switch_1.push(151);
                return switch_1;
            }

            function fill_switch_2(response) {
                var switch_2 = [];
                for (var j = 0; j < response['data']['result'].length; j++) {
                    var topic = response['data']['result'][j]['metric']['topic'];
                    if (topic == "iot/switch_2/status") {
                        for (var i = 0; i < response['data']['result'][0]['values'].length; i++) {
                            switch_2.push(response['data']['result'][j]['values'][i][1]);
                        }
                    }
                }
                switch_2.push(151);
                return switch_2;
            }

            var options = {
                chart: {
                    height: 300,
                    type: 'line',
                    zoom: {
                        enabled: false
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
                    text: 'Energy Usage',
                    align: 'left'
                },
                markers: {
                    size: 0,

                    hover: {
                        sizeOffset: 6
                    }
                },
                xaxis: {
                    type: 'category',
                    tickPlacement: 'on',
                    labels: {
                        rotate: -45,
                        rotateAlways: true
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
        });
    });

        //Bar Chart
        $(function () {
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
                    name: 'Net Profit',
                    data: [44, 55, 57, 56, 61, 58, 63]
                }, {
                    name: 'Revenue',
                    data: [76, 85, 101, 98, 87, 105, 91]
                }, {
                    name: 'Free Cash Flow',
                    data: [35, 41, 36, 26, 45, 48, 52]
                }],
                xaxis: {
                    categories: ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
                },
                yaxis: {
                    title: {
                        text: '$ (thousands)'
                    }
                },
                tooltip: {
                    y: {
                        formatter: function (val) {
                            return "$ " + val + " thousands"
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

        //Bar chart stacked
        $(function () {
            var options = {
                chart: {
                    height: 350,
                    type: 'bar',
                    stacked: true,
                    toolbar: {
                        show: true
                    },
                    zoom: {
                        enabled: true
                    }
                },
                colors: ["#4099ff", "#0e9e4a", "#FFB64D", "#FF5370"],
                responsive: [{
                    breakpoint: 480,
                    options: {
                        legend: {
                            position: 'bottom',
                            offsetX: -10,
                            offsetY: 0
                        }
                    }
                }],
                plotOptions: {
                    bar: {
                        horizontal: false,
                    },
                },
                series: [{
                    name: 'PRODUCT A',
                    data: [44, 55, 41, 67, 22, 43]
                }, {
                    name: 'PRODUCT B',
                    data: [13, 23, 20, 8, 13, 27]
                }, {
                    name: 'PRODUCT C',
                    data: [11, 17, 15, 15, 21, 14]
                }, {
                    name: 'PRODUCT D',
                    data: [21, 7, 25, 13, 22, 8]
                }],
                xaxis: {
                    type: 'datetime',
                    categories: ['01/01/2011 GMT', '01/02/2011 GMT', '01/03/2011 GMT', '01/04/2011 GMT', '01/05/2011 GMT', '01/06/2011 GMT'],
                },
                legend: {
                    position: 'right',
                    offsetY: 40
                },
                fill: {
                    type: 'gradient',
                    gradient: {
                        shade: 'light',
                        type: "horizontal",
                        shadeIntensity: 0.25,
                        inverseColors: true,
                        opacityFrom: 0.8,
                        opacityTo: 1,
                        stops: [0, 100]
                    },
                },
            }
            var chart = new ApexCharts(
                document.querySelector("#bar-chart-2"),
                options
            );
            chart.render();
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
                    console.log(labels);
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
