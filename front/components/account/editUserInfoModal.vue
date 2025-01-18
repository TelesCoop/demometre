<template>
  <div class="modal is-active">
    <div
      class="modal-background"
      @click="emit('close')"
    />
    <div class="modal-content">
      <div class="modal-card-head">
        <h2 class="title is-2">
          {{ $t("Modifier mes informations") }}
        </h2>
      </div>
      <div class="modal-card-body">
        <div class="field">
          <label class="label">Nom</label>
          <div class="control">
            <input
              v-model="username"
              class="input"
              type="text"
              :placeholder="$t(`Mon nom tel qu'affiché dans l'application`)"
            >
          </div>
        </div>
        <div class="field">
          <label class="label">{{ $t("Adresse mail") }}</label>
          <div class="control">
            <input
              v-model="email"
              class="input"
              type="text"
              :placeholder="$t('adresse@courriel.fr')"
            >
          </div>
        </div>
      </div>
      <div class="modal-card-foot">
        <button
          class="button is-rounded is-dark"
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
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from "~/stores/userStore"

const emit = defineEmits(["close"])

const userStore = useUserStore()

const username = ref(userStore.user?.username)
const email = ref(userStore.user?.email)

const save = async () => {
  const success = await userStore.editUser({ username, email })
  if (success) {
    emit("close")
  }
}
</script>
