<template>
  <tr :class="isOpen && `has-background-shade-100`">
    <td
      :aria-expanded="isOpen"
      :aria-controls="`collapse${props.id}`"
      @click.prevent="toggleAccordion()"
    >
      <i class="icon">
        <Icon v-if="isOpen" size="24" name="arrow-down-s-line" />
        <Icon v-else size="24" name="arrow-right-s-line" />
      </i>
    </td>
    <slot name="title" />
  </tr>
  <tr v-show="isOpen" :id="`collapse${props.id}`">
    <td colspan="100%" class="px-3 py-0">
      <div class="has-background-shade-100 px-3 py-1_5">
        <slot name="content" />
      </div>
    </td>
  </tr>
</template>

<script setup lang="ts">
const props = defineProps({
  id: { type: Number, required: true },
})

const isOpen = ref<boolean>(false)
function toggleAccordion() {
  isOpen.value = !isOpen.value
}
</script>
