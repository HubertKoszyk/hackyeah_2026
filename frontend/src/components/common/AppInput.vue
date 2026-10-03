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
    <!-- Label -->
    <div v-if="label" class="label-row">
      <label :for="id" class="field-label">
        <span v-if="required" class="required-star">*</span>
        {{ label }}
      </label>

      <!-- Info Icon (ℹ) -->
      <button
        v-if="hasInfo"
        type="button"
        class="info-btn"
        :title="infoText || 'Więcej informacji'"
        @click="emit('clickInfo')"
      >
        <slot name="infoIcon">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-svg">
            <circle cx="10" cy="10" r="7.5" stroke="currentColor" stroke-width="1.8" />
            <path d="M10 9V14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
            <circle cx="10" cy="6.5" r="0.9" fill="currentColor" />
          </svg>
        </slot>
      </button>
    </div>

    <!-- Field Box (Figma Node: Field 4:31168) -->
    <div class="input-control-box">
      <!-- Left Icon -->
      <span v-if="$slots.leftIcon || leftIcon" class="control-icon icon-left">
        <slot name="leftIcon">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-svg">
            <circle cx="10" cy="10" r="7.5" stroke="currentColor" stroke-width="1.8" />
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
            <circle cx="10" cy="10" r="7.5" stroke="currentColor" stroke-width="1.8" />
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
  gap: 4px;
  width: 100%;
  font-family: var(--font-family-body);
}

.label-row {
  display: flex;
  align-items: center;
  gap: 4px;
}

.field-label {
  font-family: var(--font-family-body);
  font-size: 14px;
  line-height: 16px;
  font-weight: 400;
  color: #191919; /* Gray 900 w Figmie */
}

.required-star {
  color: #ec1f00; /* Error 500 w Figmie */
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
  color: #191919;
}

/* Field Container: fill: #f5f5f5, cornerRadius: 8px, pad: (12, 8) */
.input-control-box {
  display: flex;
  align-items: center;
  background-color: #f5f5f5; /* Gray 50 w Figmie */
  border: 1px solid transparent;
  border-radius: 8px; /* cornerRadius: 8.0px w Figmie */
  padding: 8px 12px; /* pad: (12, 8) w Figmie */
  gap: 8px;
  transition: all 0.15s ease;
  box-sizing: border-box;
}

.input-control-box:focus-within {
  background-color: #ffffff;
  border-color: #0048ff; /* Brand 500 w Figmie */
  box-shadow: 0 0 0 2px rgba(0, 72, 255, 0.2);
}

.native-input {
  flex: 1;
  border: none;
  background: transparent;
  font-family: var(--font-family-body);
  font-size: 16px;
  line-height: 20px;
  color: #191919;
  font-weight: 400;
  outline: none;
  min-width: 0;
}

.native-input::placeholder {
  color: #626262; /* Gray 600 w Figmie */
  font-weight: 400;
}

.control-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #191919;
  flex-shrink: 0;
}

.icon-svg {
  width: 16px;
  height: 16px;
}

.has-error .input-control-box {
  border-color: #ec1f00;
  background-color: #fde9e5;
}
.error-text {
  color: #ec1f00;
  font-weight: 400;
}

.is-disabled {
  opacity: 0.5;
  pointer-events: none;
}
</style>
