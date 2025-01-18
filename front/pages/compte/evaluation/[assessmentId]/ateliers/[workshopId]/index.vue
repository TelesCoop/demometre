<template>
  <div class="container">
    <div class="mb-2">
      <NuxtLink
        class="button is-white is-rounded"
        to="/compte"
      >
        <span class="icon">
          <icon
            size="20"
            name="arrow-left-line"
          />
        </span>
        <span>
          {{ $t("Revenir à mon compte") }}
        </span>
      </NuxtLink>
    </div>
    <div class="section">
      <PageTitle :title="workshop?.name" />
      <hr>
      <PageSection
        title="Informations"
        :buttons="[{text: 'Modifier les informations', icon: 'list-settings-line'}]"
        @button-click="editBottomFields = false;showInformationsEditModal = true;"
      >
        <div
          class="is-flex is-flex-wrap-wrap"
          style="row-gap: 3rem; column-gap: 3rem"
        >
          <InformationDetail
            title="type d'atelier"
            :value="WORKSHOP_TYPES[workshop?.type]?.label"
          />
          <InformationDetail
            title="réalisé le"
            :value="workshop?.date"
          />
          <InformationDetail
            title="lieu"
            :value="workshop?.place"
          />
        </div>
        <div class="mt-3">
          <div class="columns">
            <div class="column is-6-tablet">
              <InformationRichDetail
                title="Contexte"
                :value="workshop?.context"
              />
            </div>
            <div class="column is-6-tablet">
              <InformationRichDetail
                title="Objectifs"
                :value="workshop?.objectives"
              />
            </div>
          </div>
          <div class="columns">
            <div class="column is-6-tablet">
              <InformationRichDetail
                title="Déroulé"
                :value="workshop?.course"
              />
            </div>
            <div class="column is-6-tablet">
              <InformationRichDetail
                title="Commentaires"
                :value="workshop?.comments"
              />
            </div>
          </div>
        </div>
      </PageSection>
      <hr>
      <PageSection
        title="Participants"
        :buttons="[{text: 'Ajouter un participant', icon: 'add-line'}, {text: 'Saisir les réponses papier', link: `/compte/evaluation/${workshop?.assessmentId}/ateliers/${workshopId}/reponses`, icon: 'file-paper'}]"
        @button-click="onParticipantsButtonClick"
      >
        <div>
          <table
            v-if="workshopStore.workshopParticipations(workshopId).length"
            class="table is-fullwidth is-striped"
          >
            <thead>
              <tr>
                <td class="has-text-shade-400 is-size-6">
                  {{ $t("Prénom nom") }}
                </td>
                <td class="has-text-shade-400 is-size-6">
                  {{ $t("Rôle") }}
                </td>
                <td class="has-text-shade-400 is-size-6">
                  {{ $t("Mail") }}
                </td>
                <td class="has-text-shade-400 is-size-6">
                  Réponses
                </td>
                <td class="has-text-shade-400 is-size-6">
                  Actions
                </td>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(participation, index) of workshopStore.workshopParticipations(workshopId)"
                :key="index"
              >
                <td>
                  {{ participation?.participantName }}
                </td>
                <td>
                  {{ profilingStore.roleById[participation?.roleId]?.name }}
                </td>
                <td>
                  {{ participation?.participantEmail }}
                </td>
                <td>
                  {{ WORKSHOP_MEDIUM[participation?.medium] }}
                </td>
                <td>
                  <button
                    class="button is-rounded is-small"
                    @click="confirmDeletion(participation)"
                  >
                    {{ $t("supprimer") }}
                  </button>
                  <button
                    class="button is-rounded is-small ml-1"
                    @click="participationCurrentEdit = participation; showParticipantEditModal = true"
                  >
                    {{ $t("modifier") }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          <div
            v-else
            class="message"
          >
            <div class="message-body">
              {{ $t("Aucun participant renseigné") }}
            </div>
          </div>
        </div>
      </PageSection>
      <hr>
      <PageSection
        :title="WORKSHOP_TYPES[workshop?.type]?.bottomFieldsLabel"
        :buttons="[{text: WORKSHOP_TYPES[workshop?.type]?.bottomFieldsButtonLabel, icon: 'list-settings-line'}]"
        @button-click="editBottomFields = true;showInformationsEditModal = true"
      >
        <div class="columns">
          <div
            v-for="field of WORKSHOP_TYPES[workshop?.type]?.bottomFields"
            :key="field"
            class="column is-6-tablet"
          >
            <InformationRichDetail
              :title="WORKSHOP_CONTEXT_FIELDS[field]"
              :value="workshop && workshop[field]"
            />
          </div>
        </div>
      </PageSection>
    </div>

    <WorkshopInformationsEditModal
      v-if="showInformationsEditModal && workshop"
      :workshop="workshop"
      :bottom-fields="editBottomFields"
      @close="showInformationsEditModal = false"
    />
    <WorkshopParticipantEditModal
      v-if="showParticipantEditModal && workshop"
      :workshop="workshop"
      :participant="participationCurrentEdit"
      @close="showParticipantEditModal = false"
    />
  </div>
</template>

<script setup lang="ts">
import { useProfilingStore } from "~/stores/profilingStore"
import { WorkshopParticipation } from "~/composables/types"
import { Ref, ref } from "vue"
import { useWorkshopStore } from "~/stores/workshopStore"
import { usePageStore } from "~/stores/pageStore"
import { useUserStore } from "~/stores/userStore"
import { WORKSHOP_CONTEXT_FIELDS, WORKSHOP_MEDIUM, WORKSHOP_TYPES } from "~/utils/constants"
import { useConfirm } from "~/composables/useConfirm"
import { useI18n } from "vue-i18n"
import { useAssessmentIsReady } from "~/composables/useAssessmentIsReady"

definePageMeta({
  title: "Atelier",
  breadcrumb: "Atelier",
})
const profilingStore = useProfilingStore()
const workshopStore = useWorkshopStore()
const pageStore = usePageStore()
const userStore = useUserStore()
const confirm = useConfirm()
const route = useRoute()
const workshopId: Ref<number> = ref(+route.params.workshopId)
const i18n = useI18n()
const $t = i18n.t

await useAssessmentIsReady()

const showInformationsEditModal = ref(false)
const showParticipantEditModal = ref(false)
const editBottomFields = ref(false)

const participationCurrentEdit = ref<WorkshopParticipation | {}>({})

if (!pageStore.animatorPage.listWorkshopsTitle) {
  pageStore.getAnimatorPage()
}
if (!profilingStore.roles.length) {
  profilingStore.getRoles()
}
const workshop = computed(() => {
  return workshopStore.workshopById[workshopId.value]
})
if (
  !workshop.value ||
  workshop.value.participationIds.length !==
  workshopStore.workshopParticipations(workshopId.value).length
) {
  console.log("### refresh workshop because of participations number mismatch")
  workshopStore.getWorkshop(workshopId.value)
}

if (!userStore.isLoggedIn) {
  navigateTo(`/login`)
}

const onParticipantsButtonClick = (buttonIx: number) => {
  if (buttonIx === 0) {
    showParticipantEditModal.value = true
  }
}

const confirmDeletion = (participant: WorkshopParticipation) => {
  confirm(
    $t("En supprimant ce participant, vous supprimez également les évaluations du participant. Cette action est irréversible."),
    `${$t("Supprimer le participant :")} ${participant.participantName}`,
    $t("Oui, supprimer"),
    () => workshopStore.deleteParticipation(participant.id),
  )
}
</script>

<style scoped lang="sass"></style>
