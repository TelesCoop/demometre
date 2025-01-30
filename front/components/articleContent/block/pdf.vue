<template>
  <div class="mt-3">
    <a
      :href="url"
      target="_blank"
      class="button is-primary"
    >
      <icon
        name="file-download-line"
        size="16"
        class="mr-0_5"
      />
      {{ $t("Télécharger :") }} {{ block.value.title }}
    </a>
  </div>
</template>

<script setup lang="ts">
import { PropType } from "vue"
import { Block } from "~/composables/types"
import { useBackendUrl } from "~/composables/api"
import { useI18n } from "vue-i18n"

const i18n = useI18n()
const $t = i18n.t
const props = defineProps({
  block: {
    type: Object as PropType<Block>,
    required: true,
  },
})
const url = `${useBackendUrl(false)}${props.block.value.url}`
</script>
