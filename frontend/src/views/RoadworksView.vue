<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { fetchRoadworks, type RoadRestriction } from '../services/api'

const mapContainer = ref<HTMLElement | null>(null)
const items = ref<RoadRestriction[]>([])
const error = ref('')
let map: L.Map | null = null
let layerGroup: L.LayerGroup | null = null
const polylines = new Map<number, L.Polyline>()

const KIND_COLORS: Record<string, string> = {
  roadwork: '#f59e0b',
  event: '#3b82f6',
  accident: '#ef4444',
  closure: '#7c3aed',
}

const fmt = (iso: string) =>
  new Date(iso).toLocaleString('pl-PL', { dateStyle: 'short', timeStyle: 'short' })

const statusLabel = (s: string) => (s === 'active' ? 'Trwa' : s === 'planned' ? 'Planowane' : 'Zakończone')

const popupHtml = (r: RoadRestriction) => {
  const conflicts = r.conflicts.length
    ? `<p style="color:#b91c1c"><b>⚠ Kolizja z:</b> ${r.conflicts.map((c) => c.title).join(', ')}</p>`
    : ''
  const parkings = r.nearby_parkings.length
    ? `<p><b>Parkingi w pobliżu:</b> ${r.nearby_parkings.map((p) => `${p.name} (${p.distance_m} m)`).join(', ')}</p>`
    : ''
  const detour = r.detour ? `<p><b>Objazd:</b> ${r.detour}</p>` : ''
  return `<b>${r.title}</b><br/>${r.kind_label} · ${statusLabel(r.status)}<br/>
    ${r.organization ? r.organization + '<br/>' : ''}${fmt(r.start_at)} – ${fmt(r.end_at)}
    ${conflicts}${detour}${parkings}`
}

const draw = () => {
  if (!map) return
  layerGroup?.clearLayers()
  polylines.clear()
  layerGroup = L.layerGroup().addTo(map)
  for (const r of items.value) {
    const hasConflict = r.conflicts.length > 0
    const line = L.polyline(
      [
        [r.start.lat, r.start.lng],
        [r.end.lat, r.end.lng],
      ],
      {
        color: KIND_COLORS[r.kind] ?? '#555',
        weight: hasConflict ? 9 : 6,
        opacity: 0.9,
        dashArray: r.status === 'planned' ? '10 8' : undefined,
      },
    )
      .bindPopup(popupHtml(r))
      .addTo(layerGroup)
    polylines.set(r.id, line)
  }
}

const focusItem = (r: RoadRestriction) => {
  if (!map) return
  map.setView([(r.start.lat + r.end.lat) / 2, (r.start.lng + r.end.lng) / 2], 16)
  polylines.get(r.id)?.openPopup()
}

const load = async () => {
  try {
    items.value = await fetchRoadworks()
    error.value = ''
    draw()
  } catch {
    error.value = 'Nie udało się pobrać danych z API'
  }
}

onMounted(() => {
  if (!mapContainer.value) return
  map = L.map(mapContainer.value, { center: [50.0617, 19.9373], zoom: 13 })
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap',
  }).addTo(map)
  load()
})

onUnmounted(() => {
  map?.remove()
  map = null
})
</script>

<template>
  <div class="rw-view">
    <div ref="mapContainer" class="rw-map"></div>

    <aside class="rw-panel">
      <h2>Ograniczenia drogowe</h2>
      <p v-if="error" class="rw-error">{{ error }}</p>
      <p v-else-if="!items.length" class="rw-muted">Brak aktywnych i planowanych ograniczeń.</p>

      <button v-for="r in items" :key="r.id" type="button" class="rw-item" @click="focusItem(r)">
        <span class="rw-dot" :style="{ background: KIND_COLORS[r.kind] }"></span>
        <span class="rw-text">
          <b>{{ r.title }}</b>
          <small>{{ r.kind_label }} · {{ statusLabel(r.status) }}</small>
          <small>{{ fmt(r.start_at) }} – {{ fmt(r.end_at) }}</small>
          <small v-if="r.conflicts.length" class="rw-warn">
            ⚠ Kolizja: {{ r.conflicts.map((c) => c.title).join(', ') }}
          </small>
        </span>
      </button>

      <div class="rw-legend">
        <span v-for="(color, kind) in KIND_COLORS" :key="kind">
          <i :style="{ background: color }"></i>{{ kind }}
        </span>
        <span class="rw-muted">linia przerywana = planowane</span>
      </div>
    </aside>
  </div>
</template>

<style scoped>
.rw-view {
  position: relative;
  width: 100%;
  height: 100vh;
}
.rw-map {
  width: 100%;
  height: 100%;
}
.rw-panel {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 1000;
  width: 340px;
  max-height: calc(100vh - 32px);
  overflow-y: auto;
  background: #fff;
  color: #111;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}
.rw-panel h2 {
  margin: 0 0 12px;
  font-size: 18px;
}
.rw-item {
  display: flex;
  gap: 10px;
  width: 100%;
  text-align: left;
  background: #f5f5f5;
  border: 0;
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 8px;
  cursor: pointer;
  color: inherit;
}
.rw-item:hover {
  background: #ebebeb;
}
.rw-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-top: 4px;
  flex-shrink: 0;
}
.rw-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: 13px;
}
.rw-text small {
  color: #555;
}
.rw-warn {
  color: #b91c1c !important;
  font-weight: 600;
}
.rw-error {
  color: #b91c1c;
}
.rw-muted {
  color: #777;
  font-size: 12px;
}
.rw-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 12px;
  margin-top: 12px;
  font-size: 12px;
}
.rw-legend i {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 2px;
  margin-right: 4px;
}
</style>