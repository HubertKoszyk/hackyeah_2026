<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'primary' | 'primary-soft' | 'secondary' | 'outline' | 'outline-blue' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  loading?: boolean
  leftIcon?: boolean
  rightIcon?: boolean
  type?: 'button' | 'submit' | 'reset'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  disabled: false,
  loading: false,
  leftIcon: false,
  rightIcon: false,
  type: 'button',
})

const emit = defineEmits<{
  (e: 'click', event: MouseEvent): void
}>()

const buttonClasses = computed(() => [
  'app-btn',
  `app-btn--${props.variant}`,
  `app-btn--${props.size}`,
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
    <!-- Left Icon Slot or Default Info Icon -->
    <span v-if="$slots.leftIcon || leftIcon" class="btn-icon btn-icon-left">
      <slot name="leftIcon">
        <!-- Default Figma-style Info Circle SVG -->
        <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-svg">
          <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.8" />
          <path d="M10 9V14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
          <circle cx="10" cy="6.5" r="0.9" fill="currentColor" />
        </svg>
      </slot>
    </span>

    <!-- Label -->
    <span class="btn-label">
      <slot>Button</slot>
    </span>

    <!-- Right Icon Slot or Default Info Icon -->
    <span v-if="$slots.rightIcon || rightIcon" class="btn-icon btn-icon-right">
      <slot name="rightIcon">
        <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-svg">
          <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.8" />
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
  gap: 0.55rem;
  font-family: var(--font-family-primary);
  font-weight: 500;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
  outline: none;
  user-select: none;
  border: 1px solid transparent;
}

/* ==========================================================================
   Sizes
   ========================================================================== */
.app-btn--sm {
  padding: 0.4rem 0.85rem;
  font-size: var(--font-size-sm);
  border-radius: 8px;
}

.app-btn--md {
  padding: 0.65rem 1.25rem;
  font-size: var(--font-size-md);
  border-radius: 12px;
}

.app-btn--lg {
  padding: 0.85rem 1.6rem;
  font-size: var(--font-size-lg);
  border-radius: 14px;
}

/* ==========================================================================
   Variants matching Figma
   ========================================================================== */

/* 1. Primary Solid Blue */
.app-btn--primary {
  background-color: var(--color-primary-electric);
  color: #ffffff;
  border-color: var(--color-primary-electric);
  box-shadow: 0 4px 14px rgba(26, 98, 255, 0.3);
}
.app-btn--primary:hover:not(.is-disabled) {
  background-color: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
  box-shadow: 0 6px 18px rgba(26, 98, 255, 0.4);
  transform: translateY(-1px);
}
.app-btn--primary:active:not(.is-disabled) {
  background-color: var(--color-primary-active);
  transform: translateY(0);
}

/* 2. Soft Blue */
.app-btn--primary-soft {
  background-color: #4b84ff;
  color: #ffffff;
  border-color: #4b84ff;
}
.app-btn--primary-soft:hover:not(.is-disabled) {
  background-color: #6395ff;
}

/* 3. Secondary Dark Surface */
.app-btn--secondary {
  background-color: #272a32;
  color: #ffffff;
  border-color: #383d47;
}
.app-btn--secondary:hover:not(.is-disabled) {
  background-color: #333742;
  border-color: #484e5b;
}

/* 4. Outline Subtle */
.app-btn--outline {
  background-color: transparent;
  color: #ffffff;
  border-color: #3f4552;
}
.app-btn--outline:hover:not(.is-disabled) {
  background-color: rgba(255, 255, 255, 0.05);
  border-color: #636b7c;
}

/* 5. Outline Blue */
.app-btn--outline-blue {
  background-color: rgba(26, 98, 255, 0.08);
  color: #ffffff;
  border-color: var(--color-primary-electric);
}
.app-btn--outline-blue:hover:not(.is-disabled) {
  background-color: rgba(26, 98, 255, 0.18);
  border-color: var(--color-primary-hover);
}

/* 6. Ghost */
.app-btn--ghost {
  background-color: transparent;
  color: var(--color-text-muted);
}
.app-btn--ghost:hover:not(.is-disabled) {
  color: #ffffff;
  background-color: rgba(255, 255, 255, 0.06);
}

/* Disabled state */
.app-btn.is-disabled {
  opacity: 0.45;
  cursor: not-allowed;
  pointer-events: none;
}

/* Icon styling */
.btn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.icon-svg {
  width: 1.15em;
  height: 1.15em;
}
</style>
