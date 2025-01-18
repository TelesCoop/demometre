<template>
  <div class="container">
    <div class="section">
      <PageTitle title="Espace animateur" />
      <PageSection
        :title="pageStore.animatorPage.listWorkshopsTitle"
        :intro="pageStore.animatorPage.listWorkshopIntro"
      >
        <div>
          <table class="table is-narrow is-fullwidth">
            <thead>
              <tr>
                <td class="has-text-shade-400 is-uppercase is-size-6">
                  {{ $t("Nom de l’atelier") }}
                </td>
                <td class="has-text-shade-400 is-uppercase is-size-6">
                  {{ $t("Date (MM/JJ/AAAA)") }}
                </td>
                <td class="has-text-shade-400 is-uppercase is-size-6">
                  {{ $t("Evaluation*") }}
                </td>
                <td />
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="workshop of [
                  ...workshopStore.workshops,
                  ...newWorkshops,
                ]"
                :key="workshop.id"
              >
                <td>
                  <input
                    v-model="workshop.name"
                    :class="`input is-shade-300`"
                    type="text"
                    placeholder="écrire ici ..."
                  >
                </td>
                <td>
                  <input
                    v-model="workshop.date"
                    :class="`input is-shade-300`"
                    type="date"
                    :timezone="true"
                    lang="fr-FR"
                  >
                </td>
                <td>
                  <div class="select">
                    <select v-model="workshop.assessmentId">
                      <option
                        v-for="assessment of workshopStore.assessments"
                        :key="assessment.id"
                        :value="assessment.id"
                      >
                        {{ assessmentTitle(assessment) }}
                      </option>
                    </select>
                  </div>
                </td>
                <td style="text-align: end; vertical-align: middle">
                  <div
                    v-if="!workshop.closed"
                    class="buttons is-justify-content-flex-end"
                  >
                    <button
                      class="button is-rounded is-shade-600 is-outlined"
                      type="button"
                      :disabled="
                        !(
                          workshop.name &&
                          workshop.date &&
                          workshop.assessmentId
                        )
                      "
                      @click.prevent="saveAndGoToParticipants(workshop)"
                    >
                      <span>{{ $t("Saisir les participant·e·s") }}</span>
                      <span class="icon">
                        <icon
                          size="16"
                          name="user-add-line"
                        />
                      </span>
                    </button>
                    <button
                      class="button is-rounded is-shade-600 is-outlined js-modal-trigger"
                      :disabled="!workshop.id"
                      @click.prevent="closeWorkshopIdModal = workshop.id"
                    >
                      <span>{{ $t("Clôturer l'atelier") }}</span>
                    </button>
                  </div>
                  <div v-else>
                    <span class="tag is-shade-500">
                      {{ $t("Atelier clôturé") }}
                      <icon
                        size="16"
                        name="check"
                      />
                    </span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          <p class="mb-1 is-size-7 has-text-shade-400">
            {{ $t("*Seulement les ateliers des évaluations dont la redevance à été réglée sont visibles ici") }}
          </p>
          <div class="buttons is-justify-content-space-between">
            <div>
              <button
                class="button is-rounded is-shade-600 is-outlined"
                type="button"
                @click.prevent="addWorkshop()"
              >
                <span class="icon">
                  <icon
                    size="16"
                    name="add-line"
                  />
                </span>
                <span>{{ $t("Ajouter un atelier") }}</span>
              </button>
              <button
                v-if="newWorkshops.length"
                class="button is-rounded is-shade-600 is-outlined"
                type="button"
                @click.prevent="removeWorkshop()"
              >
                <span class="icon">
                  <icon
                    size="16"
                    name="delete-bin-line"
                  />
                </span>
                <span>{{ $t("Retirer un atelier") }}</span>
              </button>
            </div>

            <button
              class="button is-rounded is-shade-600"
              type="button"
              :disabled="validateDisabled"
              @click.prevent="onSubmit"
            >
              <span>{{ $t("Valider") }}</span>
              <span class="icon">
                <icon
                  size="16"
                  name="check"
                />
              </span>
            </button>
          </div>
        </div>
      </PageSection>
    </div>
    <div
      id="modal-validate-workshop"
      class="modal"
      :class="closeWorkshopIdModal && `is-active`"
    >
      <div
        class="modal-background"
        @click.prevent="closeModal()"
      />
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">
            {{ $t("Clôturer l'atelier") }}
          </p>
          <button
            class="button is-ghost is-rounded is-outlined"
            @click.prevent="closeModal()"
          >
            <icon
              size="20"
              name="close"
            />
          </button>
        </header>
        <section class="modal-card-body">
          <RichText
            :rich-text="pageStore.animatorPage.closeWorkshopValidation"
          />
        </section>
        <footer class="modal-card-foot">
          <button
            class="button is-success"
            @click.prevent="closeWorkshop(workshop)"
          >
            {{ $t("Clôturer") }}
          </button>
          <button
            class="button"
            @click.prevent="closeModal()"
          >
            {{ $t("Annuler") }}
          </button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useWorkshopStore } from "~/stores/workshopStore"
