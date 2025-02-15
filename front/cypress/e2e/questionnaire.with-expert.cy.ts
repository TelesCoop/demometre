describe('go through questionnaire with expert', () => {
  it('fills the questionnaire', () => {
    cy.cleanData()
    cy.login("user1@telescoop.fr", "password")
    cy.wait(400)
    cy.startQuestionnaire('99901', 'with_expert', true)
    cy.getEl('add-participative-process').eq(0).click()
    cy.getEl('participative-process-name').eq(0).type('Process participatif 1-1')
    cy.getEl('add-participative-process').eq(0).click()
    cy.getEl('participative-process-name').eq(1).type('Process participatif 1-2')
    cy.getEl('add-participative-process').eq(1).click()
    cy.getEl('participative-process-name').eq(2).type('Process participatif 2-1')
    cy.fillObjectiveQuestions()
    cy.fillRole(0, 'Citoyen')
    // additional choice for participative processes
    cy.fillProfilingQuestions(1, 3, 0)
    const question2ParticipativeProcessesAnswers = [
      {"name": "Process participatif 1-1", "choices": [0, 1]},
      {"name": "Process participatif 1-2", "choices": [1, 2]},
    ]
    cy.fillRepresentationPillar(question2ParticipativeProcessesAnswers)
    cy.checkQuestionnaireIsDone()
    cy.checkResultsAreAvailable('Ville test 1', false)

    // login as expert user and go through expert journey
    cy.login("expert@telescoop.fr", "password")
    cy.wait(400)
    cy.visit('/compte')
    cy.getEl('current-assessments-count').should('contain', '1')
    cy.getEl('assessment-row').eq(0).within(() => {
      cy.getEl('role').should('contain', 'expert ')
      cy.getEl('details').click()
    })

  })
})
