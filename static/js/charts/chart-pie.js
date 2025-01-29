// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ["Low", "Medium", "High", "Critical"],
    datasets: [{
      data: [
        taskData.lowPriorityTasksCount,
        taskData.mediumPriorityTasksCount,
        taskData.highPriorityTasksCount,
        taskData.criticalPriorityTasksCount
      ],
      backgroundColor: ['#f6c23e', '#36b9cc', '#1cc88a', '#e74a3b'],
      hoverBackgroundColor: ['#d49a08', '#06acc4', '#05b374', '#a60b0b'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});
