# ApiPost 接口测试文档

## 测试环境
- 服务器地址: http://localhost:19088
- 数据库: 线上开发环境PG库 (47.108.29.156:25432)

---

## 测试1: 注册用户接口

### 操作步骤
1. 打开ApiPost
2. 创建新请求
3. 设置请求方法: `POST`
4. 设置请求URL: `http://localhost:19088/api/v1/users/register`
5. 设置请求头:
   - `Content-Type: application/json`
6. 设置请求体:
   ```json
   {
     "email": "jiangkuanli@example.com",
     "username": "jiangkuanli",
     "full_name": "jiangkuanli",
     "password": "123456"
   }
   ```

7. 点击发送请求

### 测试结果
```
{
	"code": 200,
	"message": "Success",
	"data": {
		"hashed_password": "$2b$12$uYnISb0kkl4uz.DVrx5k1O7HcGevFojC7vDaOixCboeLSH8fipC/y",
		"email": "jiangkuanli@123.com",
		"username": "jiangkuanli_2",
		"full_name": "jiangkuanli",
		"created_at": "2026-01-27T02:58:57.759030+00:00",
		"id": "1fe8b02b-fb2c-11f0-8e56-0c9a3c9f30ca",
		"is_active": true,
		"is_superuser": false,
		"updated_at": null
	}
}
```
![image-20260127110230027](./assets/image-20260127110230027.png)

---

## 测试2: 登录接口

### 操作步骤
1. 创建新请求
2. 设置请求方法: `POST`
3. 设置请求URL: `http://localhost:19088/api/v1/auth/login`
4. 设置请求头:
   - `Content-Type: application/x-www-form-urlencoded`
5. 设置请求体:
   - 选择 **`urlencoded`** 格式
   - 添加参数:
     - `username`: 填写注册时设置的用户名（例如：`jiangkuanli_2`）
     - `password`: 填写注册时设置的密码（例如：`123456`）
6. 点击发送请求

### 测试结果
```json
{
	"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqaWFuZ2t1YW5saUAxMjMuY29tIiwiZXhwIjoxNzY5NTAwOTgxfQ.bpzQ1sTjUSZN078zU9u0gEv57Ubi8Et633ls7JpkPEU",
	"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqaWFuZ2t1YW5saUAxMjMuY29tIiwiZXhwIjoxNzcwMDg3NzgxfQ.MCi6FZI7amQbEj5717M4tEVvikAoN6XUTHML-4M66ZY",
	"token_type": "bearer",
	"access_expires_in": 18000,
	"refresh_expires_in": 604800,
	"is_superuser": false
}
```

![image-20260127110512619](./assets/image-20260127110512619.png)

---

## 测试3: 修改信息接口（密码、昵称）

### 操作步骤
1. 创建新请求

2. 设置请求方法: `PUT`

3. 设置请求URL: `http://localhost:19088/api/v1/users/{user_id}`
   - 将 `{user_id}` 替换为测试1（注册接口）返回的用户ID
   
     > http://localhost:19088/api/v1/users/1fe8b02b-fb2c-11f0-8e56-0c9a3c9f30ca
   
4. 设置请求头:
   - `Content-Type: application/json`
   - `Authorization: Bearer {access_token}`
   - 将 `{access_token}` 替换为测试2（登录接口）获取的token
   
5. 设置请求体:
   ```json
   {
     "full_name": "修改后的昵称",
     "password": "newpassword123"
   }
   ```
   
6. 点击发送请求

### 测试结果
```json
{
	"code": 200,
	"message": "Success",
	"data": {
		"hashed_password": "$2b$12$u1jx8g6H9.jtzxLI/gKnuu5TxW75p3.E0YACc1v3Q0F4Zb5gbUJJe",
		"email": "jiangkuanli@123.com",
		"username": "jiangkuanli_2",
		"full_name": "ljk",
		"created_at": "2026-01-27T02:58:57.759030+00:00",
		"id": "1fe8b02b-fb2c-11f0-8e56-0c9a3c9f30ca",
		"is_active": true,
		"is_superuser": false,
		"updated_at": "2026-01-27T03:11:30.800074+00:00"
	}
}
```



![image-20260127111158128](C:\Users\ljk\Desktop\GitLab\assets\image-20260127111158128.png)

## 测试4: 查询用户详情接口

### 操作步骤
1. 创建新请求
2. 设置请求方法: `GET`
3. 设置请求URL: `http://localhost:19088/api/v1/users/{user_id}`
   - 将 `{user_id}` 替换为测试1（注册接口）返回的用户ID
4. 设置请求头:
   - `Authorization: Bearer {access_token}`
   - 将 `{access_token}` 替换为测试2（登录接口）获取的token
