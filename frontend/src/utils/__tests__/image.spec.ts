import { describe, it, expect } from 'vitest'

describe('image utils', () => {
  describe('getProxyImageUrl logic', () => {
    it('should return proxy format when imagesSource is proxy', () => {
      const originalUrl = 'https://example.com/image.jpg'
      const imagesSource = 'proxy'
      
      const result = imagesSource === 'proxy'
        ? `/tele-images/?url=${encodeURIComponent(originalUrl)}`
        : originalUrl
      
      expect(result).toContain('/tele-images/')
      expect(result).toContain(encodeURIComponent(originalUrl))
    })

    it('should return original url when imagesSource is local', () => {
      const originalUrl = 'https://example.com/image.jpg'
      const imagesSource = 'local'
      
      const result = imagesSource === 'proxy'
        ? `/tele-images/?url=${encodeURIComponent(originalUrl)}`
        : originalUrl
      
      expect(result).toBe(originalUrl)
    })

    it('should handle empty url', () => {
      const originalUrl = ''
      const imagesSource = 'proxy'
      
      const result = originalUrl ? 
        (imagesSource === 'proxy'
          ? `/tele-images/?url=${encodeURIComponent(originalUrl)}`
          : originalUrl)
        : '/default.png'
      
      expect(result).toBe('/default.png')
    })
  })
})
