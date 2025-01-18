import { i18n } from "~/utils/i18n-util"

const $t = i18n.global.t

export const ErrorMessages = {
  default: $t("Une erreur s'est produite dans le serveur"),
  assessment_already_initiated: $t("L'évaluation a déjà été initialisée"),
  email_not_corresponding_assessment:
    $t("L'email ne correspond pas à l'instance initiatrice"),
  incorrect_initiator_assessment: $t("Le type de l'initiateur est incorrect"),
  no_zip_code_municipality: $t("Aucune commune ne correspond à ce code postal"),
  no_zip_code_epci: $t("Aucune intercommunalité ne correspond à ce code postal"),
  email_already_exists: $t("Le mail est déjà utilisé"),
  email_not_valid: $t("Le mail n'est pas valide"),
  no_email: $t("Cet email ne correspond à aucun utilisateur"),
  wrong_password_for_email: $t("Email et mot de passe ne correspondent pas"),
  password_reset_key_outdate:
    $t("La clé de réinitialisation du mot de passe est périmée (24h max), veuillez redemander un changement de mot de passe."),
  question_not_needed: $t("Vous n'avez pas à répondre à cette question."),
  missing_data_to_validate: $t("Il manque des données afin de valider"),
  invalid_email_shape: $t("La forme de l'email n'est pas correct"),
}
