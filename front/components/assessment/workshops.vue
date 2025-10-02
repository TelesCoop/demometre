<template>
  <div>
    <PageSection
      :title="$t('Mes ateliers')"
      :buttons="assessment.isCurrent ? [{text: 'Ajouter un atelier', icon: 'add-line'}] : []"
      @button-click="showAddWorkshopModal = true"
    >
      <div v-if="workshops.length">
        <table class="table is-striped is-fullwidth">
          <thead>
            <tr>
              <td class="has-text-shade-400 is-uppercase is-size-6">
                {{ $t("Nom de l’atelier") }}
              </td>
              <td class="has-text-shade-400 is-uppercase is-size-6">
                {{ $t("Type d'atelier") }}
              </td>
              <td class="has-text-shade-400 is-uppercase is-size-6">
                {{ $t("Date (MM/JJ/AAAA)") }}
              </td>
              <td class="has-text-shade-400 is-uppercase is-size-6">
                {{ $t("Lieu") }}
              </td>
              <td class="has-text-shade-400 is-uppercase is-size-6">
                {{ $t("Participants") }}
              </td>
              <td />
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="workshop of workshops"
              :key="workshop.id"
              tabindex="0"
              :title="`Aller à l'atelier ${workshop.name}`"
              class="has-cursor-pointer"
              @click="router.push(`/compte/evaluation/${assessment.id}/ateliers/${workshop.id}`)"
            >
              <th>
                {{ workshop.name }}
              </th>
              <td>
                {{ WORKSHOP_TYPES[workshop.type].label }}
              </td>
              <td>
                {{ workshop.date }}
              </td>
              <td>
                {{ workshop.place }}
              </td>
              <td>{{ workshop.participationIds?.length || 0 }}</td>
            <!--              <td style="text-align: end; vertical-align: middle">-->
            <!--                <div-->
            <!--                  v-if="!workshop.closed"-->
            <!--                  class="buttons is-justify-content-flex-end"-->
            <!--                >-->
            <!--                  <button-->
            <!--                    class="button is-rounded is-shade-600 is-outlined"-->
            <!--                    type="button"-->
            <!--                    :disabled="-->
            <!--                      !(-->
            <!--                        workshop.name &&-->
            <!--                        workshop.date &&-->
            <!--                        workshop.assessmentId-->
            <!--                      )-->
            <!--                    "-->
            <!--                    @click.prevent="saveAndGoToParticipants(workshop)"-->
            <!--                  >-->
            <!--                    <span>Saisir les participant·e·s</span>-->
            <!--                    <span class="icon">-->
            <!--                      <icon-->
            <!--                        size="16"-->
            <!--                        name="user-add-line"-->
            <!--                      />-->
            <!--                    </span>-->
            <!--                  </button>-->
            <!--                  <button-->
            <!--                    class="button is-rounded is-shade-600 is-outlined js-modal-trigger"-->
            <!--                    :disabled="!workshop.id"-->
            <!--                    @click.prevent="closeWorkshopIdModal = workshop.id"-->
            <!--                  >-->
            <!--                    <span>Clôturer l'atelier</span>-->
            <!--                  </button>-->
            <!--                </div>-->
            <!--                <div v-else>-->
            <!--                  <span class="tag is-shade-500">-->
            <!--                    Atelier clôturé-->
            <!--                    <icon-->
            <!--                      size="16"-->
            <!--                      name="check"-->
            <!--                    />-->
            <!--                  </span>-->
            <!--                </div>-->
            <!--              </td>-->
            </tr>
          </tbody>
        </table>
      </div>
      <div
        v-else
        class="message"
      >
        <div class="message-body">
          {{ $t("Il n'y a pas encore d'atelier dans cette évaluation.") }}
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
    <AssessmentAddWorkshopModal
      v-if="showAddWorkshopModal"
      :assessment-id="assessment.id"
      @close="showAddWorkshopModal = false"
    />
  </div>
</template>

<script setup lang="ts">
import { Assessment, Workshop } from "~/composables/types"
import { usePageStore } from "~/stores/pageStore"
import { PropType } from "vue"
import { useWorkshopStore } from "~/stores/workshopStore"
import { WORKSHOP_TYPES } from "~/utils/constants"
import { useI18n } from "vue-i18n"

const i18n = useI18n()
const $t = i18n.t
const props = defineProps({ assessment: { type: Object as PropType<Assessment>, required: true } })
const workshopStore = useWorkshopStore()
const pageStore = usePageStore()
const router = useRouter()

const showAddWorkshopModal = ref(false)

if (!workshopStore.workshopsLoadedByAssessments[props.assessment.id]) {
  workshopStore.getWorkshopsForAssessment(props.assessment.id)
}

if (!pageStore.animatorPage.listWorkshopsTitle) {
  pageStore.getAnimatorPage()
}

const workshops = computed(() => {
  return Object.values(workshopStore.workshopById).filter((workshop: Workshop) => workshop.assessmentId === props.assessment.id)
})

const closeWorkshopIdModal = ref<number>(undefined)

function closeModal() {
  closeWorkshopIdModal.value = undefined
}

async function closeWorkshop() {
  await workshopStore.closeWorkshop(closeWorkshopIdModal.value)
  closeModal()
}
</script>

<style scoped lang="sass"></style>
