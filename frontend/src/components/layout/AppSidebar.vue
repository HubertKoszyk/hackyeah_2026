<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

interface NavItem {
  id: string
  label: string
  path: string
  icon: string
}

const navItems: NavItem[] = [
  { id: 'home', label: 'Home', path: '/', icon: 'home' },
  { id: 'traffic', label: 'Traffic', path: '/traffic', icon: 'traffic' },
  { id: 'parking', label: 'Parking\nlots', path: '/parking', icon: 'parking' },
//  { id: 'components', label: 'Design\nSystem', path: '/components', icon: 'components' },
]

const isActive = (item: NavItem) => {
  if (item.path === '/' && route.path === '/') return true
  if (item.path !== '/' && route.path.startsWith(item.path)) return true
  return false
}

const navigate = (item: NavItem) => {
  router.push(item.path)
}
</script>

<template>
  <aside class="app-sidebar">
    <!-- Top Logo Badge from Figma -->
    <div class="sidebar-logo-wrapper">
      <div class="logo-circle">
        <span>Logo</span>
      </div>
    </div>

    <!-- Navigation Items -->
    <nav class="sidebar-nav">
      <button
        v-for="item in navItems"
        :key="item.id"
        type="button"
        class="nav-btn"
        :class="{ 'is-active': isActive(item) }"
        @click="navigate(item)"
      >
        <span class="nav-icon">
          <!-- Home Icon -->
          <svg v-if="item.icon === 'home'" viewBox="0 0 24 24" fill="none" class="icon-svg">
            <path
              d="M3 10.5L12 3.5L21 10.5V20C21 20.5523 20.5523 21 20 21H15V14H9V21H4C3.44772 21 3 20.5523 3 20V10.5Z"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linejoin="round"
            />
          </svg>

          <!-- Traffic Icon -->
          <svg v-else-if="item.icon === 'traffic'" viewBox="0 0 24 24" fill="none" class="icon-svg">
            <rect x="7" y="3" width="10" height="18" rx="5" stroke="currentColor" stroke-width="1.8" />
            <circle cx="12" cy="7.5" r="1.5" fill="currentColor" />
            <circle cx="12" cy="12" r="1.5" fill="currentColor" />
            <circle cx="12" cy="16.5" r="1.5" fill="currentColor" />
          </svg>

          <!-- Parking Lots Icon -->
          <svg v-else-if="item.icon === 'parking'" viewBox="0 0 24 24" fill="none" class="icon-svg">
            <rect x="4" y="4" width="16" height="16" rx="4" stroke="currentColor" stroke-width="1.8" />
            <path d="M9 16V8H13C14.6569 8 16 9.34315 16 11C16 12.6569 14.6569 14 13 14H9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
          </svg>

          <!-- Design System / Components Icon -->
          <svg v-else viewBox="0 0 24 24" fill="none" class="icon-svg">
            <rect x="4" y="4" width="6" height="6" rx="1.5" stroke="currentColor" stroke-width="1.8" />
            <rect x="14" y="4" width="6" height="6" rx="1.5" stroke="currentColor" stroke-width="1.8" />
            <rect x="4" y="14" width="6" height="6" rx="1.5" stroke="currentColor" stroke-width="1.8" />
            <circle cx="17" cy="17" r="3" stroke="currentColor" stroke-width="1.8" />
          </svg>
        </span>

        <!-- Label with optional newline -->
        <span class="nav-label">{{ item.label }}</span>
      </button>
    </nav>
  </aside>
</template>

<style scoped>
/* Exact Sidebar matching Figma Screenshot */
.app-sidebar {
  width: 76px;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem 0;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.06);
  z-index: 1000;
  flex-shrink: 0;
  user-select: none;
}

.sidebar-logo-wrapper {
  margin-bottom: 1.5rem;
}

.logo-circle {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background-color: #191919;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-family-body);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: -0.02em;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.25rem;
  width: 100%;
}

.nav-btn {
  width: 64px;
  background: transparent;
  border: none;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 8px 4px;
  border-radius: 8px;
  color: #4a4a4a;
  transition: all 0.15s ease;
}

.nav-btn:hover {
  background-color: #f5f5f5;
  color: #191919;
}

.nav-btn.is-active {
  background-color: #edf2ff;
  color: #0048ff; /* Brand 500 w Figmie */
}

.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-svg {
  width: 22px;
  height: 22px;
}

.nav-label {
  font-family: var(--font-family-body);
  font-size: 11px;
  line-height: 12px;
  font-weight: 500;
  text-align: center;
  white-space: pre-line;
}
</style>
