<template>
  <Transition>
    <Teleport to="body">
      <div id="snackbar" :class="colorClass">
        {{ message }}
      </div>
    </Teleport>
  </Transition>
</template>

<script setup lang="ts">
const props = defineProps({
  message: { type: String, required: true },
  type: { type: String, default: "error" },
})

const colorClass = computed(() => {
  if (props.type === 'error') return 'has-background-danger'
  if (props.type === 'info') return 'has-background-info'
  if (props.type === 'success') return 'has-background-success'
  if (props.type === 'warning') return 'has-background-warning'
})
</script>

<style scoped lang="sass">
/* The snackbar - position it at the bottom and in the middle of the screen */
#snackbar
  min-width: 250px
  max-width: 530px
  left: 50%
  transform: translateX(-50%)
  background-color: #333
  color: #fff
  text-align: center
  border-radius: 2px
  padding: 16px
  position: fixed
  z-index: 1000
  bottom: 30px
  border: 4px solid white

/* Animations to fade the snackbar in and out */
.v-enter-active,
.v-leave-active
  transition: opacity 0.3 ease, bottom 0.3 ease

.v-enter-from,
.v-leave-to
  bottom: 0
  opacity: 0
</style>
