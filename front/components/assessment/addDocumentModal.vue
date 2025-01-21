<template>
  <div class="modal is-active">
    <div
      class="modal-background"
      @click="emit('close')"
    />
    <div class="modal-card">
      <header class="modal-card-head">
        <h2 class="modal-card-title">
          {{ $t("Ajouter un document") }}
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
          <div class="field">
            <label class="label">{{ $t("Nom du document") }}</label>
            <div class="control">
              <input
                v-model="name"
                class="input"
                type="text"
                placeholder="Mon nom de fichier"
              >
            </div>
          </div>
          <div class="field">
            <label class="label">{{ $t("Catégorie") }}</label>
            <div class="control">
              <div class="select">
                <select v-model="category">
                  <option
                    v-for="categoryOption of ASSESSMENT_DOCUMENT_CATEGORIES"
                    :key="categoryOption.value"
                    :value="categoryOption.value"
                  >
                    {{ categoryOption.label }}
                  </option>
                </select>
              </div>
            </div>
          </div>
          <div class="field">
            <label class="label">{{ $t("Fichier") }}</label>
            <div class="control">
              <div class="file has-name is-boxed">
                <label class="file-label">
                  <input
                    class="file-input"
                    type="file"
                    name="resume"
                    @change="handleFile"
                  >
                  <span class="file-cta">
                    <span class="file-icon">
                      <icon name="file-upload-line" />
                    </span>
                    <span class="file-label is-size-7">
                      {{ $t("Choisissez un fichier...") }}
                    </span>
                  </span>
                  <span
                    v-if="selectedFileName"
                    class="file-name"
                  >
                    {{ selectedFileName }}
                  </span>
                </label>
              </div>
            </div>
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
import { AssessmentDocumentCategory } from "~/composables/types"
import {
  ASSESSMENT_DOCUMENT_CATEGORIES,
} from "~/utils/constants"
import { useLoadingStore } from "~/stores/loadingStore"
import { useAssessmentStore } from "~/stores/assessmentStore"

const assessmentStore = useAssessmentStore()
const loadingStore = useLoadingStore()

const props = defineProps({ assessmentId: { type: Number, required: true } })
const emit = defineEmits(["close"])

const name = ref("")
const category = ref<AssessmentDocumentCategory>("assessment_reports")
const selectedFileParams = ref<any>({})
const selectedFileName = ref<string>("")

const handleFile = async (event) => {
  const file = event.target.files[0]
  selectedFileParams.value = { base64: await getBase64(file) as string, name: file.name }
  selectedFileName.value = file.name
  console.log("###", event.target.files)
}
const saveEdits = async () => {
  const data = {
    assessment: props.assessmentId,
    category: category.value,
    file: selectedFileParams.value,
    name: name.value,
  }
  await assessmentStore.addDocument(data, props.assessmentId)
  emit("close")
}
</script>
