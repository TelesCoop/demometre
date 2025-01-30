<template>
  <fieldset>
    <legend
      class="is-size-6bis mb-0_75 is-flex is-flex-wrap-wrap"
      :class="`has-text-${props.color}-dark `"
    >
      <div
        v-for="(responseChoice, responseChoiceIndex) of props.responseChoices"
        :key="responseChoiceIndex"
        class="mr-1_5"
      >
        <span class="has-text-weight-semibold">
          {{ responseChoiceIndex + 1 }}
        </span>
        <span class="ml-0_5">{{ responseChoice.responseChoice }}</span>
      </div>
    </legend>
    <div>
      <ResponsePaperCategoriesChoice
        :bounds="bounds"
        :color="color"
        :categories="categories"
      />
    </div>
  </fieldset>
</template>

<script setup lang="ts">
import { PropType } from "vue"
import {
  Category,
  QuestionBounds,
  ResponseChoice as ResponseChoiceType,
} from "~/composables/types"

const props = defineProps({
  categories: {
    type: Array as PropType<Category[]>,
    required: true,
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
</script>

<style lang="sass" scoped>
.legend
  align-items: center
  display: flex
  flex-basis: auto
  justify-content: center
  margin-right: 1.5rem
</style>
