<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'default' | 'outline' | 'transparent'
  disabled?: boolean
  loading?: boolean
  leftIcon?: boolean
  rightIcon?: boolean
  type?: 'button' | 'submit' | 'reset'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  disabled: false,
  loading: false,
  leftIcon: true,
  rightIcon: true,
  type: 'button',
})

const emit = defineEmits<{
  (e: 'click', event: MouseEvent): void
}>()

const buttonClasses = computed(() => [
  'app-btn',
  `app-btn--${props.variant}`,
  {
    'is-disabled': props.disabled || props.loading,
    'is-loading': props.loading,
  },
])

const handleClick = (e: MouseEvent) => {
  if (!props.disabled && !props.loading) {
    emit('click', e)
  }
}
</script>

<template>
  <button :type="type" :class="buttonClasses" :disabled="disabled || loading" @click="handleClick">
    <!-- Left Icon -->
    <span v-if="$slots.leftIcon || leftIcon" class="btn-icon">
      <slot name="leftIcon">
        <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-svg">
          <circle cx="10" cy="10" r="7.5" stroke="currentColor" stroke-width="1.8" />
          <path d="M10 9V14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
          <circle cx="10" cy="6.5" r="0.9" fill="currentColor" />
        </svg>
      </slot>
    </span>

    <span class="btn-label">
      <slot>Button</slot>
    </span>

    <!-- Right Icon -->
    <span v-if="$slots.rightIcon || rightIcon" class="btn-icon">
      <slot name="rightIcon">
        <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-svg">
          <circle cx="10" cy="10" r="7.5" stroke="currentColor" stroke-width="1.8" />
          <path d="M10 9V14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
          <circle cx="10" cy="6.5" r="0.9" fill="currentColor" />
        </svg>
      </slot>
    </span>
  </button>
</template>

<style scoped>
.app-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px; /* itemSpacing: 8px w Figmie */
  padding: 8px 12px; /* pad=(12, 8) w Figmie */
  border-radius: 8px; /* cornerRadius: 8.0px w Figmie */
  font-family: var(--font-family-body);
  font-size: 16px;
  line-height: 20px;
  font-weight: 400;
  cursor: pointer;
  white-space: nowrap;
  outline: none;
  user-select: none;
  transition: all 0.15s ease;
  box-sizing: border-box;
}

/* 1. Type: Default (Solid) */
.app-btn--default {
  background-color: #0048ff;
  border: 1px solid #003acc;
  color: #ffffff;
}
.app-btn--default:hover:not(.is-disabled) {
  background-color: #336dff;
  border-color: #0048ff;
}
.app-btn--default:active:not(.is-disabled) {
  background-color: #6691ff;
  border-color: #336dff;
}
.app-btn--default.is-disabled {
  background-color: #c7c7c7;
  border-color: #959595;
  color: #626262;
  cursor: not-allowed;
}

/* 2. Type: Outline */
.app-btn--outline {
  background-color: transparent;
  border: 1px solid #003acc;
  color: #ffffff;
}
.app-btn--outline:hover:not(.is-disabled) {
  border-color: #0048ff;
}
.app-btn--outline:active:not(.is-disabled) {
  background-color: #6691ff;
  border-color: #336dff;
  color: #ffffff;
}
.app-btn--outline.is-disabled {
  border-color: #959595;
  color: #959595;
  cursor: not-allowed;
}

/* 3. Type: Transparent (Ghost) */
.app-btn--transparent {
  background-color: transparent;
  border: 1px solid transparent;
  color: #ffffff;
}
.app-btn--transparent:hover:not(.is-disabled) {
  border-color: #0048ff;
}
.app-btn--transparent:active:not(.is-disabled) {
  background-color: #6691ff;
  border-color: #336dff;
  color: #ffffff;
}
.app-btn--transparent.is-disabled {
  color: #959595;
  cursor: not-allowed;
}

.btn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.icon-svg {
  width: 16px;
  height: 16px;
}
</style>
