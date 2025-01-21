import { useQuestionnaireStore } from "~/stores/questionnaireStore"
import { useProfilingStore } from "~/stores/profilingStore"
import { useAssessmentStore } from "~~/stores/assessmentStore"
import { useDefinitionStore } from "~~/stores/definitionStore"
import { useSettingStore } from "~~/stores/settingStore"
import { useUserStore } from "~/stores/userStore"
import { usePageStore } from "~/stores/pageStore"

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.hook("app:mounted", async () => {
    console.log("### init data client 0")
    // the data should already be fetched from SSR
    // but if it's missing, we try again from the client

    const userStore = useUserStore()
    const assessmentStore = useAssessmentStore()
    const profilingStore = useProfilingStore()
    const questionnaireStore = useQuestionnaireStore()
    const definitionStore = useDefinitionStore()
    const settingStore = useSettingStore()
    const pageStore = usePageStore()

    const toAwaitFor = []

    if (!Object.keys(userStore.user).length) {
      toAwaitFor.push(userStore.refreshProfile(false))
    }

    if (!assessmentStore.currentAssessment) {
      toAwaitFor.push(assessmentStore.getAssessmentsForUser())
    }

    if (!profilingStore.orderedQuestionId.length) {
      toAwaitFor.push(profilingStore.getProfilingQuestions())
    }
    if (!profilingStore.roles.length) {
      toAwaitFor.push(profilingStore.getRoles())
    }
    if (!Object.keys(questionnaireStore.surveyById).length) {
      toAwaitFor.push(questionnaireStore.getSurveysSetup())
    }
    if (!assessmentStore.representativityCriterias.length) {
      toAwaitFor.push(assessmentStore.getRepresentativityCriterias())
    }
    if (!definitionStore.definitionLoaded) {
      toAwaitFor.push(definitionStore.getDefinitions())
    }
    if (!settingStore.rgpdSettingsLoaded) {
      toAwaitFor.push(settingStore.getRgpdSettings())
    }
    if (!settingStore.structureSettings.email) {
      toAwaitFor.push(settingStore.getStructureSettings())
    }

    if (!pageStore.homePage.title) {
      toAwaitFor.push(pageStore.getHomePage())
    }

    await Promise.all(toAwaitFor)
    console.log("### client init done")
  })
})
