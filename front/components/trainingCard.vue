<template>
  <div class="card has-background-shade-250">
    <div class="card-content">
      <div class="is-flex is-justify-content-space-between">
        <h3 class="title is-4">
          {{ training.name }}
        </h3>
        <span
          v-if="training.isAvailableSoon"
          class="tag"
        >
          {{ $t("Bientôt disponible !") }}
        </span>
      </div>

      <div class="element-holder mb-0_5">
        <div class="element-icon">
          <icon name="check" />
        </div>
        <!-- disabling eslint because the v-html is alright, value is clean from backend -->
        <!-- eslint-disable -->
        <div
          class="element-text"
          v-html="training.description"
        />
        <!-- eslint-enable -->
      </div>
      <div class="element-holder mb-0_5">
        <div class="element-icon">
          <icon name="group" />
        </div>
        <div
          class="element-text"
        >
          {{ training.audience }}
        </div>
      </div>
      <div class="element-holder mb-0_5">
        <div class="element-icon">
          <icon name="time" />
        </div>
        <div
          class="element-text"
        >
          {{ training.duration }}
        </div>
      </div>
      <div class="mt-1_5">
        <button
          v-if="training.isAvailableSoon"
          disabled
          class="button is-dark is-rounded"
        >
          {{ $t("Vous renseigner") }}
        </button>
        <a
          v-else
          :href="training.url"
          target="_blank"
          class="button is-dark is-rounded"
        >
          <span>{{ $t("Vous renseigner") }}</span>
          <span class="icon">
            <icon
              size="16"
              name="arrow-right-line"
            />
          </span>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { PropType } from "vue"
import { Training } from "~/composables/types"
import { useI18n } from "vue-i18n"

const i18n = useI18n()
const $t = i18n.t
defineProps(
  {
    training: { type: Object as PropType<Training>, required: true },
  })
</script>

<style scoped lang="sass">
.element-holder
  display: flex

.element-icon
  width: 40px
</style>
