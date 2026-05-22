import { ApiResponse } from '../ApiResponse';
import { describe, it, expect } from '@jest/globals';

describe('ApiResponse', () => {
  describe('success', () => {
    it('should create a successful response with data', () => {
      const data = { id: 1, name: 'test' };
      const response = ApiResponse.success(data);

      expect(response.success).toBe(true);
      expect(response.code).toBe(0);
      expect(response.data).toEqual(data);
      expect(response.message).toBe('操作成功');
    });

    it('should create a successful response with custom message', () => {
      const response = ApiResponse.success(null, '登录成功');

      expect(response.success).toBe(true);
      expect(response.code).toBe(0);
      expect(response.message).toBe('登录成功');
    });

    it('should create a successful response with undefined data', () => {
      const response = ApiResponse.success();

      expect(response.success).toBe(true);
      expect(response.code).toBe(0);
      expect(response.data).toBeUndefined();
    });
  });

  describe('error', () => {
    it('should create an error response with custom message', () => {
      const response = ApiResponse.error('操作失败');

      expect(response.success).toBe(false);
      expect(response.code).toBe(10000);
      expect(response.message).toBe('操作失败');
      expect(response.data).toBeNull();
    });

    it('should create an error response with custom code', () => {
      const response = ApiResponse.error('未授权访问', 401);

      expect(response.success).toBe(false);
      expect(response.code).toBe(401);
      expect(response.message).toBe('未授权访问');
    });

    it('should create an error response with default code', () => {
      const response = ApiResponse.error('服务器错误');

      expect(response.success).toBe(false);
      expect(response.code).toBe(10000);
    });
  });
});
