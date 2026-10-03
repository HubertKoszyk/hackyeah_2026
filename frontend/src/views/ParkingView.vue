<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchParkingSpots, type ParkingItem } from '../services/api'
import AppButton from '../components/common/AppButton.vue'

const parkings = ref<ParkingItem[]>([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    parkings.value = await fetchParkingSpots()
  } catch (err: any) {
    error.value = err?.message || 'Błąd połączenia z backendem Django'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="parking-view-container">
    <div class="view-header">
      <h1 class="text-h1">Zarządzanie Parkingami Miejskim</h1>
      <p class="text-md text-muted">Dane na żywo analizowane przez kamery miejskie w Krakowie</p>
    </div>

    <div v-if="loading" class="loading-state">
      <span class="text-md">Pobieranie statusu miejsc parkingowych...</span>
    </div>

    <div v-else-if="error" class="error-banner">
      {{ error }}
    </div>

    <div v-else class="parkings-grid">
      <div v-for="spot in parkings" :key="spot.id" class="parking-card">
        <div class="parking-header">
          <h3 class="text-h3">{{ spot.name }}</h3>
          <span class="status-badge" :class="spot.status">
            {{ spot.status === 'available' ? 'Wolne miejsca' : 'Prawie pełny' }}
          </span>
        </div>

        <p class="text-sm text-muted">Współrzędne GPS: {{ spot.lat }}, {{ spot.lng }}</p>

        <div class="occupancy-bar-wrapper">
          <div class="occupancy-labels">
            <span class="text-xs">Zajętość</span>
            <span class="text-xs font-bold">{{ spot.totalSpots - spot.freeSpots }} / {{ spot.totalSpots }}</span>
          </div>
          <div class="bar-track">
            <div
              class="bar-fill"
              :style="{ width: `${((spot.totalSpots - spot.freeSpots) / spot.totalSpots) * 100}%` }"
              :class="spot.status"
            ></div>
          </div>
        </div>

        <div class="card-footer">
          <div class="free-spots-count">
            <span class="count-number">{{ spot.freeSpots }}</span>
            <span class="count-label">wolnych miejsc</span>
          </div>
          <AppButton variant="outline" :left-icon="false" :right-icon="false">
            Podgląd kamery
          </AppButton>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.parking-view-container {
  padding: 2.5rem;
  background-color: #f8fafc;
  min-height: 100vh;
  box-sizing: border-box;
}

.view-header {
  margin-bottom: 2rem;
}
.view-header h1 {
  color: #191919;
  margin-bottom: 0.5rem;
}
.text-muted {
  color: #626262;
}

.parkings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.parking-card {
  background-color: #ffffff;
  border-radius: 8px; /* cornerRadius: 8px w Figmie */
  padding: 1.5rem;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.parking-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}
.parking-header h3 {
  color: #191919;
  margin: 0;
}

.status-badge {
  font-size: 12px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 6px;
  text-transform: uppercase;
}
.status-badge.available {
  background-color: #ebfce5;
  color: #2cb100;
}
.status-badge.almost_full {
  background-color: #fef5e6;
  color: #c27b01;
}

.occupancy-bar-wrapper {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.occupancy-labels {
  display: flex;
  justify-content: space-between;
  color: #626262;
}

.bar-track {
  width: 100%;
  height: 8px;
  background-color: #e7e7e7;
  border-radius: 4px;
  overflow: hidden;
}
.bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s ease;
}
.bar-fill.available {
  background-color: #37dd00;
}
.bar-fill.almost_full {
  background-color: #f29a01;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 0.75rem;
  border-top: 1px solid #f0f0f0;
}

.free-spots-count {
  display: flex;
  flex-direction: column;
}
.count-number {
  font-family: var(--font-family-headings);
  font-size: 22px;
  font-weight: 700;
  color: #0048ff;
  line-height: 1.1;
}
.count-label {
  font-size: 11px;
  color: #7b7b7b;
}

.error-banner {
  background: #fde9e5;
  color: #ec1f00;
  padding: 1rem;
  border-radius: 8px;
}
</style>
