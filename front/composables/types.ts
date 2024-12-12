import { i18n } from "~/utils/i18n-util"

const $t = i18n.global.t

export type User = {
  email: string
  id: number | null
  isExpert: boolean
  isAdmin: boolean
  isUnknownUser: boolean
  username: string
}

// Questionnaire and profiling
export enum Objectivity {
  OBJECTIVE = "objective",
  SUBJECTIVE = "subjective",
}

export enum Method {
  QUANTITATIVE = "quantitative",
  QUALITATIVE = "qualitative",
}

export enum QuestionType {
  UNIQUE_CHOICE = "unique_choice",
  MULTIPLE_CHOICE = "multiple_choice",
  CLOSED_WITH_SCALE = "closed_with_scale",
  BOOLEAN = "boolean",
  PERCENTAGE = "percentage",
  NUMBER = "number",
}

export enum SurveyType {
  PROFILING = "profiling",
  QUESTIONNAIRE = "questionnaire",
  INITILIZATION = "initilization",
}

export enum PillarName {
  REPRESENTATION = "représentation",
  TRANSPARENCY = "transparence",
  PARTICIPATION = "participation",
  COOPERATION = "coopération",
}

export const PillarParams = {
  [PillarName.REPRESENTATION]: {
    key: "representation",
    color: "representation",
  },
  [PillarName.TRANSPARENCY]: {
    key: "transparency",
    color: "transparency",
  },
  [PillarName.PARTICIPATION]: {
    key: "participation",
    color: "participation",
  },
  [PillarName.COOPERATION]: {
    key: "cooperation",
    color: "cooperation",
  },
}
export const PILLARS_KEYS = Object.values(PillarParams).map(
  (pillar) => pillar.key,
)

export type Survey = {
  id: number
  name: string
  surveyType: SurveyType
  surveyLocality: SurveyLocality
  pillars: FullPillar[]
  questions: number[]
}
export type PillarType = {
  id: number
  code: string
  name: PillarName
  description: string
  markerIds: number[]
  surveyId: number
}
export type FullPillar = PillarType & { markers: FullMarkers[] }
export type Marker = {
  id: number
  pillarId: number
  pillarName: PillarName
  concatenatedCode: string
  name: string
  criteriaIds: number[]
  description: string
  score1: string
  score2: string
  score3: string
  score4: string
}
export type FullMarkers = Marker & { criterias: Criteria[] }
export type Criteria = {
  id: number
  markerId: number
  concatenatedCode: string
  name: string
  questionIds: number[]
  thematicTags: number[]
  description: string
  definitionIds: number[]
  explanatory: string | SimpleBlock[]
}
export type ResponseChoice = {
  id: number
  responseChoice: string
  description: string
}

export type Rule = {
  id: number
  type: string
  // Id de la question définissant la règle
  conditionalQuestionId: number

  // Type de réponse possible pour la rules
  responseChoiceIds: number
  numericalOperator: string
  numericalValue: number
  booleanResponse: boolean
}

export type ProfileType = {
  id: number
  name: string
  rulesIntersectionOperator: "and" | "or"
  rules: Rule[]
}

export type Question = {
  allowsToExplain: number
  assessmentTypes: string[]
  categories: Category[]
  code: string
  concatenatedCode: string
  criteriaId: number | null
  description: string
  explainsByQuestionIds: number[]
  id: number
  mandatory: boolean
  maxMultipleChoices: number | null
  maxNumberValue: number | null
  method: Method
  minNumberValue: number | null
  name: string
  objectivity: Objectivity
  pillarId: number | null
  pillarName: PillarName | null
  populationLowerBound: number | null
  populationUpperBound: number | null
  profileIds: number[]
  questionStatement: string
  responseChoices: ResponseChoice[]
  roleIds: number[]
  rules: Rule[]
  rulesIntersectionOperator: string
  stepNumberValue: number | null
  surveyId: number
  surveyLocality: SurveyLocality
  surveyType: SurveyType
  surveys: number[]
  type: QuestionType
}

export type QuestionBounds = { min: number; max: number }

export type Category = { id: number; category: string }

export type Role = {
  id: number
  name: string
  description: string
}

// Definition
export type Definition = {
  id: number
  word: string
  explanation: string
}

// Assessment
export const LOCALITY_TYPE: Record<string, { key: string; value: string }> = {
  MUNICIPALITY: { key: "municipality", value: $t("Commune") },
  INTERCOMMUNALITY: { key: "intercommunality", value: $t("Intercommunalité") },
  DEPARTMENT: { key: "department", value: $t("Département") },
  REGION: { key: "region", value: $t("Région") },
}
export type LocalityTypes =
  | "municipality"
  | "intercommunality"
  | "region"
  | "department"
