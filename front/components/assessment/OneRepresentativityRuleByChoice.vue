<template>
  <div class="field is-horizontal has-addons has-addons-right">
        <label class="field-label">{{ props.choice.responseChoiceName }}</label>
    <div class="field-body">
      <div class="control">
        <input
          v-model="threshold"
          class="input"
          type="number"
          :placeholder="props.representativity.minRate.toString()"
          @focusout="onSave"
        >
      </div>
      <div class="control">
        <button class="button full-height"
                :disabled="props.choice?.acceptabilityThreshold == undefined"
                @click="onReinitilize">
          <span class="icon">
        <icon
          name="close"
          size="24"
          class="icon"/>
          </span>
        </button>
      </div>
    </div>
  </div>

</template>

<script setup lang="ts">
import {useAssessmentStore} from "~/stores/assessmentStore"
import {PropType} from "vue"
import {AssessmentRepresentativity, CountByResponseChoice} from "~/composables/types"

const assessmentStore = useAssessmentStore()

const props = defineProps({
  choice: {
    type: Object as PropType<CountByResponseChoice>,
    required: true,
  },
  representativity: {type: Object as PropType<AssessmentRepresentativity>, required: true},
})
const saved = computed(() => threshold.value == null || (!!props.choice.ruleId && props.choice.acceptabilityThreshold === threshold.value))
const threshold = ref(props.choice.ruleId ? props.choice?.acceptabilityThreshold : null)


function onReinitilize() {
  if (props.choice.ruleId) {
    assessmentStore.deleteAssessmentCriteraRule({
      id: props.choice.ruleId,
      assessmentId: props.representativity.assessmentId,
    }) // TODO why string?
  }
  threshold.value = null
}

async function onSave() {
  if (!saved.value) return
  if (!threshold.value) throw "TODO error message"
  if (props.choice?.ruleId) {
    await assessmentStore.updateAssessmentCriteraRule({
      id: props.choice.ruleId,
      acceptabilityThreshold: threshold.value,
      assessmentId: props.representativity!.assessmentId,
    })
    const instance = getCurrentInstance()
    if (instance?.proxy) instance.proxy.$forceUpdate()
  } else await assessmentStore.newAssessmentCriteraRule({
    assessmentRepresentativityId: props.representativity.id,
    responseChoiceId: props.choice?.responseChoiceId,
    acceptabilityThreshold: threshold.value,
    assessmentId: props.representativity!.assessmentId,
  })

  threshold.value = null
}

</script>

<style scoped lang="sass">
.control .button.full-height
  height: 2.5em

.field-body .control input
  width: 5em

.field-label
  flex-grow: 5
  margin-top: auto
  margin-bottom: auto

.field
  margin-bottom: 0.75rem


</style>
