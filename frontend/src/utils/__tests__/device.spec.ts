import { describe, it, expect } from 'vitest'
import { isMobile, isTablet } from '../device'

describe('device utils', () => {
  describe('isMobile', () => {
    it('should return true for mobile user agents', () => {
      const mobileUserAgents = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
        'Mozilla/5.0 (Linux; Android 11; SM-G991B)',
        'Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X)',
        'Mozilla/5.0 (BlackBerry; U; BlackBerry 9900)',
        'Mozilla/5.0 (webOS; U; Palm Pixi; en)',
      ]

      mobileUserAgents.forEach((userAgent) => {
        Object.defineProperty(navigator, 'userAgent', {
          value: userAgent,
          configurable: true,
        })
        expect(isMobile()).toBe(true)
      })
    })

    it('should return false for desktop user agents', () => {
      const desktopUserAgents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
      ]

      desktopUserAgents.forEach((userAgent) => {
        Object.defineProperty(navigator, 'userAgent', {
          value: userAgent,
          configurable: true,
        })
        expect(isMobile()).toBe(false)
      })
    })
  })

  describe('isTablet', () => {
    it('should return true for tablet user agents', () => {
      const tabletUserAgents = [
        'Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X)',
        'Mozilla/5.0 (Tablet; Linux; Android 11; Pixel C)',
        'Mozilla/5.0 (Kindle; Linux; U; Linux) Opera Mobi/46',
      ]

      tabletUserAgents.forEach((userAgent) => {
        Object.defineProperty(navigator, 'userAgent', {
          value: userAgent.toLowerCase(),
          configurable: true,
        })
        expect(isTablet()).toBe(true)
      })
    })

    it('should return false for phone user agents', () => {
      Object.defineProperty(navigator, 'userAgent', {
        value: 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
        configurable: true,
      })
      expect(isTablet()).toBe(false)
    })

    it('should return false for desktop user agents', () => {
      Object.defineProperty(navigator, 'userAgent', {
        value: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        configurable: true,
      })
      expect(isTablet()).toBe(false)
    })
  })
})
