<template>
  <fieldset>
    <legend
      class="is-size-6bis mb-0_75 is-block"
      :class="`has-text-${props.color}-dark`"
    >
      <slot name="legend">
        {{ $t("Choisissez une réponse.") }}
      </slot>
    </legend>
    <div
      class="is-flex is-flex-direction-column is-align-items-start is-justify-content-center"
    >
      <ResponsePaperRadio
        v-for="(responseChoice, responseChoiceIndex) of props.responseChoices"
        :key="responseChoiceIndex"
        :response-choice="responseChoice"
        :name="questionId.toString()"
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
  color: { type: String, required: true },
  questionId: { type: [Number, String], required: true },
})
</script>
