import { useProfilingStore } from "~/stores/profilingStore"
import { useQuestionnaireStore } from "~/stores/questionnaireStore"
import { useAssessmentStore } from "~~/stores/assessmentStore"
import { useDefinitionStore } from "~~/stores/definitionStore"
import { useSettingStore } from "~~/stores/settingStore"
import { useUserStore } from "~/stores/userStore"
import { usePageStore } from "~/stores/pageStore"

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.hook("vue:setup", () => {
    const userStore = useUserStore()
    const assessmentStore = useAssessmentStore()
    const profilingStore = useProfilingStore()
    const questionnaireStore = useQuestionnaireStore()
    const definitionStore = useDefinitionStore()
    const settingStore = useSettingStore()
    const pageStore = usePageStore()
    console.log("### init data server")

    userStore.refreshProfile(false)
    // assessmentStore.getAssessmentsForUser()
    profilingStore.getProfilingQuestions()
    profilingStore.getRoles()
    questionnaireStore.getSurveysSetup()
    assessmentStore.getRepresentativityCriterias()
    definitionStore.getDefinitions()
    settingStore.getRgpdSettings()
    settingStore.getStructureSettings()
    pageStore.getHomePage()
  })
})
