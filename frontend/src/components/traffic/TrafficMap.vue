<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import {
  krakowStreets,
  krakowKeyPoints,
  getStreetCongestionForHour,
  type TrafficPoint,
  type TrafficStreet,
} from '../../data/krakowTrafficData'
import {
  getStoredApiKey,
  saveApiKey,
  getTrafficFlowTileUrl,
  getTrafficIncidentsTileUrl,
  fetchLiveFlowSegment,
  type TomTomSegmentData,
} from '../../services/tomtomService'
import { fetchRoadworks, type RoadRestriction } from '../../services/api'
import { getStreetImpact, applyImpact } from '../../services/roadworksImpact'

// State
const mapContainer = ref<HTMLElement | null>(null)
let map: L.Map | null = null

// TomTom API State
const apiKey = ref<string>(getStoredApiKey())
const showApiKeyModal = ref(false)
const inputApiKey = ref(apiKey.value)
const isLiveTomTomFlowActive = ref(true)
const isLiveTomTomIncidentsActive = ref(true)

// Roadworks State
const roadworks = ref<RoadRestriction[]>([])
const showRoadworks = ref(true)
const roadworksAffectTraffic = ref(true)
const roadworksError = ref('')
let roadworksLayer: L.LayerGroup | null = null
let roadworksTimer: number | undefined

const KIND_COLORS: Record<string, string> = {
  roadwork: '#f59e0b',
  event: '#3b82f6',
  accident: '#ef4444',
  closure: '#7c3aed',
}
const KIND_ICONS: Record<string, string> = {
  roadwork: '🚧',
  event: '🎫',
  accident: '⚠️',
  closure: '⛔',
}
const STATUS_LABELS: Record<string, string> = {
  active: 'Trwa',
  planned: 'Planowane',
  finished: 'Zakończone',
}

const esc = (v: string) =>
  v.replace(/[&<>"']/g, (c) => (({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }) as Record<string, string>)[c] ?? c)
const fmtDate = (iso: string) =>
  new Date(iso).toLocaleString('pl-PL', { dateStyle: 'short', timeStyle: 'short' })

const activeRoadworksCount = () => roadworks.value.filter((r) => r.status === 'active').length

// Simulation / Time State
const currentHour = ref(17) // 17:00 domyślnie (szczyt popołudniowy)
const selectedDistrict = ref<string>('Wszystkie')
const selectedPoint = ref<TrafficPoint | null>(krakowKeyPoints[0] ?? null) // ul. Rynek 1
const activeStreetInfo = ref<{
  name: string
  percent: number
  status: string
  color: string
  speedKmH: number
  delayMinutes: number
  isLive?: boolean
  causes?: string[]
} | null>(null)

// Layers
let tomtomFlowLayer: L.TileLayer | null = null
let tomtomIncidentsLayer: L.TileLayer | null = null
const streetLayers: { streetId: string; polyline: L.Polyline }[] = []
const markerLayers: L.Marker[] = []
let activeLivePolyline: L.Polyline | null = null

const initMap = () => {
  if (!mapContainer.value) return

  // Inicjalizacja Leafleta z widokiem na cały Kraków
  map = L.map(mapContainer.value, {
    center: [50.0617, 19.9373],
    zoom: 13,
    zoomControl: false,
  })

  // Kontrolka zoomu w prawym dolnym rogu
  L.control.zoom({ position: 'bottomright' }).addTo(map)

  // Oficjalne kafelki OpenStreetMap (identyczne jak na Figmie)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors &copy; TomTom',
  }).addTo(map)

  // Aktualizacja warstw TomTom
  updateTomTomLayers()

  // Renderowanie arterii miejskich
  renderStreets()

  // Renderowanie węzłów i ważnych punktów
  renderKeyPoints()

  // Nasłuchiwanie kliknięć w dowolną ulicę na mapie Krakowa
  map.on('click', handleMapClick)
}

const updateTomTomLayers = () => {
  if (!map) return

  // Usunięcie poprzednich warstw TomTom
  if (tomtomFlowLayer) {
    map.removeLayer(tomtomFlowLayer)
    tomtomFlowLayer = null
  }
  if (tomtomIncidentsLayer) {
    map.removeLayer(tomtomIncidentsLayer)
    tomtomIncidentsLayer = null
  }

  // Jeśli użytkownik ma klucz TomTom API
  if (apiKey.value && apiKey.value.trim().length > 0) {
    if (isLiveTomTomFlowActive.value) {
      tomtomFlowLayer = L.tileLayer(getTrafficFlowTileUrl(apiKey.value), {
        maxZoom: 19,
        opacity: 0.85,
        attribution: '&copy; TomTom Traffic',
      }).addTo(map)
    }

    if (isLiveTomTomIncidentsActive.value) {
      tomtomIncidentsLayer = L.tileLayer(getTrafficIncidentsTileUrl(apiKey.value), {
        maxZoom: 19,
        opacity: 0.9,
      }).addTo(map)
    }
  }
}

