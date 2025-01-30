<template>
  <div class="modal is-active">
    <div
      class="modal-background"
      @click="emit('close')"
    />
    <div class="modal-card">
      <header class="modal-card-head">
        <h2 class="modal-card-title">
          {{ $t("Informations de l'évaluation") }}
        </h2>
        <icon
          tabindex="0"
          aria-label="fermer la modale"
          name="close"
          class="delete has-cursor-pointer"
          @click="$emit('close')"
        />
      </header>
      <section class="modal-card-body">
        <p class="mb-3">
          {{ $t("En tant qu'initiateur ou expert de l'évaluation, pouvez modifier les informations.") }}
        </p>
        <form @submit.prevent="">
          <div class="field">
            <label class="label">{{ $t("Nom de l'évaluation") }}</label>
            <div class="control">
              <input
                v-model="assessmentName"
                class="input"
                type="text"
                placeholder="Text input"
              >
            </div>
          </div>
          <div class="field">
            <label class="label">{{ $t("Nom du porteur de l'évaluation") }}</label>
            <div class="control">
              <input
                v-model="initializedToTheNameOf"
                class="input"
                type="text"
                placeholder="Text input"
              >
            </div>
          </div>
          <div
            v-for="field of contextFields"
            :key="field.field"
            class="field"
          >
            <ClientOnly>
              <RichTextInput
                :label="field.label"
                :model-value="contextValues[field.field]"
                @update:model-value="
                  (newValue) => (contextValues[field.field] = newValue)
                "
              />
            </ClientOnly>
          </div>
        </form>
      </section>
      <footer class="modal-card-foot">
        <button
          class="button is-rounded is-dark"
          :disabled="loadingStore.isLoading('assessments')"
          @click="saveEdits"
        >
          <span>{{ $t("Valider") }}</span>
          <span class="icon">
            <icon
              size="16"
              name="check"
            />
          </span>
        </button>
        <button
          class="button is-rounded is-outlined is-dark"
          @click="$emit('close')"
        >
          {{ $t("Annuler") }}
        </button>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { PropType } from "vue"
import { Assessment } from "~/composables/types"
import {
  ASSESSMENT_CONTEXT_FIELD_TYPE,
  ASSESSMENT_CONTEXT_FIELDS,
} from "~/utils/constants"
import { useLoadingStore } from "~/stores/loadingStore"
import { useAssessmentStore } from "~/stores/assessmentStore"
import { useI18n } from "vue-i18n"

const i18n = useI18n()
const $t = i18n.t
const assessmentStore = useAssessmentStore()
const loadingStore = useLoadingStore()

const props = defineProps({
  assessment: { type: Object as PropType<Assessment>, required: true },
})
const emit = defineEmits(["close"])

const contextFields: { label: string; field: ASSESSMENT_CONTEXT_FIELD_TYPE }[] =
  [
    {
      divisionLabel: ASSESSMENT_CONTEXT_FIELDS.context,
      field: "context",
    },
    {
      divisionLabel: ASSESSMENT_CONTEXT_FIELDS.stakeholders,
      field: "stakeholders",
    },
    {
      divisionLabel: ASSESSMENT_CONTEXT_FIELDS.objectives,
      field: "objectives",
    },
    {
      divisionLabel: ASSESSMENT_CONTEXT_FIELDS.calendar,
      field: "calendar",
    },
  ]
const contextValues = ref<Record<ASSESSMENT_CONTEXT_FIELD_TYPE, string>>({})
for (const field of contextFields) {
  contextValues.value[field.field] = props.assessment[field.field] // eslint-disable-line vue/no-setup-props-destructure
}
const assessmentName = ref(props.assessment?.name)
const initializedToTheNameOf = ref(props.assessment?.initializedToTheNameOf)
const saveEdits = async () => {
  const data: any = {
    name: assessmentName.value,
    initializedToTheNameOf: initializedToTheNameOf.value,
  }
  for (const field of contextFields) {
    data[field.field] = contextValues.value[field.field]
  }
  console.log(
    "### data",
    data,
    "values",
    contextValues,
    "fields",
    contextFields,
  )
  await assessmentStore.saveAssessment(props.assessment.id, data)
  emit("close")
}
</script>
