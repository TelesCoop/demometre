import { useAssessmentStore } from "~/stores/assessmentStore"
import { useParticipationStore } from "~/stores/participationStore"

export const useAssessmentIsReady = async () => {
  const assessmentStore = useAssessmentStore()
  const participationStore = useParticipationStore()
  const route = useRoute()
  const assessmentIdStr: string = (route.params.assessmentId as string)
  const assessmentId = parseInt(assessmentIdStr as string)
  if (isNaN(assessmentId)) {
    return
  }
  await Promise.all([
    assessmentStore.getAssessmentOnce(assessmentId),
    participationStore.getParticipationForAssessmentOnce(assessmentId),
    participationStore.loadAssessmentOnce(assessmentId),
  ])
}
