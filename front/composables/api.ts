import { useLoadingStore } from "~/stores/loadingStore"
import { useMessageStore } from "~/stores/messageStore"
import { AsyncData } from "#app"
import { FetchError } from "ofetch"

let media_base_url
type MyHeaders = { [key: string]: string }

export const useBackendUrl = (api = true) => {
  let backendUrl = ""
  if (process.env.NODE_ENV !== "production") {
    backendUrl = "http://localhost:8000"
  } else {
    // production server
    if (process.server) {
      const config = useRuntimeConfig()

      // server-side rendering
      backendUrl = `http://127.0.0.1:${config.backendPort}`
      console.log("### API backend port", config.backendPort)
    }
  }

  if (!api) {
    return backendUrl
  }

  return `${backendUrl}/api/`
}

const makeLoadingKey = (path: string) => {
  // camel-case the path : auth/login -> authLogin
  if (path.endsWith("/")) {
    path = path.slice(0, -1)
  }
  if (path.startsWith("/")) {
    path = path.slice(1)
  }
  let words = path.split("/")
  words = words.filter((word) => !/^\d+$/.test(word))
  for (const [ix, word] of Object.entries(words.slice(1))) {
    const newWord = word[0].toUpperCase() + word.slice(1)
    words[parseInt(ix) + 1] = newWord
  }
  return words.join("")
}

function getCookie() {
  let cookie: string
  if (process.server) {
    cookie = useRequestHeaders(["cookie"])["cookie"] || ""
  } else {
    cookie = document.cookie
  }
  return cookie
}

function getCsrfCookie(cookie: string) {
  if (!cookie) {
    return null
  }
  const csfrRow = cookie.split("; ").find((row) => row.startsWith("csrftoken="))
  if (!csfrRow) {
    return null
  }
  return csfrRow.split("=")[1]
}

function getHeaders(withCsrfCookie = false): MyHeaders {
  const cookie = getCookie()
  const headers: MyHeaders = { cookie: cookie }
  if (withCsrfCookie) {
    const csfrToken = getCsrfCookie(cookie)
    if (csfrToken) {
      headers["X-CSRFTOKEN"] = csfrToken
    }
  }
  return headers
}

if (process.env.NODE_ENV !== "production") {
  media_base_url = "http://localhost:8000"
} else {
  // production server
  media_base_url = ""
}
export const MEDIA_BASE_URL = media_base_url

export async function useApiGet<Type>(path: string, onErrorMessage: string = "", forceKey: undefined | string = undefined) {
  const loadingStore = useLoadingStore()
  const messageStore = useMessageStore()
  const key = makeLoadingKey(path)
  loadingStore.markLoading(key)
  const { data, error } = await useFetch<Type>(`${useBackendUrl()}${path}`, {
    method: "GET",
    credentials: "include",
    headers: getHeaders(),
    key: forceKey,
    dedupe: "defer",
  }) as AsyncData<Type, FetchError>
  if (error.value) {
    loadingStore.markError(key)
    if (onErrorMessage) {
      messageStore.setError(onErrorMessage)
    }
  } else {
    loadingStore.markDone(key)
  }
  return { data, error }
}

export async function useAPIwithCsrfToken<Type>(
  path: string,
  method: string,
  payload: any = {},
  onErrorMessage: string = "",
) {
  const loadingStore = useLoadingStore()
  const messageStore = useMessageStore()
  const key = makeLoadingKey(path)
  loadingStore.markLoading(key)
  const { data, error } = await useFetch<Type>(`${useBackendUrl()}${path}`, {
    method,
    body: payload,
    credentials: "include",
    headers: getHeaders(true),
  }) as AsyncData<Type, FetchError>
  if (error.value) {
    loadingStore.markError(key)
    if (onErrorMessage) {
      messageStore.setMessage(onErrorMessage, "error")
    }
  } else {
    loadingStore.markDone(key)
  }
  return { data, error }
}

export async function useApiPost<Type>(path: string, payload: any = {}, onErrorMessage: string = "") {
  return useAPIwithCsrfToken<Type>(path, "POST", payload, onErrorMessage)
}

export async function useApiPatch<Type>(path: string, payload: any = {}, onErrorMessage: string = "") {
  return useAPIwithCsrfToken<Type>(path, "PATCH", payload, onErrorMessage)
}

export async function useApiDelete<Type>(path: string, onErrorMessage: string = "") {
  return useAPIwithCsrfToken<Type>(path, "DELETE", {}, onErrorMessage)
}
