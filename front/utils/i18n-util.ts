import { createI18n } from "vue-i18n"
import en from "~/language/en/en.json"
import { localeFromCookie } from "~/composables/useLocale"

let defaultLocale = "fr"

if (process.client) {
  defaultLocale = localeFromCookie(document.cookie)
}

export const i18n = createI18n({
  legacy: false,
  locale: defaultLocale,
  messages: {
    en: en,
  },
  silentTranslationWarn: true,
  fallbackWarn: false,
  missingWarn: false,
})
