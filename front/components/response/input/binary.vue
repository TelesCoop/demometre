<template>
  <ResponseInputUniqueChoice
    v-model="answer"
    :response-choices="responseChoices"
    :color="props.color"
    :question-id="questionId"
  >
    <template #legend>
      {{ $t("Choisissez oui ou non.") }}
    </template>
  </ResponseInputUniqueChoice>
</template>

<script setup lang="ts">
import { ResponseChoice as ResponseChoiceType } from "~/composables/types"
import { useI18n } from "vue-i18n"

const props = defineProps({
  color: { type: String, required: true },
  questionId: { type: Number, required: true },
})

const i18n = useI18n()
const $t = i18n.t

const answer = defineModel("modelValue", {
  type: Number,
  default: null,
  required: false,
})

const responseChoices = ref<ResponseChoiceType[]>([
  {
    id: 1,
    responseChoice: $t("Oui"),
    description: "",
  },
  {
    id: 0,
    responseChoice: $t("Non"),
    description: "",
  },
])
</script>

<style scoped lang="sass"></style>