export const LOCALITY_TYPES = Object.values(LOCALITY_TYPE).map((localityType) => localityType.key)
export type SurveyLocality = "city" | "region" | "department"
export const AssessmentType = {
  QUICK: { key: "quick", value: $t("Diagnostic rapide") },
  PARTICIPATIVE: { key: "participative", value: $t("Evaluation participative") },
  WITH_EXPERT: { key: "with_expert", value: $t("Evaluation avec expert") },
  "": { key: "", value: $t("Non renseigné") },
}
export type Locality = {
  id: number
  name: string
  population: number
  zip_codes: number[]
  localityType: LocalityTypes
}
export type Localities = {
  municipality: Locality[]
  intercommunality: Locality[]
  region: Locality[]
  department: Locality[]
}
type CountByResponseChoice = {
  responseChoiceName: string
  responseChoiceId: number
  total: number
  ignoreForAcceptabilityThreshold: boolean
}
export type RepresentativityCriteria = {
  id: number
  name: string
  profilingQuestionId: number
  acceptabilityThreshold: number
  minRate: number
  explanation: string
  surveyLocality: SurveyLocality
}
export type AssessmentRepresentativity = {
  id: number
  assessmentId: number
  representativityCriteriaName: string
  countByResponseChoice: CountByResponseChoice[]
  acceptabilityThresholdConsidered: number
  respected: boolean
}
export type AssessmentDetails = {
  calendar: string
  context: string
  hasDetailAccess: boolean
  objectives: string
  paymentAmount: number
  paymentAuthor: string
  paymentDate: string
  role: "initiator" | "expert" | "participant" | "" | null
  stakeholders: string
}
export type Expert = {
  email: string
  firstName: string
  lastName: string
  name: string
  username: string
}
export type Assessment = {
  assessmentType: string
  conditionsOfSaleConsent: boolean
  created: string
  code: string
  collectivityName: string
  details: AssessmentDetails
  documents: AssessmentDocumentType[]
  endDate: string
  epci: Locality | null
  experts?: Expert[]
  id: number
  initializationDate: string
  initializedToTheNameOf: string
  initiatedByUser: User
  initiatorType: string
  initiatorUsageConsent: boolean
  isCurrent: boolean
  isInitializationQuestionsCompleted: boolean
  municipality: Locality | null
  name: string
  participationCount: number
  publicInitiator: boolean
  publishedResults: boolean
  representativities: AssessmentRepresentativity[]
  surveyId: number
  surveyLocality: SurveyLocality
  surveyName: string
  workshopCount: number
}
export const InitiatorType = {
  COLLECTIVITY: { key: "collectivity", value: $t("Ma collectivité") },
  ASSOCIATION: { key: "association", value: $t("Une association") },
  INDIVIDUAL: { key: "individual", value: $t("Un particulier") },
  OTHER: { key: "other", value: $t("Autre") },
}
export type Scores = {
  byQuestionId: { [key: number]: number }
  byCriteriaId: { [key: number]: number }
  byMarkerId: { [key: number]: number }
  byPillarId: { [key: number]: number }
}
export type StrenghtsAndImprovements = {
  strengths: string[]
  improvements: string[]
}

// User participation
export type ParticipationPillarCompleted = {
  id: number | null
  completed: boolean
  pillarId: number
  participationId: number
}
export type Participation = {
  id: number | null
  assessmentId: number
  roleId: number
  consent: boolean
  isProfilingQuestionsCompleted: boolean
  isPillarQuestionsCompleted: ParticipationPillarCompleted[]
  profileIds: number[]
  isCurrent: boolean
}
export type ClosedWithScaleResponse = {
  id: number | null
  categoryId: number
  responseChoiceId: number | null
  participationResponseId: number | null
  assessmentResponseId: number | null
}

export type QuestionResponseValue = Partial<{
  uniqueChoiceResponseId: number | null
  multipleChoiceResponseIds: number[]
  booleanResponse: boolean | null
  percentageResponse: number | null
  numberResponse: number | null
  closedWithScaleResponseCategories: ClosedWithScaleResponse[]
}>
export type QuestionResponse = {
  id: number
  isDirty?: boolean
  participationId: number | null
  assessmentId: number | null
  questionId: number
  hasPassed: boolean
} & QuestionResponseValue

// Workshops
export type Workshop = {
  animatorId?: number
  assessmentId: number
  changed?: boolean
  closed?: boolean
  date: string
  id?: number
  name: string
  participationIds?: number[]
  place: string
  type: "assessment" | "results"
}
export type WorkshopParticipation = {
  assessmentId: number
  changed: boolean
  id: number
  medium: "paper" | "online"
  participantEmail: string
  participantName: string
  responseByQuestionId: { [key: number]: QuestionResponse }
  responses: QuestionResponse[]
  roleId: number
  workshopId?: number
}

