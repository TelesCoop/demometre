<template>
  <div
    v-if="data.ranges.length"
    class="interval-chart"
  >
    <div
      class="interval-chart-bar"
      :class="`has-background-${color}-hover`"
    >
      <span>
        <span
          class="interval-chart-bar-line"
          :class="`has-background-${color}-hover`"
          style="left: 0%"
        />
        <span
          v-for="index in data.ranges.length"
          :key="`line_${index}`"
          class="interval-chart-bar-line"
          :class="`has-background-${color}-hover`"
          :style="`left: ${getXPosition(index, data.ranges.length)}%`"
        />
      </span>

      <span>
        <span
          class="interval-chart-bar-line-value"
          :class="`has-text-${color}-hover`"
          style="left: 0%"
        >{{ data.ranges[0].lowerBound ?? "-∞" }}{{ unit }}</span>
        <template
          v-for="(range, index) in data.ranges"
          :key="range.id"
        >
          <span
            class="interval-chart-bar-line-value"
            :class="`has-text-${color}-hover`"
            :style="`left: ${getXPosition(index + 1, data.ranges.length)}%`"
          >{{ range.upperBound ?? "+∞" }}{{ unit }}</span>
        </template>
      </span>

      <span>
        <template
          v-for="(range, index) in data.ranges"
          :key="index"
        >
          <span
            class="interval-chart-bar-interval-score"
            :class="`has-text-${color}-hover`"
            :style="`left: ${
              getXPosition(index + 1, data.ranges.length) -
              getXPosition(1, data.ranges.length) / 2
            }%`"
          >
            <AnalyticsScore
              :class="`has-text-${color}-dark`"
              :score="range.score"
              :show-number="true"
              :color="color"
              :size-circles="9"
              size-number-class="is-size-6"
            />
          </span>
        </template>
      </span>
      <span
        class="interval-chart-bar-result-line"
        :class="`has-background-${color}-dark`"
        :style="`left: ${valuePosition}%`"
      />
      <span
        class="interval-chart-bar-result-value"
        :class="`has-text-${color}-dark is-size-4${
          valuePosition < 20 ? ' has-text-right' : ''
        }`"
        :style="`left: ${valuePosition}%`"
      >
        <strong>{{ data.value.value }}</strong>{{ unit }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue"

const props = defineProps({
  data: { type: Object, required: true },
  color: { type: String, required: true },
  unit: {
    type: String,
    default: '',
  },
})

const getXPosition = (index: number, length: number): number => {
  return (index / length) * 100
}
const valuePosition = computed(() => {
  if (!props.data.ranges.length) {
    return 0
  }
  const value = props.data.value.value

  const rangeIndex = props.data.ranges?.findIndex(
    (range) => value >= (range.lowerBound ?? -Infinity) && value <= (range.upperBound ?? Infinity),
  )
  const currentRange = props.data.ranges?.[rangeIndex]

  let intervalBetweenBound
  if (!currentRange.lowerBound) {
    // if lower bound is not defined, we assume that the value is upper bound or have an offset of 0.05
    intervalBetweenBound = currentRange.upperBound === value ? 1 : 0.95
  } else if (!currentRange.upperBound) {
    // if upper bound is not defined, we assume that the value is lower bound or have an offset of 0.05
    intervalBetweenBound = currentRange.lowerBound === value ? 0 : 0.05
  } else {
    intervalBetweenBound =
      (value - currentRange.lowerBound) /
      (currentRange.upperBound - currentRange.lowerBound)
  }
  return (
    getXPosition(rangeIndex, props.data.ranges.length) +
    intervalBetweenBound * getXPosition(1, props.data.ranges.length)
  )
})
</script>

<style scoped lang="sass">
.interval-chart
  $result-line-size: 66px
  $result-line-offset: 15px
  $chart-size: 24px
  $line-size: 2px

  display: flex
  align-items: center
  width: 100%

  &-bar
    position: relative
    height: $line-size
    margin-top: #{$result-line-size - $result-line-offset}
    margin-bottom: calc(#{($chart-size - $line-size)} / 2 + 24px) // 24px to add bottom number

    width: 100%
    &-line, &-line-value, &-interval-score, &-result-line, &-result-value
      display: flex
      position: absolute

    &-line
      width: $line-size
      height: $chart-size
      transform: translate(-50%, -50%)

    &-line-value
      transform: translate(-50%, 100%)
      bottom: -16px

      &:first-child
        transform: translate(0, 100%)
      &:last-child
        transform: translate(-100%, 100%)

    &-interval-score
      transform: translate(-50%, 100%)
      bottom: -16px

    &-result-line
      height: $result-line-size
      width: $line-size
      transform: translate(-50%, calc(-50% - $result-line-offset))

    &-result-value
      transform: translate(-120%, -#{$result-line-size - $result-line-offset})
      &.has-text-right
        transform: translate(25%, -#{$result-line-size - $result-line-offset})
</style>
