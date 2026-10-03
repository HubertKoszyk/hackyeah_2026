<script setup lang="ts">
interface Props {
  modelValue?: boolean
  label?: string
  disabled?: boolean
  id?: string
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: false,
  label: '',
  disabled: false,
  id: () => `checkbox-${Math.random().toString(36).substring(2, 9)}`,
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
}>()

const onChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.checked)
}
</script>

<template>
  <label :for="id" class="app-checkbox" :class="{ 'is-disabled': disabled }">
    <input
      :id="id"
      type="checkbox"
      :checked="modelValue"
      :disabled="disabled"
      class="checkbox-input"
      @change="onChange"
    />
    <span class="checkbox-box">
      <!-- Checkmark Icon -->
      <svg
        v-if="modelValue"
        viewBox="0 0 16 16"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        class="check-icon"
      >
        <path
          d="M3.5 8.5L6.5 11.5L12.5 5"
          stroke="white"
          stroke-width="2.2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </span>
    <span v-if="label || $slots.default" class="checkbox-label">
      <slot>{{ label }}</slot>
    </span>
  </label>
</template>

<style scoped>
.app-checkbox {
  display: inline-flex;
  align-items: center;
  gap: 0.65rem;
  font-family: var(--font-family-primary);
  font-size: var(--font-size-md);
  color: var(--color-text-main);
  cursor: pointer;
  user-select: none;
  transition: all 0.2s ease;
}

.checkbox-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
  pointer-events: none;
}

.checkbox-box {
  width: 22px;
  height: 22px;
  border-radius: 6px;
  background-color: #e5e8ee;
  border: 1.5px solid transparent;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
  flex-shrink: 0;
}

.app-checkbox:hover:not(.is-disabled) .checkbox-box {
  background-color: rgb(var(--brand-200));
}

.checkbox-input:checked + .checkbox-box {
  background-color: rgb(var(--brand-500));
  border-color: rgb(var(--brand-500));
  box-shadow: 0 2px 8px rgba(0, 98, 255, 0.35);
}

.checkbox-input:focus-visible + .checkbox-box {
  outline: 2px solid rgb(var(--brand-400));
  outline-offset: 2px;
}

.check-icon {
  width: 14px;
  height: 14px;
}

.checkbox-label {
  line-height: 1.4;
}

.app-checkbox.is-disabled {
  opacity: 0.45;
  cursor: not-allowed;
}
</style>
