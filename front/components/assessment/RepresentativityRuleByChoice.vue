<template>
  <section>
    <h2 class="title is-3 mb-2">
      Configuration des seuils de représentativité
    </h2>
    <p class="block mb-2">
      {{ $t(`Les seuils de représentativité peuvent être ajustés afin de refléter au mieux les spécificités sociologiques de chaque territoire.`) }}<br>
      {{ $t(`Ils servent à paramétrer le tableau de bord, dont la fonction est de garantir que les répondants au questionnaire reflètent la diversité des profils sociologiques du territoire.`) }}<br>
      {{ $t(`Si vous ne les configurez pas, les seuils par défaut du Démomètre seront appliqués (affichés en gris).`) }}<br>
      {{ $t(`Si vous ne souhaitez pas fixer de seuil minimum pour une réponse, vous pouvez indiquer la valeur 0.`) }}
      {{ $t(`Les seuils qui sont ignorés au niveau du Démomètre apparaissent en grisé et ne sont pas configurables.`) }}
    </p>
    <div v-for="representativity in props.assessment.representativities" :key="representativity.id" class="mb-2">
      <h3 class="title is-4 mb-1">
        {{ representativity.representativityCriteriaName }}
      </h3>

      <div class="three-columns-grid is-tight-grid">
        <OneRepresentativityRuleByChoice
          v-for="(responseChoice) in representativity.countByResponseChoice"
          :key="responseChoice.responseChoiceId"
          :choice="responseChoice"
          :representativity="representativity"
        />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import {PropType} from "vue"
import OneRepresentativityRuleByChoice from "~/components/assessment/OneRepresentativityRuleByChoice.vue"

const props = defineProps({
  assessment: {type: Object as PropType<Assessment>, required: true},
})

</script>

<style scoped lang="sass">
.is-tight-grid
  grid-column-gap: 1rem

.three-columns-grid
  display: grid
  grid-template-columns: 1fr 1fr 1fr
</style>
