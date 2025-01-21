<template>
  <div class="container">
    <div class="section">
      <div class="is-flex is-justify-content-space-between">
        <h1 class="title is-size-1-desktop is-2 has-text-black">
          {{ $t("Mon compte") }}
        </h1>
        <div>
          <button
            class="button is-rounded"
            @click.prevent="logout"
          >
            {{ $t("Se déconnecter") }}
          </button>
        </div>
      </div>
      <div v-if="userStore.isAdminOrExpertUser">
        <router-link to="/export/questionnaire">
          <button class="button is-rounded">
            {{ $t("Générer un questionnaire papier en fonction d'un profil") }}
          </button>
        </router-link>
      </div>
    </div>
    <div
      v-if="userStore.isUnknownUser"
      class="section"
      style="margin-top: -64px"
    >
      <div class="message">
        <div class="message-body">
          {{ $t("Votre participation ne sera pas comptabilisée tant que vous n'êtes pas enregistré. Elle sera supprimée au bout d'un mois.")
          }}
        </div>
      </div>
      <div class="buttons is-flex-direction-column is-align-items-flex-start">
        <router-link
          class="button is-rounded is-primary mr-1 mb-1"
          to="/signup"
        >
          {{ $t("S'enregistrer pour conserver vos résultats") }}
        </router-link>
      </div>
    </div>
    <div>
      <hr>
      <PageSection
        :title="$t('Mes informations')"
        :buttons="[
          { text: $t('Modifier les informations'), icon: 'list-settings-line' },
        ]"
        @button-click="showEditUserInfoModal = true"
      >
        <div
          class="is-flex is-flex-wrap-wrap"
          style="row-gap: 1.5rem; column-gap: 3rem"
        >
          <InformationDetail
            title="Nom"
            :value="userStore.user.username"
          />
          <InformationDetail
            data-cy="account-email"
            title="mail"
            :value="userStore.user.email"
          />
        </div>
      </PageSection>
      <hr>
      <PageSection
        :title="$t('Mes évaluations')"
        :intro="$t('Toutes mes évaluations en cours et terminées')"
        :buttons="[{ text: $t('Lancer une évaluation'), icon: 'arrow-right-line' }]"
        @button-click="newAssessment"
      >
        <div class="tabs is-fullwidth">
          <ul>
            <li
              :class="isCurrentAssessmentsTab ? 'is-active' : null"
              @click="isCurrentAssessmentsTab = true"
            >
              <a>{{ $t("Évaluations en cours") }} (<span data-cy="current-assessments-count">{{ currentAssessments.length }}</span>)</a>
            </li>
            <li
              :class="isCurrentAssessmentsTab ? null : 'is-active'"
              @click="isCurrentAssessmentsTab = false"
            >
              <a>{{ $t("Évaluations terminées") }} ({{ finishedAssessments.length }})</a>
            </li>
          </ul>
        </div>
        <div>
          <article
            v-if="!selectedAssessments.length"
            class="message"
          >
            <div class="message-body">
              <p class="title is-5">
                {{ $t("Aucune évaluation") }}
                {{ isCurrentAssessmentsTab ? $t("en cours") : $t("terminée") }}
              </p>
              <p>
                <template v-if="isCurrentAssessmentsTab">
                  {{ $t("Vous n’avez aucune évaluation en cours avec le DémoMètre.") }}
                </template>
                <template v-else>
                  {{ $t("Vous n’avez aucune évaluation terminée avec le DémoMètre.") }}
                </template>
              </p>
              <p>
                {{ $t("Pour démarrer une évaluation, cliquer sur le bouton « Lancer une évaluation ».") }}
              </p>
            </div>
          </article>
          <table
            v-else
            class="table is-striped is-fullwidth"
          >
            <thead>
              <tr>
                <th>
                  {{ $t("Nom") }}
                </th>
                <th>{{ $t("Questionnaire") }}</th>
                <th>{{ $t("Date de création") }}</th>
                <th>
                  {{ $t("Rôle") }}
                </th>
                <th>{{ $t("Échelon") }}</th>
                <th>{{ $t("Localité") }}</th>
                <th>{{ $t("Pays") }}</th>
                <th>{{ $t("Actions") }}</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="assessment of selectedAssessments"
                :key="assessment.id"
                style="cursor: pointer"
                tabindex="0"
                title="Cliquer pour accéder aux détails"
                data-cy="assessment-row"
                @click="selectAssessment(assessment.id)"
              >
                <td data-cy="assessment-name">
                  {{ assessment.name }}
                </td>
                <td data-cy="survey-name">
                  {{ assessment.surveyName }}
                </td>
                <td>{{ new Date(assessment.created).toLocaleDateString() }}</td>
                <td data-cy="role">
                  {{ PARTICIPANT_TYPE[assessment.details.role] || $t("participant - non encore rempli") }}
                  <template v-if="assessment.details.hasDetailAccess">
                    <span
                      v-if="assessment.details.paymentAmount"
                      class="tag"
                    >{{ $t("Redevance payée") }}</span>
                    <span
                      v-else-if="assessment.details.role === 'expert'"
                      class="tag is-danger"
                    >{{ $t("Redevance impayée") }}</span>
                  </template>
                </td>
                <td>{{ LOCALITY_TYPE_NAME[assessment.localityType] }}</td>
                <td>{{ assessment.collectivityName }}</td>
                <td>France</td>
                <td data-cy="details">
                  <button class="button is-small is-rounded">
                    {{ $t("Détails") }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </PageSection>
    </div>
    <AccountEditUserInfoModal
      v-if="showEditUserInfoModal"
      @close="showEditUserInfoModal = false"
    />
  </div>
</template>

<script setup lang="ts">
import { useAssessmentStore } from "~/stores/assessmentStore"
import { useUserStore } from "~/stores/userStore"
import { LOCALITY_TYPE_NAME, PARTICIPANT_TYPE } from "~/utils/constants"
import { useParticipationStore } from "~/stores/participationStore"
import { Assessment } from "~/composables/types"

definePageMeta({
  title: "Mon compte",
  breadcrumb: "Mon compte",
})

const assessmentStore = useAssessmentStore()
const participationStore = useParticipationStore()
const userStore = useUserStore()
const router = useRouter()

const isCurrentAssessmentsTab = ref(true)
const showEditUserInfoModal = ref(false)

// there might be only one assessment fetched,
// there might be a new assessment since we last visited the page,
// we want to make sure we fetch all of them
onMounted(async () => {
  await assessmentStore.getAssessmentsForUser()
})

const currentAssessments = computed(() =>
  assessmentStore.myAssessments.filter((ass) => ass.isCurrent),
)
const finishedAssessments = computed(() =>
  assessmentStore.myAssessments.filter((ass) => !ass.isCurrent),
)
const selectedAssessments = computed<Assessment[]>(() =>
  isCurrentAssessmentsTab.value
    ? currentAssessments.value
    : finishedAssessments.value,
)

const selectAssessment = (assessmentId: number) => {
  router.push(`/compte/evaluation/${assessmentId}`)
}

const newAssessment = () => {
  assessmentStore.createNewAssessment()
  participationStore.newAssessment()
  router.push("/evaluation/localisation")
}

const logout = () => {
  userStore.logout()
}
</script>

<style scoped lang="sass"></style>
