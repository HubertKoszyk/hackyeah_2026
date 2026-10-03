<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AppButton from '../components/common/AppButton.vue'
import AppInput from '../components/common/AppInput.vue'
import AppTextarea from '../components/common/AppTextarea.vue'
import AppLink from '../components/common/AppLink.vue'
import AppCheckbox from '../components/common/AppCheckbox.vue'
import AppRadio from '../components/common/AppRadio.vue'
import AppTabs, { type TabItem } from '../components/common/AppTabs.vue'
import AppBreadcrumb from '../components/common/AppBreadcrumb.vue'
import { fetchParkingSpots, type ParkingItem } from '../services/api'

const parkings = ref<ParkingItem[]>([])
const loading = ref(true)
const apiStatus = ref<'checking' | 'connected' | 'error'>('checking')
const errorMessage = ref('')

// Reactive values for inputs
const sampleInput = ref('')
const sampleTextarea = ref('')
const sampleCheckbox = ref(true)
const sampleRadio = ref('option1')
const activeTab = ref('fav1')

const sampleTabs: TabItem[] = [
  { id: 'fav1', label: 'Favorites' },
  { id: 'fav2', label: 'Favorites' },
  { id: 'fav3', label: 'Favorites' },
  { id: 'fav4', label: 'Favorites' },
  { id: 'fav5', label: 'Favorites' },
  { id: 'fav6', label: 'Favorites' },
]

const breadcrumbItems = [
  { label: 'Link', href: '#' },
  { label: 'Link', href: '#' },
  { label: 'Link', href: '#' },
  { label: 'Link', href: '#' },
  { label: 'Link', href: '#' },
  { label: 'Link', href: '#', external: true },
]

