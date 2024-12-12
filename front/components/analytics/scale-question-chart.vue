<template>
  <div class="scale-question-chart">
    <div class="scale-question-chart-grid mb-1">
      <div>
        <label class="checkbox is-size-7">
          <input
            v-model="simplifyChart"
            type="checkbox"
          >
          <template v-if="simplifyChart">
            {{ $t("Désactiver la vue simplifiée") }}
          </template>
          <template v-else>
            {{ $t("Activer la vue simplifiée") }}
          </template>
        </label>
      </div>
      <div>
        <p :class="`has-text-${color}-hover`">
          {{ $t("Personne(s) concernée(s)") }}
        </p>
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
    </div>
    <div
      class="scale-question-chart-grid mb-1"
      :class="`has-text-${color}-hover`"
    >
      <div>{{ $t("Réponses") }}</div>
      <div class="scale-question-chart-sub-grid">
        <div
          v-for="(choice, choiceKey) in data.choices"
          :key="choiceKey"
          class="scale-question-chart-menu"
        >
          {{ choice.label }}
        </div>
      </div>
    </div>
    <AnalyticsScaleQuestionChartSimplify
      v-if="simplifyChart"
      :data="data"
      :color="color"
      :question="question"
      :roles="roleIdsSelected"
    />
    <AnalyticsScaleQuestionChartClassic
      v-else
      :data="data"
      :color="color"
      :question="question"
      :roles="roleIdsSelected"
    />
  </div>
</template>

<script setup lang="ts">
import { getColorGradients } from "assets/utils/choice-question-chart"
import { useProfilingStore } from "~/stores/profilingStore"

const props = defineProps({
  data: { type: Object, required: true },
  color: { type: String, required: true },
  question: { type: Object, required: true },
})
const profilingStore = useProfilingStore()

const rolesGradiants = computed(
  () => getColorGradients(props.color)[props.question.roleIds.length],
)
const simplifyChart = ref(false)

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
</script>

<style lang="sass">
.scale-question-chart
  &-grid
    display: grid
    grid-template-columns: 1fr 4fr
    grid-gap: 1rem

  &-sub-grid
    display: flex
    grid-gap: 1rem

  &-menu
    width: 110px

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
    position: relative
    width: 110px

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
