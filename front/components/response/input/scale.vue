<template>
  <fieldset>
    <legend
      class="is-size-6bis mb-0_75 legend-container"
      :class="`has-text-${props.color}-dark `"
    >
      <div
        v-for="(responseChoice, responseChoiceIndex) of props.responseChoices"
        :key="responseChoiceIndex"
        class="legend has-text-centered mb-0_5"
      >
        <div
          class="number mr-0_5"
          :class="`has-background-${props.color}`"
        >
          <slot name="left-symbol">
            {{ responseChoiceIndex + 1 }}
          </slot>
        </div>
        <span class="legend-text">{{ responseChoice.responseChoice }}</span>
      </div>
    </legend>
    <div
      v-for="(category, categoryIndex) of props.categories"
      :key="categoryIndex"
      class="mb-1"
    >
      <ResponseNumberChoice
        :model-value="getAnswerSliderValue(category.id)"
        :category="category"
        :color="props.color"
        :bounds="bounds"
        :selected="hasAnsweredCategory(category.id)"
        @update:model-value="(val) => updateOne(val, category.id)"
      />
    </div>
  </fieldset>
</template>

<script setup lang="ts">
import { PropType } from "vue"
import {
  Category,
  ClosedWithScaleResponse,
  QuestionBounds,
  ResponseChoice as ResponseChoiceType,
} from "~/composables/types"
import { getDefaultAnswerValue } from "assets/utils/close-with-scale"

const props = defineProps({
  categories: {
    type: Array as PropType<Category[]>,
    required: true,
  },
  modelValue: {
    type: Array as PropType<ClosedWithScaleResponse[]>,
    required: false,
    default: (props) => {
      return getDefaultAnswerValue(props.categories)
    },
  },
  color: { type: String, required: true },
  responseChoices: {
    type: Array as PropType<ResponseChoiceType[]>,
    required: true,
  },
})

const bounds = computed<QuestionBounds>(() => {
  const length = props.responseChoices.length
  return {
    min: 0,
    max: length,
  }
})

const answer = defineModel("modelValue", {
  type: Array as PropType<ClosedWithScaleResponse[]>,
  default: [],
})

function updateOne(value, categoryId) {
  // If object is empty because user pass the question in first time
  // generate default answer to fix bug
  const myValue = Object.keys(answer.value).length
    ? answer.value
    : getDefaultAnswerValue(props.categories)
  const newAnswer = myValue.map((categoryResponse) => {
    if (categoryResponse.categoryId === categoryId) {
      return {
        ...categoryResponse,
        responseChoiceId:
          value === 0 ? null : props.responseChoices[value - 1].id,
      }
    } else {
      return categoryResponse
    }
  })
  answer.value = newAnswer
}

function getResponseChoiceIdByCategoryId(categoryId) {
  return answer.value.filter(
    (categoryResponse) => categoryResponse.categoryId === categoryId,
  )[0]?.responseChoiceId
}

function getAnswerSliderValue(categoryId) {
  return (
    props.responseChoices
      .map((responseChoice) => responseChoice.id)
      .indexOf(getResponseChoiceIdByCategoryId(categoryId)) + 1 || 0
  )
}

function hasAnsweredCategory(categoryId) {
  return getResponseChoiceIdByCategoryId(categoryId) !== null
}
</script>

<style lang="sass" scoped>
.number
  min-width: 32px
  height: 32px
  border-radius: 50px
  padding-top: 5px
.legend-container
  display: flex
  align-items: center
  justify-content: flex-start
  flex-wrap: wrap
.legend
  align-items: center
  display: flex
  flex-basis: auto
  justify-content: center
  margin-right: 1.5rem
  &-text
    text-align: start
@include mobile
  .legend-container
    margin-right: 1rem
  .legend
    margin-right: 0.5rem
</style>
