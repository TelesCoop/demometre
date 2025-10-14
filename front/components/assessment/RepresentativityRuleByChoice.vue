<template>
  <section>
    <h2 class="title is-3 mb-2">Configuration des seuils de représentativité</h2>
    <p class="block mb-2">
      {{ $t(`L'évaluation sera publique lorsque tous les seuils représentativité seront atteint, c'est à dire que pour chaque seuil, la proportion des participants ayant un profil qui correspond est supérieure au seuil.`)}}<br>
      {{ $t(`Si vous ne configurez pas les seuils, ceux par défaut du Démomètre seront utilisés (affichés en gris).`)}}<br>
      {{ $t(`Si vous ne voulez pas de seuil minimum pour une réponse, vous pouvez indiquer la valeur 0. Les seuils qui sont ignorés au niveau du Démomètre apparaissent en grisé et ne sont pas configurables.`)}}
    </p>
      <div v-for="representativity in props.assessment.representativities" :key="representativity.id" class="mb-2">
        <h3 class="title is-4 mb-1">{{ representativity.representativityCriteriaName }}</h3>

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
