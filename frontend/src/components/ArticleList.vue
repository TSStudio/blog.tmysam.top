<template>
  <section class="stack">
    <RouterLink
      v-for="article in articles"
      :key="article.article_id"
      class="post-card post-card-link"
      :to="`/article/${article.article_id}`"
    >
      <div class="post-meta">
        <span>创建于 {{ formatTimestamp(article.created) }}</span>
        <span v-if="article.created !== article.modified">
          更新于 {{ formatTimestamp(article.modified) }}
        </span>
      </div>
      <span class="post-title">
        {{ article.title }}
      </span>
      <span v-if="article.hidden" class="hidden-badge">已隐藏</span>
      <p class="post-abstract">{{ article.abstract }}</p>
    </RouterLink>
  </section>
</template>

<script setup lang="ts">
import { RouterLink } from "vue-router";
import type { ArticlePreview } from "../types/api";
import { formatTimestamp } from "../utils";

defineProps<{
  articles: ArticlePreview[];
}>();
</script>
