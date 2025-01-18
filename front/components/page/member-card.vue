<template>
  <div class="card is-fullheight has-background-shade-100 impact">
    <div class="card-image">
      <figure class="image">
        <img
          :src="MEDIA_BASE_URL + props.persons.imageUrl"
          :alt="props.persons.personName"
          class="fit-without-distortion"
        >
      </figure>
    </div>
    <div class="card-content">
      <p class="has-text-shade-600 has-text-weight-bold">
        {{ props.persons.name }}
      </p>
      <p class="is-size-6bis has-text-shade-500">
        {{ props.persons.jobTitle }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { MEDIA_BASE_URL } from "~/composables/api"

const props = defineProps({
  persons: { type: Object, required: true },
})
</script>
