<script setup lang="ts">
export interface TabItem {
  id: string | number
  label: string
}

interface Props {
  modelValue: string | number
  tabs: TabItem[]
}

defineProps<Props>()

const emit = defineEmits<{
  (e: 'update:modelValue', id: string | number): void
}>()
</script>

<template>
  <div class="app-tabs-container">
    <button
      v-for="tab in tabs"
      :key="tab.id"
      type="button"
      class="tab-item"
      :class="{ 'is-active': modelValue === tab.id }"
      @click="emit('update:modelValue', tab.id)"
    >
      <!-- Heart Icon from Figma -->
      <span class="tab-icon">
        <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-svg">
          <path
            d="M10 16.5C10 16.5 2.5 12 2.5 7.5C2.5 5 4.5 3 7 3C8.5 3 9.5 3.8 10 4.5C10.5 3.8 11.5 3 13 3C15.5 3 17.5 5 17.5 7.5C17.5 12 10 16.5 10 16.5Z"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linejoin="round"
          />
        </svg>
      </span>
      <span class="tab-label">{{ tab.label }}</span>
    </button>
  </div>
</template>

<style scoped>
/* Figma Node: Tab (4:31360) - fill: #f5f5f5, cornerRadius: 8px, padding: 4px, gap: 8px */
.app-tabs-container {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 4px;
  background-color: #f5f5f5;
  border-radius: 8px;
  overflow-x: auto;
  max-width: 100%;
}

/* Figma Node: .tabitem (4:31322) - cornerRadius: 8px, padding: 8px 12px, gap: 4px */
.tab-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  font-family: var(--font-family-body);
  font-size: 16px;
  line-height: 20px;
  font-weight: 400;
  border-radius: 8px;
  border: none;
  background-color: #e7e7e7; /* state=default, type=unselected w Figmie */
  color: #191919;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}

.tab-item:hover:not(.is-active) {
  background-color: #99b6ff; /* state=hover, type=unselected w Figmie */
  color: #191919;
}

.tab-item.is-active {
  background-color: #0048ff; /* state=default, type=selected w Figmie */
  color: #ffffff;
}

.tab-icon {
  display: inline-flex;
  align-items: center;
}

.icon-svg {
  width: 16px;
  height: 16px;
}
</style>
