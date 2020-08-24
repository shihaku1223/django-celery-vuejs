
<script>
import { Bubble } from 'vue-chartjs'
import points from '@/points.json'
import axes from '@/axes.json'

export default {
  extends: Bubble,

  data: () => ({
    xAxes: axes.x,
    yAxes: axes.y,
    chartData: {
      datasets: [{
        label: 'Implemented',
        borderWidth: 1,
        borderColor: '#2554FF',
        backgroundColor: '#2554FF',
        data: points
      }]
    },
    options: {
      legend: {
        display: true
      },

      responsive: true,
      maintainAspectRatio: false,
      scales: {
        xAxes: [{
          ticks: {
            callback: (value, index, values) => {
              return axes.x[value.toString() + ".0" ]
            },
          },
        }],
        yAxes: [{
          ticks: {
            callback: (value, index, values) => {
              return axes.y[value]
            },
          },
        }],
      },

      tooltips: {
        enabled: true,
        callbacks: {
          label: ((tooltipItems, data) => {
            console.log(tooltipItems)
            console.log(data)
            console.log(axes.x[tooltipItems.xLabel])
            console.log(axes.y[tooltipItems.yLabel])
            return `${axes.x[tooltipItems.xLabel]}, ${axes.y[tooltipItems.yLabel]}`
          })
        }
      }
    }
  }),
  mounted() {
    this.renderChart(this.chartData, this.options)
  }
}

</script>

