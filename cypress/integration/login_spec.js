/// <reference types="Cypress" />

describe('Login tests', () => {
    it('login successful', () => {
      cy.visit("https://fly.customer.io/")
      cy.get('.signup-title').should('exist')
      cy.get('.fly-form-control').type(Cypress.env('EMAIL'))
      cy.get('.mt-2 > .fly-flex > .fly-btn').click()
      cy.get('.jc-end > .fly-btn').should('exist')
      cy.get('#ember9 > input').type(Cypress.env('PASSWORD'))
      cy.get('.jc-end > .fly-btn').click()
      cy.get('.nav-workspace-dropdown-logo').should('exist')
    })

    it('login fail wrong password', () => {
        cy.visit("https://fly.customer.io/")
        cy.get('.signup-title').should('exist')
        cy.get('.fly-form-control').type('jnsjsn@gmailcom')
        cy.get('.mt-2 > .fly-flex > .fly-btn').click()
        cy.get('.jc-end > .fly-btn').should('exist')
        cy.get('#ember9 > input').type('skjhskjsh')
        cy.get('.jc-end > .fly-btn').click()
        cy.get('.button-link > .fly-svg-icon > .fly-svg-icon__icon > path').should('exist')
      })
  })