onMounted(async () => {
  try {
    const data = await fetchParkingSpots()
    parkings.value = data
    apiStatus.value = 'connected'
  } catch (err: any) {
    apiStatus.value = 'error'
    errorMessage.value = err?.message || 'Błąd połączenia z backendem Django'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <main class="showcase-container">
    <!-- Header -->
    <header class="showcase-header">
      <div class="brand">
        <span class="status-dot" :class="apiStatus"></span>
        <span class="text-sm text-muted">Smart City Traffic & Parking UI</span>
      </div>
      <div class="api-badge" :class="apiStatus">
        API (Django 8001): {{ apiStatus === 'connected' ? 'POŁĄCZONO' : apiStatus === 'checking' ? 'ŁĄCZENIE...' : 'BŁĄD' }}
      </div>
    </header>

    <!-- SECTION 1: TYPOGRAPHY (From Image 1) -->
    <section class="card section-typography">
      <div class="section-title">
        <span class="text-xs text-muted">DESIGN SYSTEM</span>
        <h3 class="text-h3">Typografia (Font: Plus Jakarta Sans)</h3>
      </div>

      <div class="typography-list">
        <div class="type-row">
          <span class="type-badge">H1</span>
          <h1 class="text-h1">H1 – Najlepsza aplikacja smart city winner</h1>
        </div>

        <div class="type-row">
          <span class="type-badge">H2</span>
          <h2 class="text-h2">H2 – Najlepsza aplikacja smart city winner</h2>
        </div>

        <div class="type-row">
          <span class="type-badge">H3</span>
          <h3 class="text-h3">H3 – Najlepsza aplikacja smart city winner</h3>
        </div>

        <div class="type-row">
          <span class="type-badge">Lg</span>
          <p class="text-lg">Lg - Najlepsza aplikacja smart city winner</p>
        </div>

        <div class="type-row">
          <span class="type-badge">Md</span>
          <p class="text-md">Md - Najlepsza aplikacja smart city winner</p>
        </div>

        <div class="type-row">
          <span class="type-badge">Sm</span>
          <p class="text-sm">Sm - Najlepsza aplikacja smart city winner</p>
        </div>

        <div class="type-row">
          <span class="type-badge">Xs</span>
          <p class="text-xs">Xs - Najlepsza aplikacja smart city winner</p>
        </div>
      </div>
    </section>

    <!-- SECTION 2: BUTTONS (From Image 2) -->
    <section class="card section-buttons">
      <div class="section-title">
        <span class="text-xs text-muted">FIGMA COMPONENTS</span>
        <h3 class="text-h3">Warianty przycisków (&lt;AppButton /&gt;)</h3>
      </div>

      <div class="buttons-matrix-container">
        <!-- Row 1: Primary Variants -->
        <div class="buttons-row">
          <AppButton variant="primary" left-icon right-icon>Button</AppButton>
          <AppButton variant="primary-soft" left-icon right-icon>Button</AppButton>
          <AppButton variant="primary-soft" left-icon right-icon>Button</AppButton>
        </div>

        <!-- Row 2: Secondary / Dark Variants -->
        <div class="buttons-row">
          <AppButton variant="secondary" left-icon right-icon>Button</AppButton>
          <AppButton variant="secondary" left-icon right-icon>Button</AppButton>
          <AppButton variant="primary-soft" left-icon right-icon>Button</AppButton>
        </div>

        <!-- Row 3: Outline & Special Variants -->
        <div class="buttons-row">
          <AppButton variant="outline" left-icon right-icon>Button</AppButton>
          <AppButton variant="outline-blue" left-icon right-icon>Button</AppButton>
          <AppButton variant="primary-soft" left-icon right-icon>Button</AppButton>
        </div>
      </div>
    </section>

    <!-- SECTION 3: FORM FIELDS & INPUTS (From Figma Image) -->
    <section class="card section-forms">
      <div class="section-title">
        <span class="text-xs text-muted">FIGMA FORM COMPONENTS</span>
        <h3 class="text-h3">Pola formularza (&lt;AppInput /&gt;, &lt;AppTextarea /&gt;, &lt;AppLink /&gt;)</h3>
      </div>

      <div class="forms-showcase-grid">
        <!-- Field Labels & Inputs Matrix -->
        <div class="form-column">
          <span class="text-xs text-muted font-semibold">❖ Field / Input</span>
          <div class="fields-matrix">
            <AppInput
              v-model="sampleInput"
              label="Label"
              placeholder="Placeholder"
            />
            <AppInput
              label="Label"
              required
              placeholder="Placeholder"
            />
          </div>
        </div>

        <!-- Textarea -->
        <div class="form-column">
          <span class="text-xs text-muted font-semibold">❖ Text area</span>
          <AppTextarea
            v-model="sampleTextarea"
            label="Label"
            placeholder="Placeholder"
            :rows="3"
          />
        </div>

        <!-- Links -->
        <div class="form-column">
          <span class="text-xs text-muted font-semibold">❖ Link</span>
          <div class="links-row">
            <AppLink href="#showcase">Link</AppLink>
            <AppLink href="#showcase" underline>Podkreślony link</AppLink>
            <AppLink href="#showcase" variant="muted">Muted link</AppLink>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 4: COLOR PALETTE (From Figma Image 3) -->
    <section class="card section-palette">
      <div class="section-title">
        <span class="text-xs text-muted">PALETA KOLORÓW FIGMA</span>
        <h3 class="text-h3">Oficjalna Paleta (Brand Blue, Error, Warning, Success, Gray)</h3>
      </div>

      <div class="palette-grid">
        <!-- Brand Column -->
        <div class="palette-column">
          <span class="palette-col-title">Brand</span>
          <div class="swatch-stack">
            <div class="swatch" style="background: rgb(var(--brand-900)); color: #fff;">900</div>
            <div class="swatch" style="background: rgb(var(--brand-800)); color: #fff;">800</div>
            <div class="swatch" style="background: rgb(var(--brand-700)); color: #fff;">700</div>
            <div class="swatch" style="background: rgb(var(--brand-600)); color: #fff;">600</div>
            <div class="swatch swatch-main" style="background: rgb(var(--brand-500)); color: #fff;">500 ★</div>
            <div class="swatch" style="background: rgb(var(--brand-400)); color: #fff;">400</div>
            <div class="swatch" style="background: rgb(var(--brand-300)); color: #000;">300</div>
            <div class="swatch" style="background: rgb(var(--brand-200)); color: #000;">200</div>
            <div class="swatch" style="background: rgb(var(--brand-100)); color: #000;">100</div>
            <div class="swatch" style="background: rgb(var(--brand-50)); color: #000;">50</div>
          </div>
        </div>

        <!-- Error Column -->
        <div class="palette-column">
          <span class="palette-col-title">Error</span>
          <div class="swatch-stack">
            <div class="swatch" style="background: rgb(var(--error-900)); color: #fff;">900</div>
            <div class="swatch" style="background: rgb(var(--error-800)); color: #fff;">800</div>
            <div class="swatch" style="background: rgb(var(--error-700)); color: #fff;">700</div>
            <div class="swatch" style="background: rgb(var(--error-600)); color: #fff;">600</div>
            <div class="swatch swatch-main" style="background: rgb(var(--error-500)); color: #fff;">500 ★</div>
            <div class="swatch" style="background: rgb(var(--error-400)); color: #fff;">400</div>
            <div class="swatch" style="background: rgb(var(--error-300)); color: #000;">300</div>
            <div class="swatch" style="background: rgb(var(--error-200)); color: #000;">200</div>
            <div class="swatch" style="background: rgb(var(--error-100)); color: #000;">100</div>
            <div class="swatch" style="background: rgb(var(--error-50)); color: #000;">50</div>
          </div>
        </div>

        <!-- Warning Column -->
        <div class="palette-column">
          <span class="palette-col-title">Warning</span>
          <div class="swatch-stack">
            <div class="swatch" style="background: rgb(var(--warning-900)); color: #fff;">900</div>
            <div class="swatch" style="background: rgb(var(--warning-800)); color: #fff;">800</div>
            <div class="swatch" style="background: rgb(var(--warning-700)); color: #fff;">700</div>
            <div class="swatch" style="background: rgb(var(--warning-600)); color: #fff;">600</div>
            <div class="swatch swatch-main" style="background: rgb(var(--warning-500)); color: #fff;">500 ★</div>
            <div class="swatch" style="background: rgb(var(--warning-400)); color: #000;">400</div>
            <div class="swatch" style="background: rgb(var(--warning-300)); color: #000;">300</div>
            <div class="swatch" style="background: rgb(var(--warning-200)); color: #000;">200</div>
            <div class="swatch" style="background: rgb(var(--warning-100)); color: #000;">100</div>
            <div class="swatch" style="background: rgb(var(--warning-50)); color: #000;">50</div>
          </div>
        </div>

        <!-- Success Column -->
        <div class="palette-column">
          <span class="palette-col-title">Success</span>
          <div class="swatch-stack">
            <div class="swatch" style="background: rgb(var(--success-900)); color: #fff;">900</div>
            <div class="swatch" style="background: rgb(var(--success-800)); color: #fff;">800</div>
            <div class="swatch" style="background: rgb(var(--success-700)); color: #fff;">700</div>
            <div class="swatch" style="background: rgb(var(--success-600)); color: #fff;">600</div>
            <div class="swatch swatch-main" style="background: rgb(var(--success-500)); color: #fff;">500 ★</div>
            <div class="swatch" style="background: rgb(var(--success-400)); color: #000;">400</div>
            <div class="swatch" style="background: rgb(var(--success-300)); color: #000;">300</div>
            <div class="swatch" style="background: rgb(var(--success-200)); color: #000;">200</div>
            <div class="swatch" style="background: rgb(var(--success-100)); color: #000;">100</div>
            <div class="swatch" style="background: rgb(var(--success-50)); color: #000;">50</div>
          </div>
        </div>

        <!-- Gray Column -->
        <div class="palette-column">
          <span class="palette-col-title">Gray</span>
          <div class="swatch-stack">
            <div class="swatch" style="background: rgb(var(--gray-900)); color: #fff;">900</div>
            <div class="swatch" style="background: rgb(var(--gray-800)); color: #fff;">800</div>
            <div class="swatch" style="background: rgb(var(--gray-700)); color: #fff;">700</div>
            <div class="swatch" style="background: rgb(var(--gray-600)); color: #fff;">600</div>
            <div class="swatch" style="background: rgb(var(--gray-500)); color: #fff;">500</div>
            <div class="swatch" style="background: rgb(var(--gray-400)); color: #000;">400</div>
            <div class="swatch" style="background: rgb(var(--gray-300)); color: #000;">300</div>
            <div class="swatch" style="background: rgb(var(--gray-200)); color: #000;">200</div>
            <div class="swatch" style="background: rgb(var(--gray-100)); color: #000;">100</div>
            <div class="swatch" style="background: rgb(var(--gray-50)); color: #000;">50</div>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 5: NAVIGATION & SELECTION (Breadcrumb, Tabs, Checkboxes, Radios) -->
    <section class="card section-navigation">
      <div class="section-title">
        <span class="text-xs text-muted">KOMPONENTY NAWIGACJI I WYBORU</span>
        <h3 class="text-h3">Breadcrumb, Tabs, Checkbox i Radio</h3>
      </div>

      <div class="nav-selection-grid">
        <!-- Breadcrumbs -->
        <div class="form-column">
          <span class="text-xs text-muted font-semibold">❖ Breadcrumb</span>
          <AppBreadcrumb :items="breadcrumbItems" />
        </div>

        <!-- Tabs -->
        <div class="form-column">
          <span class="text-xs text-muted font-semibold">❖ Tab &amp; .tabitem</span>
          <AppTabs v-model="activeTab" :tabs="sampleTabs" />
        </div>

        <!-- Checkboxes -->
        <div class="form-column">
          <span class="text-xs text-muted font-semibold">❖ Checkbox</span>
          <div class="selection-row">
            <AppCheckbox v-model="sampleCheckbox" label="Checkbox label" />
            <AppCheckbox :model-value="false" label="Niezaznaczony" />
            <AppCheckbox :model-value="true" disabled label="Zablokowany" />
          </div>
        </div>

        <!-- Radios -->
        <div class="form-column">
          <span class="text-xs text-muted font-semibold">❖ Radio button</span>
          <div class="selection-row">
            <AppRadio v-model="sampleRadio" value="option1" label="Radio button label" />
            <AppRadio v-model="sampleRadio" value="option2" label="Druga opcja" />
            <AppRadio :model-value="'other'" value="option3" disabled label="Zablokowane" />
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 6: LIVE BACKEND DATA -->
    <section class="card section-data">
      <div class="section-title">
        <span class="text-xs text-muted">INTEGRACJA DJANGO</span>
        <h3 class="text-h3">Dane z backendu (/parking/get/all/)</h3>
      </div>

      <div v-if="loading" class="text-md text-muted">
        Pobieranie parkingów z Django...
      </div>

      <div v-else-if="apiStatus === 'connected'" class="parking-grid">
        <div v-for="spot in parkings" :key="spot.id" class="parking-card">
          <div class="parking-card-header">
            <span class="text-md font-bold">{{ spot.name }}</span>
            <span class="status-pill" :class="spot.status">{{ spot.status }}</span>
          </div>
          <p class="text-sm text-muted">Współrzędne: {{ spot.lat }}, {{ spot.lng }}</p>
          <div class="parking-stats">
            <span class="text-sm font-semibold">Wolne miejsca:</span>
            <span class="text-md font-bold text-primary">{{ spot.freeSpots }} / {{ spot.totalSpots }}</span>
          </div>
        </div>
      </div>

      <div v-else class="error-box text-sm">
        Nie udało się połączyć z backendem Django ({{ errorMessage }}). Upewnij się, że serwer działa na porcie 8001.
      </div>
    </section>
    <div>
    <h3>
      <a href='/landing'>Tu tak dziala?</a>
    </h3>
    </div>
  </main>
</template>

<style scoped>
.showcase-container {
  max-width: 1040px;
  margin: 0 auto;
  padding: 2.5rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.showcase-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-dark-border);
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: var(--color-warning);
}
.status-dot.connected {
  background-color: var(--color-success);
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
}
.status-dot.error {
  background-color: var(--color-danger);
}

.api-badge {
  font-size: var(--font-size-xs);
  font-weight: 600;
  padding: 0.35rem 0.75rem;
  border-radius: var(--radius-full);
  border: 1px solid var(--color-dark-border);
  background: var(--color-dark-surface);
}
.api-badge.connected {
  color: var(--color-success);
  border-color: rgba(16, 185, 129, 0.3);
}
.api-badge.error {
  color: var(--color-danger);
  border-color: rgba(239, 68, 68, 0.3);
}

.card {
  background-color: var(--color-dark-card);
  border: 1px solid var(--color-dark-border);
  border-radius: var(--radius-lg);
  padding: 1.75rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.section-title {
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

/* Typography List */
.typography-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.type-row {
  display: flex;
  align-items: baseline;
  gap: 1.5rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}
.type-row:last-child {
  border-bottom: none;
}

.type-badge {
  display: inline-block;
  min-width: 38px;
  padding: 2px 6px;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--color-primary-soft);
  background: var(--color-primary-muted);
  border-radius: var(--radius-sm);
  text-align: center;
}

/* Button Matrix from Image 2 */
.buttons-matrix-container {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  padding: 1.5rem;
  background: #17191d;
  border: 1px dashed rgba(168, 85, 247, 0.4); /* Figma purple frame style */
  border-radius: var(--radius-md);
  width: fit-content;
}

.buttons-row {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* Parking Data */
.parking-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.parking-card {
  background: var(--color-dark-surface);
  border: 1px solid var(--color-dark-border);
  border-radius: var(--radius-md);
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.parking-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-pill {
  font-size: var(--font-size-xs);
  padding: 2px 8px;
  border-radius: var(--radius-full);
  text-transform: uppercase;
  font-weight: 700;
}
.status-pill.available {
  background: rgba(16, 185, 129, 0.2);
  color: #34d399;
}
.status-pill.almost_full {
  background: rgba(245, 158, 11, 0.2);
  color: #fbbf24;
}

.parking-stats {
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.error-box {
  background: rgba(239, 68, 68, 0.1);
  color: #f87171;
  padding: 1rem;
  border-radius: var(--radius-md);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

/* Forms Showcase Styles */
.forms-showcase-grid {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-column {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.fields-matrix {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
}

.links-row {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 0.5rem 0;
}

/* Palette Showcase */
.palette-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1.25rem;
}

.palette-column {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.palette-col-title {
  font-size: var(--font-size-sm);
  font-weight: 700;
  color: #ffffff;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.swatch-stack {
  display: flex;
  flex-direction: column;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.swatch {
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.05em;
}
.swatch-main {
  height: 34px;
  outline: 2px solid #ffffff;
  z-index: 1;
}

/* Nav & Selection Showcase */
.nav-selection-grid {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.selection-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 2rem;
  padding: 0.5rem 0;
}
</style>
