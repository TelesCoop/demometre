<template>
  <div v-if="question">
    <ResponseInputPercentage
      v-if="question.type === QuestionType.PERCENTAGE"
      v-model="answer"
      :color="props.color"
      :question-id="question.id"
      @change="adaptQuestionResponse()"
    />
    <ResponseInputNumber
      v-else-if="question.type === QuestionType.NUMBER"
      v-model="answer"
      :color="props.color"
      :question-id="question.id"
      :min="question.minNumberValue"
      :max="question.maxNumberValue"
      :step="question.stepNumberValue"
      @change="adaptQuestionResponse()"
    />
    <div
      v-else-if="question.type === QuestionType.UNIQUE_CHOICE"
      class="select"
    >
      <select
        v-model="answer"
        style="max-width: 400px"
        @change="adaptQuestionResponse()"
      >
        <option :value="null" />
        <option
          v-for="responseChoice of question.responseChoices"
          :key="responseChoice.id"
          :value="responseChoice.id"
        >
          {{ responseChoice.responseChoice }}
        </option>
      </select>
    </div>
    <div
      v-else-if="question.type === QuestionType.MULTIPLE_CHOICE"
      class="select is-multiple"
    >
      <select
        v-model="answer"
        multiple
        @change="adaptQuestionResponse()"
      >
        <option
          v-for="responseChoice of question.responseChoices"
          :key="responseChoice.id"
          :value="responseChoice.id"
        >
          {{ responseChoice.responseChoice }}
        </option>
      </select>
      <p class="is-size-7 has-text-shade-400">
        {{ $t("Ctrl + clic pour selectionner plusieurs options") }}
      </p>
    </div>
    <div
      v-else-if="question.type === QuestionType.BOOLEAN"
      class="select"
    >
      <select
        v-model="answer"
        @change="adaptQuestionResponse()"
      >
        <option :value="null" />
        <option
          v-for="response of [
            { id: 1, value: 'Oui' },
            { id: 0, value: 'Non' },
          ]"
          :key="response.id"
          :value="response.id"
        >
          {{ response.value }}
        </option>
      </select>
    </div>
    <div v-else-if="question.type === QuestionType.CLOSED_WITH_SCALE">
      <div
        v-for="category of question.categories"
        :key="category.id"
      >
        <div class="is-flex is-align-items-center mb-0_5">
          <p class="mr-1">
            {{ category.category }}
          </p>
          <div class="select">
            <select
              v-model="answer[category.id]"
              @change="adaptQuestionResponseForCloseWithScaleType()"
            >
              <option :value="null" />
              <option
                v-for="responseChoice of question.responseChoices"
                :key="responseChoice.id"
                :value="responseChoice.id"
              >
                {{ responseChoice.responseChoice }}
              </option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  QuestionType,
  Question,
  QuestionResponse,
  WorkshopParticipation,
} from "~/composables/types"
import { computed, PropType, watch } from "vue"
import {
  getQuestionResponseStructure,
  getQuestionResponseValue,
} from "~/utils/question-response"
import { useWorkshopStore } from "~/stores/workshopStore"
import { useI18n } from "vue-i18n"

const i18n = useI18n()
const $t = i18n.t
const props = defineProps({
  question: {
    type: Object as PropType<Question>,
    required: true,
  },
  color: { type: String, required: true },
  participation: {
    type: Object as PropType<WorkshopParticipation>,
    required: false,
    default() {
      return {}
    },
  },
  assessmentId: { type: Number, required: true },
  modelValue: {
    type: Object as PropType<QuestionResponse>,
    required: false,
    default: null,
  },
})

const questionResponse = useModel<QuestionResponse>("modelValue")
const workshopStore = useWorkshopStore()

const isAnswered = computed(() => {
  if (Array.isArray(answer.value)) return !!answer.value.length
  return !!answer.value || answer.value === 0 || answer.value === false
})

const initialValue = getAnswerInitialValue()

const answer = ref(initialValue)

watch(
  () => props.question,
  () => {
    answer.value = getAnswerInitialValue()
  },
)

function adaptQuestionResponse() {
  questionResponse.value = getQuestionResponseStructure(
    props.question,
    answer.value,
    isAnswered.value,
    props.participation.id,
    props.assessmentId,
  )
  workshopStore.markDirty(props.participation.id, props.question.id)
}

function adaptQuestionResponseForCloseWithScaleType() {
  questionResponse.value = getQuestionResponseStructure(
    props.question,
    props.question.categories.map((category) => {
      return {
        categoryId: category.id,
        responseChoiceId: answer.value[category.id],
      }
    }),
    isAnswered.value,
    props.participation.id,
    props.assessmentId,
  )
  workshopStore.markDirty(props.participation.id, props.question.id)
}

function getAnswerInitialValue() {
  let toReturn = getQuestionResponseValue(
    questionResponse.value,
    props.question.type,
  )
  if (props.question.type === QuestionType.CLOSED_WITH_SCALE) {
    if (!toReturn) {
      toReturn = {}
      props.question.categories.forEach(
        (category) => (toReturn[category.id] = null),
      )
    } else {
      const initResponses = JSON.parse(JSON.stringify(toReturn))
      toReturn = {}
      initResponses.forEach(
        (initResponse) =>
          (toReturn[initResponse.categoryId] = initResponse.responseChoiceId),
      )
    }
  }
  if (props.question.type === QuestionType.MULTIPLE_CHOICE && !toReturn) {
    toReturn = []
  }
  return toReturn
}
</script>

<style scoped lang="sass"></style>
