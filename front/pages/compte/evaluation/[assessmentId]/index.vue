<template>
  <div
    class="container"
  >
    <div class="mb-2">
      <NuxtLink
        class="button is-white is-rounded"
        to="/compte"
      >
        <span class="icon">
          <icon
            size="20"
            name="arrow-left-line"
          />
        </span>
        <span> {{ $t("Revenir à mon compte") }} </span>
      </NuxtLink>
    </div>
    <div class="is-flex is-justify-content-space-between is-align-items-center">
      <h1 class="title is-1">
        {{ assessment?.name }}
      </h1>
      <div>
        <span
          v-if="assessment.isCurrent"
          class="tag is-light is-medium"
        >
          <span>{{ $t("Évaluation en cours") }}</span>
          <icon
            size="20"
            name="loader-2-line"
            style="margin-left: 4px"
          />
        </span>
        <span
          v-else
          class="tag is-light is-info is-medium"
        ><span>{{ $t("Évaluation terminée") }}</span>
          <icon
            size="20"
            name="check"
            style="margin-left: 4px"
          />
        </span>
      </div>
    </div>

    <div>
      <hr>
      <PageSection
        v-if="assessment"
        title="Informations"
        :buttons="informationsButtons"
        @button-click="onInformationButtonClick"
      >
        <div
          v-if="assessment.details.hasDetailAccess"
          style="margin-top: -32px; margin-bottom: 32px"
        >
          <span class="tag is-light is-medium">
            <template
              v-if="assessment.details.role! === 'initiator'"
            >{{ $t("Vous êtes à l'intiative de cette évaluation")
            }}</template>
            <template v-if="assessment.details.role === 'expert'">{{ $t("Vous êtes l'expert de cette évaluation")
            }}</template>
          </span>
        </div>
        <div
          class="is-flex is-flex-wrap-wrap"
          style="row-gap: 3rem; column-gap: 3rem"
        >
          <InformationDetail
            :title="$t(`type d'évaluation`)"
            :value="AssessmentType[assessment.assessmentType?.toUpperCase() || ''].value"
          />
          <InformationDetail
            :title="$t('lancée le')"
            :value="new Date(assessment.created).toLocaleDateString()"
          />
          <InformationDetail
            v-if="assessment.initializedToTheNameOf"
            :title="$t('par')"
            :value="assessment.initializedToTheNameOf"
          />
          <InformationDetail
            :title="$t('localité')"
            :value="assessment.collectivityName"
          />
          <InformationDetail
            :title="$t('Mon rôle')"
            :value="PARTICIPANT_TYPE[assessment.details.role]"
          />
          <InformationDetail
            v-if="!assessment.details.hasDetailAccess"
            :title="$t('participants hors ateliers')"
            :value="assessment.participationCount"
          />
          <InformationDetail
            :title="$t('ateliers')"
            :value="assessment.workshopCount"
          />
          <InformationDetail
            v-if="assessment.assessmentType === AssessmentType.WITH_EXPERT.key"
            :value="withExpertValue"
            :title="`${$t('Expert')}${(assessment.experts || []).length ? 's' : ''}`"
          />
          <template v-if="assessment.details.hasDetailAccess">
            <template v-for="(count, roleName) in assessment.participationCountPerRole" :key="roleName">
              <InformationDetail
                :value="count"
                :title="`${$t('Nb participants')} - ${roleName}`"
              />
            </template>
          </template>
        </div>
        <div
          v-if="assessment.details.hasDetailAccess"
          class="mt-3"
        >
          <div class="columns">
            <div class="column is-6-tablet">
              <InformationRichDetail
                :title="$t('Contexte')"
                :value="assessment.context"
              />
            </div>
            <div class="column is-6-tablet">
              <InformationRichDetail
                :title="$t('Objectifs')"
                :value="assessment.objectives"
              />
            </div>
          </div>
          <div class="columns">
            <div class="column is-6-tablet">
              <InformationRichDetail
                :title="$t('Parties prenantes')"
                :value="assessment.stakeholders"
              />
            </div>
            <div class="column is-6-tablet">
              <InformationRichDetail
                :title="$t('Calendrier')"
                :value="assessment.calendar"
              />
            </div>
          </div>
        </div>
      </PageSection>

      <div v-if="assessment.details.hasDetailAccess">
        <hr>
        <PageSection
          title="Documents"
          :buttons="[{ text: $t('Ajouter un document'), icon: 'add-line' }]"
          @button-click="showAddDocumentModal = true"
        >
          <div class="columns is-tablet is-variable is-6">
            <div
              v-for="category of ASSESSMENT_DOCUMENT_CATEGORIES"
              :key="category.value"
              class="column is-4-tablet"
            >
              <h3 class="has-text-shade-400 is-uppercase is-size-6 mb-0_5">
                {{ category.label }}
              </h3>
              <AssessmentDocument
                v-for="document of documentsForCategory(category.value)"
                :key="document.id"
                :document="document"
                :assessment-id="assessmentId"
                class="mb-1"
              />
              <div
                v-if="!documentsForCategory(category.value).length"
                class="message is-small"
              >
                <div class="message-body">
                  <p>{{ $t("Aucun document dans cette catégorie.") }}</p>
                </div>
              </div>
            </div>
          </div>
        </PageSection>
      </div>

      <hr>
      <section class="section">
        <div class="is-flex is-justify-content-space-between">
          <div>
            <h2 class="title is-3 has-text-shade-900 mb-1">
              {{ $t("État de l'évaluation") }}
            </h2>
            <p
              v-if="participationStore.status.participated"
              class="is-size-5"
            >
              {{ $t("Nombre de questions répondues :") }}
              {{ participationStore.status.answered }} /
              {{ participationStore.status.total }}
            </p>
            <div
              v-else
              class="message mb-2"
            >
              <div class="message-body">
                {{ $t("Vous n'avez pas participé à cette évaluation.") }}
              </div>
            </div>
          </div>
          <div>
            <NuxtLink
              v-if="assessment.details.hasDetailAccess && !assessment.endDate"
              class="button is-rounded is-dark"
              @click="confirmCloseAssessment"
            >
              <span>{{ $t("Clôturer l'évaluation") }}</span>
              <span class="icon"><icon
                size="20"
                name="check"
              /></span>
            </NuxtLink>
            <NuxtLink
              v-if="!assessment.endDate"
              :to="userStep.url"
              class="button is-rounded is-dark ml-1"
            >
              <span>{{
                participationStore.status.participated
                  ? $t("Reprendre l'évaluation")
                  : $t("Participer à l'évaluation")
              }}</span>
              <span class="icon"><icon
                size="20"
                name="arrow-right-line"
              /></span>
            </NuxtLink>
            <NuxtLink
              :to="`/resultats/${assessmentId}`"
              class="button is-rounded ml-1"
            >
              <span>{{ $t("Voir les résultats") }}</span>
              <span class="icon"><icon
                size="20"
                name="bar-chart-line"
              /></span>
            </NuxtLink>
          </div>
        </div>
        <div>
          <QuestionnaireProgressBars
            v-if="participationStore.status.participated"
            class="mb-3"
          />
          <ParticipationBoard :assessment="assessmentStore.currentAssessment" />
        </div>
      </section>
    </div>

    <hr>

    <AssessmentWorkshops
      v-if="assessment.details.hasDetailAccess"
      :assessment="assessment"
    />

    <div v-if="assessment.details.hasDetailAccess">
      <hr>
      <PageSection :title="$t('État de paiement de la redevance')">
        <template v-if="assessment.details.paymentDate">
          <div class="message">
            <div class="message-body p-3">
              <div class="columns is-tablet">
                <div class="column is-8">
                  <p class="title is-4 mb-0_5">
                    {{ $t("Paiement effectué") }}
                  </p>
                  <p>
                    {{ $t("L’expert a bien réglé le paiement de la commission d’utilisation du DémoMètre.") }}
                  </p>
                </div>
                <div class="column is-4">
                  <InformationDetail
                    :title="$t('Expert')"
                    :value="assessment.details.paymentAuthor"
                  />
                </div>
              </div>
            </div>
          </div>
        </template>
        <template v-else>
          <div class="message is-warning">
            <div class="message-body p-3">
              <p class="title is-4 mb-0_5">
                {{ $t("Paiement en attente") }}
              </p>
              <p>{{ $t("Le paiement n'a pas encore été effectué.") }}</p>
            </div>
          </div>
        </template>
      </PageSection>
    </div>

    <AssessmentInformationsEditModal
      v-if="showInformationsEditModal"
      :assessment="assessment"
      @close="showInformationsEditModal = false"
    />
    <AssessmentChangeExpertModal
      v-if="showExpertsEditModal"
      :assessment="assessment"
      @close="showExpertsEditModal = false"
    />
    <AssessmentAddDocumentModal
      v-if="showAddDocumentModal"
      :assessment-id="assessmentId"
      @close="showAddDocumentModal = false"
    />
  </div>
