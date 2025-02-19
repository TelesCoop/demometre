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
          :disabled="props.choice?.ignoreForAcceptabilityThreshold"
          @change="setFocus"
          @focusout="onSave"
        >
      </div>
      <div class="control">
        <button class="button full-height"
                v-show="!props.choice?.ignoreForAcceptabilityThreshold && props.choice?.acceptabilityThreshold != undefined"
                :disabled="props.choice?.ignoreForAcceptabilityThreshold || props.choice?.acceptabilityThreshold == undefined"
                @click="onReinitilize">
          <span class="icon">
            <icon
              name="close"
              size="24"
              class="icon"
            />
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
import { i18n } from "~/utils/i18n-util"

const $t = i18n.global.t

const assessmentStore = useAssessmentStore()

const props = defineProps({
  choice: {
    type: Object as PropType<CountByResponseChoice>,
    required: true,
  },
  representativity: {type: Object as PropType<AssessmentRepresentativity>, required: true},
})
const saved = computed(() => threshold.value == null || (!!props.choice.ruleId && props.choice.acceptabilityThreshold === threshold.value))
const threshold = ref(props.choice?.ignoreForAcceptabilityThreshold ? 0 : props.choice.ruleId ? props.choice?.acceptabilityThreshold : null)


function onReinitilize() {
  if (props.choice.ruleId) {
    assessmentStore.deleteAssessmentCriteraRule({
      id: props.choice.ruleId,
      assessmentId: props.representativity.assessmentId,
    })
  }
  threshold.value = null
}

async function onSave() {
  if (saved.value) return
  if (!threshold.value) throw $t("La valeur vide ne peut pas être enregistrée. Pour réinitialiser la valeur, cliquer sur la croix")
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
}

function setFocus(e) {
  e.target.focus()
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
