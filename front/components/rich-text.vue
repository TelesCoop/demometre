<template>
  <div :class="`is-${color} has-text-${color}-dark`">
    <span v-links-in-new-window class="rich-text" v-html="richText" />
  </div>
</template>

<script setup lang="ts">
defineProps({
  richText: { type: String, default: "" },
  color: { type: String, default: "no-pillar" },
})
const vLinksInNewWindow = {
  mounted: (el) => {
    const anchors = el.querySelectorAll("a")
    anchors.forEach((anchor) => (anchor.target = "_blank"))
  },
}
</script>

<style scoped lang="sass">
.rich-text :deep(ol)
  margin-left: 1.5rem
.rich-text :deep(ul)
  margin-left: 1.5rem
  list-style-type: inherit
.rich-text :deep(li)
  margin-bottom: 4px
.rich-text :deep(p)
  padding-bottom: 6px
.rich-text :deep(a)
  text-decoration: underline
  color: var(--color-active)
  text-decoration-color: var(--color)
.rich-text :deep(a):hover
  text-decoration: underline
  color: var(--color-dark)
  text-decoration-color: var(--color-hover)
.rich-text :deep(h2)
  font-size: 2.5rem
  font-weight: 600
.rich-text :deep(h3)
  font-size: 2rem
  font-weight: 550
.rich-text :deep(h4)
  font-size: 1.5rem
  font-weight: 500
</style>
