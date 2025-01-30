<template>
  <div class="document">
    <NuxtLink
      :to="document.file?.link"
      target="_blank"
    >
      <h4 class="title is-6 mb-0_5">
        {{ document.name }}
      </h4>
      <p>{{ extension }} · {{ document.file?.size }} · {{ shownDate }}</p>
    </NuxtLink>
    <button
      class="delete-button"
      aria-label="Supprimer le document"
      title="Supprimer le document"
      @click="confirmDeletion"
    >
      <icon
        name="delete-bin-line"
        size="16"
      />
    </button>
  </div>
</template>

<script setup lang="ts">
import { AssessmentDocumentType } from "~/composables/types"
import { PropType } from "vue"
import { useConfirm } from "~/composables/useConfirm"
import { useAssessmentStore } from "~/stores/assessmentStore"

const assessmentStore = useAssessmentStore()
const confirm = useConfirm()

const props = defineProps({
  document: { type: Object as PropType<AssessmentDocumentType>, required: true },
  assessmentId: { type: Number, required: true },
})
const extension = computed(() => {
  return props.document?.file?.mimeType
})
const shownDate = computed(() => new Date(props.document?.created).toLocaleDateString())

const confirmDeletion = () => {
  confirm(
    `Voulez-vous supprimer ${props.document?.name} ?`,
    "Supprimer le document",
    "Supprimer",
    () => assessmentStore.deleteDocument(props.assessmentId, props.document.id),
  )
}
</script>

<style lang="sass">
.document
  background: $shade-100
  border-radius: 0.75rem
  padding: 1rem
  position: relative

.delete-button
  background: $shade-350
  border-radius: 50%
  cursor: pointer
  position: absolute
  top: -8px
  right: -8px
  width: 32px
  height: 32px
  border: none
</style>