const handleMapClick = async (e: L.LeafletMouseEvent) => {
  const { lat, lng } = e.latlng

  if (apiKey.value && apiKey.value.trim().length > 0) {
    const liveData: TomTomSegmentData | null = await fetchLiveFlowSegment(lat, lng, apiKey.value)
    if (liveData && map) {
      if (activeLivePolyline) {
        map.removeLayer(activeLivePolyline)
        activeLivePolyline = null
      }

      if (liveData.coordinates && liveData.coordinates.length > 0) {
        activeLivePolyline = L.polyline(liveData.coordinates, {
          color: liveData.color,
          weight: 9,
          opacity: 0.95,
        }).addTo(map)
      }

      activeStreetInfo.value = {
        name: `Odcinek drogowy (${lat.toFixed(4)}, ${lng.toFixed(4)})`,
        percent: liveData.congestionLevel,
        status: liveData.status,
        color: liveData.color,
        speedKmH: liveData.currentSpeed,
        delayMinutes: Math.round(liveData.delaySeconds / 60),
        isLive: true,
      }

      L.popup()
        .setLatLng(e.latlng)
        .setContent(`
          <div style="font-family: 'Plus Jakarta Sans', sans-serif; padding: 6px; min-width: 190px;">
            <div style="font-size: 11px; text-transform: uppercase; color: #0048ff; font-weight: 700; margin-bottom: 2px;">
              🔴 Dane na żywo (TomTom API)
            </div>
            <h4 style="margin: 0 0 6px 0; font-size: 14px; font-weight: 700; color: #191919;">
              Odcinek: ${lat.toFixed(4)}, ${lng.toFixed(4)}
            </h4>
            <div style="font-size: 13px; color: #4a4a4a; display: flex; flex-direction: column; gap: 3px;">
              <div>Natężenie: <b style="color: ${liveData.color};">${liveData.congestionLevel}% (${liveData.status.toUpperCase()})</b></div>
              <div>Prędkość: <b>${liveData.currentSpeed} km/h</b> (swobodny: ${liveData.freeFlowSpeed} km/h)</div>
              <div>Opóźnienie: <b>+${Math.round(liveData.delaySeconds / 60)} min</b></div>
            </div>
          </div>
        `)
        .openOn(map)
    }
  }
}

const renderStreets = () => {
  if (!map) return

  streetLayers.forEach((item) => map?.removeLayer(item.polyline))
  streetLayers.length = 0

  const filtered = selectedDistrict.value === 'Wszystkie'
    ? krakowStreets
    : krakowStreets.filter((s) => s.district === selectedDistrict.value)

  filtered.forEach((street) => {
    const baseCongestion = getStreetCongestionForHour(street, currentHour.value)
    const impact = roadworksAffectTraffic.value
      ? getStreetImpact(street, roadworks.value)
      : { extraPercent: 0, closed: false, causes: [] as RoadRestriction[] }
    const congestion = applyImpact(baseCongestion, impact, street.speedLimit, street.lengthKm)
    const causeTitles = impact.causes.map((c) => c.title)

    const polyline = L.polyline(street.coordinates, {
      color: congestion.color,
      weight: 7,
      opacity: 0.88,
      dashArray: impact.closed ? '2 10' : undefined,
      lineCap: 'round',
      lineJoin: 'round',
    }).addTo(map!)

    polyline.on('click', () => {
      activeStreetInfo.value = {
        name: street.name,
        percent: congestion.percent,
        status: congestion.status,
        color: congestion.color,
        speedKmH: congestion.speedKmH,
        delayMinutes: congestion.delayMinutes,
        isLive: false,
        causes: causeTitles,
      }
    })

    polyline.bindPopup(`
      <div style="font-family: 'Plus Jakarta Sans', sans-serif; padding: 4px; min-width: 200px;">
        <div style="font-size: 11px; text-transform: uppercase; color: #7b7b7b; font-weight: 700;">
          ${street.district} Kraków
        </div>
        <h4 style="margin: 2px 0 6px 0; font-size: 15px; font-weight: 700; color: #191919;">${street.name}</h4>
        <div style="font-size: 13px; color: #4a4a4a; display: flex; flex-direction: column; gap: 4px;">
          <div>Natężenie: <b style="color: ${congestion.color};">${congestion.percent}% (${congestion.status.toUpperCase()})</b></div>
          <div>Średnia prędkość: <b>${congestion.speedKmH} km/h</b> (limit: ${street.speedLimit} km/h)</div>
          <div>Opóźnienie: <b>+${congestion.delayMinutes} min</b></div>
          <div>Długość arterii: <b>${street.lengthKm} km</b></div>
          <div style="font-size: 11px; color: #7b7b7b; margin-top: 4px;">Godzina analizy: <b>${currentHour.value}:00</b></div>
          ${
            causeTitles.length
              ? `<div style="margin-top: 4px; padding: 6px 8px; background: #f5f3ff; border-radius: 6px; font-size: 12px; color: #5b21b6;">
                  <b>${impact.closed ? '⛔ Droga zamknięta' : '🚧 Wpływ ograniczeń'}</b> (+${impact.extraPercent} p.p.)<br/>
                  ${causeTitles.map(esc).join('<br/>')}
                </div>`
              : ''
          }
        </div>
      </div>
    `)

    streetLayers.push({ streetId: street.id, polyline })
  })
}

