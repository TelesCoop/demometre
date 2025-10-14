describe('login works', () => {
  it('logs in', () => {
    cy.login("user1@telescoop.fr", "password")
    cy.wait(400)
    cy.visit("/compte")
    cy.wait(800)
    cy.getEl('account-email').should('contain', 'user1@telescoop.fr')
  })
})
