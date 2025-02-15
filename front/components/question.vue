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
          :participative-process="participativeProcess"
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
  ParticipationParticipativeProcess,
} from "~/composables/types"
import { computed, PropType, watch } from "vue"
import { ref } from "vue"
import { useParticipationStore } from "~/stores/participationStore"
import {getQuestionResponseValue, toQuestionResponseValue} from "~/utils/question-response"
import { useAssessmentStore } from "~/stores/assessmentStore"
import { usePressEnter } from "~/composables/pressEnter"
import {ONE_MILLION} from "~/utils/constants"
import {getAnswerKey} from "~/utils/util"

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
const router = useRouter()
const route = useRoute()

const question = computed(() => {
  return props.context.questionById[props.questionId]
})
const { explanatory, definitions } = useQuestionHandler(question.value)

const participativeProcessId = computed({
  get: () => route.query.participativeProcessId ? +route.query.participativeProcessId : undefined,
  set: (newValue) => {
    router.push({
      query: {
        ...route.query,
        participativeProcessId: newValue,
      },
    })
  },
})

const participativeProcess = computed<ParticipationParticipativeProcess|undefined>(() => {
  if (participativeProcessId.value == null) {
    console.log("### no participative process")
    return undefined
  }
  console.log("### participativeProcess is ", participativeProcessId.value, possibleParticipativeProcesses.value, assessmentStore.currentAssessment.participativeProcesses.find(p => p.id))
  return assessmentStore.currentAssessment?.participativeProcesses.find(p => p.id === participativeProcessId.value) || undefined
})

const answerKey = computed(() => {
  return getAnswerKey(props.questionId, participativeProcessId.value)
})

const checkParticipativeProcess = () => {
  if (participativeProcessId.value == null && possibleParticipativeProcesses.value.length && question.value.isParticipativeProcessQuestion ) {
    console.log("### set", possibleParticipativeProcesses.value[0])
    participativeProcessId.value = possibleParticipativeProcesses.value[0]
  } else {
    console.log("### checkParticipativeProcess nothing")
  }
}

router.afterEach(() => {
  checkParticipativeProcess()
})

const possibleParticipativeProcesses = computed<number[]>(() => {
  return (participationStore.participation?.participativeProcesses || [])
})

checkParticipativeProcess()
setTimeout(() => {
  checkParticipativeProcess()
}, 1000)

const isAnswered = computed(() => {
  const value = getQuestionResponseValue(answer.value, question.value.type)
  if (Array.isArray(value)) return value.length > 0
  return !isNullOrUndefined(value)
})

const answer = ref<QuestionResponse | QuestionResponseValue | undefined>(
  props.context.responseByQuestionId[answerKey.value],
)
const isLoading = ref(false)

watch(question, () => {
  answer.value = props.context.responseByQuestionId[answerKey.value]
})
watch(participativeProcessId, () => {
  answer.value = props.context.responseByQuestionId[answerKey.value]
})

const nextQuestionDisabled = computed(
  () =>
    !(
      isAnswered.value ||
      props.context.responseByQuestionId[answerKey.value]?.hasPassed
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
  let result = false
  // if the question is about participative processes
  if (question.value.code === '7A' && assessmentStore.currentAssessment?.participativeProcesses?.length) {
    // we update the participation, we don't answer the question
    result = await participationStore.updateParticipation(assessmentStore.currentAssessmentId!, {participativeProcesses: answer.value!.multipleChoiceResponseIds})
  } else {
    console.log("### save response", { participativeProcessId: participativeProcessId.value })
    result = await participationStore.saveResponse(
      question.value,
      answer.value,
      isAnswered.value,
      participativeProcessId.value,
    )
  }
  if (result) {
    isLoading.value = false
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
    if (participativeProcessId.value) {
      // if the question is for a participative process, select next participative process
      if (possibleParticipativeProcesses.value.indexOf(participativeProcessId.value) === possibleParticipativeProcesses.value.length - 1) {
        participativeProcessId.value = undefined
        goToNextQuestion()
      } else {
        participativeProcessId.value = possibleParticipativeProcesses.value[possibleParticipativeProcesses.value.indexOf(participativeProcessId.value) + 1]
      }
    } else {
      goToNextQuestion()
    }
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