const roadworkPopupHtml = (r: RoadRestriction) => {
  const detour = r.detour ? `<div><b>Objazd:</b> ${esc(r.detour)}</div>` : ''
  const org = r.organization ? `<div>${esc(r.organization)}</div>` : ''
  const note =
    r.status === 'active'
      ? '<div style="margin-top:4px;color:#5b21b6;">Wpływa na natężenie ruchu na pobliskich ulicach</div>'
      : '<div style="margin-top:4px;color:#7b7b7b;">Jeszcze nie wpływa na ruch (planowane)</div>'
  return `
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; padding: 4px; min-width: 210px; font-size: 13px; color:#4a4a4a;">
      <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: ${KIND_COLORS[r.kind] ?? '#555'};">
        ${KIND_ICONS[r.kind] ?? ''} ${esc(r.kind_label)} · ${STATUS_LABELS[r.status] ?? r.status}
      </div>
      <h4 style="margin: 2px 0 6px 0; font-size: 15px; font-weight: 700; color: #191919;">${esc(r.title)}</h4>
      ${org}
      <div>${fmtDate(r.start_at)} – ${fmtDate(r.end_at)}</div>
      ${r.description ? `<div>${esc(r.description)}</div>` : ''}
      ${detour}
      ${note}
    </div>`
}

const renderRoadworks = () => {
  if (!map) return
  roadworksLayer?.clearLayers()
  if (!roadworksLayer) roadworksLayer = L.layerGroup()

  if (!showRoadworks.value) {
    map.removeLayer(roadworksLayer)
    return
  }
  roadworksLayer.addTo(map)

  for (const r of roadworks.value) {
    const color = KIND_COLORS[r.kind] ?? '#555'
    const latlngs: [number, number][] = [
      [r.start.lat, r.start.lng],
      [r.end.lat, r.end.lng],
    ]

    // Biała obwódka pod linią, żeby ograniczenie było widoczne na tle korków
    L.polyline(latlngs, { color: '#ffffff', weight: 13, opacity: 0.95, lineCap: 'round' }).addTo(roadworksLayer)
    L.polyline(latlngs, {
      color,
      weight: 7,
      opacity: 1,
      dashArray: r.status === 'planned' ? '10 8' : undefined,
      lineCap: 'round',
    })
      .bindPopup(roadworkPopupHtml(r))
      .addTo(roadworksLayer)

    const mid: [number, number] = [(r.start.lat + r.end.lat) / 2, (r.start.lng + r.end.lng) / 2]
    const icon = L.divIcon({
      className: 'roadwork-pin',
      html: `<div class="roadwork-pin-box ${r.status === 'planned' ? 'is-planned' : ''}" style="border-color:${color}">${KIND_ICONS[r.kind] ?? '🚧'}</div>`,
      iconSize: [30, 30],
      iconAnchor: [15, 15],
    })
    L.marker(mid, { icon, zIndexOffset: 1000 }).bindPopup(roadworkPopupHtml(r)).addTo(roadworksLayer)
  }
}

