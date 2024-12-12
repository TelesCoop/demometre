import { onBeforeUnmount, onMounted } from "vue"

export function usePressEnter(submit: () => void, canSubmit?: () => boolean) {
  const onPressEnter = (event: any) => {
    // If the user presses the "Enter" key on the keyboard
    if (event.key === "Enter" && (!canSubmit || canSubmit())) {
      // Cancel the default action, if needed
      event.preventDefault()
      submit()
      // Trigger the button element with a click
    }
  }

  onMounted(() => {
    document.addEventListener("keypress", onPressEnter, true)
  })

  onBeforeUnmount(() => {
    document.removeEventListener("keypress", onPressEnter, true)
  })
}
