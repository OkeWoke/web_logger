function GET (url) {
    return new Promise((resolve, reject) => {
        let xhr = new XMLHttpRequest()

        xhr.open('GET', url, true)
        xhr.onload = function () {
            if (this.status >= 200 && this.status < 300) {
                return resolve(xhr.response)
            } else {
                return reject({ status: this.status, text: xhr.statusText })
            }
        }
        xhr.onerror = reject
        xhr.send()
    })
}


function list_render(data, unitDat)
{
    let text = '<ul class="list-group">'
    const obj = JSON.parse(data);
    const units = JSON.parse(unitDat);

    Object.entries(obj).forEach(([key, value]) => {
        text+= '<li class="list-group-item">'+key + ': ' + value+' '+ units[key]+'</li>\n'; 
     });

    text+='</ul>'
    document.getElementById('statlist').innerHTML = text;
}

function graph_render(data)
{
    const obj = JSON.parse(data);

    var dims = Object.keys(obj);
    let time_array = [];
    let temp_array = [];
    let hum_array = [];


    for (let i =0; i < obj.Temperature.length; i++)
    {
        var tempItem = obj.Temperature[i].split(',');
        var humItem = obj.Humidity[i].split(',');
        time_array.push(new Date(tempItem[0]));
        temp_array.push(tempItem[1]);
        hum_array.push(humItem);
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
                yAxisID: 'y'
            },
            {
                label: "Humidity in my room",
                data: hum_array,
                backgroundColor:'rgba(99, 255, 132, 0.2)',
                borderColor: 'rgba(99, 255, 132, 1)',
                yAxisID: 'y1'
            }]
        },
        options: {
            responsive: false,
            scales: {
                y: {
                    beginAtZero: false
                },
                x: {
                    type: 'time',
                    time: 
                    {
                        unit: 'minute',
                        
                    }
                }
            },
            layout: {
                padding: 20
            }
        }
    });
}

function subHead_render()
{
    const date = new Date();
    document.getElementById('subheader').innerHTML = "The stats in my room as of: " + date.toString();
}
function list_request()
{
    GET("http://127.0.0.1:5000/Devices/0").then( function(result)
    {
        GET("http://127.0.0.1:5000/Devices/0/units").then(function(unit_result)
        {
            list_render(result, unit_result);
        });
    });
}

function graph_request()
{
    GET("http://127.0.0.1:5000/Devices/0/n=500").then( function(result)
    {
        return graph_render(result);
    });
}

list_request();
graph_request();
subHead_render();

var intervalId = setInterval(function() {
    list_request();
    subHead_render();
  }, 20000);

