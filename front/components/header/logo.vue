<template>
  <div class="logo">
    <div
      v-for="pillarName in PillarName"
      :key="pillarName"
      :class="
        `pillar-circle-${PillarParams[pillarName].key}
                    has-border-${PillarParams[pillarName].color}
              ` +
          (props.activePillarName === pillarName || props.activePillarName === ''
            ? ` has-background-${PillarParams[pillarName].color}`
            : ``)
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
.logo
  position: relative
  width: 40px
  height: 40px
$pillars: ("representation": (translateX(-13px)), "transparency": (translateY(-13px)), "participation": (translateX(13px)), "cooperation": (translateY(13px)))
@each $name, $pair in $pillars
  $translate: nth($pair, 1)
  .pillar-circle-#{$name}
    position: absolute
    top: 50%
    left: 50%
    transform: translate(-50%, -50%) $translate
    border: 1px solid
    width: 14px
    height: 14px
    border-radius: 50%
</style>
