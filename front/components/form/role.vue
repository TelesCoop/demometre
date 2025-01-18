<template>
  <form
    class="questionnaire-container mb-4"
    @submit.prevent="onSubmit"
  >
    <div class="my-1_5 nav-questionnaire-container">
      <ResponseInputUniqueChoice
        v-model="answer"
        :response-choices="responseChoices"
        :color="color"
        question-id="role"
        :white-letter-when-select="true"
      />
    </div>
    <FormButtons
      :required="true"
      color="no-pillar"
      :is-loading="isLoading"
      :is-answered="canSubmit"
      :can-submit="canSubmit"
    />
  </form>
</template>

<script setup lang="ts">
import { useProfilingStore } from "~/stores/profilingStore"
import { usePageStore } from "~/stores/pageStore"
import { usePressEnter } from "~/composables/pressEnter"

const props = defineProps({
  modelValue: {
    type: Number as PropType<number | undefined>,
    default: () => undefined,
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
})
const emits = defineEmits(["submit", "update:modelValue"])

const answer = ref(props.modelValue)
watch(
  () => props.modelValue,
  (value) => {
    answer.value = value
  },
)

const pageStore = usePageStore()
if (!pageStore.evaluationQuestionnairePage.startTitle) {
  pageStore.getEvaluationQuestionnairePage()
}

const color = ref("no-pillar")

const profilingStore = useProfilingStore()

const responseChoices = computed(() =>
  profilingStore.roles.map((role) => {
    return {
      id: role.id,
      responseChoice: role.name,
      description: role.description,
    }
  }),
)

const canSubmit = computed(() => !!answer.value)
async function onSubmit() {
  emits("update:modelValue", answer.value)
  emits("submit", answer.value)
}

usePressEnter(onSubmit, () => canSubmit.value)
</script>
