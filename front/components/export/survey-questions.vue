<template>
  <div>
    <div
      v-for="(pillar, index) in questionnaireStore.pillarsOfMainSurvey"
      :key="pillar.id"
      :class="{ 'page-break': index > 0 }"
    >
      <div class="title is-5">
        {{ $t("Pillier {name}", { name: pillar.name }) }}
      </div>
      <div class="two-columns-grid">
        <template
          v-for="question in filterQuestionsByRoleId(
            questionnaireStore.getQuestionnaireQuestionByPillarName(
              questionnaireStore.mainSurveyId,
              pillar.name,
            ),
            roleId,
          )"
          :key="question.id"
        >
          <ExportPillarQuestion
            :pillar="pillar"
            :question="question"
            class="is-6"
          />
        </template>
      </div>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { useQuestionnaireStore } from "~/stores/questionnaireStore"
import { filterQuestionsByRoleId } from "~/utils/util"

defineProps({
  roleId: { type: Number, required: true },
})
const questionnaireStore = useQuestionnaireStore()
</script>
