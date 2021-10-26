var  chart_type = 'bar';
var summary_url = $('#myChart').parent().find("input[type='hidden']").data('summary-url');

    var ctx = document.getElementById('myChart').getContext('2d');
    var config = {
        type: chart_type,
        data: {
            labels: [],
            datasets: [{
                // label: 'Last Six Months expenses',
                data: [],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)',
                    'rgba(88, 24, 69, 0.8)',
                    'rgba(199, 0, 57, 0.8)',
                    'rgba(184, 125, 7 , 0.8)',
                    'rgba(120, 81, 3, 0.8)',
                    'rgba(3, 24, 120, 0.8)',
                    'rgba(5, 3, 120, 0.8)',
                    'rgba(87, 85, 176, 0.8)',
                    'rgba(87, 14, 216, 0.8)',
                    'rgba(255, 159, 64, 0.8)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(88, 24, 69, 1)',
                    'rgba(199, 0, 57, 1)',
                    'rgba(184, 125, 7 , 1)',
                    'rgba(120, 81, 3, 1)',
                    'rgba(3, 24, 120, 1)',
                    'rgba(5, 3, 120, 1)',
                    'rgba(87, 85, 176, 1)',
                    'rgba(87, 14, 216, 1)',
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

const getChartData = (day=0, title='Today',data=null,labels=null, main_title=null) =>{
    if (data != null && labels !=null){
        config.data.datasets[0].data = data;
        config.data.labels = labels;
        if (title != null) {
            config.data.datasets[0].label = title;
        }else{
            config.data.datasets[0].label = '';
        }
        if (main_title != null){
            config.options.plugins.title.text = main_title;
        }
        myChart = new Chart(ctx, config);
    }else{
        fetch(summary_url+"?day="+day)
        .then((res) => res.json())
        .then((result) => {
            console.log(result);
            const category_data = result.category_data;
            const [labels, data] = [Object.keys(category_data), Object.values(category_data)]
            config.data.datasets[0].data = data;
            config.data.labels = labels;
            config.data.datasets[0].label = title;
            config.options.plugins.title.text = "Expenses Per Category ("+title+")";
            myChart = new Chart(ctx, config);
        });
    }
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
        getChartData(0,"Today");
    }
    if(this.value == "7"){
        myChart.destroy();
        getChartData(7,'This week');
    }
    if(this.value == "30"){
        myChart.destroy();
        getChartData(30,'This month');
    }
    if(this.value == "180"){
        myChart.destroy();
        getChartData(30,'This 6 months');
    }
    if(this.value == "366"){
        myChart.destroy();
        getChartData(366,'This year');
    }
});

var _selected_year = null;
var _selected_month = null;

$('#dobyear').on('change', function() {
    _selected_year = this.value
    let monthly_url = $('#dobyear').data('monthly-url');
    fetch(monthly_url+"?year="+this.value)
    .then((res) => res.json())
    .then((result) => {
        let months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'Septempber', 'October', 'November', 'December']
        myChart.destroy();
        getChartData(null, 'Monthly', Object.values(result.data.months), months, 'Monthly Expenses Summary for '+this.value);
    });

    if(_selected_year){
        $('#dobmonth').on('change', function() {
            // console.log(this.value);
            _selected_month = this.value
            let weekly_url = $('#dobmonth').data('weekly-url');
            fetch(weekly_url+"?year="+_selected_year+"&month="+this.value)
            .then((res) => res.json())
            .then((result) => {
                console.log(result)
                myChart.destroy();
                getChartData(null, 'Weekly', Object.values(result.data.weeks), Object.keys(result.data.weeks), 'Weekly Expenses Summary for '+result.data.month+" ("+ _selected_year+")");
            });
        });
    }

});

