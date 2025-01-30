<template>
  <div class="is-italic">
    {{ $t("La question est à répondre uniquement si vous avez un des profils suivants :") }}
    {{ profileTypesNames }}
  </div>
</template>

<script lang="ts" setup>
import type { PropType } from "vue"
import type { ProfileType } from "~/composables/types"
import { useProfilingStore } from "~/stores/profilingStore"
import { useI18n } from "vue-i18n"

const i18n = useI18n()
const $t = i18n.t
const props = defineProps({
  profileTypesIds: { type: Array as PropType<ProfileType[]>, required: true },
})
const profilingStore = useProfilingStore()

const profileTypes = computed(() => {
  return props.profileTypesIds
    .map((profileTypeId) => {
      return profilingStore.profileTypeById[profileTypeId]
    })
    .filter((profileType) => profileType)
})
const profileTypesNames = computed(() => {
  return profileTypes.value
    .map((profileType) => `"${profileType.name}"`)
    .join(", ")
})
</script>
