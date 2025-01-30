<template>
  <header
    class="header-fixed"
    fixed="top"
  >
    <nav
      class="navbar has-background-shade-600"
      role="navigation"
      aria-label="main navigation"
    >
      <div class="navbar-brand">
        <NuxtLink
          class="navbar-item"
          to="/"
        >
          <HeaderLogo :active-pillar-name="activePillar" />
        </NuxtLink>
        <a
          role="button"
          class="navbar-burger has-background-shade-600"
          aria-label="menu"
          aria-expanded="false"
          data-target="navbarMenu"
          :class="isBurgerOpen ? 'is-active' : ''"
          @click="closeMenu"
        >
          <span
            aria-hidden="true"
            class="has-text-white"
          />
          <span
            aria-hidden="true"
            class="has-text-white"
          />
          <span
            aria-hidden="true"
            class="has-text-white"
          />
        </a>
      </div>

      <div
        id="navbarMenu"
        class="navbar-menu navbar-menu-mobile"
        :class="isBurgerOpen && 'is-active'"
      >
        <div class="navbar-start px-1 navbar-items">
          <NuxtLink
            v-for="(item, index) of navItems"
            :key="index"
            :to="item.to"
            :class="
              isRouteActive(item.to)
                ? 'is-active navbar-item-active'
                : 'navbar-item-inactive'
            "
            class="navbar-item"
            @click="closeMenu"
          >
            {{ item.name }}
          </NuxtLink>
        </div>

        <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
              <!-- button to toggle locale between fr and en -->
              <HeaderLocaleSwitcher />
              <NuxtLink
                v-if="!isEvaluationRoute && assessmentStore.userHasNoAssessment"
                to="/evaluation/localisation"
                class="button evaluation is-rounded has-border-cooperation has-text-cooperation-dark"
                @click="closeMenu"
              >
                {{ $t("Lancer une évaluation") }}
              </NuxtLink>
              <NuxtLink
                v-if="!isEvaluationRoute && assessmentStore.userHasSingleAssessment"
                :to="userStep.url"
                class="button evaluation is-rounded has-border-cooperation has-text-cooperation-dark"
                @click="closeMenu"
              >
                {{ userStep.text }}
              </NuxtLink>
              <button
                v-if="isEvaluationRoute && userStore.isUnknownUser"
                class="button save is-rounded is-shade-600 is-outlined"
                @click="
                  () => {
                    participationStore.setShowSaveParticipationModal(true)
                    closeMenu()
                  }
                "
              >
                {{ $t("Enregistrer") }}
              </button>
              <NuxtLink
                v-if="userStore.isLoggedIn"
                to="/compte"
                class="button is-white is-rounded"
                @click="closeMenu"
              >
                {{ $t("Mon compte") }}
              </NuxtLink>
              <NuxtLink
                v-else
                to="/login"
                class="button is-white is-outlined is-rounded"
                @click="closeMenu"
              >
                {{ $t("Se connecter") }}
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <div
      v-if="isQuestionnaireRoute"
      class="is-flex navbar-progress-bar-wrapper"
      :class="{ 'is-unknown-user': userStore.isUnknownUser }"
    >
      <QuestionnaireProgressBars
        class="navbar-progress-bar"
        :header="true"
      />
      <div
        v-if="userStore.isUnknownUser"
        class="navbar-progress-bar-save"
      >
        <button
          class="column button is-shade-200 navbar-progress-bar-save-button"
          @click="participationStore.setShowCancelParticipationModal(true)"
        >
          <span>{{ $t("Réinitialiser") }}</span>
          <span class="icon">
            <icon
              size="15"
              name="restart"
            />
          </span>
        </button>
      </div>
    </div>
    <HeaderLine
      v-else
      :active-pillar-name="activePillar"
    />
  </header>
</template>

<script setup lang="ts">
import { useUserStore } from "~/stores/userStore"
import { useParticipationStore } from "~/stores/participationStore"
import { useAssessmentStore } from "~/stores/assessmentStore"
import { isQuestionnaireRouteFromPath } from "~/utils/util"
import { useI18n } from "vue-i18n"

const emit = defineEmits<{
  (e: "change-header-height", value: number): void
}>()

const i18n = useI18n()
const route = useRoute()
const $t = i18n.t
// global locale value is defined here, for some reason it didn´t work in plugins
i18n.locale.value = useLocale()
watch(route, () => {
  i18n.locale.value = useLocale()
})

const userStore = useUserStore()
const userStep = useUserStep()
const participationStore = useParticipationStore()
const assessmentStore = useAssessmentStore()
const isBurgerOpen = ref(false)

const isRouteActive = computed(() => (path) => {
  return route.path === path
})

const isEvaluationRoute = computed(() => {
  return route.path.includes("evaluation")
})

const isQuestionnaireRoute = computed(() => {
  const isQuestionnaireRoute = isQuestionnaireRouteFromPath(route.path)
  emit("change-header-height", isQuestionnaireRoute ? 125 : 75)
  return isQuestionnaireRoute
})

const activePillar = computed(() => {
  return route.query.pillar || ""
})

const navItems = [
  {
    name: $t("Accueil"),
    to: "/",
  },
  {
    name: $t("DémoMètre"),
    to: "/demometre",
  },
  {
    name: $t("Utilisations possibles"),
    to: "/utilisations-possibles",
  },
  {
    name: $t("Résultats"),
    to: "/resultats",
  },
  {
    name: $t("Le projet"),
    to: "/projet",
  },
]

function closeMenu() {
  isBurgerOpen.value = !isBurgerOpen.value
}
</script>

<style scoped lang="sass">
.header-fixed
  left: 0
  position: fixed
  right: 0
  top: 0
  z-index: 30

.button.evaluation:hover
  background: $cooperation

.button.save
  background: white

  &:hover
    background: $shade-600
    border-color: white

  &:focus
    background: $shade-600
    border-color: white

.navbar-progress-bar-wrapper
  $navbar-progress-bar-save-button-width: 180px
  width: 100%

  &.is-unknown-user
    .navbar-progress-bar
      width: calc(100% - #{$navbar-progress-bar-save-button-width})

  .navbar-progress-bar
    width: 100%

  .navbar-progress-bar-save
    display: flex
    flex-direction: column

  .navbar-progress-bar-save-button
    flex-grow: 1
    width: $navbar-progress-bar-save-button-width

.button .icon
  vertical-align: middle

.navbar-item-active
  color: $shade-600 !important

@include desktop
  .navbar-items
    border-radius: 1000px
    margin: 14px 24px
    background-color: white
  .navbar-item-inactive
    color: $shade-400

    &:hover
      color: $shade-500

@include touch
  .navbar-menu-mobile
    background-color: $shade-600
  .navbar-item-inactive
    color: $shade-200

    &:hover
      color: $shade-500

@include until-widescreen
  .navbar-progress-bar-wrapper
    $navbar-progress-bar-save-button-width: 50px

    &.is-unknown-user
      .navbar-progress-bar
        width: calc(100% - #{$navbar-progress-bar-save-button-width})

    .navbar-progress-bar-save-button
      width: $navbar-progress-bar-save-button-width

      .icon
        display: flex
        align-items: center
        justify-content: center
        margin-left: 0

      span:not(.icon)
        display: none

@include widescreen
  .navbar
    padding: 0 35px

@include fullhd
  .navbar
    padding: 0 70px
</style>