</template>

<script setup lang="ts">
import { useAssessmentStore } from "~/stores/assessmentStore"
import { useParticipationStore } from "~/stores/participationStore"
import {
  Assessment,
  AssessmentDocumentCategory,
  AssessmentDocumentType,
  AssessmentType,
} from "~/composables/types"
import {
  ASSESSMENT_DOCUMENT_CATEGORIES,
  PARTICIPANT_TYPE,
} from "~/utils/constants"
import { useConfirm } from "~/composables/useConfirm"
import { useI18n } from "vue-i18n"
import { useAssessmentIsReady } from "~/composables/useAssessmentIsReady"

definePageMeta({
  title: "Évaluation",
  breadcrumb: "Évaluation",
})

const assessmentStore = useAssessmentStore()
const participationStore = useParticipationStore()
const route = useRoute()
const userStep = useUserStep()
const confirm = useConfirm()

const i18n = useI18n()
const $t = i18n.t
const showInformationsEditModal = ref(false)
const showExpertsEditModal = ref(false)
const showAddDocumentModal = ref(false)

const assessmentIdStr: string = (route.params.assessmentId as string)
const assessmentId = parseInt(assessmentIdStr as string)
await useAssessmentIsReady()

onMounted(() => {
  participationStore.setTotalAndAnsweredQuestionsByPillarName()
})

