Cypress.Commands.add("getEl", (selector, ...args) => {
  return cy.get(`[data-cy="${selector}"]`, ...args)
})

Cypress.Commands.add("cleanData", () => {
  cy.request('http://localhost:8000/api/e2e/clean-data')
})

Cypress.Commands.add("selectChoice", (answerIx) => {
  return cy.get('.response-choice').eq(answerIx).click()
})

Cypress.Commands.add("inputPercentage", (percentage ) => {
  return cy.getEl('percentage-input').type(percentage)
})

Cypress.Commands.add("inputNumber", (percentage) => {
  return cy.getEl('number-input').type(percentage)
})

Cypress.Commands.add("login", (email, password) => {
  cy.session([email, password], () => {
    cy.visit("/login")
    cy.wait(400)
    const el = cy.getEl("login-email")
    el.type(email)
    cy.getEl("login-password").focus().type(password, {
      force: true,
    })
    cy.getEl("login-submit").click()
    cy.wait(400)
  })
})

Cypress.Commands.add("selectCategory", (categoryName, value) => {
  cy.get(`[data-cy="response-choice-${categoryName}"] .slider-base`).as('slider')
  let width = 0
  cy.get('@slider').invoke('width').then(w => {
    width = w!
    cy.get('@slider').click(Math.round(value*width/4), 10)
  })
})

Cypress.Commands.add("submitQuestion", () => {
  cy.getEl('submit-button').click()
})

Cypress.Commands.add("startQuestionnaire", (cityCode, assessmentType, userIsInitiator=true) => {
  cy.visit("/evaluation/localisation")
  cy.wait(400)
  cy.getEl('zip-code').type(cityCode)
  cy.getEl('search').click()
  cy.getEl(`locality-municipality-${cityCode}`).click()
  cy.getEl('submit').click()
  if (userIsInitiator) {
    cy.getEl(`${assessmentType}-choose`).click()
    cy.getEl('initiator-cgu-consent').click()
    if (assessmentType === 'with_expert') {
      cy.getEl('cgv-consent').click()
      cy.getEl('expert-select').click()
      cy.get('.vs__dropdown-menu').click()
    }
    cy.getEl('consent-submit').click()
    cy.getEl('initiator-name').type('Mairie de la ville test')
    cy.getEl('initiator-type-collectivity').click()
    cy.getEl('initiator-submit').click()
  } else {
    cy.getEl(`${assessmentType}-choose`).should('not.exist')
    cy.getEl('cgu-consent').click()
    cy.getEl('start-participation').click()
    cy.getEl('participation-board-continue').click()
  }
})

Cypress.Commands.add("fillObjectiveQuestions", () => {
  cy.getEl('start-objective-questions').click()
  cy.getEl('question-statement').contains('Nombre de doigts')
  cy.inputNumber(5)
  cy.submitQuestion()
  cy.getEl('confirm-objective-questions').click()
  cy.getEl('start-participation').click()
  cy.getEl('participation-board-continue').click()
})

Cypress.Commands.add("fillRole", (roleIndex, roleName) => {
  cy.get('.response-choice').eq(roleIndex).contains(roleName)
  cy.selectChoice(roleIndex)
  cy.submitQuestion()
})

Cypress.Commands.add("fillProfilingQuestions", (firstQuestionChoice, secondQuestionValue) => {
  cy.getEl('question-statement').contains('Profiling Question Profile-1')
  cy.selectChoice(firstQuestionChoice)
  cy.submitQuestion()
  cy.getEl('question-statement').contains('Profiling Question Profile-2')
  cy.inputNumber(secondQuestionValue)
  cy.submitQuestion()
  cy.getEl('affinage-continue').click()
})

Cypress.Commands.add("fillRepresentationPillar", () => {
  cy.getEl('rosette-start').click()
  cy.getEl('question-statement').contains('Question 1')
  cy.selectChoice(0)
  cy.submitQuestion()
  cy.getEl('question-statement').contains('Question 2')
  cy.selectChoice(1)
  cy.selectChoice(2)
  cy.submitQuestion()
  cy.getEl('question-statement').contains('Question 3')
  cy.selectCategory('Catégorie 1', 3)
  cy.selectCategory('Catégorie 2', 4)
  cy.submitQuestion()
  cy.getEl('question-statement').contains('Question 4')
  cy.selectChoice(0)
  cy.submitQuestion()
  cy.getEl('question-statement').contains('Question 5')
  cy.inputPercentage(50)
  cy.submitQuestion()
  cy.getEl('question-statement').contains('Question 6')
  cy.inputNumber(7)
  cy.submitQuestion()
})

Cypress.Commands.add("checkQuestionnaireIsDone", () => {
  cy.url().should('match', /\/evaluation\/[a-z0-9-]+\/questionnaire$/)
  cy.getEl('rosette-start').should('not.exist')
})

Cypress.Commands.add("checkResultsAreAvailable", (cityName: string, available: boolean) => {
  cy.visit("/resultats")
  if (available) {
    cy.getEl('results-select').click()
    cy.getEl('results-select').should('contain', cityName)
  } else {
    cy.getEl('no-results').should('contain', 'Aucun résultat')
  }
})

