<template>
  <div class="is-flex">
    <input
      type="checkbox"
      :name="name"
      class="mr-0_5"
      :value="responseChoice.id"
    >
    <label>
      <span>{{ responseChoice.responseChoice }} </span>
      <br v-if="responseChoice.description">
      <i v-if="responseChoice.description">{{ responseChoice.description }}</i>
    </label>
  </div>
</template>

<script setup lang="ts">
import { PropType } from "vue"
import { ResponseChoice } from "~/composables/types"
defineProps({
  name: { type: String, required: true },
  responseChoice: { required: true, type: Object as PropType<ResponseChoice> },
})
</script>

<style lang="sass" scoped></style>
