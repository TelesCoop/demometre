<template>
  <div class="modal is-active">
    <div
      class="modal-background"
      @click="emit('close')"
    />
    <div class="modal-card">
      <header class="modal-card-head">
        <h2 class="modal-card-title">
          {{ $t("Changer d'expert") }}
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
        <p class="mb-2">
          {{
            $t("Si vous souhaitez changer, sélectionnez un expert dans la liste ci-dessous et cliquez sur valider. Si votre expert n’est pas enregistré (et/ou ne figure pas dans la liste), contactez nous.")
          }}
        </p>
        <form @submit.prevent="">
          <AssessmentExpertChooser
            v-for="(expertId, expertIx) of selectedExperts"
            :key="expertId"
            v-model="selectedExperts[expertIx]"
            :expert-ix="expertIx"
            @remove="selectedExperts.splice(expertIx, 1)"
          />
        </form>
        <button
          class="button is-rounded is-outlined is-dark mt-2"
          @click="selectedExperts.push(-1)"
        >
          {{ $t("Ajouter un expert") }}
        </button>
      </section>
      <footer class="modal-card-foot">
        <button
          class="button is-rounded is-dark"
          :disabled="loadingStore.isLoading('assessments')"
          @click="saveEdits"
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
import { Assessment } from "~/composables/types"
import { useLoadingStore } from "~/stores/loadingStore"
import { useAssessmentStore } from "~/stores/assessmentStore"
import { useI18n } from "vue-i18n"

const i18n = useI18n()
const $t = i18n.t
const assessmentStore = useAssessmentStore()
const loadingStore = useLoadingStore()

const props = defineProps({ assessment: { type: Object as PropType<Assessment>, required: true } })
const emit = defineEmits(["close"])

if (!assessmentStore.experts.length) {
  await assessmentStore.getExperts()
}
const selectedExperts = ref(props.assessment.experts.map(expert => expert.id))


const saveEdits = async () => {
  await assessmentStore.saveAssessment(
    props.assessment.id,
    { experts: selectedExperts.value.filter(expertId => expertId !== -1) },
  )
  emit("close")
}
</script>
