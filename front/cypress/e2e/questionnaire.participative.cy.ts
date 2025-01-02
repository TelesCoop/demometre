describe('go through participative questionnaire', () => {
  it('fills the questionnaire', () => {
    cy.cleanData()
    cy.login("user1@telescoop.fr", "password")
    cy.wait(400)
    cy.startQuestionnaire('99902', 'participative')
    cy.fillObjectiveQuestions()
    cy.fillRole(0, 'Citoyen')
    cy.fillProfilingQuestions(1, 3)
    cy.fillRepresentationPillar()
    cy.checkQuestionnaireIsDone()
  })

  it('fills the questionnaire with another user, objective questions should be skipped ; conditional questions should be there', () => {
    // questionnaire with another user2 that should have two conditional questions
    // based on the profile
    cy.login("user2@telescoop.fr", "password")
    cy.wait(400)
    cy.startQuestionnaire('99902', 'participative', false)
    cy.fillRole(0, 'Citoyen')
    cy.fillProfilingQuestions(0, 35)
    cy.fillRepresentationPillar()
    // transparence Pillar now has two questions
    cy.getEl('rosette-start').click()
    cy.getEl('question-statement').contains('Question 1')
    cy.selectChoice(0)
    cy.submitQuestion()
    cy.getEl('question-statement').contains('Question 2')
    cy.selectChoice(1)
    cy.selectChoice(2)
    cy.submitQuestion()
    cy.checkQuestionnaireIsDone()
    cy.checkResultsAreAvailable('Ville test 2', false)
  })

  it('fills the questionnaire with a third user', () => {
    // questionnaire with another user3 that checks the third answer on
    // the first profiling question, results should then be available
    cy.login("user3@telescoop.fr", "password")
    cy.wait(400)
    cy.startQuestionnaire('99902', 'participative', false)
    cy.fillRole(0, 'Citoyen')
    cy.fillProfilingQuestions(2, 2)
    cy.fillRepresentationPillar()
    cy.checkQuestionnaireIsDone()
    cy.checkResultsAreAvailable('Ville test 2', true)
  })
})
