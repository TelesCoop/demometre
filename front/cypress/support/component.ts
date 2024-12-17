// cypress/support/component.ts
/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-namespace */
import './commands'
import {mount} from 'cypress/vue'
import {h, Suspense} from 'vue'
import {getContext} from 'unctx'
import {
  createRouter,
  createWebHistory,
  RouterLink,
  routerKey,
  routeLocationKey,
} from 'vue-router'

type MountParams = Parameters<typeof mount<any>>;
type OptionsParam = MountParams[1];
type Router = ReturnType<typeof createRouter>;

declare global {
  namespace Cypress {
    interface Chainable {
      mount(component: any, options?: OptionsParam): Chainable;
      stubNuxtInject(key: string, value: unknown): void;
      stubNuxtRouter(callback: ($rotuer: Router) => void): void;
      resetNuxt(): void;
    }
  }
}

const nuxtAppCtx = getContext('nuxt-app')
const $router = createRouter({
  routes: [],
  history: createWebHistory(),
})
const generateNuxtCTX = (): Record<string, any> => ({
  static: {data: {}},
  payload: {data: {}, _errors: {}},
  hook: () => () => ({}),
  hooks: {
    callHook: () => Promise.resolve(),
  },
  _asyncData: {},
  _asyncDataPromises: {},
  _useHead: () => ({}),
  $router,
  _route: $router.currentRoute,
})
let nuxtCTX = generateNuxtCTX()

nuxtAppCtx.set(nuxtCTX)

Cypress.Commands.add('mount', (component, options = {}) => {
  options.global = options.global || {}
  options.global.components = {RouterLink}
  options.global.provide = {
    [routerKey as symbol]: $router,
    [routeLocationKey as symbol]: $router.currentRoute.value,
  }

  return mount(
    () => h(Suspense, h(component, options?.props, options?.slots)),
    options,
  )
})

Cypress.Commands.add('stubNuxtInject', (key, value) => {
  nuxtCTX['$' + key] = value
})

Cypress.Commands.add('stubNuxtRouter', callback => {
  callback($router)
})

Cypress.Commands.add('resetNuxt', () => {
  nuxtCTX = generateNuxtCTX()
  nuxtAppCtx.unset()
  nuxtAppCtx.set(nuxtCTX)

  $router.push('/')
})
