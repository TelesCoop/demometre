<template>
  <button
    class="button is-rounded is-size-7"
    @click="toggleLocale"
  >
    {{ buttonText }}
  </button>
</template>

<script setup lang="ts">
import { useLocale } from "~/composables/useLocale"

const localeFromCookie = computed(() => {
  return useLocale()
})
const toggleLocale = async () => {
  const locale = localeFromCookie.value === "fr" ? "en" : "fr"
  // set locale using cookies
  await useApiGet(`set-locale/${locale}/`)
  // refresh page
  window.location.reload()
}
const buttonText = computed(() => {
  return localeFromCookie.value === "fr" ? "read in english 🇬🇧" : "lire en français 🇫🇷"
})
</script>
