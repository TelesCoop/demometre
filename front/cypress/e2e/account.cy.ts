describe('login works', () => {
  it('logs in', () => {
    cy.login("user@telescoop.fr", "password")
    cy.wait(400)
    cy.visit("/compte")
    cy.wait(800)
    cy.getEl('account-email').should('contain', 'user@telescoop.fr')
  })
})
