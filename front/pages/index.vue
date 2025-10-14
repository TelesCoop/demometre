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
    <div
      class="section-container-with-background"
      :class="{ 'has-background-shade-250': shouldHaveBackground('feedbacks') }"
    >
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

    <!-- International -->
    <div
      class="section-container-with-background"
      :class="{ 'has-background-shade-250': shouldHaveBackground('international') }"
    >
      <PageSection
        :title="pageStore.homePage.internationalBlockTitle"
        style="background: url('/img/Earth.png') right center no-repeat"
      >
        <div class="columns">
          <div class="column is-9 is-mobile-12">
            <p class="is-family-secondary is-size-5 mb-1">
              {{ pageStore.homePage.internationalBlockIntro }}
            </p>
          </div>
          <div class="column is-3 is-mobile-12">
            <div class="is-flex is-flex-direction-column is-align-items-center" style="gap: 0.3rem">
              <div v-for="country of pageStore.homePage.internationalBlockCountries" :key="country.id">
                <a :href="country.link" class="button is-rounded is-responsive is-dark" target="_blank">
                  <span>{{ country.buttonName }}</span>
                  <span class="ml-0_5" style="position: relative; top: 0.125rem;">
                    <Icon size="16" name="external-link"/>
                  </span>
                </a>
              </div>
            </div>
          </div>
        </div>
      </PageSection>
    </div>

    <!-- Blog -->
    <div
      class="section-container-with-background"
      :class="{ 'has-background-shade-250': shouldHaveBackground('blog') }"
    >
      <PageSection
        :title="pageStore.homePage.blogBlockTitle"
        :intro="pageStore.homePage.blogBlockIntro"
        :buttons="[{ text: $t('Explorer les articles'), link: `/blog`}]"
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
    </div>

    <!-- Partners -->
    <div
      class="section-container-with-background"
      :class="{ 'has-background-shade-250': shouldHaveBackground('partners') }"
    >
      <PageSection
        :title="pageStore.homePage.partnerBlockTitle"
        :intro="pageStore.homePage.partnerBlockIntro"
      >
      <PagePartnerList :partners="pageStore.homePage.partners" />
    </PageSection>
    </div>

    <!-- Resources -->
    <div
      class="section-container-with-background"
      :class="{ 'has-background-shade-250': shouldHaveBackground('resources') }"
    >
      <PageSection
        :title="pageStore.homePage.resourcesBlockTitle"
        :intro="pageStore.homePage.resourcesBlockTitle"
        :buttons="[{ text: $t('Explorer les ressources'), link: `/ressources`}]"
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
  </div>
</template>

<script setup lang="ts">
import { Carousel, Slide } from "vue3-carousel"
import { computed } from "vue"

import "vue3-carousel/dist/carousel.css"
import { usePageStore } from "~/stores/pageStore"

definePageMeta({
  title: "Accueil",
  breadcrumb: "Accueil",
})

const pageStore = usePageStore()

// Track which sections have content to apply alternating backgrounds
const visibleSections = computed(() => {
  const sections = []
  if (pageStore.homePage.feedbackBlockTitle) sections.push('feedbacks')
  if (pageStore.homePage.internationalBlockTitle) sections.push('international')
  if (pageStore.homePage.blogBlockTitle) sections.push('blog')
  if (pageStore.homePage.partnerBlockTitle) sections.push('partners')
  if (pageStore.homePage.resourcesBlockTitle) sections.push('resources')
  return sections
})

// Determine if a section should have background based on its position among visible sections
const shouldHaveBackground = (sectionName: string) => {
  const index = visibleSections.value.indexOf(sectionName)
  // Apply background to every other section, starting with the first (index 0, 2, 4, ...)
  return index !== -1 && index % 2 === 0
}

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
