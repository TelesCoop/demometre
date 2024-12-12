<template>
  <div class="choice-question-chart">
    <div
      class="choice-question-chart-grid mb-1"
      :class="`has-text-${color}-hover`"
    >
      <div>{{ $t("Réponse(s)") }}</div>
      <div>
        <p>{{ $t("Personne(s) concernée(s)") }}</p>
        <p :class="`has-text-${color}-dark mt-0_5`">
          {{ $t("Sélectionner ci-dessous un ou plusieurs acteurs") }}
        </p>
        <div class="buttons mt-0_5">
          <button
            v-for="(roleId, index) of question.roleIds"
            :key="roleId"
            class="button is-outlined"
            :class="
              `has-border-${color}-dark ` +
                (isRoleActive(roleId)
                  ? `has-background-${rolesGradiants[index][0]} has-text-${rolesGradiants[index][1]}`
                  : `has-text-${color}-dark`)
            "
            @click.prevent="onRoleClick(roleId)"
          >
            {{ profilingStore.roleById[roleId].name }}
          </button>
        </div>
      </div>
      <div>{{ $t("Totaux") }}</div>
    </div>
    <div class="choice-question-chart-grid">
      <template
        v-for="(choice, key) in data.value"
        :key="key"
      >
        <div
          :class="`has-background-${color}-light`"
          class="choice-question-chart-cell"
          style="text-align: left"
        >
          {{ choice.label }}
        </div>
        <div
          :class="`has-background-${color}-light`"
          class="choice-question-chart-bar-cell"
        >
          <div
            v-for="(roleId, index) of question.roleIds"
            :key="roleId"
            class="choice-question-chart-bar-container"
          >
            <div
              v-if="roleIdsSelected.includes(roleId)"
              class="choice-question-chart-bar mb-0_5"
              :class="`has-background-${rolesGradiants[index][0]} has-border-${color}-dark`"
              :style="`width: ${getPercentage(
                getValueByRoleId(choice, roleId),
                data.count
              )}%`"
              :title="`${getPercentage(getValueByRoleId(choice, roleId), data.count)}% ${$t('pour le rôle')} ${profilingStore.roleById[roleId].name}`"
            />
          </div>
        </div>
        <div
          :class="`has-background-${color}-light`"
          class="choice-question-chart-cell"
        >
          <strong>
            {{
              getPercentage(getTotalValueOfRolesSelected(choice), data.count)
            }} </strong>%
        </div>
      </template>
      <template
        v-for="index in totalSeparator"
        :key="index"
      >
        <AnalyticsChoiceQuestionChartLine
          class="choice-question-chart-line"
          :class="`is-${color}`"
          :index="index - 1"
          :color="color"
          :total-line="totalSeparator"
          :full-line-modulo="fullLineModulo"
          :percentage-of-space-already-taken="percentageOfSpaceAlreadyTaken"
          :gap-size="gapSize"
          :percentage-size="percentageSize"
        />
        <div
          v-if="(index - 1) % fullLineModulo === 0"
          class="choice-question-chart-line-number"
          :class="`has-text-${color}-hover`"
          :style="
            getLeftStyle(
              index - 1,
              percentageOfSpaceAlreadyTaken,
              totalSeparator,
              gapSize,
              percentageSize
            )
          "
        >
          {{ (index - 1) * 10 }}%
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { getPercentage } from "assets/utils/percentage"
import {
  getLeftStyle,
  getColorGradients,
} from "assets/utils/choice-question-chart"
import { useProfilingStore } from "~/stores/profilingStore"

const props = defineProps({
  data: { type: Object, required: true },
  color: { type: String, required: true },
  question: { type: Object, required: true },
})
const profilingStore = useProfilingStore()
const totalSeparator = 11
const fullLineModulo = 5
const percentageOfSpaceAlreadyTaken = 0.25
const gapSize = 2
const percentageSize = 80

const rolesGradiants = computed(
  () => {
    return getColorGradients(props.color)[props.question.roleIds.length]
  },
)

const roleIdsSelected = ref<number[]>([])

const onRoleClick = (roleId) => {
  if (!roleIdsSelected.value.includes(roleId)) {
    roleIdsSelected.value.push(roleId)
  } else {
    roleIdsSelected.value.splice(roleIdsSelected.value.indexOf(roleId), 1)
  }
}
const isRoleActive = (roleId) => {
  return roleIdsSelected.value.includes(roleId)
}
const getValueByRoleId = (choice, roleId) => {
  const roleName = profilingStore.roleById[roleId].name
  return choice[roleName] ? choice[roleName].value : 0
}
const getTotalValueOfRolesSelected = (choice) => {
  return roleIdsSelected.value.reduce(
    (value, roleId) => value + getValueByRoleId(choice, roleId),
    0,
  )
}
</script>

<style scoped lang="sass">
.choice-question-chart
  &-grid
    position: relative
    display: grid
    grid-template-columns: 1fr 3fr 80px
    grid-gap: 1rem
    align-items: end

  &-cell
    padding: 6px

  &-bar-container
    z-index: 2

  &-bar
    z-index: 1
    height: 22px
    border: 1px solid black

  &-bar-cell
    display: flex
    flex-direction: column
    justify-content: center

  &-line
    position: absolute
    height: 100%
    border-left-width: 1px
    border-left-style: solid
    border-left-color: var(--color-hover)
    z-index: 0

    &.is-dashed
      border-left-style: dashed
      border-left-color: var(--color)

  &-line-number
    position: absolute
    bottom: 0
    transform: translate(-50%, 100%)
</style>
