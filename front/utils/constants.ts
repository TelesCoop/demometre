import { i18n } from "~/utils/i18n-util"

const $t = i18n.global.t

export const PARTICIPANT_TYPE = {
  initiator: $t("initiateur"),
  expert: $t("expert"),
  participant: $t("participant"),
}
export type ASSESSMENT_CONTEXT_FIELD_TYPE =
  "context" | "objectives" | "stakeholders" | "calendar"
export type WORKSHOP_CONTEXT_FIELD_TYPE =
  "context" | "objectives" | "course" | "comments"
export const ASSESSMENT_CONTEXT_FIELDS = {
  context: $t("contexte"),
  objectives: $t("objectifs"),
  stakeholders: $t("parties prenantes"),
  calendar: $t("calendrier"),
}
export const WORKSHOP_CONTEXT_FIELDS = {
  context: $t("contexte"),
  objectives: $t("objectifs"),
  course: $t("déroulé"),
  comments: $t("commentaires"),
  demometreSuggestions: $t("sur le démomètre"),
  platformSuggestions: $t("sur la plateforme"),
  resultObservations: $t("sur les résultats"),
  improvementObservations: $t("sur les mesures d'améliorations"),
}
export const ASSESSMENT_DOCUMENT_CATEGORIES = [
  { label: $t("Rapports d'évaluation"), value: "assessment_reports" },
  { label: $t("Autres documents"), value: "other" },
  { label: $t("Factures"), value: "invoices" },
]
export const WORKSHOP_TYPES = {
  assessment: {
    label: $t("Évaluation"),
    bottomFields: ["demometreSuggestions", "platformSuggestions"],
    bottomFieldsLabel: $t("Suggestions"),
    bottomFieldsButtonLabel: $t("Modifier les suggestions"),
  },
  results: {
    label: $t("Résultats"),
    bottomFields: ["resultObservations", "improvementObservations"],
    bottomFieldsLabel: $t("Remarques"),
    bottomFieldsButtonLabel: $t("Modifier les remarques"),
  },
}
export const WORKSHOP_MEDIUM = {
  online: $t("En ligne"),
  paper: $t("Sur papier"),
}
export const LOCALITY_TYPE_NAME = {
  municipality: $t("Commune"),
  intercommunality: $t("Intercommunalité"),
  department: $t("Département"),
  region: $t("Région"),
}
