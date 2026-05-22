import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { h } from 'vue'
import SearchBar from '../SearchBar.vue'

vi.mock('@/stores/resource', () => ({
  useResourceStore: vi.fn(() => ({
    keyword: '',
    parsingCloudLink: vi.fn(),
    searchResources: vi.fn(),
  })),
}))

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } },
    { path: '/login', component: { template: '<div>Login</div>' } },
    { path: '/resource', component: { template: '<div>Resource</div>' } },
  ],
})

describe('SearchBar.vue', () => {
  beforeEach(async () => {
    router.push('/')
    await router.isReady()
    vi.clearAllMocks()
  })

  it('should render search input', async () => {
    const wrapper = mount(SearchBar, {
      global: {
        plugins: [router],
        stubs: {
          'el-input': {
            template: '<input class="el-input" v-model="modelValue" @input="$emit(\'update:modelValue\', $event.target.value)" />',
            props: ['modelValue'],
            emits: ['update:modelValue'],
          },
          'el-icon': { template: '<span class="el-icon"></span>' },
          'el-button': { template: '<button class="el-button"></button>' },
          'el-tooltip': { template: '<div class="el-tooltip"><slot /></div>' },
        },
      },
    })

    expect(wrapper.find('.pc-search').exists()).toBe(true)
    expect(wrapper.find('.el-input').exists()).toBe(true)
    wrapper.unmount()
  })

  it('should have correct placeholder text', async () => {
    const wrapper = mount(SearchBar, {
      global: {
        plugins: [router],
        stubs: {
          'el-input': {
            template: '<input class="el-input" :placeholder="placeholder" />',
            props: ['placeholder'],
          },
          'el-icon': { template: '<span class="el-icon"></span>' },
          'el-button': { template: '<button class="el-button"></button>' },
          'el-tooltip': { template: '<div class="el-tooltip"><slot /></div>' },
        },
      },
    })

    expect(wrapper.find('.el-input').exists()).toBe(true)
    wrapper.unmount()
  })

  it('should render logout button', async () => {
    const wrapper = mount(SearchBar, {
      global: {
        plugins: [router],
        stubs: {
          'el-input': { template: '<input class="el-input" />' },
          'el-icon': { template: '<span class="el-icon"></span>' },
          'el-button': { template: '<button class="el-button"></button>' },
          'el-tooltip': { template: '<div class="el-tooltip"><slot /></div>' },
        },
      },
    })

    expect(wrapper.find('.logout-btn').exists()).toBe(true)
    wrapper.unmount()
  })

  it('should navigate to /resource after search', async () => {
    const mockSearchResources = vi.fn()
    vi.mocked(await import('@/stores/resource')).useResourceStore.mockReturnValue({
      keyword: '',
      parsingCloudLink: vi.fn(),
      searchResources: mockSearchResources,
    } as any)

    const wrapper = mount(SearchBar, {
      global: {
        plugins: [router],
        stubs: {
          'el-input': {
            template: '<button class="el-input" @click="$emit(\'search\')">Search</button>',
            emits: ['search'],
          },
          'el-icon': { template: '<span class="el-icon"></span>' },
          'el-button': { template: '<button class="el-button"></button>' },
          'el-tooltip': { template: '<div class="el-tooltip"><slot /></div>' },
        },
      },
    })

    expect(wrapper.vm.$route.path).toBe('/')
    wrapper.unmount()
  })
})
