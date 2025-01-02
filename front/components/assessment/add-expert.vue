<template>
  <div>
    <div class="columns is-variable is-8">
      <div class="column is-half">
        <p
          class="has-text-weight-bold has-text-shade-800 mb-1"
        >
          {{ props.initiationPage.chooseExpertText }}
        </p>
        <v-select v-model="expertSelected" label="name" :options="assessmentStore.experts" data-cy="expert-select" />
      </div>
      <div class="column is-half">
        <p
          class="has-text-weight-bold has-text-shade-800 mb-1"
        >
          {{ props.initiationPage.ifNoExpertText }}
        </p>
        <!-- Envoyer un mail -->
        <a
          class="button is-normal is-rounded"
          :href="`mailto:${settingsStore.structureSettings.email}`"
          target="_blank"
        >
          <span>{{ $t("Nous contactez") }}</span>
          <span class="icon">
            <icon
              size="20"
              name="mail-line"
            />
          </span>
        </a>
      </div>
    </div>
    <ParticipationConsent
      class="mt-1_5"
      type="cgv"
    />
  </div>
</template>

<script setup lang="ts">
import { PropType } from "vue"
import { useAssessmentStore } from "~/stores/assessmentStore"
import { User, EvaluationInitiationPage } from "~/composables/types"
import vSelect from "vue-select"
import { useSettingStore } from "~~/stores/settingStore"

const props = defineProps({
  initiationPage: {
    type: Object as PropType<EvaluationInitiationPage>,
    required: true,
  },
  modelValue: { type: Object as PropType<User>, required: true },
})

const assessmentStore = useAssessmentStore()
const settingsStore = useSettingStore()
assessmentStore.getExperts()

const expertSelected = useModel("modelValue")
</script>
