<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { fetchRoadworks, createRoadwork, deleteRoadwork, type RoadRestriction } from '../services/api'

const mapContainer = ref<HTMLElement | null>(null)
const items = ref<RoadRestriction[]>([])
const error = ref('')
let map: L.Map | null = null
let layerGroup: L.LayerGroup | null = null
let draftLayer: L.LayerGroup | null = null
const polylines = new Map<number, L.Polyline>()

const KIND_COLORS: Record<string, string> = {
  roadwork: '#f59e0b',
  event: '#3b82f6',
  accident: '#ef4444',
  closure: '#7c3aed',
}

const KIND_OPTIONS: { value: RoadRestriction['kind']; label: string }[] = [
  { value: 'closure', label: 'Zamknięcie drogi' },
  { value: 'roadwork', label: 'Roboty drogowe' },
  { value: 'event', label: 'Wydarzenie' },
  { value: 'accident', label: 'Wypadek / awaria' },
]

const fmt = (iso: string) =>
  new Date(iso).toLocaleString('pl-PL', { dateStyle: 'short', timeStyle: 'short' })

const statusLabel = (s: string) => (s === 'active' ? 'Trwa' : s === 'planned' ? 'Planowane' : 'Zakończone')

const esc = (s: string) =>
  s.replace(/[&<>"']/g, (c) => (({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }) as Record<string, string>)[c] ?? c)

const popupHtml = (r: RoadRestriction) => {
  const conflicts = r.conflicts.length
    ? `<p style="color:#b91c1c"><b>⚠ Kolizja z:</b> ${r.conflicts.map((c) => esc(c.title)).join(', ')}</p>`
    : ''
  const parkings = r.nearby_parkings.length
    ? `<p><b>Parkingi w pobliżu:</b> ${r.nearby_parkings.map((p) => `${esc(p.name)} (${p.distance_m} m)`).join(', ')}</p>`
    : ''
  const detour = r.detour ? `<p><b>Objazd:</b> ${esc(r.detour)}</p>` : ''
  return `<b>${esc(r.title)}</b><br/>${esc(r.kind_label)} · ${statusLabel(r.status)}<br/>
    ${r.organization ? esc(r.organization) + '<br/>' : ''}${fmt(r.start_at)} – ${fmt(r.end_at)}
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

// defining new roadblock
const addMode = ref(false)
const draftPoints = ref<[number, number][]>([])
const saving = ref(false)
const formError = ref('')
const savedInfo = ref('')

const toLocalInput = (d: Date) => {
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`
}

const emptyForm = () => ({
  title: '',
  kind: 'closure' as RoadRestriction['kind'],
  organization: '',
  description: '',
  detour: '',
  start_at: toLocalInput(new Date()),
  end_at: toLocalInput(new Date(Date.now() + 60 * 60 * 1000)),
})
const form = reactive(emptyForm())

const drawDraft = () => {
  if (!draftLayer) return
  draftLayer.clearLayers()
  for (const p of draftPoints.value) {
    L.circleMarker(p, { radius: 8, color: '#111', weight: 3, fillColor: '#fff', fillOpacity: 1 }).addTo(draftLayer)
  }
  if (draftPoints.value.length === 2) {
    L.polyline(draftPoints.value, { color: '#111', weight: 6, dashArray: '4 8' }).addTo(draftLayer)
  }
}

const onMapClick = (e: L.LeafletMouseEvent) => {
  if (!addMode.value || draftPoints.value.length >= 2) return
  draftPoints.value.push([e.latlng.lat, e.latlng.lng])
  drawDraft()
}

const startAdd = () => {
  addMode.value = true
  draftPoints.value = []
  formError.value = ''
  savedInfo.value = ''
  Object.assign(form, emptyForm())
  drawDraft()
}

const resetPoints = () => {
  draftPoints.value = []
  drawDraft()
}

const cancelAdd = () => {
  addMode.value = false
  draftPoints.value = []
  formError.value = ''
  drawDraft()
}

const save = async () => {
  const start = draftPoints.value[0]
  const end = draftPoints.value[1]
  if (!start || !end) return
  if (!form.title.trim()) {
    formError.value = 'Podaj nazwę blokady'
    return
  }
  const startAt = new Date(form.start_at)
  const endAt = new Date(form.end_at)
  if (isNaN(startAt.getTime()) || isNaN(endAt.getTime())) {
    formError.value = 'Uzupełnij daty'
    return
  }

  saving.value = true
  formError.value = ''
  try {
    const created = await createRoadwork({
      title: form.title.trim(),
      kind: form.kind,
      organization: form.organization.trim(),
      description: form.description.trim(),
      detour: form.detour.trim(),
      start_lat: start[0],
      start_lng: start[1],
      end_lat: end[0],
      end_lng: end[1],
      start_at: startAt.toISOString(),
      end_at: endAt.toISOString(),
    })
    savedInfo.value = created.conflicts.length
      ? `Zapisano. ⚠ Kolizja z: ${created.conflicts.map((c) => c.title).join(', ')}`
      : 'Zapisano blokadę.'
    cancelAdd()
    await load()
    const fresh = items.value.find((i) => i.id === created.id)
    if (fresh) focusItem(fresh)
  } catch (e) {
    formError.value = e instanceof Error ? e.message : 'Błąd zapisu'
  } finally {
    saving.value = false
  }
}

const confirmTarget = ref<RoadRestriction | null>(null)
const deleting = ref(false)
const deleteError = ref('')

const askDelete = (r: RoadRestriction) => {
  confirmTarget.value = r
  deleteError.value = ''
}

const cancelDelete = () => {
  if (deleting.value) return
  confirmTarget.value = null
  deleteError.value = ''
}

const confirmDelete = async () => {
  const target = confirmTarget.value
  if (!target) return
  deleting.value = true
  deleteError.value = ''
  try {
    await deleteRoadwork(target.id)
    confirmTarget.value = null
    savedInfo.value = `Usunięto blokadę: ${target.title}`
    await load()
  } catch (e) {
    deleteError.value = e instanceof Error ? e.message : 'Błąd usuwania'
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  if (!mapContainer.value) return
  map = L.map(mapContainer.value, { center: [50.0617, 19.9373], zoom: 13 })
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap',
  }).addTo(map)
  draftLayer = L.layerGroup().addTo(map)
  map.on('click', onMapClick)
  load()
})

