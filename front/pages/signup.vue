<template>
  <div class="is-flex flex-center">
    <div class="sm-container">
      <form
        class="my-8"
        @submit.prevent="onSubmit"
      >
        <h1 class="title is-1 has-text-shade-800">
          {{ text.title }}
        </h1>

        <!-- email -->
        <div class="field">
          <label class="label">Courriel</label>
          <div class="control has-icons-left has-icons-right">
            <input
              v-model="email"
              class="input"
              type="email"
              placeholder="caroline.dupond@laposte.fr"
              :class="isMailValid ? '' : 'is-danger'"
              required
              @change="onEmailUpdate"
            >
            <span class="icon is-small is-left has-text-shade-600">
              <icon
                size="24"
                name="mail-line"
              />
            </span>
            <span
              v-if="!isMailValid"
              class="icon is-small is-right"
            >
              <i class="fas fa-exclamation-triangle" />
            </span>
          </div>
          <p
            v-if="!isMailValid"
            class="help is-danger width-fit-content"
          >
            {{ emailErrorMessage }}
          </p>
        </div>

        <!-- password -->
        <div class="field">
          <label class="label">{{ $t("Mot de passe") }}</label>
          <div class="control has-icons-left has-icons-right">
            <input
              v-model="password"
              class="input"
              type="password"
              :placeholder="$t('mot de passe')"
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
            <span
              v-if="!isPasswordValid"
              class="icon is-small is-right"
            >
              <i class="fas fa-exclamation-triangle" />
            </span>
          </div>
          <p
            v-if="!isPasswordValid"
            class="help is-danger width-fit-content"
          >
            {{ passwordErrorMessage }}
          </p>
        </div>

        <!-- password confirmation-->
        <div class="field">
          <label class="label">{{ $t("Confirmer le mot de passe") }}</label>
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
            <span
              v-if="!isSamePassword"
              class="icon is-small is-right"
            >
              <i class="fas fa-exclamation-triangle" />
            </span>
          </div>
          <p
            v-if="!isSamePassword"
            class="help is-danger width-fit-content"
          >
            {{ confirmPasswordErrorMessage }}
          </p>
        </div>

        <!-- submit -->
        <div
          class="mt-1"
          style="text-align: end"
        >
          <button
            class="button is-shade-600 is-small"
            :disabled="disabled"
          >
            <span>{{ text.button }}</span>
            <span class="icon">
              <icon
                size="16"
                name="check"
              />
            </span>
          </button>

          <!-- Permet d'appuyer sur entrer -->
          <input
            type="submit"
            hidden
          >
        </div>
        <div class="mt-1">
          <span class="is-size-7 has-text-shade-800">
            {{ $t("Vous avez déjà un compte ?") }}
            <NuxtLink
              to="/login"
              class="has-text-shade-500"
              style="text-decoration-line: revert"
              @click="
                () => {
                  userStore.afterLoginRouterGoStep -= 1
                }
              "
            >{{ $t("Connectez-vous") }}</NuxtLink>
          </span>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from "~/stores/userStore"
import { ErrorMessages } from "~/composables/errors"

const i18n = useI18n()
const $t = i18n.t

const email = ref("")
const isEmailUntouched = ref(true)
const isPasswordUntouched = ref(true)
const confirmPasswordErrorMessage = ref("")
const password = ref("")
const confirmPassword = ref("")
const confirmSignupErrorMessage = reactive({ email: [], password: [] })
const userStore = useUserStore()

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
  if (confirmSignupErrorMessage.email.length)
    return confirmSignupErrorMessage.email.join(", ")
})
const isMailValid = computed(
  () => isEmailUntouched.value || !emailErrorMessage.value,
)
const passwordErrorMessage = computed(() => {
  if (isPasswordUntouched.value) {
    return ""
  }
  if (!password.value.length) {
    return $t("Le mot de passe ne peut pas être vide")
  }
  if (confirmSignupErrorMessage.password.length)
    return confirmSignupErrorMessage.password.join(", ")
})
const isPasswordValid = computed(
  () => isPasswordUntouched.value || !passwordErrorMessage.value,
)
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
const disabled = computed(
  () =>
    !(
      isMailValid &&
      isPasswordValid &&
      isSamePassword &&
      password.value &&
      email.value
    ),
)

const text = computed(() => {
  if (userStore.isUnknownUser) {
    return {
      title: $t("Enregistrer son compte"),
      button: $t("S'enregistrer"),
    }
  }

  return {
    title: $t("Création de compte"),
    button: $t("S'inscrire"),
  }
})

async function onSubmit() {
  const response = await userStore.signup(email.value, password.value)
  if (response && response.error) {
    if (response.error.email) {
      confirmSignupErrorMessage.email = response.error.email.email
    }
    if (response.error.password) {
      confirmSignupErrorMessage.password = response.error.password.password
    }
    if (response.error.field) {
      confirmSignupErrorMessage[response.error.field] = [
        ErrorMessages[response.error.messageCode] || ErrorMessages.default,
      ]
    }
  }
}
</script>
