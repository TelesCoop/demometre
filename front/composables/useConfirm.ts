import { useMainStore } from "~/stores/mainStore"
import { i18n } from "~/utils/i18n-util"

const $t = i18n.global.t

export const useConfirm = () => {
  const mainStore = useMainStore()

  return (
    text: string,
    title = $t("Confirmation"),
    confirmationLabel = $t("Confirmer"),
    onConfirm: () => void,
    onCancel: () => void = () => {
    },
  ) => {
    const newOnCancel = () => {
      onCancel()
      mainStore.resetConfirm()
    }
    const newOnConfirm = () => {
      onConfirm()
      mainStore.resetConfirm()
    }
    mainStore.confirmation = {
      text,
      title,
      onConfirm: newOnConfirm,
      onCancel: newOnCancel,
      confirmationLabel,
    }
  }
}
