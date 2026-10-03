<script setup lang="ts">
export interface TabItem {
  id: string | number
  label: string
  icon?: string
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
      <!-- Heart Icon matching Figma or custom slot -->
      <span class="tab-icon">
        <slot name="icon" :tab="tab">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-svg">
            <path
              d="M10 16.5C10 16.5 2.5 12 2.5 7.5C2.5 5 4.5 3 7 3C8.5 3 9.5 3.8 10 4.5C10.5 3.8 11.5 3 13 3C15.5 3 17.5 5 17.5 7.5C17.5 12 10 16.5 10 16.5Z"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linejoin="round"
            />
          </svg>
        </slot>
      </span>
      <span class="tab-label">{{ tab.label }}</span>
    </button>
  </div>
</template>

<style scoped>
.app-tabs-container {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem;
  background-color: #e5e8ee;
  border-radius: 14px;
  overflow-x: auto;
  max-width: 100%;
}

.tab-item {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.55rem 1.15rem;
  font-family: var(--font-family-primary);
  font-size: var(--font-size-md);
  font-weight: 500;
  border-radius: 10px;
  border: none;
  background-color: transparent;
  color: #1a1e24;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
}

.tab-item:hover:not(.is-active) {
  background-color: rgb(var(--brand-200));
}

.tab-item.is-active {
  background-color: rgb(var(--brand-500));
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 98, 255, 0.3);
}

.tab-icon {
  display: inline-flex;
  align-items: center;
}

.icon-svg {
  width: 1.15rem;
  height: 1.15rem;
}
</style>
