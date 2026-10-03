<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  modelValue?: string
  label?: string
  placeholder?: string
  rows?: number
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
  rows: 4,
  required: false,
  hasInfo: true,
  infoText: '',
  leftIcon: true,
  rightIcon: true,
  disabled: false,
  error: '',
  id: () => `textarea-${Math.random().toString(36).substring(2, 9)}`,
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'clickInfo'): void
}>()

const onInput = (event: Event) => {
  const target = event.target as HTMLTextAreaElement
  emit('update:modelValue', target.value)
}

const wrapperClasses = computed(() => [
  'textarea-field-wrapper',
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
            <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.8" />
            <path d="M10 9V14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
            <circle cx="10" cy="6.5" r="0.9" fill="currentColor" />
          </svg>
        </slot>
      </button>
    </div>

    <!-- Textarea Box -->
    <div class="textarea-control-box">
      <!-- Top Row with Icons -->
      <div class="textarea-header-icons">
        <span v-if="$slots.leftIcon || leftIcon" class="control-icon icon-left">
          <slot name="leftIcon">
            <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-svg">
              <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.8" />
              <path d="M10 9V14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
              <circle cx="10" cy="6.5" r="0.9" fill="currentColor" />
            </svg>
          </slot>
        </span>

        <span v-if="$slots.rightIcon || rightIcon" class="control-icon icon-right">
          <slot name="rightIcon">
            <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-svg">
              <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.8" />
              <path d="M10 9V14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
              <circle cx="10" cy="6.5" r="0.9" fill="currentColor" />
            </svg>
          </slot>
        </span>
      </div>

      <!-- Native Textarea -->
      <textarea
        :id="id"
        :rows="rows"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        class="native-textarea"
        @input="onInput"
      ></textarea>
    </div>

    <!-- Error Message -->
    <span v-if="error" class="error-text text-xs">{{ error }}</span>
  </div>
</template>

<style scoped>
.textarea-field-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  width: 100%;
  font-family: var(--font-family-primary);
}

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

.textarea-control-box {
  position: relative;
  background-color: #e5e8ee;
  border: 1.5px solid transparent;
  border-radius: 12px;
  padding: 0.75rem 0.85rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-height: 110px;
  transition: all 0.2s ease;
}

.textarea-control-box:focus-within {
  background-color: #ffffff;
  border-color: var(--color-primary-electric);
  box-shadow: 0 0 0 3px rgba(26, 98, 255, 0.2);
}

.textarea-header-icons {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #64748b;
}

.control-icon {
  display: inline-flex;
  align-items: center;
}

.icon-svg {
  width: 1.15rem;
  height: 1.15rem;
}

.native-textarea {
  width: 100%;
  border: none;
  background: transparent;
  font-family: var(--font-family-primary);
  font-size: var(--font-size-md);
  color: #1a1e24;
  resize: vertical;
  outline: none;
  line-height: 1.5;
}

.native-textarea::placeholder {
  color: #838a97;
}

.has-error .textarea-control-box {
  border-color: #ef4444;
  background-color: #fff5f5;
}
.error-text {
  color: #ef4444;
  font-weight: 500;
}

.is-disabled {
  opacity: 0.55;
  pointer-events: none;
}
</style>
