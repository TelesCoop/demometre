<template>
  <div>
    <label class="label has-text-shade-800">{{ consentData.title }}</label>
    <span class="is-family-secondary is-size-6 has-text-shade-600">
      {{ consentData.desc }}
    </span>
    <label class="checkbox is-size-7 mt-1">
      <input
        v-if="props.type === `cgv`"
        v-model="assessmentStore.newAssessment.conditionsOfSaleConsent"
        type="checkbox"
        required
      >
      <input
        v-else-if="props.initiator === true"
        v-model="assessmentStore.newAssessment.initiatorUsageConsent"
        type="checkbox"
        required
      >
      <input
        v-else
        v-model="participationStore.newParticipation.consent"
        type="checkbox"
        required
      >
      {{ consentData.checkboxIntro }}
      Vous pouvez consulter ici nos
      <a
        :href="consentData.url"
        target="_blank"
        class="is-underlined"
      >{{
        consentData.urlText
      }}</a>
      et
      <a
        :href="
          MEDIA_BASE_URL + settingStore.rgpdSettings.confidentialityPolicyUrl
        "
        target="_blank"
        class="is-underlined"
      >{{ $t("Charte relative à la protection des données à caractère personnel") }}</a>
      .
    </label>
    <p class="is-family-secondary is-size-6 has-text-shade-600 mt-2">
      {{ consentData.additionalText }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { MEDIA_BASE_URL } from "~/composables/api"
import { usePageStore } from "~/stores/pageStore"
import { useSettingStore } from "~/stores/settingStore"
import { useParticipationStore } from "~/stores/participationStore"
import { useUserStore } from "~/stores/userStore"
import { useAssessmentStore } from "~/stores/assessmentStore"

const props = defineProps({
  type: { type: String, required: true },
  initiator: { type: Boolean, default: false },
})

const settingStore = useSettingStore()
const pageStore = usePageStore()
const participationStore = useParticipationStore()
const assessmentStore = useAssessmentStore()
const userStore = useUserStore()

const consentData = computed(() => {
  switch (props.type) {
  case "cgu":
    return {
      title: pageStore.evaluationInitiationPage.cguConsentTitle,
      desc: userStore.isLoggedIn
        ? pageStore.evaluationInitiationPage.cguConsentDescriptionLoggedin
        : pageStore.evaluationInitiationPage.cguConsentDescriptionLoggedout,
      checkboxIntro:
          "J’accepte les conditions générales d’utilisation de la plateforme.",
      url: MEDIA_BASE_URL + settingStore.rgpdSettings.termsOfUseUrl,
      urlText: "CGU",
      linkedState: props.initiator
        ? assessmentStore.newAssessment.initiatorUsageConsent
        : participationStore.newParticipation.consent,
    }
  case "cgv":
    return {
      title: pageStore.evaluationInitiationPage.cgvConsentTitle,
      desc: pageStore.evaluationInitiationPage.cgvConsentDescription,
      checkboxIntro:
          "J’accepte les conditions générales de vente de la plateforme.",
      url: MEDIA_BASE_URL + settingStore.rgpdSettings.termsOfSaleUrl,
      urlText: "CGV",
      linkedState: assessmentStore.newAssessment.conditionsOfSaleConsent,
      additionalText: pageStore.evaluationInitiationPage.royaltyDescription,
    }
  }
})
</script>

<style scoped lang="sass"></style>
