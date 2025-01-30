<template>
  <div class="container">
    <section class="columns section">
      <div class="column is-5">
        <PageTitle :title="pageStore.importantPages.faqPage?.title" />
      </div>
    </section>
    <section>
      <RichText :rich-text="pageStore.importantPages.faqPage?.content" />
    </section>
  </div>
</template>

<script setup lang="ts">
import { usePageStore } from "~/stores/pageStore"
import { onMounted } from "vue"

definePageMeta({
  title: "FAQ",
  breadcrumb: "FAQ",
})

const pageStore = usePageStore()

if (!pageStore.importantPages.faqPage?.title) {
  pageStore.getImportantPages()
}

// on load on client, add a button next to all h4 elements, to show / hide the content below it, up until the next heading element
if (process.client) {
  onMounted(() => {
    const headings = document.querySelectorAll("h4")
    headings.forEach((heading, index) => {
      const button = document.createElement("button")
      button.classList.add("button", "is-small", "is-primary", "ml-1")
      button.textContent = "Afficher la réponse"
      button.onclick = () => {
        const nextHeading = headings[index + 1]
        let element = heading.nextElementSibling
        while (element && element !== nextHeading) {
          element.style.display = element.style.display === "none" ? "block" : "none"
          element = element.nextElementSibling
        }
        button.textContent = button.textContent === "Afficher la réponse" ? "Cacher" : "Afficher la réponse"
      }
      heading.appendChild(button)
    })

    // hide all content initially
    headings.forEach((heading, index) => {
      const nextHeading = headings[index + 1]
      let element = heading.nextElementSibling
      while (element && element !== nextHeading) {
        if (!element.tagName.startsWith("H")) {
          element.style.display = "none"
        }
        element = element.nextElementSibling
      }
    })
  })
}
</script>

<style scoped lang="sass">
.buttons .button
  height: fit-content
</style>
