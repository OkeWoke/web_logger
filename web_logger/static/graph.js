function http_get(url, callback)
{
    var http = new XMLHttpRequest();
    http.onreadystatechange = function()
    {
        if (http.readyState == 4 && http.status == 200)
            callback(http.responseText);
    }
    http.open("GET", url, true);
    http.send(null);
}

function render(data)
{
    const obj = JSON.parse(data);
    let time_array = [];
    let temp_array = [];

    for (let i =0; i < obj.Temperature.length; i++)
    {
        var tempItem = obj.Temperature[i].split(',');
        var humItem = obj.Humidity[i].split(',');
        time_array.push(tempItem[0]);
        temp_array.push(tempItem[1]);
    }
    

    var ctx = document.getElementById("myChart");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: time_array,
            datasets: [{
                label: 'Temperature in my room',
                data: temp_array,
                backgroundColor:'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
            }]
        },
        options: {
            responsive: false,
            scales: {
                y: {
                    beginAtZero: false
                }
            },
            layout: {
                padding: 20
            }
        }
    });
}


http_get("http://127.0.0.1:5000/Devices/0/n=1000", render);