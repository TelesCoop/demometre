<template>
  <a
    class="card is-fullheight is-clickable"
    :class="
      isHovered
        ? ` has-background-${backgroundColorHover}`
        : `has-background-${backgroundColor}`
    "
    :href="props.feedback.externalLink"
    target="_blank"
    rel="external noopener noreferrer"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <div class="card-content">
      <div
        class="media is-flex is-flex-direction-row is-align-items-center mb-1_5"
      >
        <div v-if="props.feedback.pictureUrl" class="media-left mr-1">
          <div
            class="image-profile"
            :style="`background-image: url(${
              MEDIA_BASE_URL + props.feedback.pictureUrl
            })`"
          />
        </div>
        <div class="media-content">
          <p class="has-text-shade-600 has-text-weight-bold">
            {{ props.feedback.personName }}
          </p>
          <p class="subtitle is-family-secondary is-6">
            {{ props.feedback.personContext }}
          </p>
        </div>
      </div>
      <div class="content is-family-secondary is-size-6">
        {{ props.feedback.quote }}
      </div>
    </div>
  </a>
</template>

<script setup lang="ts">
import { MEDIA_BASE_URL } from "~/composables/api"

const props = defineProps({
  feedback: { type: Object, required: true },
  backgroundColor: { type: String, required: true },
  backgroundColorHover: { type: String, required: true },
})

const isHovered = ref(false)
</script>

<style scoped lang="sass">
.image
  max-height: 100px
  max-width: 100px
  img
    border-radius: 50%

.image-profile
  border-radius: 50%
  height: 100px
  width: 100px
  background-size: cover
</style>
