Cypress.Commands.add("getBySel", (selector, ...args) => {
  return cy.get(`[data-cy="${selector}"]`, ...args)
})
Cypress.Commands.add("selectChoice", (answerIx, ...args) => {
  return cy.get('.response-choice', ...args).eq(answerIx).click()
})
Cypress.Commands.add("inputPercentage", (percentage, ...args) => {
  return cy.getBySel('percentage-input').type(percentage)
})
Cypress.Commands.add("inputNumber", (percentage, ...args) => {
  return cy.getBySel('number-input').type(percentage)
})

Cypress.Commands.add("login", (email, password) => {
  cy.session([email, password], () => {
    cy.visit("/login")

    const el = cy.getBySel("login-email")
    cy.wait(400)
    el.type(email)
    cy.getBySel("login-password").focus().type(password, {
      force: true,
    })
    cy.getBySel("login-submit").click()
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

Cypress.Commands.add("submitQuestion", (categoryName, value) => {
  cy.getBySel('submit-button').click()
})
