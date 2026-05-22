import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useUserSettingStore } from '../userSetting'

vi.mock('@/api/setting', () => ({
  settingApi: {
    getSetting: vi.fn(() => Promise.resolve({ data: null })),
    saveSetting: vi.fn(() => Promise.resolve({})),
  },
}))

describe('userSetting store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
    vi.clearAllMocks()
  })

  it('should initialize with default values', () => {
    const store = useUserSettingStore()

    expect(store.globalSetting).toBeNull()
    expect(store.userSettings.cloud115Cookie).toBe('')
    expect(store.userSettings.quarkCookie).toBe('')
    expect(store.displayStyle).toBe('card')
    expect(store.imagesSource).toBe('proxy')
  })

  it('should set display style to table', () => {
    const store = useUserSettingStore()
    store.setDisplayStyle('table')

    expect(store.displayStyle).toBe('table')
    expect(localStorage.getItem('display_style')).toBe('table')
  })

  it('should set display style to card', () => {
    const store = useUserSettingStore()
    store.setDisplayStyle('card')

    expect(store.displayStyle).toBe('card')
    expect(localStorage.getItem('display_style')).toBe('card')
  })

  it('should set images source to proxy', () => {
    const store = useUserSettingStore()
    store.setImagesSource('proxy')

    expect(store.imagesSource).toBe('proxy')
    expect(localStorage.getItem('images_source')).toBe('proxy')
  })

  it('should set images source to local', () => {
    const store = useUserSettingStore()
    store.setImagesSource('local')

    expect(store.imagesSource).toBe('local')
    expect(localStorage.getItem('images_source')).toBe('local')
  })

  it('should restore display style from localStorage', () => {
    localStorage.setItem('display_style', 'table')
    const store = useUserSettingStore()

    expect(store.displayStyle).toBe('table')
  })

  it('should restore images source from localStorage', () => {
    localStorage.setItem('images_source', 'local')
    const store = useUserSettingStore()

    expect(store.imagesSource).toBe('local')
  })

  it('should handle getSettings with data', async () => {
    const mockData = {
      globalSetting: {
        httpProxyHost: '127.0.0.1',
        httpProxyPort: '8080',
        isProxyEnabled: true,
        AdminUserCode: 1,
        CommonUserCode: 0,
      },
      userSettings: {
        cloud115Cookie: 'test_cookie',
        quarkCookie: 'test_quark',
      },
    }

    vi.mocked(await import('@/api/setting')).settingApi.getSetting.mockResolvedValue({ data: mockData } as any)

    const store = useUserSettingStore()
    await store.getSettings()

    expect(store.globalSetting).toEqual(mockData.globalSetting)
    expect(store.userSettings).toEqual(mockData.userSettings)
  })
})
