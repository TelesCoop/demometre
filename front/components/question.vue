<template>
  <div v-if="question">
    <section class="section">
      <form
        v-if="question"
        class="questionnaire-container"
        @submit.prevent="submit"
      >
        <FormQuestion
          v-model="answer"
          :color="props.color"
          :question="question"
          :explanatory="explanatory"
          :definitions="definitions"
        />

        <FormButtons
          :question-id="question.id"
          :color="props.color"
          :is-loading="isLoading"
          :is-answered="isAnswered"
          :can-submit="canSubmit()"
          :is-questionnaire="props.isQuestionnaire"
          :current-assessment-id="assessmentStore.currentAssessmentId"
          :required="question.mandatory"
        />

        <!-- TAB : responses -->
        <!-- button previous next -->
        <ButtonsArrowButton
          v-if="
            !props.context.journey.isFirstQuestion(question.id) ||
              props.context.hasPreviousStep
          "
          class="arrow-button-fixed is-left"
          :color="props.color"
          @click.prevent="goToPreviousQuestion"
        />
        <ButtonsArrowButton
          class="arrow-button-fixed is-right"
          :disabled="nextQuestionDisabled"
          :color="props.color"
          @click.prevent="goToNextQuestion"
        />
      </form>
    </section>
  </div>
  <div
    v-else
    style="text-align: center"
  >
    <Loader :color="props.color" />
  </div>
</template>

<script setup lang="ts">
import { isNullOrUndefined } from "assets/utils"
import { useQuestionHandler } from "~/composables/questionHandler"
import {
  QuestionContextProps,
  SurveyType,
  QuestionResponse,
  QuestionResponseValue,
} from "~/composables/types"
import { computed, PropType, watch } from "vue"
import { ref } from "vue"
import { useParticipationStore } from "~/stores/participationStore"
import { getQuestionResponseValue } from "~/utils/question-response"
import { useAssessmentStore } from "~/stores/assessmentStore"
import { usePressEnter } from "~/composables/pressEnter"

const props = defineProps({
  questionId: { type: Number, required: true },
  context: { type: Object as PropType<QuestionContextProps>, required: true },
  color: { type: String, required: true },
  isQuestionnaire: { type: Boolean, required: true },
})

console.log("### question setup", {
  questionId: props.questionId,
  context: props.context,
})

const participationStore = useParticipationStore()
const assessmentStore = useAssessmentStore()

const question = computed(() => {
  return props.context.questionById[props.questionId]
})
const { explanatory, definitions } = useQuestionHandler(question.value)

const isAnswered = computed(() => {
  const value = getQuestionResponseValue(answer.value, question.value.type)
  if (Array.isArray(value)) return value.length > 0
  return !isNullOrUndefined(value)
})

const answer = ref<QuestionResponse | QuestionResponseValue | undefined>(
  props.context.responseByQuestionId[props.questionId],
)
const isLoading = ref(false)

watch(question, () => {
  answer.value = props.context.responseByQuestionId[props.questionId]
})

const nextQuestionDisabled = computed(
  () =>
    !(
      isAnswered.value ||
      props.context.responseByQuestionId[props.questionId]?.hasPassed
    ),
)

const goToPreviousQuestion = () => {
  isLoading.value = true
  props.context.journey.goToPreviousQuestion(question.value.id)
}

const goToNextQuestion = () => {
  isLoading.value = true
  props.context.journey.goToNextQuestion(question.value.id)
}

const submit = async () => {
  isLoading.value = true
  const result = await participationStore.saveResponse(
    question.value,
    answer.value,
    isAnswered.value,
  )
  if (result) {
    if (props.context.journey.isLastQuestion(question.value.id)) {
      if (props.context.journey.surveyType() === SurveyType.INITILIZATION) {
        // await assessmentStore.saveEndInitializationQuestions()
      } else if (
        props.context.journey.surveyType() === SurveyType.QUESTIONNAIRE
      ) {
        await participationStore.saveEndQuestionnaire(
          false,
          question.value.pillarId,
        )
      }
    }
    goToNextQuestion()
  }
}
const canSubmit = () => isAnswered.value
const canPressEnter = () => isAnswered.value || !question.value.mandatory
usePressEnter(submit, canPressEnter)
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
