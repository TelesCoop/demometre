import { useParticipationStore } from "~/stores/participationStore"
import { useAssessmentStore } from "~/stores/assessmentStore"

export async function getUserData() {
  console.log("### get user data")
  await useAssessmentStore().getAssessmentsForUser()
}

export function cleanUserData(onlyResponses = false) {
  useParticipationStore().onUserLogout()
  useAssessmentStore().onUserLogout(onlyResponses)
}
