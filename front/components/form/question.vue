<template>
  <div>
    <h1
      class="title is-size-3-tablet is-size-4-mobile"
      :class="`has-text-${props.color}-dark`"
      data-cy="question-statement"
    >
      {{ question.questionStatement }}
    </h1>
    <RichText
      v-if="question.description"
      class="is-family-secondary"
      :rich-text="question.description"
      :color="props.color"
    />
    <section
      id="menu"
      class="section container is-tight pb-0 pt-0 mt-1"
      :class="`menu is-${color}`"
      style="width: 100%"
    >
      <div
        v-if="tabs.length > 1"
        class="tabs"
        style="width: 100%"
      >
        <ul>
          <li
            v-for="tab of tabs"
            :key="tab.id"
          >
            <a
              class="tab is-size-6"
              :class="[
                `is-${color}`,
                tab.id === currentTabId ? `is-active` : ``,
              ]"
              @click="setTab(tab.id)"
            >{{ tab.label }}</a>
          </li>
        </ul>
      </div>
      <div>
        <!-- TAB : definitions -->
        <div
          v-show="currentTabId === 'definitions'"
          v-if="definitions"
        >
          <div
            v-for="definition of definitions"
            :key="definition.id"
            class="mt-2"
          >
            <span class="has-text-weight-bold">{{ definition.word }}</span>
            <RichText
              class="mt-1 is-block is-family-secondary"
              :rich-text="definition.explanation"
              :color="props.color"
            />
          </div>
        </div>

        <!-- TAB : explanations -->
        <template
          v-for="element of explanatoryWithId"
          :key="element.id"
        >
          <div v-show="currentTabId === element.id">
            <RichText
              :rich-text="element.description"
              :color="props.color"
            />
          </div>
        </template>

        <!-- TAB : responses -->
        <div v-show="currentTabId === 'responses'">
          <!-- Center bloc : question inputs + button previous and next -->
          <div
            class="nav-questionnaire-container"
            style="position: relative"
          >
            <!-- all possible inputs -->
            <FormQuestionInput
              v-model="answer"
              :color="color"
              :question="question"
            />
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import type {
  Definition,
  QuestionResponse,
  SimpleBlock,
  Question,
} from "~/composables/types"
import { computed, PropType } from "vue"
import { useI18n } from "vue-i18n"

const i18n = useI18n()
const $t = i18n.t

type tabDef = { label: string; id: string }
const props = defineProps({
  question: { type: Object as PropType<Question>, required: true },
  explanatory: { type: Array as PropType<SimpleBlock[]>, default: () => [] },
  definitions: {
    type: Object as PropType<{ [key: number]: Definition }>,
    required: false,
    default: () => ({}),
  },
  color: { type: String, required: true },
})

const answer = defineModel("modelValue", {
  type: Object as PropType<QuestionResponse | undefined>,
})
type SimpleBlockWithId = SimpleBlock & { id: string }
const explanatoryWithId = computed<SimpleBlockWithId[]>(() => {
  return props.explanatory.map((element) => {
    return { id: element.title?.replace(/\s+/g, ""), ...element }
  })
})

const tabs = computed(() => {
  const tabs: tabDef[] = [
    {
      label: $t("Réponses"),
      id: "responses",
    },
  ]
  if (props.definitions && Object.keys(props.definitions).length) {
    tabs.push({
      label: $t("Définitions"),
      id: "definitions",
    })
  }
  if (props.explanatory?.length) {
    explanatoryWithId.value.forEach((element) => {
      tabs.push({
        label: `${element.title}`,
        id: element.id,
      })
    })
  }
  return tabs
})
const currentTabId = ref<string>(tabs.value[0]?.id)

function setTab(tabId: string) {
  currentTabId.value = tabId
}
</script>

<style scoped lang="sass">
.tabs
  ul
    border-bottom-color: var(--color)

  .tab
    color: var(--color-hover)
    border-bottom-color: var(--color)
    padding: 0.5em 1.5em 0.5em 0em

    &.is-active
      color: var(--color-dark)
      border-bottom-color: var(--color-dark)

    &:hover
      color: var(--color-active)
      border-bottom-color: var(--color-active)
</style>
