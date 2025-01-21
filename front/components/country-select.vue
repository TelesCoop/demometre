<template>
  <select>
    <slot />
    <option
      v-for="country in COUNTRIES"
      :key="country.code"
      :value="country.code"
    >
      {{ country.name }}
    </option>
  </select>
</template>

<script setup lang="ts">
import { COUNTRIES } from "~/utils/countries"
</script>
