<template>
  <div>
    <figure class="image">
      <img
        :src="url"
        alt=""
      >
      <figcaption class="has-text-shade-500 is-size-7">
        {{ block.value.caption }}
      </figcaption>
    </figure>
  </div>
</template>

<script setup lang="ts">
import { PropType } from "vue"
import { Block } from "~/composables/types"
import { useBackendUrl } from "~/composables/api"

const props = defineProps({
  block: {
    type: Object as PropType<Block>,
    required: true,
  },
})
const url = `${useBackendUrl(false)}${props.block.value.url}`
</script>
