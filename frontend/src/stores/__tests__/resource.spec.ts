import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useResourceStore, CLOUD_DRIVES } from '../resource'

vi.mock('@/api/cloud115', () => ({
  cloud115Api: {
    getShareInfo: vi.fn(),
    saveFile: vi.fn(),
  },
}))

vi.mock('@/api/quark', () => ({
  quarkApi: {
    getShareInfo: vi.fn(),
    saveFile: vi.fn(),
  },
}))

vi.mock('@/api/resource', () => ({
  resourceApi: {
    search: vi.fn(() => Promise.resolve({ data: [] })),
  },
}))

describe('resource store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
    vi.clearAllMocks()
  })

  describe('CLOUD_DRIVES', () => {
    it('should have 115 cloud drive configured', () => {
      const cloud115Drive = CLOUD_DRIVES.find((d) => d.type === 'pan115')
      expect(cloud115Drive).toBeDefined()
      expect(cloud115Drive?.name).toBe('115网盘')
    })

    it('should have quark drive configured', () => {
      const quarkDrive = CLOUD_DRIVES.find((d) => d.type === 'quark')
      expect(quarkDrive).toBeDefined()
      expect(quarkDrive?.name).toBe('夸克网盘')
    })
  })

  describe('initial state', () => {
    it('should have correct initial state', () => {
      const store = useResourceStore()

      expect(store.keyword).toBe('')
      expect(store.resources).toEqual([])
      expect(store.shareInfo).toEqual({})
      expect(store.resourceSelect).toEqual([])
      expect(store.loading).toBe(false)
      expect(store.backupPlan).toBe(false)
      expect(store.loadTree).toBe(false)
    })

    it('should have correct tag colors', () => {
      const store = useResourceStore()

      expect(store.tagColor.baiduPan).toBe('primary')
      expect(store.tagColor.weiyun).toBe('info')
      expect(store.tagColor.aliyun).toBe('warning')
      expect(store.tagColor.pan115).toBe('danger')
      expect(store.tagColor.quark).toBe('success')
    })
  })

  describe('setLoadTree', () => {
    it('should set loadTree to true', () => {
      const store = useResourceStore()
      store.setLoadTree(true)
      expect(store.loadTree).toBe(true)
    })

    it('should set loadTree to false', () => {
      const store = useResourceStore()
      store.setLoadTree(false)
      expect(store.loadTree).toBe(false)
    })
  })

  describe('setSelectedResource', () => {
    it('should set selected resources', () => {
      const store = useResourceStore()
      const mockResources = [
        { id: '1', name: 'test', isChecked: true },
        { id: '2', name: 'test2', isChecked: false },
      ] as any

      store.setSelectedResource(mockResources)
      expect(store.resourceSelect).toEqual(mockResources)
    })

    it('should clear selected resources', () => {
      const store = useResourceStore()
      store.setSelectedResource([])
      expect(store.resourceSelect).toEqual([])
    })
  })

  describe('handleError', () => {
    it('should handle Error instance', () => {
      const store = useResourceStore()
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})

      store.handleError('Error occurred', new Error('Test error'))

      expect(consoleSpy).toHaveBeenCalled()
      consoleSpy.mockRestore()
    })

    it('should handle unknown error', () => {
      const store = useResourceStore()
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})

      store.handleError('Error occurred', 'Unknown error')

      expect(consoleSpy).toHaveBeenCalled()
      consoleSpy.mockRestore()
    })
  })

  describe('cloud drive regex matching', () => {
    it('should match 115 cloud share links', () => {
      const cloud115Drive = CLOUD_DRIVES.find((d) => d.type === 'pan115')!
      const testUrls = [
        'https://115.com/s/abc123',
        'https://anxia.com/s/def456?password=ghi',
        'https://115cdn.com/s/jkl789',
      ]

      testUrls.forEach((url) => {
        expect(cloud115Drive.regex.test(url)).toBe(true)
      })
    })

    it('should match quark share links', () => {
      const quarkDrive = CLOUD_DRIVES.find((d) => d.type === 'quark')!
      const testUrls = [
        'https://pan.quark.cn/s/abc123ABC',
        'https://pan.quark.cn/s/xyz789',
      ]

      testUrls.forEach((url) => {
        expect(quarkDrive.regex.test(url)).toBe(true)
      })
    })

    it('should not match invalid URLs', () => {
      const cloud115Drive = CLOUD_DRIVES.find((d) => d.type === 'pan115')!
      const quarkDrive = CLOUD_DRIVES.find((d) => d.type === 'quark')!

      expect(cloud115Drive.regex.test('https://google.com')).toBe(false)
      expect(quarkDrive.regex.test('https://google.com')).toBe(false)
    })
  })
})
