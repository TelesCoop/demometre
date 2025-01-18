export const pick = (obj, keysToFind) =>
  Object.fromEntries(
    keysToFind.filter((key) => key in obj).map((key) => [key, obj[key]]),
  )
