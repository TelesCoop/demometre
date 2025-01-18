module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
  },
  extends: ["@nuxt/eslint-config"],
  rules: {
    "vue/multi-word-component-names": "off",
    "vue/script-setup-no-uses-vars": "off",
    "@typescript-eslint/no-explicit-any": "off",
    indent: ["error", 2, { SwitchCase: 1 }],
    "comma-dangle": ["error", "always-multiline"],
    // "@stylistic/js/comma-dangle": ["error", "always-multiline"],
    semi: [2, "never"],
    "vue/max-attributes-per-line": ["error", {
      "singleline": {
        "max": 10,
      },
      "multiline": {
        "max": 1,
      },
    }],
  },
}
