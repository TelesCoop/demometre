<template>
  <Teleport to="body">
    <div
      class="modal"
      :class="{ 'is-active': participationStore.showSaveParticipationModal }"
    >
      <div
        class="modal-background"
        @click="$emit('close')"
      />
      <div class="modal-content has-background-shade-100 p-2">
        <h2 class="is-size-4 has-text-weight-bold pb-0_5">
          {{ $t("Souhaitez-vous enregistrer vos réponses pour pouvoir y revenir et contribuer à l’évaluation ?")
          }}
        </h2>
        <p>
          {{ $t(`Vous pourrez ensuite y revenir via l'onglet Mon compte.`) }}
        </p>
        <div class="buttons">
          <button
            class="button is-shade-600 is-outlined"
            @click="saveParticipation"
          >
            {{ $t("Oui, créer un compte") }}
          </button>
          <button
            class="button is-shade-600 is-outlined"
            @click="closeModal"
          >
            {{ $t("Non, ne rien enregistrer") }}
          </button>
        </div>
      </div>
      <button
        class="modal-close is-large"
        aria-label="close"
        @click="closeModal()"
      />
    </div>
  </Teleport>
</template>
<script setup lang="ts">
import { useParticipationStore } from "~/stores/participationStore"

const participationStore = useParticipationStore()
const router = useRouter()

const closeModal = () => {
  participationStore.setShowSaveParticipationModal(false)
}

const saveParticipation = () => {
  closeModal()
  router.push("/signup")
}
</script>

<style lang="sass" scoped>
.modal-content
  border-radius: 5px
</style>
