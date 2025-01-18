<template>
  <div class="two-columns-grid">
    <FormPaperQuestion
      v-for="question in profilingQuestions"
      :key="question.id"
      class=""
      :question="question"
      :color="color"
    />
  </div>
</template>

<script lang="ts" setup>
import { useProfilingStore } from "~/stores/profilingStore"
import { filterQuestionsByRoleId } from "~/utils/util"
const color = "no-pillar"
const props = defineProps({
  roleId: { type: Number, required: true },
})

const profilingStore = useProfilingStore()

const profilingQuestions = computed(() => {
  return filterQuestionsByRoleId(
    profilingStore.orderedQuestionId.map((questionId) => {
      return profilingStore.questionById[questionId]
    }),
    props.roleId,
  )
})
</script>
