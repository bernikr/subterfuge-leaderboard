document.addEventListener('DOMContentLoaded', function () {
    let current_stats = JSON.parse(document.getElementById('current_stats').textContent);
    let outcome_data = [current_stats.finished, current_stats.eliminated, current_stats.resigned];
    new Chart(document.getElementById('outcome_chart'), {
        type: 'doughnut',
        data: {
            labels: [
                'Finished',
                'Eliminated',
                'Resigned'
            ],
            datasets: [{
                label: 'Game Outcomes',
                data: outcome_data,
                backgroundColor: [
                    'green',
                    'red',
                    'yellow'
                ],
                hoverOffset: 4
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: (context) => context.label + ": " + context.formattedValue + "%",
                    }
                }
            }
        }
    });
    let data = JSON.parse(document.getElementById('data').textContent);
    let chart = new Chart(document.getElementById('main_chart'), {
        type: 'line',
        data: {
            datasets: [
                {
                    label: "Rating",
                    data: data,
                    parsing: {
                        xAxisKey: 'timestamp',
                        yAxisKey: 'elo'
                    },
                    yAxisID: 'yElo',
                    borderColor: "red",
                    backgroundColor: "red",
                }, {
                    label: "Rank",
                    data: data,
                    parsing: {
                        xAxisKey: 'timestamp',
                        yAxisKey: 'rank'
                    },
                    yAxisID: 'yRank',
                    borderColor: "blue",
                    backgroundColor: "blue",
                }
            ],
        },
        options: {
            scales: {
                xAxis: {
                    type: "time",
                    time: {
                        unit: "day",
                        parser: (t) => {
                            console.log(t);
                            return t;
                        }
                    }
                },
                yElo: {
                    type: 'linear',
                    position: 'left',
                },
                yRank: {
                    type: 'linear',
                    position: 'right',
                },
            },
            plugins: {
                zoom: {
                    zoom: {
                        drag: {
                            enabled: true
                        },
                        mode: 'x',
                    },
                },
            },
        }
    });
});
