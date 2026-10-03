<script setup lang="ts">
interface Props {
  href?: string
  to?: string
  variant?: 'primary' | 'muted' | 'white'
  underline?: boolean
}

withDefaults(defineProps<Props>(), {
  href: '',
  to: '',
  variant: 'primary',
  underline: false,
})
</script>

<template>
  <RouterLink v-if="to" :to="to" class="app-link" :class="[`link--${variant}`, { 'has-underline': underline }]">
    <slot>Link</slot>
  </RouterLink>

  <a v-else :href="href || '#'" class="app-link" :class="[`link--${variant}`, { 'has-underline': underline }]">
    <slot>Link</slot>
  </a>
</template>

<style scoped>
.app-link {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-family: var(--font-family-primary);
  font-size: var(--font-size-md);
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.link--primary {
  color: var(--color-primary-electric);
}
.link--primary:hover {
  color: var(--color-primary-hover);
  text-decoration: underline;
}

.link--muted {
  color: var(--color-text-muted);
}
.link--muted:hover {
  color: #ffffff;
}

.link--white {
  color: #ffffff;
}
.link--white:hover {
  color: var(--color-primary-soft);
}

.has-underline {
  text-decoration: underline;
}
</style>
