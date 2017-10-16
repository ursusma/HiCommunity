/**
 * Created by Oliver on 2017/10/13 0013.
 */


var exceptionTrans = {

    // Base
    0: '未知异常',

    // User
    1000: '未知用户异常',
    1001: '用户名或邮件格式错误，用户名为4-16个英文或2-8个中文字符',
    1002: '密码格式错误，密码长度为8-32位，且只包含数字字母和下划线',
    1003: '密码错误',
    1004: '用户名或邮件不存在',
    1005: '用户已登录',
    1006: '账户创建失败',
    1007: '用户名或邮箱已被注册',
    1008: '用户退出失败',

    // Common
    9000: '未知普通异常',
    9001: '请登录后继续',

    // Http
    404: '页面未找到',

};