// Pages
type Feedback = {
  id: number
  personName: string
  pictureUrl: string
  personContext: string
  quote: string
  externalLink: string
  publish: boolean
}
export type Block = {
  type: string
  id: string
  value: any
}
export type Article = {
  id: number
  title: string
  slug: string
  content: Block[]
  shortDescription: string
  publicationDate: string
  imageUrl: string
  externalLink: string
  pillars: number[]
}
type Partner = {
  id: number
  name: string
  logoImageUrl: string
  height: number
  showInHomePage: boolean
}
type Person = {
  id: number
  name: string
  imageUrl: string
  jobTitle: string
}
export type HomePage = {
  title: string
  introduction: string
  tagLine: string
  introImageUrl: string
  introYoutubeVideoId: string
  feedbackBlockTitle: string
  feedbackBlockIntro: string
  feedbacks: Feedback[]
  blogBlockTitle: string
  blogBlockIntro: string
  blogPosts: Article[]
  resourcesBlockTitle: string
  resourcesBlockIntro: string
  resources: Article[]
  partnerBlockTitle: string
  partnerBlockIntro: string
  partners: Partner[]
}
export type ReferentialPage = {
  title: string
  introduction: string
  rosetteLegend: string
  pillarBlockTitle: string
  pillarBlockLeftContent: string
  pillarBlockRightContent: string
  pillarBlockImageUrl: string
  pillarStructureLegend: string
  markerBlockTitle: string
  markerBlockContent: string
  criteriaBlockTitle: string
  criteriaBlockLeftContent: string
  criteriaBlockRightContent: string
}
export type ParticipationBoardPage = {
  title: string
}
export type ResultsPage = {
  title: string
  tagLine: string
  tagLineNoResults: string
  introduction: string
  introImageUrl: string
}

type ImageUrl = { id: number; url: string }
export type AssessmentTypeDetails = {
  id: number
  name: string
  assessmentType: string
  title: string
  forWho: string
  what: string
  forWhat: string
  results: string
  price: string
  pdfUrl: string
  pdf_button: string
}
type SimpleBlockWithImage = {
  image: number
  imageUrl: string
  title: string
  description: string
}
export type SimpleBlock = {
  title: string
  description: string
}
export type UsagePage = {
  assessmentTypesDetails: AssessmentTypeDetails[]
  introImageUrl: string
  introduction: string
  participateBlockIntro: string
  participateBlockTitle: string
  participateLeftParagraph: string
  participateRightParagraph: string
  startAssessmentBlockData: string | AssessmentTypeDetails[]
  startAssessmentBlockIntro: string
  startAssessmentBlockTitle: string
  stepOfUseIntro: string
  stepOfUseTitle: string
  stepsImagesUrl: ImageUrl[]
  stepsOfUse: string | SimpleBlockWithImage[]
  tagLine: string
  title: string
  trainingBlockIntro: string
  trainingBlockTitle: string
}
type ObjectiveBlock = {
  svg: number
  svgUrl: string
  title: string
}
type CommitteeMember = {
  id: string
  type: string
  value: number
}
type CommitteeSubBlockValue = {
  committee: string
  committeeMembers: CommitteeMember
}
export type CommitteeSubBlock = {
  id: string
  type: string
  value: CommitteeSubBlockValue
}
export type ProjectPage = {
  title: string
  introduction: string
  tagLine: string
  introImageUrl: string | null
  whyBlockTitle: string
  whyBlockData: string
  objectiveBlockTitle: string
  objectiveBlockData: string | ObjectiveBlock[]
  impactBlockTitle: string
  impactBlockData: string | SimpleBlockWithImage[]
  whoBlockTitle: string
  whoCrewSubBlockTitle: string
  whoCrewSubBlockImageUrl: ImageUrl
  whoCrewSubBlockMemberIds: number[]
  whoCommitteeSubBlockTitle: string
  whoCommitteeSubBlockDescription: string
  whoCommitteeSubBlockData: string | CommitteeSubBlock[]
  whoPartnerSubBlockTitle: string
  whoPartnerSubBlockData: string
  howBlockTitle: string
  howBlockData: string
  imagesUrl: ImageUrl[]
  svgsUrl: ImageUrl[]
  persons: Person[]
  partners: Partner[]
}
export type EvaluationInitiationPage = {
  searchAssessmentTitle: string
  searchAssessmentDescription: string
  searchAssessmentLocalityTypeQuestion: string
  searchAssessmentLocalityTypeDescription: string
  searchAssessmentZipCodeQuestion: string
  searchAssessmentZipCodeDescription: string
  searchAssessmentNoResult: string
  cguConsentTitle: string
  cguConsentDescriptionLoggedin: string
  cguConsentDescriptionLoggedout: string
  cgvConsentTitle: string
  cgvConsentDescription: string
  royaltyDescription: string
  noAssessmentTitle: string
  noAssessmentDescription: string
  oneQuickAssessmentTitle: string
  oneQuickAssessmentDescription: string
  oneAssessmentWithExpertTitle: string
  oneAssessmentWithExpertDescription: string
  oneParticipationAssessmentTitle: string
  oneParticipationAssessmentDescription: string
  addExpertTitle: string
  addExpertDescription: string
  addExpertButtonYes: string
  addExpertButtonNo: string
  dashboardTitle: string
  dashboardDescription: string
  mustBeConnectedToCreateTitle: string
  mustBeConnectedToCreateDescription: string
  createQuickAssessmentTitle: string
  createQuickAssessmentDescription: string
  createParticipationAssessmentTitle: string
  createParticipationAssessmentDescription: string
  createAssessmentWithExpertTitle: string
  createAssessmentWithExpertDescription: string
  chooseExpertText: string
  ifNoExpertText: string
  initTitle: string
  initDescription: string
  initiatorNameQuestion: string
  initiatorNameDescription: string
  representativityTitle: string
  representativityDescription: string
  objectiveQuestionsTitle: string
  objectiveQuestionsDescription: string
  objectiveQuestionsCallToAction: string
  initializationValidationTitle: string
  initializationValidationDescription: string
  initializationValidationCallToAction: string
}
export type EvaluationQuestionnairePage = {
  roleQuestionTitle: string
  roleQuestionDescription: string
  endOfProfilingTitle: string
  endOfProfilingDescription: string
  endOfProfilingCallToAction: string
  startTitle: string
  startText: string
  intermediateStepTitle: string
  intermediateStepTextLoggedIn: string
  intermediateStepTextLoggedOut: string
  isIntermediateStepTitleWithPillarNames: string
  finishedTitle: string
  finishedTextLoggedIn: string
  finishedTextLoggedOut: string
}
export type AnimatorPage = {
  listWorkshopsTitle: string
  listWorkshopIntro: string
  closeWorkshopValidation: string
  addParticipantsTitle: string
  addParticipantsIntro: string
  responsesTitle: string
  responsesIntro: string
}

