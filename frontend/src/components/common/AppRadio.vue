<script setup lang="ts">
interface Props {
  modelValue?: string | number | boolean
  value: string | number | boolean
  label?: string
  name?: string
  disabled?: boolean
  id?: string
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  label: '',
  name: '',
  disabled: false,
  id: () => `radio-${Math.random().toString(36).substring(2, 9)}`,
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | number | boolean): void
}>()

const isChecked = () => props.modelValue === props.value

const onChange = () => {
  emit('update:modelValue', props.value)
}
</script>

<template>
  <label :for="id" class="app-radio" :class="{ 'is-disabled': disabled }">
    <input
      :id="id"
      type="radio"
      :name="name"
      :checked="isChecked()"
      :disabled="disabled"
      class="radio-input"
      @change="onChange"
    />
    <span class="radio-circle">
      <span v-if="isChecked()" class="radio-inner-dot"></span>
    </span>
    <span v-if="label || $slots.default" class="radio-label">
      <slot>{{ label }}</slot>
    </span>
  </label>
</template>

<style scoped>
.app-radio {
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

.radio-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
  pointer-events: none;
}

.radio-circle {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background-color: #e5e8ee;
  border: 1.5px solid transparent;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
  flex-shrink: 0;
}

.app-radio:hover:not(.is-disabled) .radio-circle {
  background-color: rgb(var(--brand-200));
}

.radio-input:checked + .radio-circle {
  background-color: rgb(var(--brand-500));
  border-color: rgb(var(--brand-500));
  box-shadow: 0 2px 8px rgba(0, 98, 255, 0.35);
}

.radio-inner-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #ffffff;
}

.radio-label {
  line-height: 1.4;
}

.app-radio.is-disabled {
  opacity: 0.45;
  cursor: not-allowed;
}
</style>
