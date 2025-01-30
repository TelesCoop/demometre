<template>
  <div class="container is-fluid">
    <form
      class="column is-one-third is-offset-one-third"
      action="/evaluation/localisation"
      @submit.prevent="onSubmit"
    >
      <h1 class="title is-3 has-text-black">
        {{ $t("Commencer une évaluation") }}
      </h1>
      <div class="buttons mt-4">
        <button class="button is-normal is-rounded">
          <span>{{ $t("Commencer") }}</span>
        </button>
        <span class="is-size-7 is-hidden-mobile">
          {{ $t("appuyez sur Entrer ⏎") }}
        </span>

        <!-- Permet d'appuyer sur entrer -->
        <input
          type="submit"
          hidden
        >
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  title: "Évaluation",
  breadcrumb: "Évaluation",
  step: "localisation",
})

function onSubmit() {
  useRouter().push("/evaluation/localisation")
}
</script>

<style scoped lang="sass"></style>
