<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  modelValue?: string | number
  label?: string
  placeholder?: string
  type?: string
  required?: boolean
  hasInfo?: boolean
  infoText?: string
  leftIcon?: boolean
  rightIcon?: boolean
  disabled?: boolean
  error?: string
  id?: string
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  label: '',
  placeholder: 'Placeholder',
  type: 'text',
  required: false,
  hasInfo: true,
  infoText: '',
  leftIcon: true,
  rightIcon: true,
  disabled: false,
  error: '',
  id: () => `input-${Math.random().toString(36).substring(2, 9)}`,
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'clickInfo'): void
  (e: 'clickRightIcon'): void
}>()

const onInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}

const wrapperClasses = computed(() => [
  'input-field-wrapper',
  {
    'is-disabled': props.disabled,
    'has-error': !!props.error,
  },
])
</script>

<template>
  <div :class="wrapperClasses">
    <!-- Field Label Row -->
    <div v-if="label" class="label-row">
      <label :for="id" class="field-label">
        <span v-if="required" class="required-star">*</span>
        {{ label }}
      </label>

      <!-- Info Icon (ℹ) from Figma -->
      <button
        v-if="hasInfo"
        type="button"
        class="info-btn"
        :title="infoText || 'Więcej informacji'"
        @click="emit('clickInfo')"
      >
        <slot name="infoIcon">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-svg">
            <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.8" />
            <path d="M10 9V14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
            <circle cx="10" cy="6.5" r="0.9" fill="currentColor" />
          </svg>
        </slot>
      </button>
    </div>

    <!-- Input Container -->
    <div class="input-control-box">
      <!-- Left Icon -->
      <span v-if="$slots.leftIcon || leftIcon" class="control-icon icon-left">
        <slot name="leftIcon">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-svg">
            <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.8" />
            <path d="M10 9V14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
            <circle cx="10" cy="6.5" r="0.9" fill="currentColor" />
          </svg>
        </slot>
      </span>

      <!-- Native Input -->
      <input
        :id="id"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        class="native-input"
        @input="onInput"
      />

      <!-- Right Icon -->
      <span
        v-if="$slots.rightIcon || rightIcon"
        class="control-icon icon-right"
        @click="emit('clickRightIcon')"
      >
        <slot name="rightIcon">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-svg">
            <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.8" />
            <path d="M10 9V14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
            <circle cx="10" cy="6.5" r="0.9" fill="currentColor" />
          </svg>
        </slot>
      </span>
    </div>

    <!-- Error Message -->
    <span v-if="error" class="error-text text-xs">{{ error }}</span>
  </div>
</template>

<style scoped>
.input-field-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  width: 100%;
  font-family: var(--font-family-primary);
}

/* Label styling matching Figma */
.label-row {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.field-label {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-text-main);
  user-select: none;
}

.required-star {
  color: #ef4444;
  font-weight: 700;
  margin-right: 2px;
}

.info-btn {
  background: transparent;
  border: none;
  padding: 0;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  color: var(--color-text-muted);
  transition: color 0.2s ease;
}
.info-btn:hover {
  color: #ffffff;
}

/* Control box matching Figma image */
.input-control-box {
  position: relative;
  display: flex;
  align-items: center;
  background-color: #e5e8ee;
  border: 1.5px solid transparent;
  border-radius: 12px;
  padding: 0.55rem 0.85rem;
  gap: 0.6rem;
  transition: all 0.2s ease;
}

.input-control-box:focus-within {
  background-color: #ffffff;
  border-color: var(--color-primary-electric);
  box-shadow: 0 0 0 3px rgba(26, 98, 255, 0.2);
}

.native-input {
  flex: 1;
  border: none;
  background: transparent;
  font-family: var(--font-family-primary);
  font-size: var(--font-size-md);
  color: #1a1e24;
  font-weight: 400;
  outline: none;
  min-width: 0;
}

.native-input::placeholder {
  color: #838a97;
  font-weight: 400;
}

.control-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  flex-shrink: 0;
}

.icon-svg {
  width: 1.15rem;
  height: 1.15rem;
}

/* Error state */
.has-error .input-control-box {
  border-color: #ef4444;
  background-color: #fff5f5;
}
.error-text {
  color: #ef4444;
  font-weight: 500;
}

/* Disabled state */
.is-disabled {
  opacity: 0.55;
  pointer-events: none;
}
</style>
