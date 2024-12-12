<template>
  <div class="is-fullwidth">
    <table class="is-fullwidth">
      <thead>
        <tr>
          <th />
          <th
            v-for="possibleAnwer in possibleAnwers"
            :key="`header-${possibleAnwer}`"
            class="input-cell"
          >
            {{ possibleAnwer }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="category in categories"
          :key="category.id"
        >
          <td>{{ category.category }}</td>
          <td
            v-for="possibleAnswer in possibleAnwers"
            :key="`answer-${possibleAnswer}`"
            class="input-cell"
          >
            <input
              :name="category.id.toString()"
              :value="possibleAnswer"
              type="radio"
            >
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts" setup>
import { PropType } from "vue"
import {
  Category,
  QuestionBounds,
} from "~/composables/types"

const props = defineProps({
  categories: {
    type: Array as PropType<Category[]>,
    required: true,
  },
  color: { type: String, required: true },
  bounds: { type: Object as PropType<QuestionBounds>, required: true },
})

const possibleAnwers = computed(() => {
  const answers = []
  for (let i = props.bounds.min + 1; i <= props.bounds.max; i++) {
    answers.push(i)
  }
  return answers
})
</script>

<style src="@vueform/slider/themes/default.css"></style>

<style lang="sass" scoped>
.input-cell
  width: 30px
  text-align: center
</style>
