<script setup lang="ts">
import TrafficMap from '../components/traffic/TrafficMap.vue'
</script>

<template>
  <div class="traffic-view-container">
    <TrafficMap />
  </div>
</template>

<style scoped>
.traffic-view-container {
  width: 100%;
  height: 100vh;
  position: relative;
  overflow: hidden;
}
</style>
