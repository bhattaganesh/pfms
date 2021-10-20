var  chart_type = 'bar';
var summary_url = $('#myChart').parent().find("input[type='hidden']").data('summary-url');

    var ctx = document.getElementById('myChart').getContext('2d');
    var config = {
        type: chart_type,
        data: {
            labels: [],
            datasets: [{
                label: 'Last Six Months expenses',
                data: [],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)',
                    'rgba(255, 159, 64, 0.8)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Expenses Per Category'
                }
            }
        },
    }
    // var myChart = new Chart(ctx, config);

// } 

const getChartData = (day=30*6, title = 'Last Six Months expenses') =>{
    fetch(summary_url+"?day="+day)
    .then((res) => res.json())
    .then((result) => {
        const category_data = result.category_data;
        const [labels, data] = [Object.keys(category_data), Object.values(category_data)]
        config.data.datasets[0].data = data;
        config.data.labels = labels;
        config.data.datasets[0].label = title;
        myChart = new Chart(ctx, config);
    })
}

document.onload = getChartData();




$('.chart-type').on('click', function(e){
    chart_type = $(this).data('chart-type');
    myChart.destroy();
    config.type = chart_type;
    myChart = new Chart(ctx, config);
});


$('#dayChart').on('change', function() {
    if(this.value == "0"){
        myChart.destroy();
        getChartData(0,"Todays's expenses");
    }
    if(this.value == "7"){
        myChart.destroy();
        getChartData(7,'This week\'s sexpenses');
    }
    if(this.value == "30"){
        myChart.destroy();
        getChartData(30,'This month\'s expenses');
    }
    if(this.value == "366"){
        myChart.destroy();
        getChartData(366,'This year\'s expenses');
    }
});