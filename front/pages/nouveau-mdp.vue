<template>
  <div class="is-flex flex-center">
    <div class="sm-container">
      <div class="my-8">
        <h1 class="title is-1 has-text-shade-800">
          <span v-if="!hasResetKey">Récupérer mon <br>{{ $t("mot de passe") }}</span>
          <span v-else>{{ $t("Changer mon mot de passe") }}</span>
        </h1>

        <div
          v-if="!hasResetKey"
          class=""
        >
          <!-- email -->
          <div class="field has-text-shade-800">
            <label class="label">{{ $t("Courriel") }}</label>
            <div class="control has-icons-left has-icons-right">
              <input
                v-model="email"
                class="input"
                type="email"
                placeholder="jean@laposte.fr"
                :class="isMailValid ? '' : 'is-danger'"
                @change="onEmailUpdate"
              >
              <span class="icon is-small is-left has-text-shade-600">
                <icon
                  size="24"
                  name="mail-line"
                />
              </span>
              <span v-if="!isMailValid" class="icon is-small is-right">
                <i class="fas fa-exclamation-triangle" />
              </span>
            </div>
            <p
              v-if="!isMailValid"
              class="help is-danger"
            >
              {{ emailErrorMessage }}
            </p>
          </div>

          <div
            class="mt-1"
            style="text-align: end"
          >
            <button
              class="button is-shade-600 is-small"
              type="button"
              :disabled="emailDisabled"
              @click="sendResetLink"
            >
              {{ $t("Envoyer un lien de récupération") }}
            </button>
          </div>
        </div>
        <div
          v-else
          class="mt-2"
        >
          <!-- password -->
          <div class="field has-text-shade-800">
            <label class="label">{{ $t("Nouveau mot de passe") }}</label>
            <div class="control has-icons-left has-icons-right">
              <input
                v-model="password"
                class="input"
                type="password"
                placeholder="mot de passe"
                :class="isPasswordValid ? '' : 'is-danger'"
                required
                @change="onPasswordUpdate"
              >
              <span class="icon is-small is-left has-text-shade-600">
                <icon
                  size="24"
                  name="lock-line"
                />
              </span>
              <span v-if="!isPasswordValid" class="icon is-small is-right">
                <i class="fas fa-exclamation-triangle" />
              </span>
            </div>
            <p
              v-if="!isPasswordValid"
              class="help is-danger"
            >
              {{ passwordErrorMessage }}
            </p>
          </div>

          <!-- password confirmation-->
          <div class="field has-text-shade-800">
            <label class="label">{{ $t("Confirmer le nouveau mot de passe") }}</label>
            <div class="control has-icons-left has-icons-right">
              <input
                v-model="confirmPassword"
                class="input"
                type="password"
                placeholder="mot de passe"
                :class="isSamePassword ? '' : 'is-danger'"
                required
                @change="onPasswordUpdate"
              >
              <span class="icon is-small is-left has-text-shade-600">
                <icon
                  size="24"
                  name="lock-line"
                />
              </span>
              <span v-if="!isSamePassword" class="icon is-small is-right">
                <i class="fas fa-exclamation-triangle" />
              </span>
            </div>
            <p
              v-if="!isSamePassword"
              class="help is-danger"
            >
              {{ confirmPasswordErrorMessage }}
            </p>
          </div>
          <div
            class="mt-1"
            style="text-align: end"
          >
            <button
              class="button is-small is-shade-600"
              type="button"
              :disabled="passwordDisabled"
              @click="resetPassword"
            >
              <span class="icon">
                <icon
                  size="16"
                  name="mail-line"
                />
              </span>
              <span>{{ $t("Confirmer") }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from "~/stores/userStore"
import { useI18n } from "vue-i18n"

const i18n = useI18n()
const $t = i18n.t

definePageMeta({
  // title: $t("Nouveau mot de passe"),
})

const route = useRoute()
const email = ref("")
const isEmailUntouched = ref(true)
const isPasswordUntouched = ref(true)
const passwordErrorMessage = ref("")
const password = ref("")
const confirmPassword = ref("")
const confirmPasswordErrorMessage = ref("")
const userStore = useUserStore()
const hasResetKey = computed(() => !!route.query.reset_key)

const onEmailUpdate = () => {
  isEmailUntouched.value = false
}
const onPasswordUpdate = () => {
  isPasswordUntouched.value = false
}

const emailErrorMessage = computed(() => {
  if (isEmailUntouched.value) {
    return ""
  }
  if (!email.value.includes("@")) {
    return $t("Le courriel doit contenir @")
  }
  return ""
})
const isMailValid = computed(
  () => isEmailUntouched.value || !emailErrorMessage.value,
)

const isPasswordValid = computed(() => {
  if (isPasswordUntouched.value) {
    return true
  }
  if (!password.value.length) {
    passwordErrorMessage.value = $t("Le mot de passe ne peut pas être vide")
    return false
  }
  passwordErrorMessage.value = ""
  return true
})
const isSamePassword = computed(() => {
  if (isPasswordUntouched.value) {
    return true
  }
  if (password.value === confirmPassword.value) {
    confirmPasswordErrorMessage.value = ""
    return true
  }
  confirmPasswordErrorMessage.value = $t("Les deux mots de passe sont différents")
  return false
})
const emailDisabled = computed(() => !(isMailValid && email.value))
const passwordDisabled = computed(
  () => !(isPasswordValid && isSamePassword && password.value),
)
const sendResetLink = () => {
  userStore.sendResetLink(email.value)
}
const resetPassword = () => {
  const resetKey = useRoute().query.reset_key
  if (typeof resetKey === "string") {
    userStore.resetPassword(resetKey, password.value)
  } else {
    userStore.resetPassword(resetKey[0], password.value)
  }
}
</script>
