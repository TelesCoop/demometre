<template>
  <div
    class="dropdown is-right mb-0_75 ml-1"
    :class="{ 'is-active': isDropdownActive }"
  >
    <div
      class="dropdown-trigger has-text-white is-flex mt-0_5"
      style="cursor: pointer"
      @click="isDropdownActive = !isDropdownActive"
    >
      <span>{{ currentLocaleText }}</span>
      <span class="icon is-small ml-0_5">
        <Icon name="arrow-down-s" size="20" />
      </span>
    </div>
    <div
      class="dropdown-menu"
      role="menu"
      style="min-width: initial;"
    >
      <div class="dropdown-content">
        <a
          v-for="locale in otherLocales"
          :key="locale.code"
          class="dropdown-item"
          @click="changeLocale(locale.code)"
        >
          {{ locale.text }}
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useLocale } from "~/composables/useLocale"

const isDropdownActive = ref(false)

const localeFromCookie = computed(() => {
  return useLocale()
})

const availableLocales = [
  { code: "fr", text: "FR" },
  { code: "en", text: "EN" },
]

const currentLocaleText = computed(() => {
  const locale = availableLocales.find((l) => l.code === localeFromCookie.value)
  return locale?.text || "FR"
})

const otherLocales = computed(() => {
  return availableLocales.filter((l) => l.code !== localeFromCookie.value)
})

const changeLocale = async (locale: string) => {
  if (locale === localeFromCookie.value) {
    isDropdownActive.value = false
    return
  }
  // set locale using cookies
  await useApiGet(`set-locale/${locale}/`)
  // refresh page because we need to refresh all data from backend
  window.location.reload()
}

// Close dropdown when clicking outside
onMounted(() => {
  document.addEventListener("click", (event) => {
    const dropdown = event.target as HTMLElement
    if (!dropdown.closest(".dropdown")) {
      isDropdownActive.value = false
    }
  })
})
</script>

<style lang="sass" scoped>
.dropdown-item
  color: $shade-400
</style>
