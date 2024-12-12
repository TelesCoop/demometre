<template>
  <div>
    <FormPaperQuestion
      :question="question"
      color="no-pillar"
    />
  </div>
</template>

<script lang="ts" setup>
import { PropType } from "vue"
import { type PillarType, type Question } from "~/composables/types"

defineProps({
  pillar: {
    type: Object as PropType<PillarType>,
    required: true,
  },
  question: {
    type: Object as PropType<Question>,
    required: true,
  },
})
</script>
