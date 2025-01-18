export const getDefaultAnswerValue = (categories) => {
  return categories.map((category) => {
    return { categoryId: category.id, responseChoiceId: null }
  })
}
