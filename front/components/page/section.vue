<template>
  <div class="container">
    <section
      v-if="title"
      class="section"
    >
      <div class="is-flex is-justify-content-space-between">
        <div>
          <h3
            v-if="isInsideBigSection"
            :class="titleClasses"
          >
            {{ title }}
          </h3>
          <h1
            v-else-if="isFirstElement"
            :class="titleClasses"
          >
            {{ title }}
          </h1>
          <h2
            v-else
            :class="titleClasses"
          >
            {{ title }}
          </h2>
          <p
            v-if="intro && !introIsRichText"
            class="is-family-secondary is-size-5 mb-1"
          >
            {{ intro }}
          </p>
          <RichText
            v-if="intro && introIsRichText"
            :rich-text="intro"
            class="is-family-secondary"
          />
        </div>

        <div
          class="is-flex is-flex-direction-row is-justify-content-space-between is-flex-wrap-wrap mb-3"
        >
          <div>
            <template
              v-for="(button, buttonIx) in buttons"
              :key="buttonIx"
            >
              <NuxtLink
                class="button is-rounded is-responsive"
                :class="[
                  buttonIx == 0 ? 'is-dark' : 'is-normal is-outlined ml-1'
                ]"
                :to="button.link"
                @click="$emit('buttonClick', buttonIx)"
              >
                <span v-if="!button.leftIcon">{{ button.text }}</span>
                <span
                  v-if="icon"
                  class="icon"
                >
                  <icon
                    size="20"
                    :name="button.icon"
                  />
                </span>
                <span v-if="button.leftIcon">{{ button.text }}</span>
              </NuxtLink>
            </template>
          </div>
        </div>
      </div>

      <slot />
    </section>
  </div>
</template>

<script setup lang="ts">
import { PropType } from "vue"
import { SectionButton } from "~/composables/types"

defineProps({
  title: { type: String, required: true, default: "" },
  intro: { type: String, required: false, default: undefined },
  buttons: {
    type: Array as PropType<SectionButton[]>, default() {
      return []
    },
  },
  leftIcon: { type: Boolean, default: false },
  icon: { type: String, required: false, default: "" },
  isInsideBigSection: { type: Boolean, default: false },
  isFirstElement: { type: Boolean, default: false },
  introIsRichText: { type: Boolean, default: false },
})
defineEmits(["buttonClick"])

const titleClasses = ["title", "is-3", "has-text-shade-900", "mb-1"]
</script>

<style scoped lang="sass"></style>
