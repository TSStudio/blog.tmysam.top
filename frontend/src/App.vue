<template>
  <div class="shell">
    <header class="site-header">
      <div>
        <RouterLink class="brand" to="/">Blog - Mingyang Tong</RouterLink>
        <p class="tagline">鬼点子生产中～故障即将发生。</p>
      </div>
      <div class="header-actions">
        <nav class="nav">
          <RouterLink to="/">文章</RouterLink>
          <RouterLink to="/manage">管理</RouterLink>
        </nav>
        <button class="ghost-button theme-toggle" type="button" @click="toggleTheme">
          {{ isDark ? "浅色" : "深色" }}
        </button>
      </div>
    </header>
    <main class="page">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { RouterLink, RouterView } from "vue-router";

type ThemeMode = "light" | "dark";

const THEME_STORAGE_KEY = "blog_theme_mode";
const isDark = ref(false);

function applyTheme(mode: ThemeMode) {
  document.documentElement.dataset.theme = mode;
  isDark.value = mode === "dark";
}

function getPreferredTheme(): ThemeMode {
  const saved = localStorage.getItem(THEME_STORAGE_KEY);
  if (saved === "light" || saved === "dark") {
    return saved;
  }
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function toggleTheme() {
  const nextTheme: ThemeMode = isDark.value ? "light" : "dark";
  localStorage.setItem(THEME_STORAGE_KEY, nextTheme);
  applyTheme(nextTheme);
}

onMounted(() => {
  applyTheme(getPreferredTheme());
});
</script>