const loadRoadworks = async () => {
  try {
    roadworks.value = await fetchRoadworks()
    roadworksError.value = ''
  } catch {
    roadworksError.value = 'Nie udało się pobrać ograniczeń drogowych'
    return
  }
  renderRoadworks()
  // Ruch zależy od aktywnych ograniczeń, więc przeliczamy ulice po każdym odświeżeniu danych
  renderStreets()
}

const renderKeyPoints = () => {
  if (!map) return

  markerLayers.forEach((m) => map?.removeLayer(m))
  markerLayers.length = 0

  krakowKeyPoints.forEach((point) => {
    const customIcon = L.divIcon({
      className: 'custom-traffic-pin',
      html: `
        <div class="pin-box ${selectedPoint.value?.id === point.id ? 'is-selected' : ''}">
          <svg viewBox="0 0 20 20" fill="none" class="pin-svg">
            <path d="M4 10L10 4M10 4L16 10M10 4V16" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
      `,
      iconSize: [32, 32],
      iconAnchor: [16, 16],
    })

    const marker = L.marker([point.lat, point.lng], { icon: customIcon }).addTo(map!)
    marker.on('click', () => {
      selectPoint(point)
    })

    markerLayers.push(marker)
  })
}

const selectPoint = (point: TrafficPoint) => {
  selectedPoint.value = point
  if (map) {
    map.flyTo([point.lat, point.lng], 15, { duration: 0.9 })
  }
}

const applyDistrictFilter = (district: string) => {
  selectedDistrict.value = district
  renderStreets()

  if (!map) return
  if (district === 'Wszystkie') {
    map.flyTo([50.0617, 19.9373], 12.5, { duration: 0.8 })
  } else if (district === 'Centrum') {
    map.flyTo([50.0617, 19.9373], 14.5, { duration: 0.8 })
  } else if (district === 'Północ') {
    map.flyTo([50.0880, 19.9400], 13.5, { duration: 0.8 })
  } else if (district === 'Południe') {
    map.flyTo([50.0300, 19.9450], 13.5, { duration: 0.8 })
  } else if (district === 'Nowa Huta') {
    map.flyTo([50.0680, 20.0200], 13.5, { duration: 0.8 })
  } else if (district === 'Zachód') {
    map.flyTo([50.0550, 19.9050], 13.5, { duration: 0.8 })
  }
}

const handleSaveApiKey = () => {
  saveApiKey(inputApiKey.value)
  apiKey.value = inputApiKey.value.trim()
  showApiKeyModal.value = false
  updateTomTomLayers()
}

// Watchers
watch(currentHour, () => {
  renderStreets()
})

watch(showRoadworks, () => {
  renderRoadworks()
})

watch(roadworksAffectTraffic, () => {
  renderStreets()
})

watch(isLiveTomTomFlowActive, () => {
  updateTomTomLayers()
})

watch(isLiveTomTomIncidentsActive, () => {
  updateTomTomLayers()
})

onMounted(() => {
  initMap()
  loadRoadworks()
  // Odświeżanie ograniczeń co minutę (status planned -> active zmienia się w czasie)
  roadworksTimer = window.setInterval(loadRoadworks, 60_000)
})

onUnmounted(() => {
  if (roadworksTimer) window.clearInterval(roadworksTimer)
  if (map) {
    map.remove()
    map = null
  }
})
</script>