type ContentPage = {
  title: string
  content: string
}

export type ImportantPages = {
  faqPage: ContentPage
}

// Props
export type QuestionContextProps = {
  journey: any
  questionById: { [key: number]: Question }
  responseByQuestionId: { [key: number]: QuestionResponse }
  hasPreviousStep: boolean
}

// Settings
export type RgpdSettings = {
  legalMentionUrl: string
  termsOfUseUrl: string
  termsOfSaleUrl: string
  confidentialityPolicyUrl: string
  contentLicenseUrl: string
}

export type StructureSettings = {
  email: string
}
export type SectionButton = {
  icon: string
  iconLeft?: boolean
  link?: string
  text: string
}

// rich text (TipTap)
export enum HeadingType {
  H1 = "h1",
  H2 = "h2",
  H3 = "h3",
  H4 = "h4",
  H5 = "h5",
  H6 = "h6",
}

export enum OtherRichTextActions {
  BOLD = "bold",
  ITALIC = "italic",
  LIST_ORDERED = "list-ordered",
  LIST_UNORDERED = "list-unordered",
  LINK = "link",
  LINK_UNLINK = "link",
}

type RichTextToolbarActions = HeadingType | OtherRichTextActions
export type RichTextToolbarHeadingSwitch = {
  [key in HeadingType]?: Level
}
export type RichTextToolbarOptions = {
  show?: RichTextToolbarActions[]
  headingSwitch?: RichTextToolbarHeadingSwitch
}
export type RichTextToolbarItem = {
  name: RichTextToolbarActions
  testActive: () => boolean
  onClick: () => void
  icon?: string
  disabled: () => boolean
  text?: string
  title: string
}
export type RichTextToolbar = RichTextToolbarItem[]
export type AssessmentDocumentCategory =
  | "assessment_reports"
  | "other"
  | "invoices"
export type AssessmentDocumentTypeFile = {
  link: string
  mimetype: string
  name: string
  size: string
}
export type AssessmentDocumentType = {
  assessment: number
  category: AssessmentDocumentCategory
  created: string
  file: AssessmentDocumentTypeFile
  id: number
  name: string
}
export type Training = {
  audience: string
  description: string
  duration: string
  id: number
  isAvailableSoon: boolean
  name: string
  url: string
}
