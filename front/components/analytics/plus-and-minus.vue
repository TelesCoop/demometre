<template>
  <div class="columns mt-1_5">
    <div class="column">
      <div class="is-flex">
        <Picto name="strengths" />
        <p class="is-uppercase ml-0_75">
          {{ $t("Points forts") }}
        </p>
      </div>
      <li
        v-for="strength of props.strengthsAndImprovements.strengths"
        :key="strength"
        class="ml-2 is-family-secondary"
      >
        {{ strength }}
      </li>
    </div>
    <div class="column">
      <div class="is-flex">
        <Picto name="weaknesses" />
        <p class="is-uppercase ml-0_75">
          {{ $t("Points d'amélioration") }}
        </p>
      </div>
      <li
        v-for="improvement of props.strengthsAndImprovements.improvements"
        :key="improvement"
        class="ml-2 is-family-secondary"
      >
        {{ improvement }}
      </li>
    </div>
  </div>
</template>

<script setup lang="ts">
import { PropType } from "vue"
import { StrenghtsAndImprovements } from "~/composables/types"
import { useI18n } from "vue-i18n"

const i18n = useI18n()
const $t = i18n.t
const props = defineProps({
  strengthsAndImprovements: {
    type: Object as PropType<StrenghtsAndImprovements>,
    required: true,
  },
})
</script>
