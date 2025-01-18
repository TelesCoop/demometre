<template>
  <div class="field">
    <label class="label">{{ $t("Expert") }} {{ expertIx + 1 }}</label>
    <div class="select">
      <select
        id="workshop_type"
        v-model="selectedExpertId"
        name="workshop_type"
        data-cy="expert-select"
      >
        <option
          v-for="expert of assessmentStore.experts"
          :key="expert.id"
          :value="expert.id"
        >
          {{ expert.username }} ({{ expert.email }})
        </option>
      </select>
    </div>
    <div class="mt-0_5">
      <button
        class="button is-small is-rounded is-black is-outlined"
        @click="$emit('remove')"
      >
        {{ $t("Retirer cet expert") }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAssessmentStore } from "~/stores/assessmentStore"

defineProps({
  modelValue: { type: Number, required: true },
  expertIx: { type: Number, default: 0 },
})
defineEmits(["remove", "update:modelValue"])

const assessmentStore = useAssessmentStore()
const selectedExpertId = useModel("modelValue")
</script>