import { Workshop } from "~/composables/types"
import { useUserStore } from "~/stores/userStore"
import { usePageStore } from "~/stores/pageStore"

definePageMeta({
  title: "Ateliers",
  breadcrumb: "Ateliers",
})

const workshopStore = useWorkshopStore()
const userStore = useUserStore()
const pageStore = usePageStore()
const router = useRouter()

if (!pageStore.animatorPage.listWorkshopsTitle) {
  pageStore.getAnimatorPage()
}
if (!workshopStore.allAssessmentsLoaded) {
  workshopStore.getAnimatorAssessments()
}
if (!workshopStore.allWorkshopsLoaded) {
  workshopStore.getWorkshops()
}

if (!userStore.isLoggedIn) {
  navigateTo(`/login`)
}
if (!userStore.isExpertUser) {
  navigateTo(`/`)
}

const closeWorkshopIdModal = ref<number>(undefined)
const newWorkshops = ref<Workshop[]>([])
const validateDisabled = computed(() =>
  [...newWorkshops.value, ...workshopStore.workshops].some(
    (workshop) => !(workshop.assessmentId && workshop.date && workshop.name),
  ),
)

function assessmentTitle(assessment) {
  return assessment?.municipality
    ? `Ville : ${assessment.municipality.name}`
    : `Inter-communalité : ${assessment.epci.name}`
}

function addWorkshop() {
  newWorkshops.value.push({
    id: undefined,
    assessmentId: undefined,
    name: "",
    date: "",
    animatorId: userStore.user.id,
    participationIds: [],
    changed: true,
    closed: false,
  })
}

function removeWorkshop() {
  newWorkshops.value.pop()
}

function closeModal() {
  closeWorkshopIdModal.value = undefined
}

async function saveAndGoToParticipants(workshop) {
  if (!workshop.id) {
    newWorkshops.value.shift()
  }
  const workshopResponse = await workshopStore.createOrUpdateWorkshop(workshop)

  if (workshopResponse) {
    await workshopStore.getWorkshop(workshopResponse.id)
    router.push(`/compte/ateliers/${workshopResponse.id}/participants`)
  }
}

async function onSubmit() {
  const newWorkshopsTmp = newWorkshops.value
  for (const workshop of [...workshopStore.workshops, ...newWorkshopsTmp]) {
    if (!workshop.id) {
      newWorkshops.value.shift()
    }
    if (workshop.changed) {
      await workshopStore.createOrUpdateWorkshop(workshop)
    }
  }
}

async function closeWorkshop() {
  await workshopStore.closeWorkshop(closeWorkshopIdModal.value)
  closeModal()
}
</script>

<style scoped lang="sass"></style>
