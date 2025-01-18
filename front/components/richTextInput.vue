<template>
  <div class="field">
    <label
      v-if="label"
      class="label"
      @click="editor.default.focus()"
    >
      <!-- @slot Slot pour personnaliser tout le contenu de la balise <label> -->
      <slot name="label">
        {{ label }}
        <!-- @slot Slot pour indiquer que le champ est obligatoire. Par défaut, met une astérisque si `required` est à true (dans un `<span class="required">`) -->
        <slot name="required-tip">
          <span
            v-if="$attrs.required"
            class="required"
          >&nbsp;*</span>
        </slot>
      </slot>
    </label>

    <div
      :id="id"
      class="input rich-input content"
      :class="{
        'is-danger': isInvalid,
      }"
      v-bind="$attrs"
    >
      <client-only>
        <div class="">
          <button
            v-for="(button, index) of toolbar"
            :key="index"
            class="button toolbar-button"
            :class="{ 'is-active': button.testActive() }"
            :title="button.title"
            @click="button.onClick"
          >
            <icon
              v-if="button.icon"
              :name="button.icon"
              size="16"
            />
            <span v-else>{{ button.text }}</span>
          </button>
        </div>
        <editor-content :editor="editor" />
      </client-only>
      <Teleport to="body">
        <div
          class="modal"
          :class="{ 'is-active': isAddingLink }"
        >
          <div
            class="modal-background"
            @click="emit('close')"
          />
          <div class="modal-content">
            <div class="modal-card-head">
              <h2 class="title is-2">
                {{ $t("Ajouter un lien") }}
              </h2>
            </div>
            <div class="modal-card-body">
              <div class="field">
                <label class="label">{{ $t("URL") }}</label>
                <div class="control">
                  <input
                    v-model="correctedLink"
                    class="input"
                    type="url"
                    placeholder="https://"
                  >
                </div>
              </div>
            </div>
            <footer class="modal-card-foot">
              <button
                class="button is-rounded is-dark"
                @click="onClick"
              >
                <span>{{ $t("Valider") }}</span>
                <span class="icon">
                  <icon
                    size="16"
                    name="check"
                  />
                </span>
              </button>
              <button
                class="button is-rounded is-outlined is-dark"
                @click="closeLinkModal"
              >
                {{ $t("Annuler") }}
              </button>
            </footer>
          </div>
        </div>
      </Teleport>
    </div>
    <p
      v-if="hint"
      class="help"
    >
      {{ hint }}
    </p>
  </div>
</template>

<script lang="ts" setup>
import { useEditor, EditorContent } from "@tiptap/vue-3"
import StarterKit from "@tiptap/starter-kit"
import Link from "@tiptap/extension-link"
import { mergeAttributes } from "@tiptap/core"
import { PropType } from "vue"
import { Level, Heading } from "@tiptap/extension-heading"
import {
  HeadingType,
  OtherRichTextActions,
  RichTextToolbar,
  RichTextToolbarItem,
  RichTextToolbarOptions,
} from "~/composables/types"
import { useLegacyModel } from "~/composables/modelWrapper"
import { generateRandomId } from "~/utils/util"
import { useI18n } from "vue-i18n"

const i18n = useI18n()
const $t = i18n.t

const props = defineProps({
  id: {
    type: String,
    default() {
      return generateRandomId()
    },
  },
  modelValue: { type: String, required: true },
  toolbarOptions: {
    type: Object as PropType<RichTextToolbarOptions>,
    default: () => {
      return {}
    },
  },
  isInvalid: Boolean,
  label: {
    type: String,
    default: "",
  },
  labelClass: {
    type: String,
    default: "",
  },
  hint: {
    type: String,
    default: "",
  },
})

const modelValueRef = useLegacyModel<string>("modelValue")
const editor = useEditor({
  content: modelValueRef.value,
  extensions: [
    StarterKit.configure({
      heading: false,
    }),
    Heading.configure({ levels: [1, 2, 3] }).extend({
      levels: [1, 2, 3],
      renderHTML({ node, HTMLAttributes }) {
        const level = this.options.levels.includes(node.attrs.level)
          ? node.attrs.level
          : this.options.levels[0]
        const classes = {
          1: "title is-2",
          2: "title is-3",
          3: "title is-4",
        }
        return [
          `h${level + 1}`,
          mergeAttributes(this.options.HTMLAttributes, HTMLAttributes, {
            class: `${classes[level]}`,
          }),
          0,
        ]
      },
    }),
    Link.configure({
      HTMLAttributes: {
        class: "no-append-ico",
      },
    }),
  ],
  onUpdate() {
    modelValueRef.value = editor.value!.getHTML()
  },
})
const testActiveHeading = (level: Level): boolean =>
  Boolean(editor.value?.isActive("heading", { level }))
const onClickHeading = (level: Level) =>
  editor.value?.chain().focus().toggleHeading({ level: level }).run()

