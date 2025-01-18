<template>
  <footer class="footer has-background-shade-600">
    <div class="container">
      <div class="columns">
        <div class="column footer-column is-3">
          <NuxtLink
            to="/"
            class="has-text-weight-bold has-text-shade-200"
          >
            {{ $t("DémoMètre") }}
          </NuxtLink>
          <a
            class="has-text-shade-350"
            :href="MEDIA_BASE_URL + settingStore.rgpdSettings.contentLicenseUrl"
            target="_blank"
          >
            <!-- TODO : Put the right year automaticaly -->
            {{ $t("Licence") }}
          </a>
          <a
            class="has-text-shade-350"
            :href="MEDIA_BASE_URL + settingStore.rgpdSettings.termsOfUseUrl"
            target="_blank"
          >{{ $t("Conditions générales d'utilisation") }}</a>
          <a
            class="has-text-shade-350"
            :href="MEDIA_BASE_URL + settingStore.rgpdSettings.termsOfSaleUrl"
            target="_blank"
          >{{ $t("Conditions générales de vente") }}</a>
          <a
            class="has-text-shade-350"
            :href="MEDIA_BASE_URL + settingStore.rgpdSettings.legalMentionUrl"
            target="_blank"
          >{{ $t("Mentions légales") }}</a>
          <a
            class="has-text-shade-350"
            :href="
              MEDIA_BASE_URL +
                settingStore.rgpdSettings.confidentialityPolicyUrl
            "
            target="_blank"
          >{{ $t("Politique de confidentialité") }}</a>
        </div>
        <div class="column footer-column is-3">
          <NuxtLink
            to="/demometre"
            class="has-text-white"
          >
            {{ $t("DémoMètre") }}
          </NuxtLink>
          <NuxtLink
            to="/utilisations-possibles"
            class="has-text-white"
          >
            {{ $t("Utilisations possibles") }}
          </NuxtLink>
          <NuxtLink
            to="/resultats"
            class="has-text-white"
          >
            {{ $t("Résultats") }}
          </NuxtLink>
          <NuxtLink
            to="/projet"
            class="has-text-white"
          >
            {{ $t("Le projet") }}
          </NuxtLink>
        </div>
        <div class="column footer-column is-3">
          <NuxtLink
            to="/blog"
            class="has-text-white"
          >
            {{ $t("Blog") }}
          </NuxtLink>
          <NuxtLink
            to="/ressources"
            class="has-text-white"
          >
            {{ $t("Ressources") }}
          </NuxtLink>
          <NuxtLink
            to="/faq"
            class="has-text-white"
          >
            {{ $t("FAQ") }}
          </NuxtLink>
        </div>
        <div class="column footer-column is-3">
          <a
            class="has-text-shade-200"
            href="https://praticable.fr/"
            target="_blank"
          >
            {{ $t(`Designé par`) }} <b>Praticable</b>
          </a>
          <a
            class="has-text-shade-200"
            href="https://www.telescoop.fr/"
            target="_blank"
          >
            {{ $t(`Réalisé par`) }} <b>TelesCoop</b>
          </a>

          <!-- <label class="label is-size-7" for="email"
            >Lettre d'information</label
          >
          <div class="field has-addons">
            <div class="control">
              <input
                id="email"
                v-model="email"
                class="input is-small"
                type="text"
                placeholder="prenom@laposte.fr"
              />
            </div>
            <div class="control">
              <button type="button" class="button is-info is-small">
                Je m'abonne
              </button>
            </div>
          </div>-->
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { MEDIA_BASE_URL } from "~/composables/api"
import { useSettingStore } from "~/stores/settingStore"

// const email = ref("")
const settingStore = useSettingStore()
</script>

<style scoped lang="sass">
.footer-column
  display: flex
  flex-direction: column

  & a
    color: black
    font-weight: 400
    font-size: 0.75rem !important

  & a + a
    margin-top: 8px

.footer
  padding: 4rem
  margin-top: 4rem
  @include mobile
    margin-top: 2rem
    padding: 1rem
</style>
