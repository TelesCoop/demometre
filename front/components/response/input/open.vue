<template>
  <div class="open">
    <label
      class="is-size-6bis mb-0_75 is-block"
      :class="`has-text-${props.color}-dark`"
      :for="`$question-${props.questionId}-open`"
    >{{ $t("Réponse ouverte") }}</label>
    <textarea
      :id="`$question-${props.questionId}-open`"
      v-model="answer"
      class="textarea has-text-grey-dark"
      :class="`has-background-${props.color}-light has-border-${props.color}-dark`"
      rows="12"
      placeholder="..."
    />
  </div>
</template>

<script setup lang="ts">
import { useLegacyModel } from "~/composables/modelWrapper"
import { useI18n } from "vue-i18n"

const i18n = useI18n()
const $t = i18n.t
const props = defineProps({
  color: { type: String, required: true },
  modelValue: { type: Boolean, required: true },
  questionId: { required: true, type: Number },
})

const answer = useLegacyModel("modelValue")
</script>

<style scoped lang="sass">
.open
  margin-right: 85px
  margin-left: 85px
</style>
