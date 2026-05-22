import { describe, it, expect, beforeEach, jest } from '@jest/globals';

jest.mock('../../models/UserSetting');
jest.mock('../../models/GlobalSetting');

const UserSettingMock = require('../../models/UserSetting').default;
const GlobalSettingMock = require('../../models/GlobalSetting').default;

import { SettingService } from '../../services/SettingService';

describe('SettingService', () => {
  let settingService: SettingService;
  let mockImageService: any;

  beforeEach(() => {
    jest.clearAllMocks();
    mockImageService = {
      updateAxiosInstance: jest.fn<() => Promise<void>>().mockResolvedValue(undefined as void),
    };
    settingService = new SettingService(mockImageService);
  });

  describe('getSettings', () => {
    it('should throw error when userId is invalid', async () => {
      await expect(settingService.getSettings(undefined, 0)).rejects.toThrow('用户ID无效');
      await expect(settingService.getSettings('', 0)).rejects.toThrow('用户ID无效');
    });

    it('should create user settings if not exists', async () => {
      const mockUserSettings = {
        userId: '123',
        cloud115Cookie: '',
        quarkCookie: '',
      };
      
      UserSettingMock.findOne.mockResolvedValue(null);
      UserSettingMock.create.mockResolvedValue(mockUserSettings);
      GlobalSettingMock.findOne.mockResolvedValue(null);

      const result = await settingService.getSettings('123', 0);

      expect(UserSettingMock.create).toHaveBeenCalledWith({
        userId: '123',
        cloud115Cookie: '',
        quarkCookie: '',
      });
      expect(result.data.userSettings).toEqual(mockUserSettings);
    });

    it('should return user settings and global settings', async () => {
      const mockUserSettings = {
        userId: '123',
        cloud115Cookie: 'cookie123',
        quarkCookie: 'quark456',
      };
      const mockGlobalSetting = {
        httpProxyHost: '127.0.0.1',
        httpProxyPort: 8080,
        isProxyEnabled: true,
        CommonUserCode: 9527,
        AdminUserCode: 230713,
      };

      UserSettingMock.findOne.mockResolvedValue(mockUserSettings);
      GlobalSettingMock.findOne.mockResolvedValue(mockGlobalSetting);

      const result = await settingService.getSettings('123', 1);

      expect(result.data.userSettings).toEqual(mockUserSettings);
      expect(result.data.globalSetting).toEqual(mockGlobalSetting);
    });

    it('should hide global settings for non-admin users', async () => {
      const mockUserSettings = {
        userId: '123',
        cloud115Cookie: '',
        quarkCookie: '',
      };
      const mockGlobalSetting = {
        httpProxyHost: '127.0.0.1',
      };

      UserSettingMock.findOne.mockResolvedValue(mockUserSettings);
      GlobalSettingMock.findOne.mockResolvedValue(mockGlobalSetting);

      const result = await settingService.getSettings('123', 0);

      expect(result.data.globalSetting).toBeNull();
    });
  });

  describe('saveSettings', () => {
    it('should throw error when userId is invalid', async () => {
      await expect(
        settingService.saveSettings(undefined, 0, { userSettings: {} })
      ).rejects.toThrow('用户ID无效');
    });

    it('should update user settings', async () => {
      UserSettingMock.update.mockResolvedValue([1]);
      
      const mockImageServiceUpdate = jest.fn<() => Promise<void>>().mockResolvedValue(undefined as void);
      settingService = new SettingService({
        updateAxiosInstance: mockImageServiceUpdate,
      } as any);

      const result = await settingService.saveSettings('123', 0, {
        userSettings: { cloud115Cookie: 'test' },
      });

      expect(UserSettingMock.update).toHaveBeenCalledWith(
        { cloud115Cookie: 'test' },
        { where: { userId: '123' } }
      );
      expect(result.message).toBe('保存成功');
    });

    it('should update global settings only for admin users', async () => {
      UserSettingMock.update.mockResolvedValue([1]);
      GlobalSettingMock.update.mockResolvedValue([1]);

      const mockImageServiceUpdate = jest.fn<() => Promise<void>>().mockResolvedValue(undefined as void);
      settingService = new SettingService({
        updateAxiosInstance: mockImageServiceUpdate,
      } as any);

      await settingService.saveSettings('123', 1, {
        userSettings: {},
        globalSetting: { httpProxyHost: 'newhost' },
      });

      expect(GlobalSettingMock.update).toHaveBeenCalledWith(
        { httpProxyHost: 'newhost' },
        { where: {} }
      );
    });

    it('should not update global settings for non-admin users', async () => {
      UserSettingMock.update.mockResolvedValue([1]);

      const mockImageServiceUpdate = jest.fn<() => Promise<void>>().mockResolvedValue(undefined as void);
      settingService = new SettingService({
        updateAxiosInstance: mockImageServiceUpdate,
      } as any);

      await settingService.saveSettings('123', 0, {
        userSettings: {},
        globalSetting: { httpProxyHost: 'newhost' },
      });

      expect(GlobalSettingMock.update).not.toHaveBeenCalled();
    });
  });

  describe('updateSettings', () => {
    it('should call updateAxiosInstance', async () => {
      const mockImageServiceUpdate = jest.fn<() => Promise<void>>().mockResolvedValue(undefined as void);
      settingService = new SettingService({
        updateAxiosInstance: mockImageServiceUpdate,
      } as any);

      await settingService.updateSettings();

      expect(mockImageServiceUpdate).toHaveBeenCalled();
    });
  });
});
