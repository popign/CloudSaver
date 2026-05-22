import { describe, it, expect, beforeEach, jest } from '@jest/globals';

jest.mock('../../models/User');
jest.mock('../../models/GlobalSetting');
jest.mock('bcrypt');
jest.mock('jsonwebtoken');

const UserMock = require('../../models/User').default;
const GlobalSettingMock = require('../../models/GlobalSetting').default;
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

import { UserService } from '../../services/UserService';
import { config } from '../../config';

describe('UserService', () => {
  let userService: UserService;

  beforeEach(() => {
    jest.clearAllMocks();
    userService = new UserService();
  });

  describe('isValidInput', () => {
    it('should return false for input with spaces', () => {
      expect(userService.isValidInput('user name')).toBe(false);
      expect(userService.isValidInput('password with space')).toBe(false);
    });

    it('should return false for input with Chinese characters', () => {
      expect(userService.isValidInput('用户名')).toBe(false);
      expect(userService.isValidInput('密码中文')).toBe(false);
    });

    it('should return true for valid alphanumeric input', () => {
      expect(userService.isValidInput('username123')).toBe(true);
      expect(userService.isValidInput('password123')).toBe(true);
      expect(userService.isValidInput('test_user')).toBe(true);
    });
  });

  describe('register', () => {
    it('should throw error for invalid register code', async () => {
      GlobalSettingMock.findOne.mockResolvedValue({
        dataValues: {
          CommonUserCode: 9527,
          AdminUserCode: 230713,
        },
      });

      await expect(userService.register('test', 'password', '0000')).rejects.toThrow('注册码错误');
      await expect(userService.register('test', 'password', '')).rejects.toThrow('注册码错误');
    });

    it('should throw error for invalid username', async () => {
      GlobalSettingMock.findOne.mockResolvedValue({
        dataValues: {
          CommonUserCode: 9527,
          AdminUserCode: 230713,
        },
      });

      await expect(userService.register('用户名', 'password', '9527')).rejects.toThrow(
        '用户名、密码或注册码不能包含空格或汉字'
      );
    });

    it('should throw error for invalid password', async () => {
      GlobalSettingMock.findOne.mockResolvedValue({
        dataValues: {
          CommonUserCode: 9527,
          AdminUserCode: 230713,
        },
      });

      await expect(userService.register('test', '密码123', '9527')).rejects.toThrow(
        '用户名、密码或注册码不能包含空格或汉字'
      );
    });

    it('should throw error for duplicate username', async () => {
      GlobalSettingMock.findOne.mockResolvedValue({
        dataValues: {
          CommonUserCode: 9527,
          AdminUserCode: 230713,
        },
      });
      UserMock.findOne.mockResolvedValue({ username: 'test' });

      await expect(userService.register('test', 'password', '9527')).rejects.toThrow('用户名已存在');
    });

    it('should create new user successfully', async () => {
      GlobalSettingMock.findOne.mockResolvedValue({
        dataValues: {
          CommonUserCode: 9527,
          AdminUserCode: 230713,
        },
      });
      UserMock.findOne.mockResolvedValue(null);
      bcrypt.hash.mockResolvedValue('hashedpassword');
      UserMock.create.mockResolvedValue({
        userId: '123',
        username: 'test',
        role: 0,
      });

      const result = await userService.register('test', 'password', '9527');

      expect(bcrypt.hash).toHaveBeenCalledWith('password', 10);
      expect(UserMock.create).toHaveBeenCalledWith({
        username: 'test',
        password: 'hashedpassword',
        role: 0,
      });
      expect(result.message).toBe('用户注册成功');
    });

    it('should create admin user with admin register code', async () => {
      GlobalSettingMock.findOne.mockResolvedValue({
        dataValues: {
          CommonUserCode: 9527,
          AdminUserCode: 230713,
        },
      });
      UserMock.findOne.mockResolvedValue(null);
      bcrypt.hash.mockResolvedValue('hashedpassword');
      UserMock.create.mockResolvedValue({
        userId: '123',
        username: 'admin',
        role: 1,
      });

      const result = await userService.register('admin', 'password', '230713');

      expect(UserMock.create).toHaveBeenCalledWith({
        username: 'admin',
        password: 'hashedpassword',
        role: 1,
      });
      expect(result.data.role).toBe(1);
    });
  });

  describe('login', () => {
    it('should throw error for non-existent user', async () => {
      UserMock.findOne.mockResolvedValue(null);

      await expect(userService.login('nonexistent', 'password')).rejects.toThrow('用户名或密码错误');
    });

    it('should throw error for wrong password', async () => {
      UserMock.findOne.mockResolvedValue({
        password: 'hashedpassword',
      });
      bcrypt.compare.mockResolvedValue(false);

      await expect(userService.login('test', 'wrongpassword')).rejects.toThrow('用户名或密码错误');
    });

    it('should return token for valid credentials', async () => {
      const mockUser = {
        userId: '123',
        role: 0,
        password: 'hashedpassword',
      };
      UserMock.findOne.mockResolvedValue(mockUser);
      bcrypt.compare.mockResolvedValue(true);
      jwt.sign.mockReturnValue('mocktoken');

      const result = await userService.login('test', 'password');

      expect(jwt.sign).toHaveBeenCalledWith(
        { userId: '123', role: 0 },
        config.jwtSecret,
        { expiresIn: '6h' }
      );
      expect(result.data.token).toBe('mocktoken');
    });

    it('should return token for admin user', async () => {
      const mockUser = {
        userId: '456',
        role: 1,
        password: 'hashedpassword',
      };
      UserMock.findOne.mockResolvedValue(mockUser);
      bcrypt.compare.mockResolvedValue(true);
      jwt.sign.mockReturnValue('admintoken');

      const result = await userService.login('admin', 'adminpassword');

      expect(result.data.token).toBe('admintoken');
    });
  });
});
