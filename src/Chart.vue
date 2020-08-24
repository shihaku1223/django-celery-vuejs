<template>
  <v-app>
    <h3>データ定義表 Chart</h3>
    <div :style="mainStyle">
      <metric-chart id='chart'/>
    </div>
    </v-app>
</template>

<style>
#chart {
  height: 1024px;
  width: 4028px;
}
</style>

<script>
import MetricChart from '@/components/MetricChart'

export default {
  data: () => ({
    mainStyle: {
      overflow: 'auto'
    }
  }),
  components: {
    MetricChart
  }
}
</script>
