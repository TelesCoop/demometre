import en from "~/language/en/en.json"

export default defineI18nConfig(() => ({
  legacy: false,
  locale: "fr",
  messages: {
    en: en,
  },
}))