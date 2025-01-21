<template>
  <div
    v-if="items.length > 1"
    class="container mt-1 mb-2"
  >
    <nav
      role="navigation"
      class="breadcrumb is-small"
      :aria-label="`Vous êtes ici : ${route.meta.breadcrumb}`"
    >
      <ul>
        <li
          v-for="item in items"
          :key="item.path"
          :class="{ 'is-active': item.path === route.path }"
        >
          <router-link :to="item.path">
            {{ item.meta?.breadcrumb }}
          </router-link>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from "vue-router"
import { computed } from "vue"

const route = useRoute()
const router = useRouter()
const ROOT_PATH = router.resolve("/")

const items = computed(() => {
  // Do not show if no breadcrumb on this page
  if (!route.meta.breadcrumb) {
    return []
  }
  const routeSplit = route.path.split("/").filter((value) => value)
  const paths = [ROOT_PATH]
  let path = ""
  routeSplit.forEach((value) => {
    path = `${path}/${value}`
    const result = router.resolve(path)
    if (result?.meta.breadcrumb) {
      paths.push(result)
    }
  })
  return paths
})
</script>

<style lang="sass">
.breadcrumb li:not(.is-active) a
    text-decoration: underline
</style>
