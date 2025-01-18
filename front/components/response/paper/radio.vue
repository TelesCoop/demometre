<template>
  <div class="is-flex is-justify-content-center is-align-items-center">
    <input
      type="radio"
      :name="name"
      class="mr-0_5"
      :value="responseChoice.id"
    >
    <label>
      <span>{{ responseChoice.responseChoice }} </span>
      <br>
      <i>{{ responseChoice.description }}</i>
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
