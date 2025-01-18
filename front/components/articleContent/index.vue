<template>
  <div>
    <ArticleContentBlock
      v-for="block of props.content"
      :key="block.id"
      :block="block"
    />
  </div>
</template>

<script setup lang="ts">
import { PropType } from "vue"
import { Block } from "~/composables/types"

const props = defineProps({
  content: {
    type: Array as PropType<Block[]>,
    required: true,
  },
})
</script>
