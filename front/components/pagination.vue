<template>
  <div class="container">
    <section class="section">
      <slot :page-list="pageList" />
      <nav
        v-if="numberOfPages > 1"
        class="pagination is-centered"
        role="navigation"
        aria-label="pagination"
      >
        <button
          class="pagination-previous button is-outlined has-border-shade-300 has-text-shade-600"
          :disabled="previousDisabled"
          @click.prevent="previousPage"
        >
          <span class="icon">
            <icon size="20" name="arrow-left-line" />
          </span>
        </button>
        <button
          class="pagination-next button is-outlined has-border-shade-300 has-text-shade-600"
          :disabled="nextDisabled"
          @click.prevent="nextPage"
        >
          <span class="icon">
            <icon size="20" name="arrow-right-line" />
          </span>
        </button>
        <ul class="pagination-list">
          <li v-if="numberOfPages > 1 && currentPage > 2">
            <button
              class="pagination-link button is-outlined has-border-shade-300 has-text-shade-600"
              :disabled="previousDisabled"
              @click.prevent="firstPage"
            >
              1
            </button>
          </li>
          <li v-if="numberOfPages > 3 && currentPage > 3">
            <span class="pagination-ellipsis">&hellip;</span>
          </li>
          <li v-if="currentPage > 1">
            <button
              class="pagination-link button is-outlined has-border-shade-300 has-text-shade-600"
              :disabled="previousDisabled"
              @click.prevent="previousPage"
            >
              {{ currentPage - 1 }}
            </button>
          </li>
          <li>
            <button
              class="pagination-link button has-background-shade-600 has-text-white"
              aria-current="page"
            >
              {{ currentPage }}
            </button>
          </li>
          <li v-if="currentPage < numberOfPages">
            <button
              class="pagination-link button is-outlined has-border-shade-300 has-text-shade-600"
              :disabled="nextDisabled"
              @click.prevent="nextPage"
            >
              {{ currentPage + 1 }}
            </button>
          </li>
          <li v-if="numberOfPages > 3 && currentPage < numberOfPages - 2">
            <span class="pagination-ellipsis">&hellip;</span>
          </li>
          <li v-if="numberOfPages > 2 && currentPage < numberOfPages - 1">
            <button
              class="pagination-link button is-outlined has-border-shade-300 has-text-shade-600"
              :disabled="nextDisabled"
              @click.prevent="lastPage"
            >
              {{ numberOfPages }}
            </button>
          </li>
        </ul>
      </nav>
    </section>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  list: { type: Array, required: true },
  numberPerPage: { type: Number, required: true },
})

const currentPage = ref<number>(1)
const pagination = reactive({ begin: 0, end: props.numberPerPage })

const numberOfPages = computed<number>(() =>
  Math.ceil(props.list.length / props.numberPerPage),
)
const pageList = computed(() =>
  props.list.slice(pagination.begin, pagination.end),
)

const nextDisabled = computed(() => currentPage.value === numberOfPages.value)
const previousDisabled = computed(() => currentPage.value === 1)

function nextPage() {
  currentPage.value += 1
  loadList()
}
function previousPage() {
  currentPage.value -= 1
  loadList()
}
function firstPage() {
  currentPage.value = 1
  loadList()
}
function lastPage() {
  currentPage.value = numberOfPages.value
  loadList()
}
function loadList() {
  pagination.begin = (currentPage.value - 1) * props.numberPerPage
  pagination.end = pagination.begin + props.numberPerPage
}
</script>

<style scoped lang="sass"></style>
