<template>
  <div>
    <PageSection
      :title="pageStore.participativeProcessPage.processesTitle"
      :intro="pageStore.participativeProcessPage.description"
      :is-first-element="true"
      :intro-is-rich-text="true"
      class="column is-8 questionnaire-container"
    >
      <div v-for="category of categories" :key="category.id">
        <h3 class="title is-4 mt-2">
          {{ category.responseChoice }}
        </h3>
        <div v-for="(process, index) of processesPerCategory[category.id]" :key="process.id" style="display: flex; align-items: center" class="mb-1">
          <input v-model="processesPerCategory[category.id][index].name" data-cy="participative-process-name" class="input" style="max-width: 400px;" type="text">
          <button class="button is-small ml-1" @click="deleteProcess(category.id, processesPerCategory[category.id][index].name)">
            {{ $t('supprimer') }}
          </button>
        </div>
        <button class="button mt-1" data-cy="add-participative-process" @click="addParticipativeProcess(category.id)">
          {{ pageStore.participativeProcessPage.addParticipativeProcessCallToAction }}
        </button>
      </div>
      <div class="buttons mt-0_5">
        <button
          class="button is-rounded mt-4"
          data-cy="skip-participative-processes"
          @click.prevent="confirm"
        >
          {{ pageStore.participativeProcessPage.skipCallToAction }}
        </button>
        <button
          class="button is-shade-600 is-rounded mt-4"
          data-cy="start-objective-questions"
          :disabled="isDisabled"
          @click.prevent="confirm"
        >
          {{ pageStore.participativeProcessPage.confirmCallToAction }}
        </button>
      </div>
    </PageSection>
  </div>
</template>

<script setup lang="ts">
import {usePageStore} from "~/stores/pageStore"
import {useProfilingStore} from "~/stores/profilingStore"
import {ParticipativeProcess, Question} from "~/composables/types"
import {useRoute} from "vue-router"
import {useQuestionnaireStore} from "~/stores/questionnaireStore"

const questionnaireStore = useQuestionnaireStore()
const route = useRoute()
const assessmentId = Number(route.params.assessmentId)
const pageStore = usePageStore()
const profilingStore = useProfilingStore()
if (!pageStore.participativeProcessPage?.processesTitle) {
  pageStore.getParticipativeProcessPage()
}
const categories = computed(() => {
  const question7A: Question = Object.values(profilingStore.questionById).find(question => question.code === '7A')!
  if (question7A == null) {
    throw "Profiling question 7A not found"
  }
  return question7A?.responseChoices || []
})
const processesPerCategory = ref<Record<number, ParticipativeProcess[]>>({})

const isDisabled = computed(() => {
  if (isLoading.value) {
    return true
  }
  console.log("### is disabled ?", Object.values(processesPerCategory.value))
  for (const processes of Object.values(processesPerCategory.value)) {
    if (processes.some(process => process.name !== '')) {
      return false
    }
  }
  return true
})
const isLoading = ref(false)

const addParticipativeProcess = (categoryId: number) => {
  console.log("### before", processesPerCategory.value)
  processesPerCategory.value = {
    ...processesPerCategory.value,
    [categoryId]: [
      ...processesPerCategory.value[categoryId] || [],
      { name: '', responseChoice: categoryId, assessmentId, id: generateRandomId() },
    ],
  }
  console.log("### after", processesPerCategory.value)
}
const deleteProcess = (categoryId: number, processName: string) => {
  processesPerCategory.value = {
    ...processesPerCategory.value,
    [categoryId]: processesPerCategory.value[categoryId].filter(process => process.name !== processName),
  }
}

const confirm = async () => {
  isLoading.value = true
  const processes: ParticipativeProcess[] = Object.values(processesPerCategory.value).flat().filter(process => process.name !== '')
  await questionnaireStore.addParticipativeProcesses(assessmentId, processes)
  isLoading.value = false
  const journey = useInitializationJourney()
  journey.goToNextQuestion(undefined)
}
</script>
