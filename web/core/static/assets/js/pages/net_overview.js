'use strict';
var port_info = JSON.parse(document.getElementById('port-info').textContent);

$(document).ready(function() {
    $(function() {
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
                name: 'Device 1',
                data: Object.values(port_info)//[44, 55, 57, 56, 61, 58]
            }],
            xaxis: {
                categories: Object.keys(port_info),//['23', '6668', '7103'],
            },
            yaxis: {
                title: {
                    text: '# of Devices'
                }
            },
            tooltip: {
                y: {
                    formatter: function(val) {
                        return val + " messages"
                    }
                }
            }
        }
        var chart = new ApexCharts(
            document.querySelector("#port-graph"),
            options
        );
        chart.render();
    });
});