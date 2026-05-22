import { sendSuccess, sendError } from '../response';
import { describe, it, expect, beforeEach, jest } from '@jest/globals';

describe('response utils', () => {
  let mockRes: any;

  beforeEach(() => {
    mockRes = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn().mockReturnThis(),
    };
  });

  describe('sendSuccess', () => {
    it('should send success response with default code', () => {
      const response = { data: { id: 1 } };
      sendSuccess(mockRes, response);

      expect(mockRes.status).toHaveBeenCalledWith(200);
      expect(mockRes.json).toHaveBeenCalledWith({ data: { id: 1 }, code: 0 });
    });

    it('should send success response with custom code', () => {
      const response = { data: { id: 1 } };
      sendSuccess(mockRes, response, 200);

      expect(mockRes.status).toHaveBeenCalledWith(200);
      expect(mockRes.json).toHaveBeenCalledWith({ data: { id: 1 }, code: 200 });
    });

    it('should send success response with message', () => {
      const response = { message: '登录成功', data: { token: 'abc' } };
      sendSuccess(mockRes, response);

      expect(mockRes.status).toHaveBeenCalledWith(200);
      expect(mockRes.json).toHaveBeenCalledWith({ message: '登录成功', data: { token: 'abc' }, code: 0 });
    });
  });

  describe('sendError', () => {
    it('should send error response with default code', () => {
      const response = { message: '操作失败' };
      sendError(mockRes, response);

      expect(mockRes.status).toHaveBeenCalledWith(200);
      expect(mockRes.json).toHaveBeenCalledWith({ message: '操作失败', code: 10000 });
    });

    it('should send error response with custom code', () => {
      const response = { message: '未授权' };
      sendError(mockRes, response, 401);

      expect(mockRes.status).toHaveBeenCalledWith(200);
      expect(mockRes.json).toHaveBeenCalledWith({ message: '未授权', code: 401 });
    });

    it('should preserve existing properties in response', () => {
      const response = { message: '错误', data: null, extra: 'info' };
      sendError(mockRes, response);

      expect(mockRes.json).toHaveBeenCalledWith({ message: '错误', data: null, extra: 'info', code: 10000 });
    });
  });
});
