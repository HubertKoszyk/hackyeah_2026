<style scoped>
/* Stylowanie standardowych tagów HTML wewnątrz komponentu */
h1 {
    /* Użycie głównego fioletu z kategorii Brand */
    color: rgb(var(--brand-500));
}

p {
    /* Użycie skali szarości z dodatkiem 80% przezroczystości (kanał alfa) */
    color: rgb(var(--gray-900) / 80%);
}

.warning-text {
    /* Użycie koloru ostrzegawczego */
    color: rgb(var(--warning-500));
}
</style>

<script setup lang="ts">
import { ref } from 'vue';

// Import wszystkich 8 komponentów bazowych widocznych w drzewie projektu
import AppButton from '../components/common/AppButton.vue';
import AppInput from '../components/common/AppInput.vue';
import AppTextarea from '../components/common/AppTextarea.vue';
import AppLink from '../components/common/AppLink.vue';
import AppCheckbox from '../components/common/AppCheckbox.vue';
import AppRadio from '../components/common/AppRadio.vue';
import AppTabs, { type TabItem } from '../components/common/AppTabs.vue';
import AppBreadcrumb from '../components/common/AppBreadcrumb.vue';

// 1. Nawigacja i zakładki[cite: 5]
const breadcrumbItems = [
    { label: 'Strona Główna', href: '/' },
    { label: 'Test Komponentów', href: '#' }
];

const activeTab = ref('formularz');
const sampleTabs: TabItem[] = [
    { id: 'formularz', label: 'Dane podstawowe' },
    { id: 'opcje', label: 'Wybór wariantów' }
];

// 2. Stan (zmienne reaktywne) dla pól formularza[cite: 5]
const sampleInput = ref('');
const sampleTextarea = ref('');
const sampleCheckbox = ref(false);
const sampleRadio = ref('opcja_A');

// 3. Logika testowa po kliknięciu przycisku
const weryfikujDane = () => {
    console.log('--- Wprowadzone dane ---');
    console.log('Input:', sampleInput.value);
    console.log('Textarea:', sampleTextarea.value);
    console.log('Radio:', sampleRadio.value);
    console.log('Checkbox:', sampleCheckbox.value);
};
</script>

<template>

    <main class="sandbox-container">
        <h1>Hello World</h1>
        <!-- Komponent 1: Ścieżka nawigacyjna[cite: 5] -->
        <AppBreadcrumb :items="breadcrumbItems" class="mb-4" />

        <!-- Komponent 2: System zakładek[cite: 5] -->
        <AppTabs :tabs="sampleTabs" v-model="activeTab" />

        <!-- Warunkowe renderowanie za pomocą v-show, by nie tracić danych formularza przy przełączaniu zakładek -->
        <section v-show="activeTab === 'formularz'" class="tab-panel">
            
            <!-- Komponent 3: Standardowe pole tekstowe[cite: 5] -->
            <AppInput 
                
                v-model="sampleInput" 
                label="Tytuł zgłoszenia" 
                placeholder="Wpisz krótki tytuł..." 
            />
            
            <!-- Komponent 4: Wieloliniowe pole tekstowe[cite: 5] -->
            <AppTextarea 
                v-model="sampleTextarea" 
                
                label="Opis szczegółowy" 
                placeholder="Podaj więcej informacji..." 
            />

            <!-- Komponent 5: Pole wyboru[cite: 5] -->
            <AppCheckbox    
                v-model="sampleCheckbox" 
                label="Akceptuję przetwarzanie danych" 
            />
            
            
        </section>

        <section v-show="activeTab === 'opcje'" class="tab-panel">
            <p class="section-title">Wybierz priorytet zadania:</p>
            
            <div class="radio-group">
                <!-- Komponent 6: Przyciski opcji[cite: 5] -->
                <AppRadio 
                    v-model="sampleRadio" 
                    
                    value="opcja_A" 
                    label="Priorytet Normalny" 
                />
                <AppRadio 
                    v-model="sampleRadio" 
                    value="opcja_B" 
                    label="Priorytet Wysoki" 
                />
            </div>
        </section>

        <hr class="divider" />

        <footer class="action-footer">
            <!-- Komponent 7: Link do strony zewnętrznej[cite: 5] -->
            <AppLink href="https://vuejs.org" external>
                Potrzebujesz pomocy?
            </AppLink>
            
            <!-- Komponent 8: Przycisk akcji blokowany do czasu zaznaczenia checkboxa[cite: 5] -->
            <AppButton @click="weryfikujDane" :disabled="!sampleCheckbox">
                Wyślij formularz do konsoli
            </AppButton>
        </footer>
    </main>
</template>

<style scoped>
/* Style izolowane na potrzeby piaskownicy komponentów */
.sandbox-container {
    max-width: 700px;
    margin: 2rem auto;
    padding: 2rem;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.tab-panel {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding: 2rem 0;
}

.section-title {
    margin: 0 0 1rem 0;
    font-weight: 600;
}

.radio-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.divider {
    margin: 1.5rem 0;
    border: 0;
    border-top: 1px solid #e5e7eb;
}

.action-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.mb-4 {
    margin-bottom: 1.5rem;
}
</style>