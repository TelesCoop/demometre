<template>
  <div class="homepage">
    <PageIntro
      :title="pageStore.homePage.title"
      :subtitle="pageStore.homePage.tagLine"
      :introduction="pageStore.homePage.introduction"
      :youtube-video-id="pageStore.homePage.introYoutubeVideoId"
      :image-url="pageStore.homePage.introImageUrl"
      :column-gap="16"
      class="pt-2"
    />

    <!-- Feedbacks -->
    <div class="has-background-shade-250">
      <PageSection
        :title="pageStore.homePage.feedbackBlockTitle"
        :intro="pageStore.homePage.feedbackBlockIntro"
      >
        <div class="mb-2">
          <Carousel
            v-if="pageStore.homePage.feedbacks.length"
            :settings="settings"
            :breakpoints="breakpointsSmallElements"
          >
            <Slide
              v-for="feedback in pageStore.homePage.feedbacks"
              :key="feedback.id"
            >
              <PageFeedbackCard
                :feedback="feedback"
                background-color="white"
                background-color-hover="shade-100"
                class="carousel-item"
              />
            </Slide>
          </Carousel>
        </div>
      </PageSection>
    </div>

    <!-- Blog -->
    <PageSection
      :title="pageStore.homePage.blogBlockTitle"
      :intro="pageStore.homePage.blogBlockIntro"
      :buttons="[{ text: $t('Explorer les articles'), link: `/blog` }]"
    >
      <div class="mb-2">
        <Carousel
          v-if="pageStore.homePage.blogPosts.length"
          :settings="settings"
          :breakpoints="breakpointsLargeElements"
        >
          <Slide
            v-for="blogPost of pageStore.homePage.blogPosts"
            :key="blogPost.id"
          >
            <PageArticleCard
              :article="blogPost"
              background-color="shade-100"
              background-color-hover="shade-200"
              :image-height="260"
              class="carousel-item"
            />
          </Slide>
        </Carousel>
      </div>
    </PageSection>

    <!-- Resources -->
    <div class="has-background-shade-250">
      <PageSection
        :title="pageStore.homePage.resourcesBlockTitle"
        :intro="pageStore.homePage.resourcesBlockTitle"
        :buttons="[{ text: $t('Explorer les ressources'), link: `/ressources` }]"
      >
        <div
          class="mb-2"
          style="display: block"
        >
          <Carousel
            v-if="pageStore.homePage.resources.length"
            :settings="settings"
            :breakpoints="breakpointsSmallElements"
          >
            <Slide
              v-for="resource of pageStore.homePage.resources"
              :key="resource.id"
            >
              <PageArticleCard
                :article="resource"
                background-color="white"
                background-color-hover="shade-100"
                :image-height="300"
                class="carousel-item"
              />
            </Slide>
          </Carousel>
        </div>
      </PageSection>
    </div>

    <!-- Parteners -->
    <PageSection
      :title="pageStore.homePage.partnerBlockTitle"
      :intro="pageStore.homePage.partnerBlockIntro"
    >
      <PagePartnerList :partners="pageStore.homePage.partners" />
    </PageSection>
  </div>
</template>

<script setup lang="ts">
import { Carousel, Slide } from "vue3-carousel"

import "vue3-carousel/dist/carousel.css"
import { usePageStore } from "~/stores/pageStore"

definePageMeta({
  title: "Accueil",
  breadcrumb: "Accueil",
})

const pageStore = usePageStore()

const settings = {
  itemsToShow: 1.05,
  snapAlign: "start",
}
const breakpointsLargeElements = {
  1024: {
    itemsToShow: 3.1,
    snapAlign: "start",
  },
  768: {
    itemsToShow: 1.1,
    snapAlign: "start",
  },
}
const breakpointsSmallElements = {
  1024: {
    itemsToShow: 3.1,
    snapAlign: "start",
  },
  768: {
    itemsToShow: 1.1,
    snapAlign: "start",
  },
}
</script>

<style scoped lang="sass">
.carousel-item
  width: 100%
  text-align: start

.carousel__slide:not(:last-child)
  padding-right: 20px
</style>
