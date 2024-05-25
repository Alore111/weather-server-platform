
# 用户认证与管理 API 文档

## 登录

- **URL**

  `/api/login`

- **Method:**

  `POST`

- **请求体参数**

  | 参数名   | 类型   | 描述             |
  | -------- | ------ | ---------------- |
  | username | string | 用户名或 QQ 号码 |
  | password | string | 密码             |
  
- **成功响应**

  - **Code:** 200
  - **Content:**

    ```json
    {
        "login": true,
        "access_token": "JWT Token",
        "user_info": {
            "id": 123,
            "username": "example_user",
            "email": "example@example.com",
            // 其他用户信息
        }
    }
    ```

- **失败响应**

  - **Code:** 400
  - **Content:**

    ```json
    {
        "login": false
    }
    ```

## 检查登录状态

- **URL**

  `/api/checkLoginStatus`

- **Method:**

  `GET`

- **请求头**

  | 参数名         | 类型   | 描述             |
  | -------------- | ------ | ---------------- |
  | Authorization | string | JWT Token        |

- **成功响应**

  - **Code:** 200
  - **Content:**

    ```json
    {
        "logged_in": true,
        "user_info": {
            "id": 123,
            "username": "example_user",
            "email": "example@example.com",
            // 其他用户信息
        }
    }
    ```

## 注册

- **URL**

  `/api/register`

- **Method:**

  `POST`

- **请求体参数**

  | 参数名        | 类型   | 描述         |
  | ------------- | ------ | ------------ |
  | username      | string | 用户名       |
  | password      | string | 密码         |
  | qq            | string | QQ 号码      |
  | captcha       | string | 验证码       |
  | captcha_seed  | string | 验证码种子   |

- **成功响应**

  - **Code:** 200
  - **Content:**

    ```json
    {
        "message": "注册成功",
        "code": 200
    }
    ```

- **失败响应**

  - **Code:** 400
  - **Content:**

    ```json
    {
        "message": "参数不完整",
        "code": 400
    }
    ```

## 发送重置密码链接

- **URL**

  `/api/find`

- **Method:**

  `POST`

- **请求体参数**

  | 参数名        | 类型   | 描述         |
  | ------------- | ------ | ------------ |
  | email         | string | 注册邮箱     |
  | captcha       | string | 验证码       |
  | captcha_seed  | string | 验证码种子   |

- **成功响应**

  - **Code:** 200
  - **Content:**

    ```json
    {
        "message": "已发送重置链接至邮箱",
        "code": 200
    }
    ```

- **失败响应**

  - **Code:** 400
  - **Content:**

    ```json
    {
        "message": "参数不完整",
        "code": 400
    }
    ```

## 重置密码

- **URL**

  `/api/resetPassword`

- **Method:**

  `POST`

- **请求体参数**

  | 参数名        | 类型   | 描述         |
  | ------------- | ------ | ------------ |
  | password      | string | 新密码       |
  | reset_token   | string | 重置密码 token |

- **成功响应**

  - **Code:** 200
  - **Content:**

    ```json
    {
        "message": "密码重置成功",
        "code": 200
    }
    ```

- **失败响应**

  - **Code:** 400
  - **Content:**

    ```json
    {
        "message": "参数不完整",
        "code": 400
    }
    ```

## 检查重置密码 Token 的有效性

- **URL**

  `/api/checkResetToken`

- **Method:**

  `GET` 或 `POST`

- **请求参数**

  | 参数名      | 类型   | 描述             |
  | ----------- | ------ | ---------------- |
  | reset_token | string | 重置密码 token   |

- **成功响应**

  - **Code:** 200
  - **Content:**

    ```json
    {
        "message": "重置密码 token 有效",
        "code": 200
    }
    ```

- **失败响应**

  - **Code:** 400
  - **Content:**

    ```json
    {
        "message": "重置密码 token 无效",
        "code": 400
    }
    ```

## 获取激活状态

- **URL**

  `/api/getActivateFromStudentId`

- **Method:**

  `GET` 或 `POST`

- **请求参数**

  | 参数名      | 类型   | 描述               |
  | ----------- | ------ | ------------------ |
  | student_id  | string | 学生ID             |

- **成功响应**

  - **Code:** 200
  - **Content:**

    ```json
    {
        "message": "已激活",
        "code": 200
    }
    ```

- **失败响应**

  - **Code:** 400
  - **Content:**

    ```json
    {
        "message": "未激活",
        "code": 400
    }
    ```

## 激活账户

- **URL**

  `/api/activate`

- **Method:**

  `POST`

- **请求体参数**

  | 参数名         | 类型   | 描述                   |
  | -------------- | ------ | ---------------------- |
  | identifier     | string | 标识符 (激活码或学号)  |
  | activate_type  | string | 激活类型 (`code` 或 `student_id`) |
  | user_id        | string | 用户 ID                |

- **成功响应**

  - **Code:** 200
  - **Content:**

    ```json
    {
        "message": "账户激活成功",
        "code": 200
    }
    ```

- **失败响应**

  - **Code:** 400
  - **Content:**

    ```json
    {
        "

message": "账户激活失败",
        "code": 400
    }
    ```

## 获取验证码

- **URL**

  `/api/captcha`

- **Method:**

  `GET`

- **请求参数**

  | 参数名 | 类型   | 描述           |
  | ------ | ------ | -------------- |
  | seed   | string | 验证码种子     |

- **成功响应**

  - **Content-Type:** image/png

## 校验验证码

- **URL**

  `/api/check_captcha`

- **Method:**

  `POST`

- **请求体参数**

  | 参数名        | 类型   | 描述         |
  | ------------- | ------ | ------------ |
  | captcha       | string | 用户输入验证码 |
  | seed          | string | 验证码种子   |

- **成功响应**

  - **Code:** 200
  - **Content:**

    ```json
    {
        "message": "验证码正确",
        "code": 200
    }
    ```

- **失败响应**

  - **Code:** 400
  - **Content:**

    ```json
    {
        "message": "验证码错误",
        "code": 400
    }
    ```
