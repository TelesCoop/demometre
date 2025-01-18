<template>
  <div :class="`is-${color} lds-ring`">
    <div />
    <div />
    <div />
    <div />
  </div>
</template>

<script setup lang="ts">
defineProps({
  color: { type: String, required: true },
})
</script>

<style scoped lang="sass">
.lds-ring
  display: inline-block
  position: relative
  width: 80px
  height: 80px

  & div
    box-sizing: border-box
    display: block
    position: absolute
    width: 64px
    height: 64px
    margin: 5px
    border: 5px solid var(--color)
    border-radius: 50%
    animation: lds-ring 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite
    border-color: var(--color) transparent transparent transparent

  & div:nth-child(1)
    animation-delay: -0.45s

  & div:nth-child(2)
    animation-delay: -0.3s

  & div:nth-child(3)
    animation-delay: -0.15s

@keyframes lds-ring
  0%
    transform: rotate(0deg)

  100%
    transform: rotate(360deg)
</style>
