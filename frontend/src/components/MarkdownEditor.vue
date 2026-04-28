<template>
  <div class="editor-shell">
    <div class="editor-toolbar" role="toolbar" aria-label="Markdown tools">
      <button
        v-for="action in actions"
        :key="action.label"
        class="tool-button"
        type="button"
        :title="action.title"
        @click="action.run"
      >
        {{ action.label }}
      </button>
    </div>
    <textarea
      ref="textareaRef"
      :value="modelValue"
      class="editor"
      :placeholder="placeholder"
      @input="handleInput"
      @keydown.tab.prevent="handleTab"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";

const props = defineProps<{
  modelValue: string;
  placeholder?: string;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: string];
}>();

const textareaRef = ref<HTMLTextAreaElement | null>(null);

function handleInput(event: Event) {
  const target = event.target as HTMLTextAreaElement;
  emit("update:modelValue", target.value);
}

function updateValue(nextValue: string, selectionStart: number, selectionEnd = selectionStart) {
  emit("update:modelValue", nextValue);
  requestAnimationFrame(() => {
    const textarea = textareaRef.value;
    if (!textarea) {
      return;
    }
    textarea.focus();
    textarea.setSelectionRange(selectionStart, selectionEnd);
  });
}

function wrapSelection(before: string, after = before, fallback = "") {
  const textarea = textareaRef.value;
  if (!textarea) {
    return;
  }
  const { selectionStart, selectionEnd, value } = textarea;
  const selected = value.slice(selectionStart, selectionEnd) || fallback;
  const nextValue =
    value.slice(0, selectionStart) +
    before +
    selected +
    after +
    value.slice(selectionEnd);
  const start = selectionStart + before.length;
  const end = start + selected.length;
  updateValue(nextValue, start, end);
}

function prefixLines(prefix: string, fallback = "列表项") {
  const textarea = textareaRef.value;
  if (!textarea) {
    return;
  }
  const { selectionStart, selectionEnd, value } = textarea;
  const selected = value.slice(selectionStart, selectionEnd) || fallback;
  const transformed = selected
    .split("\n")
    .map((line) => `${prefix}${line}`)
    .join("\n");
  const nextValue = value.slice(0, selectionStart) + transformed + value.slice(selectionEnd);
  updateValue(nextValue, selectionStart, selectionStart + transformed.length);
}

function insertBlock(snippet: string) {
  const textarea = textareaRef.value;
  if (!textarea) {
    return;
  }
  const { selectionStart, selectionEnd, value } = textarea;
  const leadingNewline = selectionStart > 0 && !value.slice(0, selectionStart).endsWith("\n") ? "\n" : "";
  const trailingNewline = value.slice(selectionEnd).startsWith("\n") ? "" : "\n";
  const insertion = `${leadingNewline}${snippet}${trailingNewline}`;
  const nextValue = value.slice(0, selectionStart) + insertion + value.slice(selectionEnd);
  const cursor = selectionStart + insertion.length;
  updateValue(nextValue, cursor, cursor);
}

function handleTab() {
  const textarea = textareaRef.value;
  if (!textarea) {
    return;
  }
  const { selectionStart, selectionEnd, value } = textarea;
  const nextValue = value.slice(0, selectionStart) + "  " + value.slice(selectionEnd);
  const cursor = selectionStart + 2;
  updateValue(nextValue, cursor, cursor);
}

const actions = computed(() => [
  {
    label: "H1",
    title: "一级标题",
    run: () => prefixLines("# ", "标题"),
  },
  {
    label: "H2",
    title: "二级标题",
    run: () => prefixLines("## ", "小节标题"),
  },
  {
    label: "B",
    title: "加粗",
    run: () => wrapSelection("**", "**", "加粗文字"),
  },
  {
    label: "I",
    title: "斜体",
    run: () => wrapSelection("*", "*", "斜体文字"),
  },
  {
    label: "Link",
    title: "链接",
    run: () => wrapSelection("[", "](https://example.com)", "链接文字"),
  },
  {
    label: "Code",
    title: "行内代码",
    run: () => wrapSelection("`", "`", "code"),
  },
  {
    label: "Quote",
    title: "引用",
    run: () => prefixLines("> ", "引用内容"),
  },
  {
    label: "List",
    title: "无序列表",
    run: () => prefixLines("- ", "列表项"),
  },
  {
    label: "Block",
    title: "代码块",
    run: () => insertBlock("```ts\nconst message = 'hello';\n```"),
  },
]);
</script>
