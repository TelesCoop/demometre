<template>
  <div class="columns">
    <aside class="menu column is-5 mr-2">
      <div class="tabs">
        <ul
          :class="`has-text-${color}`"
          :style="`border-bottom-color: currentColor`"
        >
          <li class="is-active">
            <a
              :class="`has-text-${color}-dark`"
              :style="`border-bottom-color: currentColor`"
            >{{ $t("Questions") }}</a>
          </li>
        </ul>
      </div>
      <ul class="menu-list">
        <li
          v-for="question of questions"
          :key="question.id"
        >
          <a
            :class="[
              `has-text-${props.color}-dark `,
              question === activeQuestion && `has-background-${props.color}`,
              question.id === hoverQuestionId &&
                `has-background-${props.color}-light`,
            ]"
            @click="onSelectQuestion(question)"
            @mouseenter="hoverQuestionId = question.id"
            @mouseleave="hoverQuestionId = null"
          >
            <span :class="`has-text-${props.color}-active`">
              {{ question.concatenatedCode }}
            </span>
            {{ question.questionStatement }}
          </a>
        </li>
      </ul>
    </aside>
    <div class="content column is-7 mb-1_5">
      <h2
        class="title is-4 mb-0_75"
        :class="`has-text-${props.color}-dark`"
      >
        {{ wordTitleCase(props.pillar.name) }}
      </h2>
      <hr
        class="my-0_75"
        :class="`has-background-${props.color}`"
      >
      <div v-if="activeQuestion">
        <QuestionnaireQuestionStatement
          :color="props.color"
          :question="activeQuestion"
        >
          <table
            v-if="activeQuestion.objectivity === Objectivity.SUBJECTIVE"
            class="is-fullwidth"
          >
            <tr :class="`is-uppercase is-size-6bis pb-0_5`">
              <td class="pb-0_5">
                {{ $t("Participant·e·s") }}
              </td>
              <td class="pb-0_5">
                {{ $t("Réponses") }}
              </td>
            </tr>
            <tr
              v-for="participation of workshopStore.workshopParticipations(
                props.workshopId, 'paper'
              )"
              :key="participation.id"
            >
              <td class="pb-1 pr-0_75">
                <p
                  :class="`has-background-${props.color}-light is-fullheight py-0_5 px-1`"
                >
                  {{ participation.participantName }}
                </p>
              </td>
              <td class="pb-1">
                <ResponseAnimator
                  v-model="
                    participation.responseByQuestionId[activeQuestion.id]
                  "
                  :question="activeQuestion"
                  :participation="participation"
                  :assessment-id="participation.assessmentId"
                  :color="props.color"
                />
              </td>
            </tr>
          </table>
          <div v-else>
            <p class="is-size-7 is-family-secondary mb-1">
              {{ $t("Réponse unique car question objective") }}
            </p>
            <ResponseAnimator
              v-model="
                workshopStore.assessmentResponseByQuestionIdByWorkshopId[
                  props.workshopId
                ][activeQuestion.id]
              "
              :question="activeQuestion"
              :assessment-id="
                workshopStore.workshopById[props.workshopId].assessmentId
              "
              :color="props.color"
            />
          </div>
        </QuestionnaireQuestionStatement>
      </div>
      <div v-else>
        <p>{{ $t("Selectionner une question") }}</p>
      </div>
      <div class="buttons mt-2">
        <button
          v-if="activeQuestionIndex + 1 < questions.length"
          :class="`button is-rounded is-${color} is-outlined has-text-${color}-active`"
          type="button"
          @click.prevent="nextQuestion()"
        >
          <span class="icon">
            <icon
              size="16"
              name="arrow-right-line"
            />
          </span>
          <span>{{ $t("Question suivante") }}</span>
        </button>

        <button
          v-if="activeQuestion"
          :class="`button is-rounded is-${color} ml-auto`"
          type="button"
          :disabled="workshopStore.workshopById[workshopId].closed"
          @click.prevent="onSubmit"
        >
          <span>{{ $t("Valider les réponses") }}</span>
          <span class="icon">
            <icon
              size="16"
              name="check"
            />
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue"
import { useQuestionnaireStore } from "~/stores/questionnaireStore"
import { Question, Objectivity } from "~/composables/types"
import { wordTitleCase } from "~/utils/util"
import { useWorkshopStore } from "~/stores/workshopStore"
import { useConfirm } from "~/composables/useConfirm"
import { useAssessmentStore } from "~/stores/assessmentStore"

const i18n = useI18n()
const $t = i18n.t
const questionnaireStore = useQuestionnaireStore()
const workshopStore = useWorkshopStore()
const confirm = useConfirm()
const assessmentStore = useAssessmentStore()

const props = defineProps({
  pillar: { type: Object, required: true },
  color: { type: String, required: true },
  workshopId: { type: Number, required: true },
})

const questions = computed<Question[]>(() =>
  questionnaireStore.getQuestionnaireQuestionByPillarName(assessmentStore.currentAssessment.surveyId, props.pillar.name),
)
const activeQuestion = ref<Question>()
const hoverQuestionId = ref<number>()

const activeQuestionIndex = computed(() =>
  questions.value.indexOf(activeQuestion.value),
)

const onSelectQuestion = (question: Question) => {
  activeQuestion.value = question
}

const nextQuestion = () => {
  if (isDirty.value) {
    confirm(
      $t("Des réponses ont été rentrées mais non sauvegardées. Pour les enregistrer, annulez et cliquez sur le bouton Valider les réponses."),
      $t("Ignorer les réponses rentrées ?"),
      $t("Ignorer et aller à la question suivante"),
      goNextQuestion,
    )
    return
  }
  goNextQuestion()
}
const goNextQuestion = () => {
  activeQuestion.value = questions.value[activeQuestionIndex.value + 1]
}

watch(
  () => props.pillar,
  () => {
    activeQuestion.value = null
  },
)

const isDirty = computed(() => {
  for (const participation of workshopStore.workshopParticipations(
    props.workshopId,
  )) {
    if (workshopStore.isDirty(participation.id, activeQuestion.value?.id)) {
      return true
    }
  }
  return false
})

async function onSubmit() {
  const isSuccessful = await workshopStore.createOrUpdateQuestionnaireResponses(
    props.workshopId,
    activeQuestion.value,
  )
  if (isSuccessful) {
    // mark answers clean (not dirty anymore, selected choices have been answered)
    for (const participation of workshopStore.workshopParticipations(
      props.workshopId,
    )) {
      workshopStore.markDirty(participation.id, activeQuestion.value?.id, false)
    }
  }
}
</script>

<style scoped lang="sass"></style>