<template>
  <div class="traffic-map-wrapper">
    <!-- Map Container -->
    <div ref="mapContainer" class="leaflet-map-element"></div>

    <!-- 1. Floating Top-Left Header Badge (Figma: "🚦 Ruch uliczny") -->
    <div class="floating-header-group">
      <div class="floating-header-badge">
        <span class="header-icon">
          <svg viewBox="0 0 24 24" fill="none" class="icon-svg">
            <rect x="7" y="3" width="10" height="18" rx="5" stroke="currentColor" stroke-width="2" />
            <circle cx="12" cy="7.5" r="1.5" fill="#ec1f00" />
            <circle cx="12" cy="12" r="1.5" fill="#f29a01" />
            <circle cx="12" cy="16.5" r="1.5" fill="#37dd00" />
          </svg>
        </span>
        <h2 class="header-title">Ruch uliczny Kraków</h2>
      </div>

      <!-- Live API Status Button / Modal Trigger -->
      <button
        class="api-status-pill"
        :class="{ 'has-key': !!apiKey }"
        @click="showApiKeyModal = true"
        title="Kliknij, aby skonfigurować TomTom Traffic API dla danych na żywo"
      >
        <span class="live-pulse" :class="{ 'pulse-active': !!apiKey }"></span>
        <span class="api-label">
          {{ apiKey ? 'TomTom API: Połączono' : 'TomTom API: Dodaj klucz na żywo' }}
        </span>
        <span class="api-gear">⚙️</span>
      </button>

      <!-- District Filters -->
      <div class="district-filters-bar">
        <button
          v-for="d in ['Wszystkie', 'Centrum', 'Północ', 'Południe', 'Nowa Huta', 'Zachód']"
          :key="d"
          class="district-btn"
          :class="{ 'is-active': selectedDistrict === d }"
          @click="applyDistrictFilter(d)"
        >
          {{ d }}
        </button>
      </div>

      <!-- Roadworks toggles -->
      <div class="roadworks-toggles">
        <label class="toggle-row">
          <input v-model="showRoadworks" type="checkbox" />
          <span>🚧 Pokaż ograniczenia drogowe ({{ roadworks.length }})</span>
        </label>
        <label class="toggle-row">
          <input v-model="roadworksAffectTraffic" type="checkbox" />
          <span>Uwzględnij w natężeniu ruchu ({{ activeRoadworksCount() }} aktywnych)</span>
        </label>
        <span v-if="roadworksError" class="toggle-error">{{ roadworksError }}</span>
      </div>
    </div>

    <!-- 2. Floating Top-Right Points Panel (Figma: "ℹ Ważne punkty -> ul. Rynek 1") -->
    <div class="floating-points-panel">
      <!-- Section Title Card -->
      <div class="points-card-header">
        <span class="info-icon">
          <svg viewBox="0 0 20 20" fill="none" class="icon-svg">
            <circle cx="10" cy="10" r="7.5" stroke="currentColor" stroke-width="1.8" />
            <path d="M10 9V14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
            <circle cx="10" cy="6.5" r="0.9" fill="currentColor" />
          </svg>
        </span>
        <span class="points-title">Ważne punkty Krakowa</span>
      </div>

      <!-- Point Items List -->
      <div class="points-list">
        <div
          v-for="point in krakowKeyPoints"
          :key="point.id"
          class="point-item-card"
          :class="{ 'is-active': selectedPoint?.id === point.id }"
          @click="selectPoint(point)"
        >
          <span class="point-icon">
            <svg viewBox="0 0 20 20" fill="none" class="icon-svg">
              <rect x="3" y="3" width="14" height="14" rx="4" stroke="currentColor" stroke-width="1.8" />
              <path d="M6 14L14 6M14 6H9M14 6V11" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
          <div class="point-info">
            <span class="point-name">{{ point.name }}</span>
            <span class="point-district">{{ point.district }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 3. Active Street Info Card (When a street is clicked) -->
    <div v-if="activeStreetInfo" class="active-street-card">
      <div class="active-street-header">
        <div>
          <span class="text-xs text-muted" v-if="activeStreetInfo.isLive">DANE NA ŻYWO (IRL)</span>
          <span class="text-xs text-muted" v-else>SYMULACJA DLA GODZINY {{ currentHour }}:00</span>
          <h3 class="active-street-title">{{ activeStreetInfo.name }}</h3>
        </div>
        <button class="close-btn" @click="activeStreetInfo = null">✕</button>
      </div>
      <div v-if="activeStreetInfo.causes?.length" class="active-street-causes">
        🚧 Wpływ ograniczeń: {{ activeStreetInfo.causes.join(', ') }}
      </div>
      <div class="active-street-stats">
        <div class="stat-box">
          <span class="stat-label">Natężenie ruchu</span>
          <span class="stat-value" :style="{ color: activeStreetInfo.color }">
            {{ activeStreetInfo.percent }}%
          </span>
        </div>
        <div class="stat-box">
          <span class="stat-label">Śr. prędkość</span>
          <span class="stat-value">{{ activeStreetInfo.speedKmH }} km/h</span>
        </div>
        <div class="stat-box">
          <span class="stat-label">Opóźnienie</span>
          <span class="stat-value">+{{ activeStreetInfo.delayMinutes }} min</span>
        </div>
      </div>
    </div>

    <!-- 4. Floating Bottom Time Slider (Simulate Traffic by Hour) -->
    <div class="floating-time-controller">
      <div class="time-header">
        <div class="time-display">
          <span class="text-xs text-muted">ANALIZA CZASOWA DLA CAŁEGO KRAKOWA</span>
          <span class="hour-badge">
            Godzina: <strong>{{ currentHour }}:00</strong>
            <span v-if="currentHour >= 7 && currentHour <= 9" class="peak-tag peak-morning">Szczyt poranny</span>
            <span v-else-if="currentHour >= 15 && currentHour <= 18" class="peak-tag peak-afternoon">Szczyt popołudniowy</span>
            <span v-else-if="currentHour >= 22 || currentHour <= 5" class="peak-tag peak-night">Noc (puste drogi)</span>
            <span v-else class="peak-tag peak-normal">Ruch umiarkowany</span>
          </span>
        </div>

        <!-- Legend -->
        <div class="traffic-legend">
          <span class="legend-item"><i class="dot dot-green"></i> Płynny (&lt;40%)</span>
          <span class="legend-item"><i class="dot dot-orange"></i> Umiarkowany (40-70%)</span>
          <span class="legend-item"><i class="dot dot-red"></i> Korek (&gt;70%)</span>
          <span class="legend-item"><i class="dot dot-closure"></i> Ograniczenie</span>
        </div>
      </div>

      <!-- Range Slider -->
      <div class="slider-wrapper">
        <input
          v-model.number="currentHour"
          type="range"
          min="0"
          max="23"
          step="1"
          class="time-slider"
        />
        <div class="slider-ticks">
          <span>00:00</span>
          <span>06:00</span>
          <span class="highlight">08:00</span>
          <span>12:00</span>
          <span class="highlight">17:00</span>
          <span>20:00</span>
          <span>23:00</span>
        </div>
      </div>
    </div>

    <!-- 5. TomTom API Key Modal -->
    <div v-if="showApiKeyModal" class="modal-overlay" @click.self="showApiKeyModal = false">
      <div class="modal-card">
        <div class="modal-header">
          <h3 class="modal-title">Konfiguracja TomTom Traffic API (Na żywo)</h3>
          <button class="close-btn" @click="showApiKeyModal = false">✕</button>
        </div>
        <div class="modal-body">
          <p class="modal-desc">
            Wklej darmowy klucz TomTom API, aby wyświetlać oficjalne natężenie ruchu na żywo (IRL), zatory i wypadki na wszystkich ulicach Krakowa w czasie rzeczywistym.
          </p>

          <div class="form-group">
            <label class="form-label">Twój klucz TomTom API:</label>
            <input
              v-model="inputApiKey"
              type="text"
              class="api-input"
              placeholder="np. a1b2c3d4e5f6g7h8i9j0..."
            />
          </div>

          <div class="api-help-box">
            <div class="help-title">💡 Jak uzyskać darmowy klucz TomTom (bez karty)?</div>
            <ol class="help-steps">
              <li>Wejdź na stronę <a href="https://developer.tomtom.com" target="_blank" rel="noopener">developer.tomtom.com</a> i kliknij <b>Register</b>.</li>
              <li>W zakładce <b>Keys</b> skopiuj swój wygenerowany klucz.</li>
              <li>Plan darmowy daje <b>50 000 kafelków korków i 2 500 zapytań dziennie</b> za darmo.</li>
            </ol>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="showApiKeyModal = false">Anuluj</button>
          <button class="btn-save" @click="handleSaveApiKey">Zapisz i aktywuj</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.traffic-map-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 100vh;
  overflow: hidden;
}

