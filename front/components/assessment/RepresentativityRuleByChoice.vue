<template>
  <section>
    <h2 class="title is-3 mb-2">Configuration des seuils de représentativité</h2>
    <div class="two-columns-grid">
    <div v-for="representativity in props.assessment.representativities" :key="representativity.id" class="mb-2">
      <h3 class="title is-4 mb-1">{{representativity.representativityCriteriaName}}</h3>
      <OneRepresentativityRuleByChoice
        v-for="(responseChoice) in representativity.countByResponseChoice"
        :key="responseChoice.responseChoiceId"
        :choice="responseChoice"
        :representativity="representativity"
      /></div>
    </div>
  </section>


  <!-- TODO around here add configuration of response choices thresholds
  afficher les critères de représentativité et le champ pour chaque truc. Bouton de suppression
  à la création valider que reponse choice corresponde à un critère de représentativité
  -->
</template>

<script setup lang="ts">
import {PropType} from "vue"
import OneRepresentativityRuleByChoice from "~/components/assessment/OneRepresentativityRuleByChoice.vue"

const props = defineProps({
  assessment: {type: Object as PropType<Assessment>, required: true},
})

</script>

<style scoped lang="sass">

</style>
