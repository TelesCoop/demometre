<template>
  <div class="button-bar my-1_5">
    <div class="is-flex is-align-items-center">
      <button
        v-if="canSubmit || required"
        :class="
          props.color === 'no-pillar'
            ? `is-shade-600`
            : `is-${props.color} text-color-dark`
        "
        class="button is-rounded mr-0_75"
        :disabled="!isAnswered"
        type="submit"
        data-cy="submit-button"
      >
        <span>{{ $t("Valider") }}</span>
        <i class="icon">
          <Icon
            v-if="isLoading"
            size="20"
            name="loader-2-line"
          />
          <Icon
            v-else
            size="20"
            name="check"
          />
        </i>
      </button>
      <button
        v-else
        :class="
          props.color === 'no-pillar'
            ? `is-shade-600`
            : `is-${props.color} text-color-dark`
        "
        class="button is-outlined is-rounded mr-0_75"
        type="submit"
      >
        <span class="is-hidden-mobile">{{ $t("Je ne sais pas / Je passe") }}</span>
        <span class="is-hidden-tablet">{{ $t("Je passe") }}</span>
        <i class="icon">
          <Icon
            v-if="isLoading"
            size="20"
            name="loader-2-line"
          />
          <Icon
            v-else
            size="20"
            name="arrow-right-line"
          />
        </i>
      </button>
      <span
        v-if="isLoading"
        class="is-size-7 has-text-shade-600"
      >{{ $t("en cours de chargement") }}</span>
      <span
        v-else-if="canSubmit"
        class="is-size-7 is-hidden-mobile"
        :class="
          color === 'no-pillar'
            ? 'has-text-shade-600'
            : `has-text-${color}-dark`
        "
      >
        {{ $t("appuyez sur Entrer ⏎") }}
      </span>
    </div>
    <div
      v-if="isQuestionnaire && currentAssessmentId"
      class="is-flex buttons"
    >
      <NuxtLink
        :to="`/resultats/${currentAssessmentId}?question=${questionId}`"
        :class="`is-${color}`"
        class="button is-outlined text-color-hover is-rounded"
        title="Voir les résultats"
        target="_blank"
        data-cy="results-button"
      >
        <span class="is-hidden-mobile">{{ $t("Voir les résultats") }}</span>
        <span class="is-hidden-tablet">Résultats</span>
        <span class="icon">
          <Icon
            size="20"
            name="bar-chart-line"
          />
        </span>
      </NuxtLink>
      <NuxtLink
        :to="`/faq`"
        :class="`is-${props.color}`"
        class="button is-outlined text-color-hover round"
        title="FAQ"
        target="_blank"
      >
        <i class="icon">
          <Icon
            size="16"
            name="question-mark"
          />
        </i>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n"

const i18n = useI18n()
const $t = i18n.t
const props = defineProps({
  questionId: { type: Number, required: false, default: -1 },
  required: { type: Boolean, required: false },
  isLoading: { type: Boolean, required: true },
  color: { type: String, required: true },
  isQuestionnaire: { type: Boolean, required: false },
  currentAssessmentId: { type: Number, default: null },
  isAnswered: { type: Boolean, required: false },
  canSubmit: { type: Boolean, required: false },
})
</script>

<style scoped lang="sass">
.button-bar
  display: flex
  justify-content: space-between
  position: relative
  flex-wrap: wrap
  row-gap: 1rem

  .absolute-centered
    position: absolute
    top: 50%
    left: 50%
    transform: translate(-50%, -50%)

.buttons .round, .button.round
  height: 40px
  width: 40px
  padding: 0
  border-radius: 50%

.tabs
  ul
    border-bottom-color: var(--color)

  .tab
    color: var(--color-hover)
    border-bottom-color: var(--color)
    padding: 0.5em 1.5em 0.5em 0em

    &.is-active
      color: var(--color-dark)
      border-bottom-color: var(--color-dark)

    &:hover
      color: var(--color-active)
      border-bottom-color: var(--color-active)
</style>
