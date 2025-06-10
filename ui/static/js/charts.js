function drawChart(canvasId, data, labels) {
    const ctx = document.getElementById(canvasId).getContext("2d");
    new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Portfolio Value",
                data: data,
                borderColor: "blue",
                fill: false
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: "Date" } },
                y: { title: { display: true, text: "Value ($)" } }
            }
        }
    });
}