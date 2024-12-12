<template>
  <div
    class="is-flex is-flex-direction-row is-flex-wrap-wrap"
    :style="`column-gap: ${props.columnGap}; row-gap:${props.rowGap}`"
  >
    <figure v-for="partner of props.partners" :key="partner.id" class="image">
      <img
        :src="MEDIA_BASE_URL + partner.logoImageUrl"
        :alt="partner.name"
        :style="`height: ${partner.height}px`"
      >
    </figure>
  </div>
</template>

<script setup lang="ts">
import { MEDIA_BASE_URL } from "~/composables/api"

const props = defineProps({
  partners: { type: Array, required: true },
  columnGap: { type: String, default: "4rem" },
  rowGap: { type: String, default: "3rem" },
})
</script>

<style scoped lang="sass">
img
  width: 100%
  object-fit: cover
</style>
