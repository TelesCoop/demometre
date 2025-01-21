<template>
  <div style="min-width: 250px">
    <p class="has-text-shade-400 is-uppercase is-size-6 mb-0_5">
      {{ title }}
    </p>
    <p
      class="has-text-shade-600 is-size-5"
      style="white-space: pre-line"
    >
      {{ value }}
    </p>
  </div>
</template>
<script setup lang="ts">

defineProps({
  title: { type: String, required: true },
  value: { type: [String, Number], required: false, default: "" },
})
</script>
