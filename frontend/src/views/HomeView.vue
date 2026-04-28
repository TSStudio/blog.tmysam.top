<template>
  <section class="stack">
    <div>
      <h1 class="section-title">文章列表</h1>
      <p class="section-subtitle">共 {{ totalResults }} 篇文章</p>
    </div>

    <p v-if="errorMessage" class="feedback error">{{ errorMessage }}</p>
    <p v-else-if="loading" class="feedback">正在加载文章列表...</p>
    <p v-else-if="!articles.length" class="feedback">还没有文章，先去管理页写第一篇吧。</p>
    <ArticleList v-else :articles="articles" />

    <div v-if="totalPages > 1" class="pagination">
      <button
        class="ghost-button"
        type="button"
        @click="goToPage(currentPage - 1)"
        :disabled="loading || currentPage <= 1"
      >
        上一页
      </button>
      <span class="pagination-status">第 {{ currentPage }} / {{ totalPages }} 页</span>
      <button
        class="ghost-button"
        type="button"
        @click="goToPage(currentPage + 1)"
        :disabled="loading || currentPage >= totalPages"
      >
        下一页
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import ArticleList from "../components/ArticleList.vue";
import { fetchArticles } from "../api";
import type { ArticlePreview } from "../types/api";

const PAGE_SIZE = 20;
const route = useRoute();
const router = useRouter();
const articles = ref<ArticlePreview[]>([]);
const totalResults = ref(0);
const loading = ref(false);
const errorMessage = ref("");
const currentPage = computed(() => {
  const rawPage = Number(route.query.page ?? 1);
  return Number.isFinite(rawPage) && rawPage > 0 ? Math.floor(rawPage) : 1;
});
const totalPages = computed(() => Math.max(1, Math.ceil(totalResults.value / PAGE_SIZE)));

async function loadArticles() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const beginOffset = (currentPage.value - 1) * PAGE_SIZE;
    const token = localStorage.getItem("blog_admin_token") ?? undefined;
    const response = await fetchArticles(beginOffset, beginOffset + PAGE_SIZE, token);
    articles.value = response.results;
    totalResults.value = response.total_results;

    if (currentPage.value > totalPages.value) {
      goToPage(totalPages.value);
      return;
    }
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加载失败";
  } finally {
    loading.value = false;
  }
}

function goToPage(page: number) {
  const nextPage = Math.max(1, Math.min(page, totalPages.value || 1));
  router.push({
    query: nextPage === 1 ? {} : { page: String(nextPage) },
  });
}

watch(
  () => route.query.page,
  () => {
    void loadArticles();
  },
  { immediate: true },
);
</script>
