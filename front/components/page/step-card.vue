<template>
  <div
    class="card is-fullheight"
    :class="
      `has-background-${backgroundColor} ` +
        (props.svgMode ? `svg-mode` : `image-mode`)
    "
  >
    <div class="card-image">
      <figure class="image" :style="`height: ${props.imageHeight}`">
        <img
          :src="imageUrl"
          :alt="props.step.title"
          class="fit-without-distortion"
        >
      </figure>
      <div class="step-number-container is-flex flex-center">
        <span
          class="has-background-shade-800 has-text-white is-flex flex-center step-number"
          :class="props.svgMode ? 'is-size-6' : 'is-size-5'"
        >{{ props.index + 1 }}</span>
      </div>
    </div>
    <div class="card-content px-2 pb-2">
      <div class="mb-1_5">
        <p
          class="is-size-4 has-text-shade-600 has-text-weight-bold has-text-centered"
        >
          {{ props.step.title }}
        </p>
      </div>
      <div class="content">
        <p
          v-if="props.step.description"
          class="is-family-secondary is-size-6 has-text-shade-600"
        >
          {{ props.step.description }}
        </p>
        <RichText
          v-if="props.step.richtext"
          :rich-text="props.step.richtext"
          class="is-family-secondary mb-2"
        />
        <div class="has-text-centered">
          <a
            v-if="props.step.link"
            :href="props.step.link"
            target="_blank"
            class="button is-shade-600 is-rounded is-small"
          >
            <span>En savoir plus</span>
            <span class="icon">
              <icon size="12" name="arrow-right-line" />
            </span>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { MEDIA_BASE_URL } from "~/composables/api"

const props = defineProps({
  step: { type: Object, required: true },
  backgroundColor: { type: String, required: true },
  imageHeight: { type: String, default: "250px" },
  index: { type: Number, required: true },
  svgMode: { type: Boolean, default: false },
})

const imageUrl = computed(
  () =>
    MEDIA_BASE_URL +
    (props.step.imageUrl ? props.step.imageUrl : props.step.svgUrl),
)
</script>

<style scoped lang="sass">
.image-mode
  img
    width: 100%
    object-fit: cover
  .step-number
    border-radius: 6px
    height: 40px
    width: 40px
    &-container
      margin-top: -25px
.svg-mode
  figure
    text-align: center
  img
    width: 100px
    object-fit: cover
    margin-top: 2rem
  .step-number
    border-radius: 6px
    height: 24px
    width: 24px
    &-container
      margin-top: -18px
</style>
