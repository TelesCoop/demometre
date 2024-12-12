<template>
  <ResponsePaperInputUniqueChoice
    :response-choices="responseChoices"
    :color="props.color"
    :question-id="questionId"
  >
    <template #legend>
      {{ $t("Choisissez oui ou non.") }}
    </template>
  </ResponsePaperInputUniqueChoice>
</template>

<script setup lang="ts">
import { ResponseChoice as ResponseChoiceType } from "~/composables/types"

const props = defineProps({
  color: { type: String, required: true },
  questionId: { type: Number, required: true },
})

const responseChoices = ref<ResponseChoiceType[]>([
  {
    id: 1,
    responseChoice: "Oui",
    description: "",
  },
  {
    id: 0,
    responseChoice: "Non",
    description: "",
  },
])
</script>

<style scoped lang="sass"></style>
