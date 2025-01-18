import { defineStore } from "pinia"
import {
  AnimatorPage,
  Article,
  EvaluationInitiationPage,
  EvaluationQuestionnairePage,
  HomePage,
  ImportantPages,
  ParticipationBoardPage,
  ProjectPage,
  ReferentialPage,
  ResultsPage,
  UsagePage,
} from "~/composables/types"
import { useApiGet } from "~~/composables/api"
import {
  getStreamFieldListStructMediaWithUrl,
  getStreamFieldMediaWithUrl,
  getStreamFieldStructMediaWithUrl,
  getStreamFieldStructWithLinkedObject,
  getStreamFieldStructWithListLinkedObjects,
} from "~/utils/streamFields"
import { useMessageStore } from "./messageStore"

export const usePageStore = defineStore("page", {
  state: () => ({
    homePage: <HomePage>{},
    blogPostsBySlug: <Record<string, Article>>{},
    resources: <Article[]>[],
    blogLoaded: <boolean>false,
    resourcesLoaded: <boolean>false,
    referentialPage: <ReferentialPage>{},
    participationBoardPage: <ParticipationBoardPage>{},
    resultsPage: <ResultsPage>{},
    usagePage: <UsagePage>{},
    projectPage: <ProjectPage>{},
    evaluationInitiationPage: <EvaluationInitiationPage>{},
    evaluationQuestionnairePage: <EvaluationQuestionnairePage>{},
    animatorPage: <AnimatorPage>{},
    importantPages: <ImportantPages>{},
  }),
  getters: {
    projectPageMember: (state) => {
      return (memberId: number) =>
        state.projectPage.persons.find((person) => person.id === memberId)
    },
    blogPosts: (state) => Object.values(state.blogPostsBySlug),
  },
  actions: {
    setBlogPosts(blogPostsList: Article[]) {
      const blogPosts: Record<string, Article> = {}
      for (const post of blogPostsList) {
        blogPosts[post.slug] = post
      }
      this.blogPostsBySlug = blogPosts
    },
    async getHomePage() {
      const { data, error } = await useApiGet<HomePage[]>("home-pages/")
      if (!error.value) {
        if (data.value?.length) {
          const homePageData = data.value[0]
          this.setBlogPosts(homePageData.blogPosts)
          this.resources = homePageData.resources
          this.homePage = homePageData
        } else {
          console.error("Impossible to retrieve home page")
        }
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
    async getBlogPosts() {
      const { data, error } = await useApiGet<Article[]>("blog-posts/")
      if (!error.value && data.value) {
        this.setBlogPosts(data.value)
        this.blogLoaded = true
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error!.value.data?.messageCode)
      }
    },
    async getBlogPost(slug: string) {
      const { data, error } = await useApiGet<Article>(`blog-posts/by-slug/${slug}`)
      if (!error.value && data.value) {
        const post: Article = data.value
        this.blogPostsBySlug[post.slug] = slug
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error!.value.data?.messageCode)
      }
    },
    async getResources() {
      const { data, error } = await useApiGet<Article[]>("resources/")
      if (!error.value) {
        this.resources = data.value
        this.resourcesLoaded = true
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
    async getReferentialPage() {
      const { data, error } = await useApiGet<ReferentialPage[]>(
        "referential-pages/",
      )
      if (!error.value) {
        if (data.value.length) {
          this.referentialPage = data.value[0]
        } else {
          console.error("Impossible to retrieve referential page")
        }
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
    async getParticipationBoardPage() {
      const { data, error } = await useApiGet<ParticipationBoardPage[]>(
        "participation-board-pages/",
      )
      if (!error.value) {
        if (data.value.length) {
          this.participationBoardPage = data.value[0]
        } else {
          console.error("Impossible to retrieve participation board page")
        }
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
    async getResultsPage() {
      const { data, error } = await useApiGet<ResultsPage[]>("results-pages/")
      if (!error.value) {
        if (data.value.length) {
          this.resultsPage = data.value[0]
        } else {
          console.error("Impossible to retrieve results page")
        }
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
    async getUsagePage() {
      const { data, error } = await useApiGet<UsagePage[]>("usage-pages/")
      if (!error.value) {
        if (data.value.length) {
          this.usagePage = data.value[0]
          // Treat json data sent in string
          this.usagePage.stepsOfUse = getStreamFieldStructMediaWithUrl(
            this.usagePage.stepsOfUse,
            "image",
            this.usagePage.stepsImagesUrl,
          )
          this.usagePage.startAssessmentBlockData =
            getStreamFieldStructWithLinkedObject(
              this.usagePage.startAssessmentBlockData,
              "type",
              this.usagePage.assessmentTypesDetails,
              "assessmentType",
            )
          // NB : to improve (fine enough for now) : eval function do not transform to camelCase, so we have pdf_button instead of pdfButton
        } else {
          console.error("Impossible to retrieve usage page")
        }
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
    async getProjectPage() {
      const { data, error } = await useApiGet<ProjectPage[]>("project-pages/")
      if (!error.value) {
        if (data.value.length) {
          this.projectPage = data.value[0]
          this.projectPage.whyBlockData = getStreamFieldMediaWithUrl(
            this.projectPage.whyBlockData,
            "image",
            this.projectPage.imagesUrl,
          )
          this.projectPage.objectiveBlockData =
            getStreamFieldStructMediaWithUrl(
              this.projectPage.objectiveBlockData,
              "svg",
              this.projectPage.svgsUrl,
            )
          this.projectPage.impactBlockData = getStreamFieldStructMediaWithUrl(
            this.projectPage.impactBlockData,
            "image",
            this.projectPage.imagesUrl,
          )
          this.projectPage.whoCommitteeSubBlockData = JSON.parse(
            this.projectPage.whoCommitteeSubBlockData,
          )
          this.projectPage.whoPartnerSubBlockData =
            getStreamFieldStructWithListLinkedObjects(
              this.projectPage.whoPartnerSubBlockData,
              "partners",
              this.projectPage.partners,
              "id",
            )
          this.projectPage.howBlockData = getStreamFieldListStructMediaWithUrl(
            this.projectPage.howBlockData,
            "step",
            "svg",
            this.projectPage.svgsUrl,
          )
        } else {
          console.error("Impossible to retrieve usage page")
        }
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
    async getEvaluationInitiationPage() {
      const { data, error } = await useApiGet<EvaluationInitiationPage[]>(
        "evaluation-initiation-pages/",
      )
      if (!error.value) {
        if (data.value.length) {
          this.evaluationInitiationPage = data.value[0]
        } else {
          console.error("Impossible to retrieve evaluation initiation page")
        }
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
    async getEvaluationQuestionnairePage() {
      const { data, error } = await useApiGet<EvaluationQuestionnairePage[]>(
        "evaluation-questionnaire-pages/",
      )
      if (!error.value) {
        if (data.value.length) {
          this.evaluationQuestionnairePage = data.value[0]
        } else {
          console.error("Impossible to retrieve evaluation questionnaire page")
        }
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
    async getAnimatorPage() {
      const { data, error } = await useApiGet<AnimatorPage[]>("animator-pages/")
      if (!error.value) {
        if (data.value.length) {
          this.animatorPage = data.value[0]
        } else {
          console.error("Impossible to retrieve animator page")
        }
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
    async getImportantPages() {
      const { data, error } = await useApiGet<ImportantPages[]>(
        "important-pages-settings/",
      )
      if (!error.value) {
        this.importantPages = data.value[0]
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
  },
})
