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
  gap: 8px;
  font-family: var(--font-family-body);
  font-size: 16px;
  line-height: 20px;
  color: #191919;
  cursor: pointer;
  user-select: none;
}

.radio-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
  pointer-events: none;
}

/* Figma: cornerRadius: 9999px (circle), size: 24px */
.radio-circle {
  width: 24px;
  height: 24px;
  border-radius: 9999px;
  background-color: #f5f5f5; /* unchecked default w Figmie */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
  flex-shrink: 0;
}

.app-radio:hover:not(.is-disabled) .radio-circle {
  background-color: #99b6ff; /* state=hover, clicked=false w Figmie */
}

.radio-input:checked + .radio-circle {
  background-color: #0048ff; /* state=default, clicked=true w Figmie */
}

.app-radio:hover:not(.is-disabled) .radio-input:checked + .radio-circle {
  background-color: #336dff; /* state=hover, clicked=true w Figmie */
}

.radio-inner-dot {
  width: 8px;
  height: 8px;
  border-radius: 9999px;
  background-color: #ffffff;
}

.app-radio.is-disabled .radio-circle {
  background-color: #c7c7c7; /* state=disabled w Figmie */
}
.app-radio.is-disabled {
  color: #7b7b7b;
  cursor: not-allowed;
}
</style>
