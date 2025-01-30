<template>
  <div class="modal is-active">
    <div
      class="modal-background"
      @click="emit('close')"
    />
    <div class="modal-card">
      <header class="modal-card-head">
        <h2 class="modal-card-title">
          {{ title }}
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
        <form @submit.prevent="">
          <template v-if="!bottomFields">
            <div class="field">
              <label class="label">{{ $t("Nom de l'atelier") }}</label>
              <div class="control">
                <input
                  v-model="workshopName"
                  class="input"
                  type="text"
                  placeholder="Text input"
                >
              </div>
            </div>
            <div class="field">
              <label class="label">Lieu</label>
              <div class="control">
                <input
                  v-model="place"
                  class="input"
                  type="text"
                  :placeholder="$t('Salle polyvalente de la ville de ...')"
                >
              </div>
            </div>
            <div class="field">
              <label class="label">{{ $t("Date") }}</label>
              <div class="control">
                <input
                  v-model="date"
                  class="input"
                  type="date"
                  lang="fr-FR"
                >
              </div>
            </div>
          </template>

          <div
            v-for="field of contextFields"
            :key="field.field"
            class="field"
          >
            <ClientOnly>
              <RichTextInput
                :label="field.label"
                :model-value="contextValues[field.field]"
                @update:model-value="newValue => contextValues[field.field] = newValue"
              />
            </ClientOnly>
          </div>
        </form>
      </section>
      <footer class="modal-card-foot">
        <button
          class="button is-rounded is-dark"
          :disabled="loadingStore.isLoading('workshops')"
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
import { Workshop } from "~/composables/types"
import { WORKSHOP_CONTEXT_FIELDS } from "~/utils/constants"
import { useLoadingStore } from "~/stores/loadingStore"
import { useWorkshopStore } from "~/stores/workshopStore"
import { useI18n } from "vue-i18n"

const workshopStore = useWorkshopStore()
const loadingStore = useLoadingStore()

const i18n = useI18n()
const $t = i18n.t

const props = defineProps({
  workshop: { type: Object as PropType<Workshop>, required: true },
  bottomFields: { type: Boolean, default: false },
})
console.log("### edit modal", props.workshop)
const emit = defineEmits(["close"])

const title = computed<string>(() => {
  if (props.bottomFields) {
    return props.workshop?.type === "assessment" ? $t("Modifier les suggestions") : $t("Modifier les remarques")
  } else {
    return $t("Informations de l'atelier")
  }
})

const contextFields = computed<{
  label: string,
  field: WORKSHOP_CONTEXT_FIELD_TYPE
}[]>(() =>
  props.bottomFields ? (
    props.workshop.type === "assessment" ? [
      {
        label: WORKSHOP_CONTEXT_FIELDS.demometreSuggestions,
        field: "demometreSuggestions",
      },
      {
        label: WORKSHOP_CONTEXT_FIELDS.platformSuggestions,
        field: "platformSuggestions",
      },
    ] : [
      {
        label: WORKSHOP_CONTEXT_FIELDS.improvementObservations,
        field: "improvementObservations",
      },
      {
        label: WORKSHOP_CONTEXT_FIELDS.resultObservations,
        field: "resultObservations",
      },
    ]) : [
    {
      label: WORKSHOP_CONTEXT_FIELDS.context,
      field: "context",
    },
    {
      label: WORKSHOP_CONTEXT_FIELDS.objectives,
      field: "objectives",
    },
    {
      label: WORKSHOP_CONTEXT_FIELDS.course,
      field: "course",
    },
    {
      label: WORKSHOP_CONTEXT_FIELDS.comments,
      field: "comments",
    },
  ])
const contextValues = ref<Record<WORKSHOP_CONTEXT_FIELD_TYPE, string>>({})
for (const field of contextFields.value) {
  contextValues.value[field.field] = props.workshop[field.field]  // eslint-disable-line vue/no-setup-props-destructure
}
const workshopName = ref(props.workshop?.name)
const place = ref(props.workshop?.place)
const date = ref(props.workshop?.date)
const saveEdits = async () => {
  const data: any = { name: workshopName.value, place: place.value, date: date.value }
  for (const field of contextFields.value) {
    data[field.field] = contextValues.value[field.field]
  }
  console.log("### data", data, "values", contextValues, "fields", contextFields.value)
  await workshopStore.saveWorkshop(props.workshop.id, data)
  emit("close")
}
</script>
