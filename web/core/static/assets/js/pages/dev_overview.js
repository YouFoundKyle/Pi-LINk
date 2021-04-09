'use strict';
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
                data: [44, 55, 57, 56, 61, 58, 63]
            }, {
                name: 'Device 2',
                data: [76, 85, 101, 98, 87, 0, 0]
            }],
            xaxis: {
                categories: ['23', '6668', '7103'],
            },
            yaxis: {
                title: {
                    text: '# of Messages (by 1000)'
                }
            },
            tooltip: {
                y: {
                    formatter: function(val) {
                        return "$ " + val + " thousands"
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



// var lease_data = [{"Analysis Date": "01_59_17", 
//                     "IP Address": "10.1.1.11", 
//                     "MAC Address": "44:01:bb:7d:b0:23", 
//                     "Lease State": "active", 
//                     "Hostname": "Not provided.", 
//                     "Device Vendor": "SHENZHEN BILIAN ELECTRONIC CO.\uff0cLTD", 
//                     "Port Usage": [{
//                     "Port ID": "23", 
//                     "Protocol": "tcp", 
//                     "State": "open", 
//                     "Service": "telnet"}, 
//                     {"Port ID": "6668", 
//                     "Protocol": "tcp", 
//                     "State": "open", 
//                     "Service": "irc"}, 
//                     {"Port ID": "7103", 
//                     "Protocol": "tcp", 
//                     "State": "open", 
//                     "Service": "unknown"}]}]

// for (var i in lease_data) {
//     var row = document.createElement("tr");
//     var ce 
// }


// {/* <script src="https://code.jquery.com/jquery-3.5.1.js">
//     var lease = [
//     {"Analysis Date": "01_24_03", 
//     "Device Info": [{
//         "IP Address": "10.1.1.11", 
//         "MAC Address": "44:01:bb:7d:b0:23", 
//         "Lease State": "active", 
//         "Hostname": "Not provided.", 
//         "Device Vendor": "SHENZHEN BILIAN ELECTRONIC CO. LTD"}], 
//         "Port Usage": [{
//             "Port ID": "23", 
//             "Protocol": "tcp", 
//             "State": "open", 
//             "Service": "telnet"}, 
//             {"Port ID": "6668", 
//             "Protocol": "tcp", 
//             "State": "open", 
//             "Service": "irc"}, 
//             {"Port ID": "7103", 
//             "Protocol": "tcp", 
//             "State": "open", 
//             "Service": "unknown"}]}]

//     function buildTable(data) {
//         var table = document.getElementById('dev_table')

//         for (var i = 0, i < data.length, i++){
//             var row
//         }
//     }
// </script> */}

// fetch("/etc/pilink/overwatch/sample_lease_info.json")
// .then(response => {
//     return response.json();
// })
// .then(data => console.log(data));

// // console.log("hellooooo1\n")
// // $(document).ready(function(){
// //     console.log("hellooooo2\n")
// //     // FETCHING DATA FROM JSON FILE
// //     $.getJSON("/etc/pilink/overwatch/sample_lease_info.json", function(data) {
// //         console.log("hellooooo3\n")
// //         var device = '';
// //         console.log(data["Analysis Date"])
// //         // ITERATING THROUGH OBJECTS
// //         $.each(data, function (key, value) {

// //             //CONSTRUCTION OF ROWS HAVING
// //             // DATA FROM JSON OBJECT
// //             device += '<tr>';
// //             device += '<td>' + 
// //                 value["Analysis Date"] + '</td>';

// //             device += '<td>' + 
// //                 value["Device Info"]["IP Address"] + '</td>';

// //             device += '<td>' + 
// //                 value["Device Info"]["MAC Address"] + '</td>';

// //             device += '<td>' + 
// //                 value["Device Info"]["Hostname"] + '</td>';

// //             device += '</tr>';
// //         });

// //         //INSERTING ROWS INTO TABLE 
// //         $('#dev_table').append(device);
// //     });
// // });