.leaflet-map-element {
  width: 100%;
  height: 100%;
  z-index: 1;
}

/* ==========================================================================
   1. Floating Header Group (Figma: "🚦 Ruch uliczny")
   ========================================================================== */
.floating-header-group {
  position: absolute;
  top: 1.5rem;
  left: 2rem;
  z-index: 500;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.floating-header-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  background-color: #ffffff;
  padding: 10px 18px;
  border-radius: 8px; /* cornerRadius: 8px w Figmie */
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.12);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.header-icon {
  display: inline-flex;
  align-items: center;
  color: #191919;
}
.header-icon .icon-svg {
  width: 22px;
  height: 22px;
}

.header-title {
  font-family: var(--font-family-headings);
  font-size: 20px;
  line-height: 24px;
  font-weight: 700;
  color: #191919; /* Gray 900 */
  margin: 0;
}

/* API Status Pill */
.api-status-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background-color: #ffffff;
  border: 1px solid #e7e7e7;
  border-radius: 8px;
  padding: 6px 12px;
  font-family: var(--font-family-body);
  font-size: 12px;
  font-weight: 600;
  color: #4a4a4a;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.2s ease;
  width: fit-content;
}

.api-status-pill:hover {
  background-color: #f8fafc;
  border-color: #0048ff;
  color: #0048ff;
}

