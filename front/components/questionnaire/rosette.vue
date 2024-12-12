<template>
  <div class="container">
    <section class="columns is-centered">
      <div class="rosette">
        <div class="center-button are-normal is-shade-600">
          <button
            v-if="props.centerButtonName"
            class="button is-rounded is-responsive is-outlined is-shade-600"
            @click.prevent="onCenterButtonClick()"
          >
            {{ props.centerButtonName }}
          </button>
        </div>
        <div
          v-for="pillar in questionnaireStore.pillarsOfMainSurvey"
          :key="pillar.name"
          :class="`pillar-container-${PillarParams[pillar.name].key} has-text-${
            PillarParams[pillar.name].color
          }-dark`"
        >
          <div
            :class="
              `pillar-circle-${PillarParams[pillar.name].key}
                    has-border-${PillarParams[pillar.name].color}
              ` +
                (pillar.id === hoverPillarId ||
                  pillar.markerIds.includes(hoverMarkerId) ||
                  props.pillarsCompleted.includes(pillar.name)
                  ? `has-background-${PillarParams[pillar.name].color}`
                  : `has-background-${PillarParams[pillar.name].color}-light`)
            "
            @mouseenter="hoverPillarId = pillar.id"
            @mouseleave="hoverPillarId = null"
            @click="onPillarClick(pillar.name)"
          >
            <div
              v-if="pillar.markerIds.includes(hoverMarkerId)"
              class="pillar-marker-title"
            >
              <span
                class="is-size-7 has-text-weight-bold"
                style="margin: 0px 8px"
              >
                {{ questionnaireStore.markerById[hoverMarkerId].name }}
              </span>
            </div>
            <div v-else>
              <Picto
                :name="`${pillar.name}-little`"
                :class="`pillar-icon-${PillarParams[pillar.name].key}`"
              />
              <span
                class="pillar-title is-size-7 has-text-weight-bold is-capitalized"
              >{{ $t(pillar.name) }}</span>
            </div>
          </div>

          <div
            v-for="(markerId, index) in pillar.markerIds"
            :key="markerId"
            :class="
              `
            marker-circle-${PillarParams[pillar.name].key}
            has-border-${PillarParams[pillar.name].color} ` +
                (markerId === hoverMarkerId
                  ? `has-background-${PillarParams[pillar.name].color}`
                  : ``)
            "
            @mouseenter="hoverMarkerId = markerId"
            @mouseleave="hoverMarkerId = null"
            @click="onMarkerClick(markerId)"
          >
            <span class="marker-index is-size-7 has-text-weight-bold">
              {{ index + 1 }}
            </span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useQuestionnaireStore } from "~/stores/questionnaireStore"
import { PillarParams } from "~/composables/types"
import { useI18n } from "vue-i18n"

const i18n = useI18n()
const $t = i18n.t

// only here to be picked up by i18n for translations
const vars = ([ // eslint-disable-line
  $t("coopération"),
  $t("transparence"),
  $t("participation"),
  $t("représentation"),
] as string[])

const props = defineProps({
  centerButtonName: { type: String, required: true },
  pillarsCompleted: {
    type: Array,
    default() {
      return []
    },
  },
})

const emit = defineEmits<{
  (e: "center-button-click"): void
  (e: "pillar-click", value: any): void
  (e: "marker-click", value: any): void
}>()

const questionnaireStore = useQuestionnaireStore()

const hoverMarkerId = ref<number>()
const hoverPillarId = ref<number>()

function onCenterButtonClick() {
  emit("center-button-click")
}

function onPillarClick(pillarName) {
  emit("pillar-click", pillarName)
}

function onMarkerClick(markerId) {
  emit("marker-click", markerId)
}
</script>

<style scoped lang="sass">
.rosette
  position: relative
  width: 600px
  height: 500px

.center-button
  position: absolute
  top: 50%
  left: 50%
  transform: translate(-50%, -50%)

$pillars: ("representation": (translateX(-170px), 5, translateX(-90px)), "transparency": (translateY(-125px), 4, translateY(-90px)), "participation": (translateX(170px), 5, translateX(90px)), "cooperation": (translateY(125px), 4, translateY(90px)))
@each $name, $pair in $pillars
  $translate: nth($pair, 1)
  $nb-markers: nth($pair, 2)
  $marker-translate: nth($pair, 3)

  .pillar
    &-container-#{$name}
      position: absolute
      width: 210px
      height: 210px
      top: 50%
      left: 50%
      transform: translate(-50%, -50%) $translate

    &-circle-#{$name}
      position: absolute
      top: 50%
      left: 50%
      transform: translate(-50%, -50%)
      border: 1px solid
      width: 120px
      height: 120px
      border-radius: 50%
      cursor: pointer

    &-icon-#{$name}
      position: absolute
      bottom: 50%
      left: 50%
      transform: translate(-50%, 12px)

  .marker-circle-#{$name}
    position: absolute
    display: flex
    align-items: center
    justify-content: center
    top: 50%
    left: 50%
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