const defaultToolbar = (): RichTextToolbar => [
  {
    name: HeadingType.H1,
    testActive: () => testActiveHeading(1),
    onClick: () => onClickHeading(1),
    icon: "",
    disabled: () => false,
    text: $t("titre 1"),
    title: $t("Titre de niveau 1"),
  },
  {
    name: HeadingType.H2,
    testActive: () => testActiveHeading(2),
    onClick: () => onClickHeading(2),
    icon: "",
    disabled: () => false,
    text: $t("titre 2"),
    title: $t("Titre de niveau 2"),
  },
  {
    name: HeadingType.H3,
    testActive: () => testActiveHeading(3),
    onClick: () => onClickHeading(3),
    icon: "",
    disabled: () => false,
    text: $t("titre 3"),
    title: $t("Titre de niveau 3"),
  },
  {
    name: OtherRichTextActions.BOLD,
    testActive: () => Boolean(editor.value?.isActive("bold")),
    onClick: () => editor.value!.chain().focus().toggleBold().run(),
    icon: "bold",
    disabled: () => false,
    title: $t("Text gras"),
  },
  {
    name: OtherRichTextActions.ITALIC,
    testActive: () => Boolean(editor.value?.isActive("italic")),
    onClick: () => editor.value?.chain().focus().toggleItalic().run(),
    icon: "italic",
    disabled: () => false,
    title: $t("Texte italique"),
  },
  {
    name: OtherRichTextActions.LIST_ORDERED,
    testActive: () => Boolean(editor.value?.isActive("orderedList")),
    onClick: () => editor.value?.chain().focus().toggleOrderedList().run(),
    icon: "list-ordered",
    disabled: () => false,
    title: $t("Liste numérotée"),
  },
  {
    name: OtherRichTextActions.LIST_UNORDERED,
    testActive: () => Boolean(editor.value?.isActive("bulletList")),
    onClick: () => editor.value?.chain().focus().toggleBulletList().run(),
    icon: "list-unordered",
    disabled: () => false,
    title: $t("Liste à puce"),
  },
  {
    name: OtherRichTextActions.LINK,
    testActive: () => Boolean(editor.value?.isActive("link")),
    onClick: () => openLinkModal(),
    icon: "link",
    disabled: () => false,
    title: $t("Créer un hyperlien"),
  },
  {
    name: OtherRichTextActions.LINK_UNLINK,
    testActive: () => !editor.value?.isActive("link"),
    onClick: () => editor.value?.chain().focus().unsetLink().run(),
    icon: "link-unlink",
    disabled: () => !editor.value?.isActive("link"),
    title: $t("Retirer l'hyperlien"),
  },
]

const toolbarOptionsStrategy = {
  show: {
    test(toolbarOptions: RichTextToolbarOptions): boolean {
      return Boolean(toolbarOptions.show)
    },
    run(toolbar: RichTextToolbar, toolbarOptions: RichTextToolbarOptions) {
      return toolbar.filter((toolbarItem: any) =>
        toolbarOptions.show!.includes(toolbarItem.name),
      )
    },
  },
  headingSwitch: {
    test(toolbarOptions: RichTextToolbarOptions): boolean {
      return Boolean(toolbarOptions.headingSwitch)
    },
    run(toolbar: RichTextToolbar, toolbarOptions: RichTextToolbarOptions) {
      return toolbar.map((toolbarItem: RichTextToolbarItem) => {
        if (!(toolbarItem.name in toolbarOptions.headingSwitch!)) {
          return toolbarItem
        }
        return {
          ...toolbarItem,
          testActive: () =>
            testActiveHeading(
              toolbarOptions.headingSwitch![toolbarItem.name as HeadingType]!,
            ),
          onClick: () =>
            onClickHeading(
              toolbarOptions.headingSwitch![toolbarItem.name as HeadingType]!,
            ),
        }
      })
    },
  },
}

const getToolbar = (toolbarOptions: RichTextToolbarOptions) => {
  let newToolbar = defaultToolbar()
  Object.values(toolbarOptionsStrategy)
    .filter((strategy: any) => strategy.test(toolbarOptions))
    .forEach((strategy: any) => {
      newToolbar = strategy.run(newToolbar, toolbarOptions)
    })
  return newToolbar
}

const toolbar = ref(getToolbar(props.toolbarOptions))

watch(
  () => modelValueRef.value,
  (value) => {
    const isSame = editor.value!.getHTML() === value
    if (isSame) return
    editor.value!.commands.setContent(value, false)
  },
)

watch(
  () => props.toolbarOptions,
  (value) => (toolbar.value = getToolbar(value)),
)

const isAddingLink = ref<boolean>(false)
const linkToAdd = ref<string>("")
const correctedLink = computed<string>({
  get() {
    return linkToAdd.value
  },
  set(value) {
    if (/^https?:\/\/.*/.test(linkToAdd.value)) return (linkToAdd.value = value)
    linkToAdd.value = `http://${value || ""}`
  },
})

function openLinkModal() {
  if (!editor.value) return

  const previousUrl = editor.value.getAttributes("link").href
  correctedLink.value = previousUrl
  isAddingLink.value = true
}

function closeLinkModal() {
  correctedLink.value = ""
  isAddingLink.value = false
}

function setLink() {
  if (!editor.value) return

  // empty
  if (correctedLink.value === "") {
    editor.value.chain().focus().extendMarkRange("link").unsetLink().run()
    return
  }

  // update link
  editor.value
    .chain()
    .focus()
    .extendMarkRange("link")
    .setLink({ href: correctedLink.value })
    .run()
}

const onClick = () => {
  setLink()
  closeLinkModal()
}

onBeforeUnmount(() => editor.value!.destroy())
</script>

<style lang="sass" scoped>
button:not(:disabled).is-active
  background-color: $shade-300

.rich-input
  display: block
  height: auto

.toolbar-button
  padding: 2px 4px 0 4px
  height: 22px
  line-height: 28px
  font-size: 10px

.proseMirror
  padding-left: 2px
</style>
