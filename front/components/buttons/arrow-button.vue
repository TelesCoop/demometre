<template>
  <button
    :class="
      color === 'no-pillar' ? `is-shade-600` : `is-${color} text-color-hover`
    "
    class="button is-outlined arrow-button"
    type="button"
  >
    <i class="icon">
      <Icon size="16" name="arrow-left-line" />
    </i>
  </button>
</template>

<script setup lang="ts">
// NB : To use this component
//  set class `nav-questionnaire-container` to the container
//  and `questionnaire-container` to the container of the container
defineProps({
  color: { type: String, required: true },
})
</script>

<style lang="sass">
.arrow-button
  width: 40px
  height: 40px
  border-radius: 50%
</style>
