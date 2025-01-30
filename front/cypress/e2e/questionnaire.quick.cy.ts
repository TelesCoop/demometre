describe('go through quick questionnaire', () => {
  it('fills the questionnaire and checks results', () => {
    cy.cleanData()
    cy.login("user1@telescoop.fr", "password")
    cy.wait(400)

    cy.startQuestionnaire('99901', 'quick')
    cy.fillObjectiveQuestions()
    cy.fillRole(0, 'Citoyen')
    cy.fillProfilingQuestions(1, 3)
    cy.fillRepresentationPillar()
    cy.checkQuestionnaireIsDone()
    cy.checkResults('Ville test 1')

  })

  it('fills the questionnaire with conditions on the profile', () => {
    // questionnaire with another user2 that has two conditional questions
    // based on the profile
    cy.login("user2@telescoop.fr", "password")
    cy.wait(400)
    cy.startQuestionnaire('99901', 'quick')
    cy.fillObjectiveQuestions()
    cy.fillRole(0, 'Citoyen')
    // different profiling question answers
    // 0 because the first choice triggers the first conditional question
    // 35 because any number >= 30 triggers the second conditional question
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
    // questionnaire is done
    cy.checkQuestionnaireIsDone()
  })

  it('fills the questionnaire with conditions on the role', () => {
    // questionnaire with another user3 that has one conditional question
    // based on the role
    cy.login("user3@telescoop.fr", "password")
    cy.wait(400)
    cy.startQuestionnaire('99901', 'quick')
    cy.fillObjectiveQuestions()
    cy.fillRole(1, 'Élu')
    // different profiling question answers
    cy.fillProfilingQuestions(1, 3)
    cy.fillRepresentationPillar()
    // transparence Pillar now has one question
    cy.getEl('rosette-start').click()
    cy.getEl('question-statement').contains('Question 3')
    cy.selectChoice(0)
    cy.submitQuestion()
    // questionnaire is done
    cy.checkQuestionnaireIsDone()
  })
})
