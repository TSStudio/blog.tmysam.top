<template>
  <section class="stack">
    <p v-if="loading" class="feedback">正在加载文章...</p>
    <p v-else-if="errorMessage" class="feedback error">{{ errorMessage }}</p>
    <article v-else-if="article" class="article-panel">
      <div class="toolbar">
        <div class="post-meta">
          <span>创建于 {{ formatTimestamp(article.created) }}</span>
          <span v-if="article.created !== article.modified">
            更新于 {{ formatTimestamp(article.modified) }}
          </span>
        </div>
        <RouterLink
          v-if="isLoggedIn"
          class="ghost-button inline-button"
          :to="`/manage?articleId=${encodeURIComponent(articleId)}`"
        >
          编辑
        </RouterLink>
      </div>
      <h1 class="article-title">{{ article.title }}</h1>
      <div class="markdown-body" v-html="renderMarkdown(article.content)"></div>
    </article>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { RouterLink } from "vue-router";
import { fetchArticle } from "../api";
import { formatTimestamp, renderMarkdown } from "../utils";
import type { ArticleResponse } from "../types/api";

const props = defineProps<{
  articleId: string;
}>();

const article = ref<ArticleResponse | null>(null);
const loading = ref(false);
const errorMessage = ref("");
const isLoggedIn = computed(() => Boolean(localStorage.getItem("blog_admin_token")));

async function loadArticle() {
  loading.value = true;
  errorMessage.value = "";
  try {
    article.value = await fetchArticle(props.articleId);
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加载失败";
  } finally {
    loading.value = false;
  }
}

watch(() => props.articleId, loadArticle);
onMounted(loadArticle);
</script>
