<template>
  <div class="line">
    <div
      v-for="pillarName in PillarName"
      :key="pillarName"
      :class="`line-pillar has-background-${PillarParams[pillarName].color}`"
      :style="
        props.activePillarName === ''
          ? `width: 25%`
          : props.activePillarName === pillarName
            ? `width: 100%`
            : `width: 0`
      "
    />
  </div>
</template>

<script setup lang="ts">
import { PillarParams, PillarName } from "~/composables/types"

const props = defineProps({
  activePillarName: { type: String, required: false, default: "" },
})
</script>

<style scoped lang="sass">
.line
  display: flex
  height: 6px
  max-height: 6px
  width: 100%

  &-pillar
    height: 100%
</style>
