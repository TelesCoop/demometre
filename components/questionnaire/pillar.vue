<template>
  <div
    class="pillar-card"
    :class="
      (isHovered && `has-background-${colorClass}-light`) +
        (props.isCompleted && ` has-background-${colorClass}-light-active`) +
        ` is-${colorClass}`
    "
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <div :class="circleClass" class="pillar-circle">
      <Picto :name="`${props.name}-big`" class="picto big" />
      <Picto :name="`${props.name}-mini`" class="picto little" />
    </div>
    <p :class="`has-text-${colorClass}-dark is-size-4-tablet is-size-5-mobile`">
      {{ textTitle }}
    </p>
    <AnalyticsScore
      v-if="!isNullOrUndefined(score)"
      :score="props.score"
      :color="props.active ? `${colorClass}-active` : colorClass"
      :size-circles="12"
      size-number-class="is-size-5"
    />
    <span
      class="icon"
      :class="
        (!isNullOrUndefined(score) && `with-score `) + `has-text-${colorClass}`
      "
    >
      <icon size="24" name="arrow-right-line" />
    </span>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue"
import { PillarParams } from "~/composables/types"
import { isNullOrUndefined } from "assets/utils"
import { useI18n } from "vue-i18n"

const i18n = useI18n()
const $t = i18n.t

const props = defineProps({
  name: { type: String, required: true },
  isCompleted: { type: Boolean, default: false },
  active: { type: Boolean, default: true },
  score: { type: Number, required: false, default: undefined },
})
const isHovered = ref(false)

const colorClass = computed(() => PillarParams[props.name].color)
const textTitle = computed(
  () => $t(props.name[0].toUpperCase() + props.name.slice(1)),
)
const circleClass = computed(() => {
  const toReturn = `pillar-circle has-border-${colorClass.value} `

  const other = props.active
    ? `has-background-${colorClass.value} has-text-white`
    : `has-background-${colorClass.value}-light has-text-${colorClass.value}`
  return `${toReturn} ${other}`
})
</script>

<style scoped lang="sass">
.pillar-card
  width: 270px
  display: flex
  flex-direction: column
  align-items: center
  padding: 24px
  flex-grow: 0
  flex-shrink: 0

.pillar-circle
  position: relative
  width: 100px
  height: 100px
  border-radius: 100%
  text-align: center
  padding-top: 16px
  margin-bottom: 0.75rem

.picto
  vertical-align: bottom
  position: absolute
  left: 50%
  transform: translateX(-50%)
  bottom: 23px

  &.little
    display: none

.icon
  display: none

@include mobile
  .pillar-card
    display: flex
    flex-direction: row
    padding: 1rem
    background-color: var(--color-light)
    justify-content: flex-start
    column-gap: 1rem
    height: fit-content
    width: auto
    margin: 0 0.5rem
    position: relative

    p
      margin-right: 23px
  .icon
    display: block
    position: absolute
    right: 1rem

    svg
      vertical-align: middle

  .pillar-circle
    width: 50px
    height: 50px
    border-radius: 100%
    font-size: 24px
    text-align: center
    padding-top: 6px
    margin-bottom: 0rem
    position: relative
  .picto
    bottom: 0

    &.big
      display: none

    &.little
      display: block

@include until(430px)
  .pillar-card
    padding: 0.75rem
    margin: 0
    column-gap: 0.3rem

    p
      margin-right: 2px
      font-size: 1rem !important
  .pillar-circle
    width: 45px
    height: 45px
  .icon.with-score
    display: none
</style>
