<template>
  <div v-for="item in freeBody" :key="item.id">
    <RichText
      v-if="item.type === 'richtext'"
      :rich-text="item.value"
      class="is-family-secondary mb-2"
      :class="!props.insideTwoColumns && 'column-2'"
    />
    <img
      v-else-if="item.type === 'image'"
      :src="MEDIA_BASE_URL + item.imageUrl"
      alt="img"
      class="mb-1"
      style="border-radius: 6px"
    >
    <h3
      v-else-if="item.type === 'title' && props.hTitle === 'h3'"
      :class="titleClasses"
    >
      {{ item.value }}
    </h3>
    <h2 v-else-if="item.type === 'title'" :class="titleClasses">
      {{ item.value }}
    </h2>
    <div v-else-if="item.type === 'step'" class="columns mb-2 is-variable is-6">
      <div
        v-for="(step, index) in item.value"
        :key="index"
        :class="`column is-one-quarter`"
      >
        <PageStepCard
          :step="step"
          :svg-mode="true"
          :index="index"
          background-color="white"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { MEDIA_BASE_URL } from "~/composables/api"

const props = defineProps({
  freeBody: { type: Array, required: true },
  hTitle: { type: String, default: "h2" },
  insideTwoColumns: { type: Boolean, required: true },
})

const titleClasses = ["title", "is-3", "has-text-shade-900", "mb-1", "mt-4"]
</script>

<style scoped lang="sass"></style>
