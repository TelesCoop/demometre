<template>
  <div class="is-flex flex-center">
    <div class="sm-container">
      <div class="my-8 has-text-shade-800">
        <h1 class="title is-3 has-text-shade-600">
          {{ $t("Nous avons bien pris en compte votre demande") }}
        </h1>
        <p>{{ $t("Veuillez vérifier votre boîte mail et suivre les instructions.") }}</p>

        <NuxtLink
          to="/login"
          class="button is-shade-600"
        >
          {{ $t("Retourner à la connexion") }}
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>