assessmentStore.currentAssessmentId = assessmentId
const assessment = computed<Assessment>(
  () => assessmentStore.assessmentById[assessmentId],
)

const withExpertValue = computed(() => {
  const experts = assessment?.value.experts || []
  if (!experts.length) {
    return $t("Aucun expert pour le moment")
  } else {
    return experts
      .map((expert) => `${expert.firstName} ${expert.lastName}`)
      .join("\n")
  }
})

const documentsForCategory = computed(
  () => (category: AssessmentDocumentCategory) => {
    return assessment.value.documents.filter(
      (document: AssessmentDocumentType) => document.category === category,
    )
  },
)

const onInformationButtonClick = (buttonIx: number) => {
  if (buttonIx === 0) {
    showInformationsEditModal.value = true
  } else if (buttonIx === 1) {
    showExpertsEditModal.value = true
  }
}
const informationsButtons = computed(() => {
  if (!assessment.value.details.hasDetailAccess) {
    return []
  }
  const toReturn = [
    { text: $t("Modifier les informations"), icon: "list-settings-line" },
  ]
  if (
    assessment.value.details.role === "initiator" &&
    assessment.value.assessmentType === AssessmentType.WITH_EXPERT.key
  ) {
    toReturn.push({
      text: assessment.value.experts?.length
        ? $t("Changer d'expert")
        : $t("Ajouter un expert"),
      icon: "user-2-line",
    })
  }
  return toReturn
})
const confirmCloseAssessment = () => {
  confirm(
    $t("En clôturant l’évaluation, vous mettez fin à l’évaluation et n’autorisez plus de participation. Cette action est irréversible, n’oubliez pas de bien vérifier avant. Si vous êtes accompagnateur et que vous n'avez pas encore payé l'utilisation du DémoMètre pour cette évaluation, Démocratie Ouverte vous enverra une facture."),
    `${$t("Souhaitez-vous clôturer l'évaluation")} ${assessment.value.name} ?`,
    $t("Oui, clôturer l'évaluation"),
    () =>
      assessmentStore.saveAssessment(assessmentId, {
        endDate: new Date().toISOString().split("T")[0],
      }),
  )
}
</script>
