<template>
  <section class="intro-text" :class="`mb-${marginBottom}`">
    <h1 class="title is-size-1-desktop is-2 has-text-black">
      {{ title }}
    </h1>
    <div
      v-if="subtitle"
      class="is-family-secondary is-size-5 is-size-4-desktop"
    >
      {{ subtitle }}
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps({
  title: { type: String, required: true, default: "" },
  subtitle: { type: String, required: false, default: undefined },
  marginBottom: { type: Number, default: 3 },
})
</script>

<style scoped lang="sass">
.intro-text
  @include desktop
    margin-right: 60px
</style>
