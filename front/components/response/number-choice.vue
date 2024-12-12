<template>
  <label class="number-choice">
    <ResponseChoice
      :response-choice="responseChoice"
      :response-choice-index="responseChoice.id"
      :color="props.color"
      :selected="props.selected"
      hide-left-symbol
    >
      <template #right-symbol>
        <div class="is-flex input-container">
          <Slider
            v-model="answer"
            class="choice-slider"
            :min="props.bounds.min"
            :max="props.bounds.max"
            :tooltips="false"
            :lazy="false"
          />
          <div class="value-display is-size-5">
            {{ props.selected ? answer : "?" }}
          </div>
        </div>
      </template>
    </ResponseChoice>
  </label>
</template>

<script setup lang="ts">
import { PropType } from "vue"
import {
  Category,
  QuestionBounds,
  ResponseChoice as ResponseChoiceType,
} from "~/composables/types"
import { useLegacyModel } from "~/composables/modelWrapper"
import Slider from "@vueform/slider"

const props = defineProps({
  category: {
    type: Object as PropType<Category>,
    required: true,
  },
  modelValue: { type: Number, default: null },
  color: { type: String, required: true },
  bounds: { type: Object as PropType<QuestionBounds>, required: true },
  selected: { type: Boolean, default: false },
})

const answer = useLegacyModel<number>("modelValue")
const responseChoice = computed<ResponseChoiceType>(() => {
  return {
    id: props.category.id,
    responseChoice: props.category.category,
    description: "",
  }
})
</script>

<style src="@vueform/slider/themes/default.css"></style>

<style lang="sass">
// do not add scoped, it would break slider customizations
.number-choice .input-container
  width: 178px
  justify-content: space-between
  align-items: center
  margin-left: 15px
  .choice-slider
    --slider-bg: #FFF
    --slider-connect-bg: var(--color)
    --slider-handle-shadow: 0
    --slider-handle-shadow-active: 0
    --slider-handle-border: 0
    --slider-handle-width: 32px
    --slider-handle-height: 32px
    --slider-handle-bg: var(--color)
    --slider-height: 15px
    width: 138px
    margin-left: 0px

    // customization not planned by the module
    .slider-base
      border: 2px solid var(--color)
      box-sizing: content-box

    &.slider-horizontal .slider-handle
      top: calc(var(--slider-handle-height, 16px)/2*-1 - var(--slider-height, 6px)/2*-1)
    // end of customization not planned by the module

    .value-display
      margin-top: -2px
@include mobile
  .number-choice .input-container
    .choice-slider
      width: 120px
</style>
