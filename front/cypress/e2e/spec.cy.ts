describe('template spec', () => {
  it('logs in', () => {
    cy.login("user@telescoop.fr", "password")
    cy.visit("/compte")
  })
})
