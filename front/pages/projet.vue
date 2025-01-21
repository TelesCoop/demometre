<template>
  <div>
    <PageIntro
      :title="pageStore.projectPage.title"
      :subtitle="pageStore.projectPage.tagLine"
      :introduction="pageStore.projectPage.introduction"
      :image-url="pageStore.projectPage.introImageUrl"
      class="pt-2"
    >
      <div class="is-flex buttons is-outlined is-shade-600">
        <button
          class="button is-rounded is-outlined is-shade-600 is-responsive"
          @click.prevent="scrollIntoWhyBlock"
        >
          <span>{{ $t("Pourquoi") }}</span>
          <span class="icon">
            <icon
              name="arrow-right-line"
              size="16"
              class="icon"
            />
          </span>
        </button>
        <button
          class="button is-rounded is-outlined is-shade-600 is-responsive"
          @click.prevent="scrollIntoWhoBlock"
        >
          <span>{{ $t("Avec qui") }}</span>
          <span class="icon">
            <icon
              name="arrow-right-line"
              size="16"
              class="icon"
            />
          </span>
        </button>
        <button
          class="button is-rounded is-outlined is-shade-600 is-responsive"
          @click.prevent="scrollIntoHowBlock"
        >
          <span>{{ $t("Méthode") }}</span>
          <span class="icon">
            <icon
              name="arrow-right-line"
              size="16"
              class="icon"
            />
          </span>
        </button>
      </div>
    </PageIntro>

    <!-- Why block -->
    <div
      ref="whyBlockRef"
      class="scroll-margin-top_5"
    >
      <PageBigSection
        :title="pageStore.projectPage.whyBlockTitle"
        :label="$t('Pourquoi')"
      >
        <div class="container">
          <section class="column-2 section">
            <PageFreeBody
              :free-body="pageStore.projectPage.whyBlockData"
              :inside-two-columns="true"
            />
          </section>
        </div>
        <div class="has-background-shade-250">
          <PageSection
            v-if="pageStore.projectPage.objectiveBlockTitle"
            :title="pageStore.projectPage.objectiveBlockTitle"
          >
            <div class="columns my-2">
              <div
                v-for="(objective, index) in pageStore.projectPage
                  .objectiveBlockData"
                :key="index"
                class="column is-one-quarter"
              >
                <div class="card is-fullheight has-background-white">
                  <div class="card-image">
                    <figure class="image is-4by3 has-text-centered">
                      <img
                        :src="MEDIA_BASE_URL + objective.svgUrl"
                        :alt="objective.title"
                        :style="`height: 100px; width: 100px`"
                        class="mt-2"
                      >
                    </figure>
                  </div>
                  <div class="card-content px-2 pb-2">
                    <p
                      class="is-size-5 has-text-shade-700 has-text-weight-bold has-text-centered"
                    >
                      {{ objective.title }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </PageSection>
          <PageSection
            v-if="pageStore.projectPage.impactBlockTitle"
            :title="pageStore.projectPage.impactBlockTitle"
          >
            <div class="columns my-2">
              <div
                v-for="(impact, index) in pageStore.projectPage.impactBlockData"
                :key="index"
                class="column is-one-third"
              >
                <div class="card is-fullheight has-background-white impact">
                  <div class="card-image">
                    <figure class="image has-text-centered">
                      <img
                        :src="MEDIA_BASE_URL + impact.imageUrl"
                        :alt="impact.title"
                        class="fit-without-distortion"
                      >
                    </figure>
                  </div>
                  <div class="card-content px-2 pb-2">
                    <p
                      class="is-size-4-tablet is-size-5-mobile has-text-shade-500 has-text-centered"
                    >
                      {{ impact.title }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </PageSection>
        </div>
      </PageBigSection>
    </div>

    <!-- Who block -->
    <div
      ref="whoBlockRef"
      class="scroll-margin-top_5"
    >
      <PageBigSection
        :title="pageStore.projectPage.whoBlockTitle"
        :label="$t('Avec qui')"
      >
        <PageSection
          v-if="pageStore.projectPage.whoCrewSubBlockTitle"
          :title="pageStore.projectPage.whoCrewSubBlockTitle"
        >
          <figure class="image">
            <img
              :src="
                MEDIA_BASE_URL + pageStore.projectPage.whoCrewSubBlockImageUrl
              "
              :alt="pageStore.projectPage.whoCrewSubBlockTitle"
              class="logo-open-democracy is-hidden-mobile"
            >
          </figure>
          <div class="columns is-mobile is-multiline">
            <div
              v-for="memberId in pageStore.projectPage.whoCrewSubBlockMemberIds"
              :key="memberId"
              class="column is-one-fifth-tablet is-half-mobile mb-1"
            >
              <PageMemberCard
                :persons="pageStore.projectPageMember(memberId)"
              />
            </div>
          </div>
        </PageSection>
        <PageSection
          v-if="pageStore.projectPage.whoCommitteeSubBlockTitle"
          :title="pageStore.projectPage.whoCommitteeSubBlockTitle"
        >
          <div class="my-2">
            <RichText
              class="is-family-secondary column-2 mb-2"
              :rich-text="pageStore.projectPage.whoCommitteeSubBlockDescription"
            />
            <div>
              <div class="tabs">
                <ul>
                  <li
                    v-for="tab of tabs"
                    :key="tab.id"
                    :class="
                      tab.id === currentTabId
                        ? 'is-active'
                        : `has-text-shade-500-hover`
                    "
                  >
                    <a
                      class="tab is-size-6 has-text-weight-bold has-text-shade-500"
                      @click="setTab(tab.id)"
                    >{{ tab.label }}</a>
                  </li>
                </ul>
              </div>
              <div
                v-for="(group_committees, index) in pageStore.projectPage
                  .whoCommitteeSubBlockData"
                :key="index"
              >
                <div
                  v-show="
                    currentTabId ===
                      group_committees.value.committee.replace(/\s+/g, '')
                  "
                  class="columns is-mobile is-multiline"
                >
                  <div
                    v-for="committee_member in group_committees.value
                      .committee_members"
                    :key="committee_member"
                    class="column is-half-mobile is-one-fifth-tablet mb-1"
                  >
                    <PageMemberCard
                      :persons="
                        pageStore.projectPageMember(committee_member.value)
                      "
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </PageSection>
        <PageSection
          v-if="pageStore.projectPage.whoPartnerSubBlockTitle"
          :title="pageStore.projectPage.whoPartnerSubBlockTitle"
        >
          <div class="my-2">
            <div
              v-for="(partner_group, index) in pageStore.projectPage
                .whoPartnerSubBlockData"
              :key="index"
            >
              <p class="is-size-4 has-text-black has-text-weight-bold pb-1">
                {{ partner_group.title }}
              </p>
              <div class="columns mb-3">
                <div class="column is-5 pr-4">
                  <p class="is-size-5 is-family-secondary has-text-shade-600">
                    {{ partner_group.description }}
                  </p>
                </div>
                <div class="column is-7">
                  <PagePartnerList
                    :partners="partner_group.partners"
                    :logo-height="60"
                    column-gap="3rem"
                    row-gap="2rem"
                  />
                </div>
              </div>
            </div>
          </div>
        </PageSection>
      </PageBigSection>
    </div>

    <!-- How block -->
    <div
      ref="howBlockRef"
      class="scroll-margin-top_5"
    >
      <PageBigSection
        :title="pageStore.projectPage.howBlockTitle"
        :label="$t('Comment')"
      >
        <div class="container">
          <PageFreeBody
            :free-body="pageStore.projectPage.howBlockData"
            :inside-two-columns="false"
            h-title="h3"
          />
        </div>
      </PageBigSection>
    </div>
  </div>
</template>

<script setup lang="ts">
import { CommitteeSubBlock } from "~/composables/types"
import { MEDIA_BASE_URL } from "~/composables/api"
import { usePageStore } from "~/stores/pageStore"

definePageMeta({
  title: "Le projet",
  breadcrumb: "Le projet",
})

const pageStore = usePageStore()
const route = useRoute()

if (!pageStore.projectPage.title) {
  pageStore.getProjectPage()
}

const howBlockRef = ref(null)
const whoBlockRef = ref(null)
const whyBlockRef = ref(null)

type tabDef = { label: string; id: string }
const tabs = ref<tabDef[]>([])
const committeeData = (pageStore.projectPage.whoCommitteeSubBlockData ||
  []) as CommitteeSubBlock[]
if (committeeData.length) {
  committeeData.forEach((element) => {
    tabs.value.push({
      label: `${element.value.committee}`,
      id: `${element.value.committee.replace(/\s+/g, "")}`,
    })
  })
}
const currentTabId = ref<string>(tabs.value[0]?.id)

function setTab(tabId) {
  currentTabId.value = tabId
}

onMounted(() => {
  howBlockRef.value.focus()
  whoBlockRef.value.focus()
  whyBlockRef.value.focus()
  if (route.query.hash === "howBlockRef") {
    scrollIntoHowBlock()
  }
})

const scrollIntoHowBlock = () => {
  howBlockRef.value.scrollIntoView({ behavior: "smooth" })
}
const scrollIntoWhoBlock = () => {
  whoBlockRef.value.scrollIntoView({ behavior: "smooth" })
}
const scrollIntoWhyBlock = () => {
  whyBlockRef.value.scrollIntoView({ behavior: "smooth" })
}
</script>

<style scoped lang="sass">
.buttons .button
  height: fit-content

.impact
  .image
    height: 240px
    width: 100%

@include mobile
  .impact
    .image
      height: 150px

.logo-open-democracy
  position: absolute
  top: 3rem
  right: 0
  max-height: 40px
</style>