Cypress.Commands.add("checkScore", (elementName, score) => {
  // its data-score attribute should be the score value
  cy.getEl(`${elementName}-score`).should('have.attr', 'data-score', score)
})

Cypress.Commands.add("selectElementWithScore", (elementName) => {
  cy.getEl(`${elementName}-score`).click()
})


Cypress.Commands.add("checkResults", (cityName) => {
  cy.checkResultsAreAvailable(cityName, true)
  cy.get('.vs__dropdown-menu').click()
  cy.getEl('go-to-results').click()
  // Participation has only the objective question
  cy.checkScore('participation', '1')
  // we trust the backend on this, more exact scores are tested in the backend
  cy.checkScore('représentation', '3')
  cy.selectElementWithScore('représentation')
  cy.getEl(`représentation-score`).click()
  cy.checkScore('Marker R.1', '3')
  cy.selectElementWithScore('Marker R.1')
  cy.selectElementWithScore('Criteria R.1.1')

  cy.getEl("question-result").eq(0).within(() => {
    cy.getEl('question-statement').contains('Question 1')
    cy.getEl('role-button').click({multiple: true})
    cy.get(`[data-cy="chart-total"][data-choice="choice 1"]`).should('contain', '100%')
    cy.get(`[data-cy="chart-total"][data-choice="choice 2"]`).should('contain', '0%')
    cy.get(`[data-cy="chart-total"][data-choice="choice 3"]`).should('contain', '0%')
    cy.get(`[data-cy="chart-total"][data-choice="choice 4"]`).should('contain', '0%')
    cy.get(`[data-cy="chart-bar"][data-choice="choice 1"][data-role="Citoyen"]`).should('have.attr', 'style', 'width: 100%;')
    cy.get(`[data-cy="chart-bar"][data-choice="choice 1"][data-role="Élu"]`).should('have.attr', 'style', 'width: 0%;')
  })
  cy.getEl("question-result").eq(1).within(() => {
    cy.getEl('question-statement').contains('Question 2')
    cy.getEl('role-button').click({multiple: true})
    cy.get(`[data-cy="chart-total"][data-choice="choice 1"]`).should('contain', '0%')
    cy.get(`[data-cy="chart-total"][data-choice="choice 2"]`).should('contain', '50%')
    cy.get(`[data-cy="chart-total"][data-choice="choice 3"]`).should('contain', '50%')
    cy.get(`[data-cy="chart-total"][data-choice="choice 4"]`).should('contain', '0%')
    cy.get(`[data-cy="chart-bar"][data-choice="choice 2"][data-role="Citoyen"]`).should('have.attr', 'style', 'width: 50%;')
    cy.get(`[data-cy="chart-bar"][data-choice="choice 2"][data-role="Élu"]`).should('have.attr', 'style', 'width: 0%;')
    cy.get(`[data-cy="chart-bar"][data-choice="choice 3"][data-role="Citoyen"]`).should('have.attr', 'style', 'width: 50%;')
    cy.get(`[data-cy="chart-bar"][data-choice="choice 3"][data-role="Élu"]`).should('have.attr', 'style', 'width: 0%;')
  })
  cy.getEl("question-result").eq(2).within(() => {
    cy.getEl('question-statement').contains('Question 3')
    cy.getEl('role-button').click({multiple: true})
    // not corresponding
    cy.get(`[data-cy="chart-bar"][data-category="Catégorie 1"][data-choice="choice 1"][data-role="Citoyen"]`).should('have.attr', 'style', 'width: 0%;')
    cy.get(`[data-cy="chart-bar"][data-category="Catégorie 1"][data-choice="choice 1"][data-role="Élu"]`).should('have.attr', 'style', 'width: 0%;')
    cy.get(`[data-cy="chart-bar"][data-category="Catégorie 2"][data-choice="choice 2"][data-role="Citoyen"]`).should('have.attr', 'style', 'width: 0%;')
    // is corresponding
    cy.get(`[data-cy="chart-bar"][data-category="Catégorie 1"][data-choice="choice 3"][data-role="Citoyen"]`).should('have.attr', 'style', 'width: 100%;')
    cy.get(`[data-cy="chart-bar"][data-category="Catégorie 2"][data-choice="choice 4"][data-role="Citoyen"]`).should('have.attr', 'style', 'width: 100%;')
  })
  cy.getEl("question-result").eq(3).within(() => {
    cy.getEl('question-statement').contains('Question 4')
    cy.getEl("boolean-true").should('have.text', '100%')
    cy.getEl("boolean-false").should('have.text', '0%')
  })
  cy.getEl("question-result").eq(4).within(() => {
    cy.getEl('question-statement').contains('Question 5')
    cy.getEl("result-value").should('have.text', '50%')
  })
  cy.getEl("question-result").eq(5).within(() => {
    cy.getEl('question-statement').contains('Question 6')
    cy.getEl("result-value").should('have.text', '7')
  })
})
