<template>
  <fieldset>
    <legend
      class="is-size-6bis mb-0_75 is-block"
      :class="`has-text-${props.color}-dark`"
    >
      {{ $t("Choisissez entre 1 et {n_choices} réponses").replace("{n_choices}", props.maxMultipleChoices.toString()) }}
    </legend>
    <div
      class="is-flex is-flex-direction-column is-align-items-start is-justify-content-center"
    >
      <ResponsePaperCheckbox
        v-for="(responseChoice, responseChoiceIndex) of props.responseChoices"
        :key="responseChoiceIndex"
        class="mb-1"
        :name="questionId.toString()"
        :response-choice="responseChoice"
      />
    </div>
  </fieldset>
</template>

<script setup lang="ts">
import { PropType } from "vue"
import { ResponseChoice as ResponseChoiceType } from "~/composables/types"

const props = defineProps({
  responseChoices: {
    type: Array as PropType<ResponseChoiceType[]>,
    required: true,
  },
  maxMultipleChoices: { type: Number, required: true },
  color: { type: String, required: true },
  questionId: { type: Number, required: true },
})
</script>
