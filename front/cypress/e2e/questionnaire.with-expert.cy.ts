describe('go through questionnaire with expert', () => {
  it('fills the questionnaire', () => {
    cy.cleanData()
    cy.login("user1@telescoop.fr", "password")
    cy.wait(400)
    cy.startQuestionnaire('99901', 'with_expert', true)
    cy.fillObjectiveQuestions()
    cy.fillRole(0, 'Citoyen')
    cy.fillProfilingQuestions(1, 3)
    cy.fillRepresentationPillar()
    cy.checkQuestionnaireIsDone()
    cy.checkResultsAreAvailable('Ville test 1', false)
  })
})