onUnmounted(() => {
  map?.remove()
  map = null
})
</script>

<template>
  <div class="rw-view">
    <div ref="mapContainer" class="rw-map" :class="{ 'is-adding': addMode }"></div>

    <aside class="rw-panel">
      <h2>Ograniczenia drogowe</h2>

      <div v-if="!addMode">
        <button type="button" class="rw-btn rw-btn-primary" @click="startAdd">+ Dodaj blokadę</button>
        <p v-if="savedInfo" class="rw-saved">{{ savedInfo }}</p>
      </div>

      <div v-else class="rw-form">
        <p v-if="draftPoints.length === 0" class="rw-hint">1/2 · Kliknij na mapie <b>początek</b> odcinka</p>
        <p v-else-if="draftPoints.length === 1" class="rw-hint">2/2 · Kliknij na mapie <b>koniec</b> odcinka</p>
        <template v-else>
          <label>Nazwa <input v-model="form.title" type="text" placeholder="np. Zamknięcie ul. Długa" /></label>
          <label>
            Rodzaj
            <select v-model="form.kind">
              <option v-for="o in KIND_OPTIONS" :key="o.value" :value="o.value">{{ o.label }}</option>
            </select>
          </label>
          <label>Zgłaszający <input v-model="form.organization" type="text" placeholder="np. ZIKiT" /></label>
          <label>Objazd <input v-model="form.detour" type="text" placeholder="np. objazd ul. Basztową" /></label>
          <label>Opis <textarea v-model="form.description" rows="2"></textarea></label>
          <label>Od <input v-model="form.start_at" type="datetime-local" /></label>
          <label>Do <input v-model="form.end_at" type="datetime-local" /></label>
          <p v-if="formError" class="rw-error">{{ formError }}</p>
          <button type="button" class="rw-btn rw-btn-primary" :disabled="saving" @click="save">
            {{ saving ? 'Zapisywanie…' : 'Zapisz blokadę' }}
          </button>
        </template>
        <div class="rw-row">
          <button v-if="draftPoints.length > 0" type="button" class="rw-btn" @click="resetPoints">Wybierz punkty ponownie</button>
          <button type="button" class="rw-btn" @click="cancelAdd">Anuluj</button>
        </div>
      </div>

      <p v-if="error" class="rw-error">{{ error }}</p>
      <p v-else-if="!items.length" class="rw-muted">Brak aktywnych i planowanych ograniczeń.</p>

      <div v-for="r in items" :key="r.id" class="rw-item-row">
        <button type="button" class="rw-item" @click="focusItem(r)">
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
        <button type="button" class="rw-del" title="Usuń blokadę" @click="askDelete(r)">🗑</button>
      </div>

      <div class="rw-legend">
        <span v-for="(color, kind) in KIND_COLORS" :key="kind">
          <i :style="{ background: color }"></i>{{ kind }}
        </span>
        <span class="rw-muted">linia przerywana = planowane</span>
      </div>
    </aside>
    <div v-if="confirmTarget" class="rw-modal-backdrop" @click.self="cancelDelete">
      <div class="rw-modal">
        <h3>Usunąć blokadę?</h3>
        <p>
          Czy na pewno chcesz usunąć <b>{{ confirmTarget.title }}</b>? Tej operacji nie można cofnąć.
        </p>
        <p v-if="deleteError" class="rw-error">{{ deleteError }}</p>
        <div class="rw-row">
          <button type="button" class="rw-btn rw-btn-danger" :disabled="deleting" @click="confirmDelete">
            {{ deleting ? 'Usuwanie…' : 'Tak, usuń' }}
          </button>
          <button type="button" class="rw-btn" :disabled="deleting" @click="cancelDelete">Anuluj</button>
        </div>
      </div>
    </div>
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
.rw-map.is-adding,
.rw-map.is-adding :deep(.leaflet-grab),
.rw-map.is-adding :deep(.leaflet-interactive) {
  cursor: crosshair !important;
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
.rw-btn {
  border: 1px solid #ccc;
  background: #fff;
  color: #111;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 13px;
  cursor: pointer;
}
.rw-btn-primary {
  width: 100%;
  background: #111;
  color: #fff;
  border-color: #111;
  margin-bottom: 8px;
}
.rw-btn:disabled {
  opacity: 0.6;
  cursor: wait;
}
.rw-row {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}
.rw-form {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}
.rw-form label {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: 12px;
  color: #444;
}
.rw-form input,
.rw-form select,
.rw-form textarea {
  font: inherit;
  font-size: 13px;
  padding: 6px 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
  color: #111;
  background: #fff;
}
.rw-hint {
  background: #fef3c7;
  border-radius: 8px;
  padding: 10px;
  font-size: 13px;
  margin: 0;
}
.rw-saved {
  font-size: 13px;
  margin: 0 0 8px;
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
  font-size: 13px;
  margin: 0;
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

.rw-item-row {
  display: flex;
  gap: 6px;
  margin-bottom: 8px;
}
.rw-item-row .rw-item {
  flex: 1;
  width: auto;
  margin-bottom: 0;
}
.rw-del {
  border: 0;
  background: #fee2e2;
  border-radius: 8px;
  padding: 0 10px;
  cursor: pointer;
  font-size: 16px;
}
.rw-del:hover {
  background: #fecaca;
}
.rw-modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 3000;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
}
.rw-modal {
  background: #fff;
  color: #111;
  border-radius: 12px;
  padding: 20px;
  width: 340px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
}
.rw-modal h3 {
  margin: 0 0 8px;
}
.rw-btn-danger {
  background: #b91c1c;
  border-color: #b91c1c;
  color: #fff;
}
</style>