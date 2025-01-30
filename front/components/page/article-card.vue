<template>
  <NuxtLink
    class="card is-fullheight is-clickable"
    :class="
      isHovered
        ? ` has-background-${backgroundColorHover}`
        : `has-background-${backgroundColor}`
    "
    :to="href"
    :target="isExternal ? '_blank' : null"
    rel="external noopener noreferrer"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <div
      v-if="props.article.imageUrl"
      class="card-image"
    >
      <figure class="image">
        <img
          :src="MEDIA_BASE_URL + props.article.imageUrl"
          :alt="props.article.title"
          :style="`max-height: ${props.imageHeight}px`"
        >
      </figure>
    </div>
    <div
      class="card-content"
      :class="
        isHovered
          ? ` has-background-${backgroundColorHover}`
          : `has-background-${backgroundColor}`
      "
    >
      <div class="mb-1_5">
        <p class="is-size-4 has-text-shade-600 has-text-weight-bold">
          {{ props.article.title }}
        </p>
        <p class="has-text-shade-500">
          {{ publicationDate }}
        </p>
      </div>
      <div class="content">
        <p class="is-family-secondary is-size-6">
          {{ props.article.shortDescription }}
        </p>
        <div
          v-if="props.showLinkedPillars"
          class="is-size-7 mt-2"
        >
          <span
            v-for="pillarId of props.article.pillars"
            :key="pillarId"
            :class="`tag mr-0_5 is-${
              PillarParams[questionnaireStore.getPillarNameById(pillarId)].color
            }`"
            style="padding: 6px 12px"
          >
            {{ wordTitleCase(questionnaireStore.getPillarNameById(pillarId)) }}
          </span>
        </div>
      </div>
    </div>
  </NuxtLink>
</template>

<script setup lang="ts">
import { MEDIA_BASE_URL } from "~/composables/api"
import { useQuestionnaireStore } from "~/stores/questionnaireStore"
import { PillarParams, Article } from "~/composables/types"
import { wordTitleCase } from "~/utils/util"
import { PropType } from "vue/dist/vue"

const props = defineProps({
  article: { type: Object as PropType<Article>, required: true },
  backgroundColor: { type: String, required: true },
  backgroundColorHover: { type: String, required: true },
  imageHeight: { type: Number, required: true },
  showLinkedPillars: { type: Boolean, default: false },
})

const questionnaireStore = useQuestionnaireStore()

const isHovered = ref(false)

const publicationDate = computed(() =>
  new Date(props.article.publicationDate).toLocaleString("fr-FR", {
    year: "numeric",
    month: "long",
    day: "numeric",
  }),
)
const isExternal = !!props.article?.externalLink
const href = isExternal
  ? props.article?.externalLink
  : `/blog/${props.article.slug}`
</script>

<style scoped lang="sass">
img
    width: 100%
    object-fit: cover
</style>