.api-status-pill.has-key {
  border-color: #37dd00;
  background-color: #f6fff4;
  color: #1a7800;
}

.live-pulse {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #f29a01;
}

.live-pulse.pulse-active {
  background-color: #37dd00;
  box-shadow: 0 0 0 3px rgba(55, 221, 0, 0.25);
  animation: pulse 1.6s infinite;
}

@keyframes pulse {
  0% { transform: scale(0.95); opacity: 0.9; }
  50% { transform: scale(1.15); opacity: 1; }
  100% { transform: scale(0.95); opacity: 0.9; }
}

/* District Filters Bar */
.district-filters-bar {
  display: flex;
  align-items: center;
  gap: 4px;
  background-color: #ffffff;
  padding: 4px;
  border-radius: 8px;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.district-btn {
  background: transparent;
  border: none;
  font-family: var(--font-family-body);
  font-size: 12px;
  font-weight: 600;
  color: #4a4a4a;
  padding: 5px 10px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.district-btn:hover {
  background-color: #f5f5f5;
  color: #0048ff;
}

.district-btn.is-active {
  background-color: #0048ff;
  color: #ffffff;
}

/* ==========================================================================
   2. Floating Points Panel (Figma: "ℹ Ważne punkty -> ul. Rynek 1")
   ========================================================================== */
.floating-points-panel {
  position: absolute;
  top: 1.5rem;
  right: 2rem;
  z-index: 500;
  width: 310px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.points-card-header {
  background-color: #ffffff;
  padding: 12px 18px;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.info-icon {
  display: inline-flex;
  align-items: center;
  color: #191919;
}
.info-icon .icon-svg {
  width: 20px;
  height: 20px;
}

.points-title {
  font-family: var(--font-family-headings);
  font-size: 17px;
  line-height: 22px;
  font-weight: 700;
  color: #191919;
}

.points-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-height: calc(100vh - 270px);
  overflow-y: auto;
  padding-right: 4px;
}

.point-item-card {
  background-color: #ffffff;
  padding: 10px 14px;
  border-radius: 8px;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  border: 1.5px solid transparent;
  transition: all 0.18s ease;
}

.point-item-card:hover {
  background-color: #f8fafc;
  transform: translateY(-1px);
}

.point-item-card.is-active {
  border-color: #0048ff; /* Brand 500 */
  background-color: #f0f5ff;
}

.point-icon {
  display: inline-flex;
  align-items: center;
  color: #191919;
}
.point-icon .icon-svg {
  width: 18px;
  height: 18px;
}

.point-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.point-name {
  font-family: var(--font-family-headings);
  font-size: 14px;
  line-height: 18px;
  font-weight: 700;
  color: #191919;
}

.point-district {
  font-size: 11px;
  color: #7b7b7b;
}

/* ==========================================================================
   3. Active Street Info Card
   ========================================================================== */
.active-street-card {
  position: absolute;
  top: 1.5rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 500;
  background-color: #ffffff;
  border-radius: 10px;
  padding: 14px 20px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(0, 0, 0, 0.06);
  min-width: 380px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.active-street-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.active-street-title {
  margin: 2px 0 0 0;
  font-family: var(--font-family-headings);
  font-size: 16px;
  font-weight: 700;
  color: #191919;
}

.close-btn {
  background: transparent;
  border: none;
  font-size: 16px;
  color: #7b7b7b;
  cursor: pointer;
  padding: 2px 6px;
  border-radius: 4px;
}
.close-btn:hover {
  background: #f5f5f5;
  color: #191919;
}

.active-street-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.stat-box {
  display: flex;
  flex-direction: column;
  background-color: #f9f9f9;
  padding: 8px 12px;
  border-radius: 6px;
}

.stat-label {
  font-size: 11px;
  color: #7b7b7b;
}

.stat-value {
  font-family: var(--font-family-headings);
  font-size: 16px;
  font-weight: 700;
  color: #191919;
}

/* ==========================================================================
   4. Bottom Time Controller & Slider
   ========================================================================== */
.floating-time-controller {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 500;
  width: min(640px, calc(100% - 4rem));
  background-color: #ffffff;
  border-radius: 12px;
  padding: 1rem 1.5rem;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.time-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.time-display {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.hour-badge {
  font-family: var(--font-family-body);
  font-size: 15px;
  color: #191919;
  display: flex;
  align-items: center;
  gap: 8px;
}

.peak-tag {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 6px;
  text-transform: uppercase;
}
.peak-morning, .peak-afternoon {
  background: #fde9e5;
  color: #ec1f00;
}
.peak-night {
  background: #ebfce5;
  color: #2cb100;
}
.peak-normal {
  background: #fef5e6;
  color: #c27b01;
}

.traffic-legend {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  font-weight: 600;
  color: #4a4a4a;
}
.legend-item {
  display: flex;
  align-items: center;
  gap: 4px;
}
.dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  display: inline-block;
}
.dot-green { background: #37dd00; }
.dot-orange { background: #f29a01; }
.dot-red { background: #ec1f00; }
.dot-closure { background: #7c3aed; }

.roadworks-toggles {
  display: flex;
  flex-direction: column;
  gap: 4px;
  background-color: #ffffff;
  padding: 8px 12px;
  border-radius: 8px;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  font-family: var(--font-family-body);
  font-size: 12px;
  font-weight: 600;
  color: #4a4a4a;
}
.toggle-row {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}
.toggle-error {
  color: #ec1f00;
  font-size: 11px;
}
.active-street-causes {
  background: #f5f3ff;
  color: #5b21b6;
  border-radius: 6px;
  padding: 6px 10px;
  font-size: 12px;
  font-weight: 600;
}

.slider-wrapper {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.time-slider {
  width: 100%;
  accent-color: #0048ff; /* Brand 500 */
  cursor: pointer;
}

.slider-ticks {
  display: flex;
  justify-content: space-between;
  font-size: 10px;
  font-weight: 500;
  color: #7b7b7b;
}
.slider-ticks .highlight {
  font-weight: 700;
  color: #ec1f00;
}

/* ==========================================================================
   5. TomTom API Key Modal
   ========================================================================== */
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(4px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.modal-card {
  background-color: #ffffff;
  border-radius: 12px;
  width: min(520px, 100%);
  padding: 1.5rem;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-title {
  margin: 0;
  font-family: var(--font-family-headings);
  font-size: 18px;
  font-weight: 700;
  color: #191919;
}

.modal-desc {
  font-size: 14px;
  color: #4a4a4a;
  line-height: 1.5;
  margin: 0;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: 13px;
  font-weight: 600;
  color: #191919;
}

.api-input {
  width: 100%;
  padding: 10px 14px;
  border-radius: 8px;
  border: 1.5px solid #e7e7e7;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}
.api-input:focus {
  border-color: #0048ff;
}

.api-help-box {
  background-color: #f5f8ff;
  border: 1px solid #d4e3ff;
  border-radius: 8px;
  padding: 12px 14px;
  font-size: 13px;
  color: #191919;
}

.help-title {
  font-weight: 700;
  color: #0048ff;
  margin-bottom: 6px;
}

.help-steps {
  margin: 0;
  padding-left: 18px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.help-steps a {
  color: #0048ff;
  text-decoration: underline;
}

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
}

.btn-cancel {
  background: #f5f5f5;
  border: none;
  padding: 9px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #4a4a4a;
  cursor: pointer;
}

.btn-save {
  background: #0048ff;
  border: none;
  padding: 9px 18px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #ffffff;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-save:hover {
  background: #003acc;
}
</style>

<style>
/* Roadworks pins */
.roadwork-pin-box {
  width: 30px;
  height: 30px;
  background: #ffffff;
  border: 3px solid #f59e0b;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
}
.roadwork-pin-box.is-planned {
  opacity: 0.75;
  border-style: dashed;
}

/* Global Leaflet Custom Pin Styles */
.custom-traffic-pin .pin-box {
  width: 32px;
  height: 32px;
  background-color: #ffffff;
  border: 2px solid #0048ff;
  border-radius: 8px;
  box-shadow: 0 3px 10px rgba(0, 72, 255, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #0048ff;
  transition: all 0.2s ease;
}

.custom-traffic-pin .pin-box.is-selected {
  background-color: #0048ff;
  color: #ffffff;
  transform: scale(1.15);
  box-shadow: 0 4px 16px rgba(0, 72, 255, 0.6);
}

.custom-traffic-pin .pin-svg {
  width: 18px;
  height: 18px;
}
</style>
