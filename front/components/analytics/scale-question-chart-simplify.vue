<template>
  <div class="scale-question-chart-classic">
    <div class="scale-question-chart-grid">
      <template
        v-for="(category, categoryKey) in data.value"
        :key="categoryKey"
      >
        <div
          :class="`has-background-${color}-light`"
          class="scale-question-chart-cell"
          style="text-align: left"
        >
          {{ category.label }}
        </div>
        <div class="scale-question-chart-sub-grid">
          <div
            v-for="(choice, key) in category.value"
            :key="key"
            :class="`has-background-${color}-light`"
            class="scale-question-chart-bar-cell"
          >
            <template v-for="(roleId, index) of question.roleIds" :key="roleId">
              <div
                v-if="roles.includes(roleId)"
                class="scale-question-chart-bar-container"
                :class="`is-${color}`"
              >
                <div
                  class="scale-question-chart-checked"
                  :class="`has-background-${rolesGradiants[index][0]} has-border-${color}-dark`"
                  :style="{
                    opacity:
                      simplifyData[categoryKey][roleId].choiceKey === key
                        ? 1
                        : 0,
                  }"
                >
                  <icon
                    size="20"
                    name="check"
                    :class="`has-svg-path-fill-${rolesGradiants[index][1]}`"
                  />
                </div>
              </div>
            </template>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { getColorGradients } from "assets/utils/choice-question-chart"
import { useProfilingStore } from "~/stores/profilingStore"
import { PropType } from "vue"
const props = defineProps({
  data: { type: Object, required: true },
  color: { type: String, required: true },
  question: { type: Object, required: true },
  roles: { type: Array as PropType<number[]>, required: true },
})
const profilingStore = useProfilingStore()

const rolesGradiants = computed(
  () => getColorGradients(props.color)[props.question.roleIds.length],
)
const getValueByRoleId = (choice, roleId) => {
  const roleName = profilingStore.roleById[roleId].name
  return choice[roleName]?.value
}
const getSimplifyData = (): {
  [category: number]: {
    [roleId: number]: {
      value: number
      choiceKey: string
    }
  }
} => {
  const data = props.data.value
  const result = {}
  for (const [key, category] of Object.entries(data)) {
    const categoryResult = {}
    for (const roleId of props.roles) {
      const maxCategoryByRole = Object.entries(category.value).reduce(
        (acc, [choiceKey, choice]) => {
          const value = getValueByRoleId(choice, roleId)
          if (value > acc.value) {
            return { value, choiceKey }
          }
          return acc
        },
        { value: 0, choiceKey: null },
      )
      categoryResult[roleId] = maxCategoryByRole
    }
    result[key] = categoryResult
  }
  return result
}
const simplifyData = ref(getSimplifyData())

watch(props.roles, () => {
  simplifyData.value = getSimplifyData()
})

watch(props.data, () => {
  simplifyData.value = getSimplifyData()
})
</script>

<style scoped lang="sass">
.scale-question-chart-checked
  display: flex
  align-items: center
  justify-content: center
</style>
