import { computed, getCurrentInstance } from "vue"

export function useLegacyModel<Type>(
  propName,
  options: { type?: "object" | "array" } = {},
) {
  const vm = getCurrentInstance().proxy

  let valueToSet
  if (options.type === "object") {
    valueToSet = (value: object) => {
      return { ...value }
    }
  } else if (options.type === "array") {
    valueToSet = (value: any[]) => [...value]
  } else valueToSet = (value) => value

  return computed<Type>({
    get() {
      return vm.$props[propName]
    },
    set(value) {
      vm.$emit(`update:${propName}`, valueToSet(value))
    },
  })
}
