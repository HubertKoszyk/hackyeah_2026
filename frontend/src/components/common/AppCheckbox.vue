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
  gap: 8px;
  font-family: var(--font-family-body);
  font-size: 16px;
  line-height: 20px;
  color: #191919;
  cursor: pointer;
  user-select: none;
}

.checkbox-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
  pointer-events: none;
}

/* Figma: cornerRadius: 8px, size: 24px */
.checkbox-box {
  width: 24px;
  height: 24px;
  border-radius: 8px; /* cornerRadius: 8.0px w Figmie */
  background-color: #f5f5f5; /* unchecked default w Figmie */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
  flex-shrink: 0;
}

.app-checkbox:hover:not(.is-disabled) .checkbox-box {
  background-color: #99b6ff; /* state=hover, checked=false w Figmie */
}

.checkbox-input:checked + .checkbox-box {
  background-color: #0048ff; /* state=default, checked=true w Figmie */
}

.app-checkbox:hover:not(.is-disabled) .checkbox-input:checked + .checkbox-box {
  background-color: #336dff; /* state=hover, checked=true w Figmie */
}

.check-icon {
  width: 14px;
  height: 14px;
}

.app-checkbox.is-disabled .checkbox-box {
  background-color: #c7c7c7; /* state=disabled w Figmie */
}
.app-checkbox.is-disabled {
  color: #7b7b7b;
  cursor: not-allowed;
}
</style>
