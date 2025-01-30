<template>
  <div class="container">
    <div
      v-if="post?.imageUrl"
      class="background-center main-image"
      :style="`background-image: url(${mainImageUrl})`"
    />
    <section
      v-if="post"
      class="columns section"
      style="justify-content: center"
    >
      <div class="column is-5">
        <PageTitle :title="post.title" />
        <p
          class="has-text-shade-500 is-size-7 mb-1"
          style="margin-top: -20px"
        >
          {{ date }}
        </p>
        <template v-if="post">
          <ArticleContent :content="post.content" />
        </template>
        <template v-else />
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { usePageStore } from "~/stores/pageStore"

definePageMeta({
  title: "title",
  breadcrumb: "Article",
})

const route = useRoute()
const pageStore = usePageStore()
const slug: string = route.params.slug as string
if (!pageStore.blogPostsBySlug[slug]) {
  await pageStore.getBlogPost(slug)
}
const post = pageStore.blogPostsBySlug[slug]
let mainImageUrl: string
let date: string
if (post == null) {
  if (process.client) {
    // blog post does not exist, redirect to blog list
    window.location.href = "/blog"
  }
} else {
  date = new Date(post.publicationDate).toLocaleDateString("fr-FR", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  })
  mainImageUrl = `${useBackendUrl(false)}${post.imageUrl}`
}
</script>

<style lang="sass" scoped>
.main-image
  width: 100%
  height: 30vh

figcaption
  text-align: center
</style>
