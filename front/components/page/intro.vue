<template>
  <div class="container">
    <section
      class="intro columns section is-variable"
      :class="`is-${props.columnGap}`"
    >
      <div class="column" :class="`is-${props.columnDistribution[0]}`">
        <PageTitle
          :title="props.title"
          :subtitle="props.subtitle"
          :margin-bottom="1"
        />
        <RichText
          v-if="props.introduction"
          :rich-text="props.introduction"
          class="is-family-secondary"
        />
        <slot />
      </div>
      <div
        class="column"
        :class="`is-offset-${props.columnDistribution[1]} is-${props.columnDistribution[2]}`"
        style="text-align: end"
      >
        <div v-if="props.youtubeVideoId" class="video-container">
          <iframe
            width="100%"
            height="100%"
            :src="`https://www.youtube-nocookie.com/embed/${props.youtubeVideoId}`"
            title="YouTube video player"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
          />
        </div>
        <figure v-else-if="props.imageUrl" class="image">
          <img
            :src="MEDIA_BASE_URL + props.imageUrl"
            alt
            style="border-radius: 6px"
          >
        </figure>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { MEDIA_BASE_URL } from "~/composables/api"

const props = defineProps({
  title: { type: String, required: true, default: "" },
  subtitle: { type: String, required: true, default: "" },
  introduction: { type: String, required: false, default: undefined },
  youtubeVideoId: { type: String, required: false, default: undefined },
  imageUrl: { type: String, required: false, default: undefined },
  columnDistribution: {
    type: Array,
    default() {
      return [6, 0, 6]
    },
  },
  columnGap: { type: Number, default: 8 },
})
</script>

<style scoped lang="sass">
.buttons
  &.are-medium-desktop
    .button:not(.is-normal):not(.is-medium):not(.is-large)
      @include desktop
        font-size: 1.25rem

  .button
    margin-bottom: 1rem

.columns.is-variable.is-16
  --columnGap: 4rem

.video-container
  width: 100%
  height: 100%
  max-width: 600px
  max-height: 337px
</style>
