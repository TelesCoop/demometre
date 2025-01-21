<template>
  <div class="modal is-active">
    <div
      class="modal-background"
      @click="emit('close')"
    />
    <div class="modal-card">
      <header class="modal-card-head">
        <h2 class="modal-card-title">
          {{ title }}
        </h2>
        <icon
          tabindex="0"
          aria-label="fermer la modale"
          name="close"
          class="delete has-cursor-pointer"
          @click="$emit('close')"
        />
      </header>
      <section class="modal-card-body">
        <form @submit.prevent="">
          <div class="field">
            <label class="label">{{ $t("Nom / pseudo") }}</label>
            <div class="control">
              <input
                v-model="participation.participantName"
                :class="`input is-shade-300`"
                type="text"
                placeholder="Karim Bastin"
              >
            </div>
          </div>
          <div class="field">
            <label class="label">{{ $t("Adresse mail") }}</label>
            <div class="control">
              <input
                v-model="participation.participantEmail"
                :class="`input is-shade-300`"
                type="email"
                placeholder="écrire ici ..."
              >
            </div>
          </div>
          <div class="field">
            <label
              for="role"
              class="label"
            >{{ $t("Rôle") }}</label>
            <div class="select">
              <select
                id="role"
                v-model="participation.roleId"
              >
                <option
                  v-for="role in profilingStore.roles"
                  :key="role.id"
                  :value="role.id"
                >
                  {{ role.name }}
                </option>
              </select>
            </div>
          </div>
          <div class="field">
            <label
              for="role"
              class="label"
            >{{ $t("Réponses") }}</label>
            <div class="select">
              <select
                id="role"
                v-model="participation.medium"
              >
                <option value="online">
                  {{ WORKSHOP_MEDIUM.online }}
                </option>
                <option value="paper">
                  {{ WORKSHOP_MEDIUM.paper }}
                </option>
              </select>
            </div>
            <p class="help">
              {{ $t("Les participants peuvent répondre en ligne ou via questionnaire papier, dont les réponses peuvent être saisies par vos soins avec la plateforme. Si vous souhaitez saisir des réponses papier, sélectionnez « Sur papier », puis remplissez les questions de profilage, validez puis cliquez ensuite sur « Saisir les réponses papier ».")
              }}
            </p>
          </div>

          <div>
            <div
              v-for="questionId in profilingStore.orderedQuestionId"
              :key="questionId"
              class="field"
            >
              <label
                :for="questionId"
                class="label"
              >{{ profilingStore.questionById[questionId].name }}</label>
              <ResponseAnimator
                :id="questionId"
                v-model="
                  participation.responseByQuestionId[questionId]
                "
                :question="profilingStore.questionById[questionId]"
                :participation="participation"
                :assessment-id="
                  workshop?.assessmentId
                "
                color="no-pillar"
              />
            </div>
          </div>
        </form>
      </section>
      <footer class="modal-card-foot">
        <button
          class="button is-rounded is-dark"
          :disabled="!canValidate || loadingStore.isLoading('workshopsParticipation')"
          @click="save"
        >
          <span>{{ $t("Valider") }}</span>
          <span class="icon">
            <icon
              size="16"
              name="check"
            />
          </span>
        </button>
        <button
          class="button is-rounded is-outlined is-dark"
          @click="$emit('close')"
        >
          {{ $t("Annuler") }}
        </button>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { PropType } from "vue"
import { Workshop, WorkshopParticipation } from "~/composables/types"
import { useLoadingStore } from "~/stores/loadingStore"
import { useWorkshopStore } from "~/stores/workshopStore"
import { useProfilingStore } from "~/stores/profilingStore"
import { WORKSHOP_MEDIUM } from "~/utils/constants"
import { useI18n } from "vue-i18n"

const workshopStore = useWorkshopStore()
const loadingStore = useLoadingStore()
const profilingStore = useProfilingStore()
const route = useRoute()

const i18n = useI18n()
const $t = i18n.t

const props = defineProps({
  workshop: { type: Object as PropType<Workshop>, required: true },
  participant: { type: Object as PropType<WorkshopParticipation>, default: () => ({}) },
})
const workshopId: number = +route.params.workshopId
const assessmentId: number = +route.params.id
const emit = defineEmits(["close"])
const isNew = computed(() => Object.keys(props.participant).length == 0)
const participation = ref<WorkshopParticipation>({ ...props.participant })
console.log("### edit modal with", participation)
if (participation.value.responseByQuestionId == null) {
  participation.value.responseByQuestionId = {}
}

const title = computed<string>(() => {
  if (isNew.value) {
    return $t("Ajout d'un participant")
  } else {
    return $t("Modification d'un participant")
  }
})

const canValidate = computed<boolean>(() => {
  for (const field of ["participantEmail", "participantName", "roleId"]) {
    if (participation.value[field] == null) {
      return false
    }
  }
  return true
})

const save = async () => {
  const res = await workshopStore.createOrUpdateParticipation(participation.value, workshopId, assessmentId)
  if (res) {
    emit("close")
  }
}
</script>
