<template>
  <div
    ref="choiceElement"
    class="response-choice"
    :class="
      `is-${color} has-border-transparent ` +
        (props.selected || props.dragging
          ? `has-background-${props.color}-light-active`
          : `has-background-${props.color}-light`) +
        (props.dragging ? ` dragging` : '')
    "
  >
    <div
      v-if="!props.hideLeftSymbol"
      class="letter"
      :class="
        props.selected || props.dragging
          ? props.color === 'no-pillar'
            ? 'has-text-white has-background-shade-800 has-border-shade-800'
            : `has-text-${props.color}-dark has-background-${props.color} has-border-${props.color}-dark `
          : `has-border-${props.color} has-background-white`
      "
    >
      <slot name="left-symbol">
        {{ letter }}
      </slot>
    </div>
    <div class="response-choice-content">
      <p
        class="response-choice-title"
        :class="`${responseChoiceSize} has-text-${props.color}-dark`"
      >
        {{ props.responseChoice.responseChoice }}
      </p>
      <p class="response-choice-description is-size-6bis">
        {{ props.responseChoice.description }}
      </p>
    </div>
    <div class="mb-auto mt-auto ml-auto">
      <slot name="right-symbol">
        <icon
          v-if="props.dragging"
          name="drag-drop-line"
          size="24"
          class="icon mt-0_5 mr-0_5"
        />
        <template v-else>
          <icon
            name="check"
            size="24"
            class="icon mt-0_5 mr-0_5"
            :style="`opacity: ${props.selected ? 1 : 0}`"
          />
        </template>
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { PropType } from "vue"
import { ResponseChoice } from "~/composables/types"

const props = defineProps({
  responseChoice: { required: true, type: Object as PropType<ResponseChoice> },
  responseChoiceIndex: { type: Number, default: 0 },
  selected: { type: Boolean, default: false },
  color: { type: String, required: true },
  hideLeftSymbol: { type: Boolean, default: false },
  responseChoiceSize: { type: String, default: "is-size-5 is-size-6-mobile" },
})
const choiceElement = ref<HTMLElement>()
const letters = "ABCDEFGHIJKLMOPQRSTUVWXYZ"

onMounted(() => {
  window.addEventListener("keydown", (event) => compareKey(event.key))
})

const letter = computed(() => letters[props.responseChoiceIndex])

function compareKey(key: string) {
  if ((key as string).toUpperCase() === letter.value && choiceElement.value)
    choiceElement.value.click()
}
</script>

<style lang="sass" scoped>
@mixin choice-hover
  background-color: var(--color-light-hover) !important
  .letter
    border-color: var(--color) !important
    background-color: var(--color) !important
  &.is-no-pillar .letter
    color: white !important
    background-color: var(--color-dark) !important
    border-color: var(--color-dark) !important

input:focus-visible,input:not(:checked):hover + label .response-choice
  @include choice-hover

.response-choice:hover, .response-choice.dragging, *:focus .response-choice
  @include choice-hover

.response-choice:focus-within
  @include choice-hover

.response-choice
  display: flex
  padding: 16px
  border-radius: 6px
  cursor: pointer
  line-height: 1.3
  min-height: 72px
  align-items: center
  @include mobile
    padding: 8px 10px
  .letter
    text-align: center
    padding-top: 8px
    min-width: 40px
    height: 40px
    border-radius: 6px
    margin-right: 1rem
    @include mobile
      margin-right: 0.5rem
      padding-top: 4px
      min-width: 30px
      height: 30px
  .check
    color: var(--color-dark)
</style>
