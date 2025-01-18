<template>
  <div class="container">
    <section class="columns is-centered">
      <div :class="`pillar-container-${key} has-text-${color}-dark`">
        <div
          :class="
            `pillar-circle-${key}
                    has-border-${color}
              ` +
              (isHovered
                ? `has-background-${color}`
                : `has-background-${color}-light`)
          "
          @mouseenter="isHovered = true"
          @mouseleave="isHovered = false"
        >
          <div
            v-if="pillar.markerIds.includes(hoverMarkerId)"
            class="pillar-marker-title"
          >
            <span class="is-size-7 has-text-weight-bold">
              {{ questionnaireStore.markerById[hoverMarkerId].name }}
            </span>
          </div>
          <div v-else>
            <Picto
              :name="`${pillar.name}-little`"
              :class="`pillar-icon-${key}`"
            />
            <span
              class="pillar-title is-size-7 has-text-weight-bold is-capitalized"
            >{{ pillar.name }}</span>
          </div>
        </div>

        <div
          v-for="(markerId, index) in pillar.markerIds"
          :key="markerId"
          :class="
            `
            marker-circle-${key}
            has-border-${color} ` +
              (markerId === hoverMarkerId ? `has-background-${color}` : ``)
          "
          @mouseenter="hoverMarkerId = markerId"
          @mouseleave="hoverMarkerId = null"
        >
          <span class="marker-index is-size-7 has-text-weight-bold">
            {{ index + 1 }}
          </span>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useQuestionnaireStore } from "~/stores/questionnaireStore"
import { PillarParams, PillarName } from "~/composables/types"

const questionnaireStore = useQuestionnaireStore()

const hoverMarkerId = ref<number>()
const isHovered = ref<boolean>(false)

const color = PillarParams[PillarName.COOPERATION].color
const key = PillarParams[PillarName.COOPERATION].key
const pillar = questionnaireStore.getPillarByName(PillarName.COOPERATION)
</script>

<style scoped lang="sass">
$nb-markers: 4
$marker-translate: translateY(90px)
.pillar
  &-container-cooperation
    width: 210px
    height: 210px
    position: relative
  &-circle-cooperation
    position: absolute
    top: 50%
    left: 50%
    transform: translate(-50%, -50%)
    border: 1px solid
    width: 120px
    height: 120px
    border-radius: 50%
    cursor: pointer
  &-icon-cooperation
    position: absolute
    bottom: 50%
    left: 50%
    transform: translate(-50%, 12px)

.marker-circle-cooperation
  position: absolute
  top: 50%
  left: 50%
  display: flex
  align-items: center
  justify-content: center
  border: 1px solid
  width: 30px
  height: 30px
  border-radius: 50%
  cursor: pointer
  @for $i from 1 through 8
    &:nth-child(#{$i})
      transform: translate(-50%, -50%) rotate((($i - 2) * 45deg) - calc(($nb-markers - 1) * 45 / 2)) $marker-translate rotate(calc(($nb-markers - 1) * 45 / 2) - (($i - 2) * 45deg))
.marker-index
  text-align: center

.pillar
  &-title
    position: absolute
    top: 50%
    transform: translateY(9px)
    width: 100%
    text-align: center
  &-marker-title
    justify-content: center
    align-items: center
    border-radius: 100%
    text-align: center
    display: flex
    height: 100%
</style>
