<template>
  <div>
    <ArticleContentBlockImage
      v-if="block.type == 'image'"
      :block="block"
    />
    <ArticleContentBlockPdf
      v-else-if="block.type == 'pdf'"
      :block="block"
    />
    <ArticleContentBlockRichText
      v-else-if="block.type == 'rich_text'"
      :block="block"
    />
    <ArticleContentBlockTitle
      v-else-if="block.type == 'heading'"
      :block="block"
    />
  </div>
</template>

<script setup lang="ts">
import { PropType } from "vue"
import { Block } from "~/composables/types"

defineProps({
  block: {
    type: Object as PropType<Block>,
    required: true,
  },
})
</script>
