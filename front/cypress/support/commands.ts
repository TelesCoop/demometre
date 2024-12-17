Cypress.Commands.add("getBySel", (selector, ...args) => {
  return cy.get(`[data-cy=${selector}]`, ...args)
})

Cypress.Commands.add("login", (email, password) => {
  cy.visit("/login")

  const el = cy.getBySel("login-email")
  cy.wait(100)
  el.type(email)
  cy.getBySel("login-password").focus().type(password, {
    force: true,
  })
  cy.getBySel("login-submit").click()
})
