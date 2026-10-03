<script setup lang="ts">
export interface BreadcrumbItem {
  label: string
  to?: string
  href?: string
  external?: boolean
}

interface Props {
  items: BreadcrumbItem[]
  showHomeIcon?: boolean
}

withDefaults(defineProps<Props>(), {
  showHomeIcon: true,
})
</script>

<template>
  <nav class="app-breadcrumb" aria-label="Nawigacja okruszkowa">
    <ol class="breadcrumb-list">
      <li v-for="(item, index) in items" :key="index" class="breadcrumb-item">
        <!-- Home icon on the very first element -->
        <span v-if="index === 0 && showHomeIcon" class="home-icon">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-svg">
            <path
              d="M3 8.5L10 3L17 8.5V16C17 16.5523 16.5523 17 16 17H12.5C12 17 12 16.5 12 16V12C12 11.5 11.5 11 11 11H9C8.5 11 8 11.5 8 12V16C8 16.5 8 17 7.5 17H4C3.44772 17 3 16.5523 3 16V8.5Z"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linejoin="round"
            />
          </svg>
        </span>

        <!-- Link or text -->
        <RouterLink v-if="item.to" :to="item.to" class="breadcrumb-link">
          {{ item.label }}
        </RouterLink>
        <a
          v-else-if="item.href"
          :href="item.href"
          class="breadcrumb-link"
          :target="item.external ? '_blank' : undefined"
          :rel="item.external ? 'noopener noreferrer' : undefined"
        >
          {{ item.label }}
          <svg
            v-if="item.external"
            viewBox="0 0 16 16"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            class="external-icon"
          >
            <path
              d="M4 12L12 4M12 4H6M12 4V10"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </a>
        <span v-else class="breadcrumb-current">{{ item.label }}</span>

        <!-- Separator '>' (except for last element) -->
        <span v-if="index < items.length - 1" class="breadcrumb-separator">
          <svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" class="sep-icon">
            <path d="M6 3.5L10.5 8L6 12.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </span>
      </li>
    </ol>
  </nav>
</template>

<style scoped>
.app-breadcrumb {
  font-family: var(--font-family-primary);
  font-size: var(--font-size-md);
}

.breadcrumb-list {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  list-style: none;
  padding: 0;
  margin: 0;
  gap: 0.4rem;
}

.breadcrumb-item {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}

.home-icon {
  display: inline-flex;
  align-items: center;
  color: var(--color-text-muted);
}

.icon-svg {
  width: 1.15rem;
  height: 1.15rem;
}

.breadcrumb-link {
  color: var(--color-text-muted);
  text-decoration: none;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  transition: color 0.15s ease;
}
.breadcrumb-link:hover {
  color: #ffffff;
}

.external-icon {
  width: 0.95rem;
  height: 0.95rem;
}

.breadcrumb-current {
  color: #ffffff;
  font-weight: 600;
}

.breadcrumb-separator {
  display: inline-flex;
  align-items: center;
  color: #555c68;
}

.sep-icon {
  width: 0.85rem;
  height: 0.85rem;
}
</style>
