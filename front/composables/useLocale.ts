export const localeFromCookie = (cookie: string) => {
  let localCookie = cookie
  localCookie = localCookie.split("; ")
    .find((row) => row.startsWith("django_language="))
  return localCookie ? localCookie.split("=")[1] : "fr"
}

export const useLocale = () => {
  let cookie: string
  if (process.client) {
    cookie = document.cookie
  } else {
    cookie = useRequestHeaders(["cookie"])["cookie"] || ""
  }
  return localeFromCookie(cookie)
}