5. 点击发送请求

### 测试结果
```json
{
	"code": 200,
	"message": "Success",
	"data": {
		"hashed_password": "$2b$12$u1jx8g6H9.jtzxLI/gKnuu5TxW75p3.E0YACc1v3Q0F4Zb5gbUJJe",
		"email": "jiangkuanli@123.com",
		"username": "jiangkuanli_2",
		"full_name": "ljk",
		"created_at": "2026-01-27T02:58:57.759030+00:00",
		"id": "1fe8b02b-fb2c-11f0-8e56-0c9a3c9f30ca",
		"is_active": true,
		"is_superuser": false,
		"updated_at": "2026-01-27T03:11:30.800074+00:00"
	}
}
```

![image-20260127111853640](./assets/image-20260127111853640.png)

## 测试5: 查询用户列表接口

### 操作步骤
1. 创建新请求
2. 设置请求方法: `GET`
3. 设置请求URL: `http://localhost:19088/api/v1/users/?skip=0&limit=100`
4. 设置请求头:
   - `Authorization: Bearer {access_token}`
   - 将 `{access_token}` 替换为测试2（登录接口）获取的token
5. 点击发送请求

### 测试结果
```json
{
	"code": 200,
	"message": "Success",
	"data": [
		{
			"hashed_password": "$2b$12$EcmpGyPTH/pwAe7zDPr/UuJ880DliLXnFmy.wbScm1TVqJet5f.0W",
			"email": "testuser@example.com",
			"username": "testuser",
			"full_name": "测试用户",
			"created_at": "2026-01-26T13:46:28.818814+00:00",
			"id": "6a21a172-fabd-11f0-ab96-9408534bfc68",
			"is_active": true,
			"is_superuser": false,
			"updated_at": null
		},
		{
			"hashed_password": "$2b$12$UnBp1FPwsD/zXCU/xbkMgu5.jhnENzTFsyBnynpdGT1Wqol05GMAO",
			"email": "testuser2@example.com",
			"username": "testuser2",
			"full_name": "测试用户",
			"created_at": "2026-01-26T14:12:12.519492+00:00",
			"id": "020e3975-fac1-11f0-8082-9408534bfc68",
			"is_active": true,
			"is_superuser": false,
			"updated_at": null
		},
		{
			"hashed_password": "$2b$12$i/CSGzOeaX012rJ8JCMgR.aRSbOOn9ugzX2feqpk0FJfteszsOUZG",
			"email": "admin@bx.com",
			"username": "user_admin",
			"full_name": "李四修改后",
			"created_at": "2026-01-26T13:24:22.806463+00:00",
			"id": "d2e96bf6-7273-11f0-8553-3c7c3f4b902b",
			"is_active": true,
			"is_superuser": true,
			"updated_at": "2026-01-27T02:49:54.047151+00:00"
		},
		{
			"hashed_password": "$2b$12$i2dTTjDTpqZedDr3GOzDcOB47gHRRT6gUWk1loFDx2.Y8Eyci90mW",
			"email": "jiangkuanli@example.com",
			"username": "jiangkuanli",
			"full_name": "jiangkuanli",
			"created_at": "2026-01-27T02:56:01.931315+00:00",
			"id": "b71e3ece-fb2b-11f0-bd0f-0c9a3c9f30ca",
			"is_active": true,
			"is_superuser": false,
			"updated_at": null
		},
		{
			"hashed_password": "$2b$12$LN0yujd8XQYW6P9uPfsiy.6gCl/lZeEpkoGzP81PAaA0otLf35goy",
			"email": "jiangkuanli@163.com",
			"username": "jiangkuanli_1",
			"full_name": "jiangkuanli",
			"created_at": "2026-01-27T02:56:53.419447+00:00",
			"id": "d5cb645e-fb2b-11f0-b588-0c9a3c9f30ca",
			"is_active": true,
			"is_superuser": false,
			"updated_at": null
		},
		{
			"hashed_password": "$2b$12$u1jx8g6H9.jtzxLI/gKnuu5TxW75p3.E0YACc1v3Q0F4Zb5gbUJJe",
			"email": "jiangkuanli@123.com",
			"username": "jiangkuanli_2",
			"full_name": "ljk",
			"created_at": "2026-01-27T02:58:57.759030+00:00",
			"id": "1fe8b02b-fb2c-11f0-8e56-0c9a3c9f30ca",
			"is_active": true,
			"is_superuser": false,
			"updated_at": "2026-01-27T03:11:30.800074+00:00"
		}
	]
}
```

![image-20260127112321171](./assets/image-20260127112321171.png)

---
