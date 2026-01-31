# AI Chat Frontend

基于 React + TypeScript + Vite 的 AI 对话前端应用，仿照 KimiUI 设计风格。

## 功能特性

- 用户认证（登录/注册）
- 对话管理（创建、删除、查询）
- 多轮对话支持
- 流式响应展示（SSE）
- LangChain 集成（对话总结、上下文管理）
- 现代化 UI 设计（仿照 KimiUI）
- 响应式布局

## 技术栈

- React 18
- TypeScript
- Vite
- Ant Design 5
- React Router
- Axios
- EventSource

## 安装依赖

```bash
cd frontend
npm install
```

## 开发

```bash
npm run dev
```

应用将在 http://localhost:3000 启动

## 构建

```bash
npm run build
```

## 预览

```bash
npm run preview
```

## 配置

### API 代理

前端通过 Vite 代理将 `/api` 请求转发到后端 API（默认 http://localhost:19088）。

在 `vite.config.ts` 中修改代理配置：

```typescript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:19088',  // 修改为你的后端地址
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api')
      }
    }
  }
})
```

## 项目结构

```
frontend/
├── src/
│   ├── components/       # 可复用组件
│   ├── pages/          # 页面组件
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   └── Chat.tsx
│   ├── services/        # API 服务
│   │   └── api.ts
│   ├── hooks/          # 自定义 Hooks
│   │   └── useAuth.ts
│   ├── types/          # TypeScript 类型定义
│   │   └── index.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── index.html
├── package.json
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```

## 使用说明

### 1. 登录

访问 http://localhost:3000/login，输入用户名和密码登录。

### 2. 创建对话

点击"新建对话"按钮创建新的对话。

### 3. 发送消息

在输入框中输入消息，按 Enter 发送，Shift + Enter 换行。

### 4. 查看对话总结

点击"总结"按钮查看当前对话的总结。

### 5. 查看对话上下文

点击"上下文"按钮查看当前对话的上下文信息。

### 6. 删除对话

在对话列表中点击删除按钮删除对话。

## 注意事项

- 确保 后端 API 服务已启动
- 确保 已配置有效的 DeepSeek API 密钥（用于 LangChain 功能）
- 浏览器需要支持 EventSource（现代浏览器都支持）

## 浏览器支持

- Chrome (推荐)
- Firefox
- Safari
- Edge
