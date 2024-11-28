<template>
  <div class="scale-question-chart-classic">
    <div class="scale-question-chart-grid">
      <template
        v-for="(category, categoryKey) in data.value"
        :key="categoryKey"
      >
        <div
          :class="`has-background-${color}-light`"
          class="scale-question-chart-cell"
          style="text-align: left"
        >
          {{ category.label }}
        </div>
        <div class="scale-question-chart-sub-grid">
          <div
            v-for="(choice, key) in category.value"
            :key="key"
            :class="`has-background-${color}-light`"
            class="scale-question-chart-bar-cell"
          >
            <div
              v-for="(roleId, index) of question.roleIds"
              :key="roleId"
              class="scale-question-chart-bar-container"
            >
              <div
                v-if="roles.includes(roleId)"
                class="scale-question-chart-bar"
                :class="`has-background-${rolesGradiants[index][0]} has-border-${color}-dark`"
                :style="`width: ${getPercentage(
                  getValueByRoleId(choice, roleId),
                  data.count
                )}%`"
              />
            </div>
            <template v-for="index in totalSeparator" :key="index">
              <AnalyticsChoiceQuestionChartLine
                class="scale-question-chart-line"
                :class="`is-${color}`"
                :index="index - 1"
                :color="color"
                :total-line="totalSeparator"
                :full-line-modulo="fullLineModulo"
                :percentage-of-space-already-taken="
                  percentageOfSpaceAlreadyTaken
                "
                :gap-size="gapSize"
                :percentage-size="percentageSize"
                :left-base-margin="leftBaseMargin"
              />
            </template>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { getPercentage } from "assets/utils/percentage"
import { getColorGradients } from "assets/utils/choice-question-chart"
import { useProfilingStore } from "~/stores/profilingStore"
import { PropType } from "vue"

const props = defineProps({
  data: { type: Object, required: true },
  color: { type: String, required: true },
  question: { type: Object, required: true },
  roles: { type: Array as PropType<number[]>, required: true },
})
const profilingStore = useProfilingStore()
const totalSeparator = 11
const fullLineModulo = 5
const percentageOfSpaceAlreadyTaken = 0
const gapSize = 0
const percentageSize = 0
const leftBaseMargin = 0

const rolesGradiants = computed(
  () => getColorGradients(props.color)[props.question.roleIds.length],
)
const getValueByRoleId = (choice, roleId) => {
  let roleName = profilingStore.roleById[roleId].name
  if (props.question.objectivity === "objective") {
    // for an objective question, there is only one role
    // for historical reasons, the data is stored in the choice
    // with the assessment response id as key instead of the role name
    const possibleAssessmentResponseIds = Object.keys(choice).filter(key => !["label", "value"].includes(key))
    if (possibleAssessmentResponseIds.length) {
      roleName = possibleAssessmentResponseIds[0]
    }
  }
  return choice[roleName] ? choice[roleName].value : 0
}
</script>

<style scoped lang="sass"></style>
