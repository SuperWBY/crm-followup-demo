<template>
  <div id="app">
    <el-container>
      <el-header class="app-header">
        <div class="header-container">
          <!-- 左侧 Logo 和标题 -->
          <div class="header-left">
            <div class="logo-section">
              <div class="logo-icon">
                <el-icon size="32"><TrendCharts /></el-icon>
              </div>
              <div class="logo-text">
                <h1 class="app-title">CRM 客户跟进系统</h1>
                <span class="app-subtitle">WallTech 跨境物流 SaaS 平台</span>
              </div>
            </div>
          </div>

          <!-- 右侧用户信息和状态 -->
          <div class="header-right">
            <!-- 系统状态指示器 -->
            <div class="status-indicators">
              <div class="status-item">
                <el-icon class="status-icon"><Connection /></el-icon>
                <span class="status-text">在线</span>
              </div>
              <div class="status-item dev-mode">
                <el-icon class="status-icon"><Tools /></el-icon>
                <span class="status-text">开发模式</span>
              </div>
            </div>

            <!-- 通知和设置 -->
            <div class="header-actions">
              <el-button type="text" class="action-btn" @click="handleNotifications">
                <el-icon><Bell /></el-icon>
                <el-badge :value="notificationCount" :hidden="notificationCount === 0" />
              </el-button>
              
              <el-dropdown @command="handleUserAction" trigger="click">
                <el-button type="text" class="action-btn user-btn">
                  <el-avatar :size="32" class="user-avatar">
                    <el-icon><User /></el-icon>
                  </el-avatar>
                  <span class="user-name">管理员</span>
                  <el-icon><ArrowDown /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="profile">
                      <el-icon><User /></el-icon>
                      个人资料
                    </el-dropdown-item>
                    <el-dropdown-item command="settings">
                      <el-icon><Setting /></el-icon>
                      系统设置
                    </el-dropdown-item>
                    <el-dropdown-item divided command="logout">
                      <el-icon><SwitchButton /></el-icon>
                      退出登录
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
        </div>

        <!-- 开发模式横幅 -->
        <div class="dev-banner" v-if="isDevMode">
          <div class="dev-banner-content">
            <el-icon class="dev-icon"><Tools /></el-icon>
            <span>开发模式 - 实时热重载已启用</span>
            <el-button type="text" size="small" @click="isDevMode = false" class="close-btn">
              <el-icon><Close /></el-icon>
            </el-button>
          </div>
        </div>
      </el-header>
      
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()

// 响应式数据
const isDevMode = ref(true)
const notificationCount = ref(3)

// 通知处理
const handleNotifications = () => {
  ElMessage.info('通知中心功能开发中...')
}

// 用户操作处理
const handleUserAction = (command) => {
  switch (command) {
    case 'profile':
      ElMessage.info('个人资料功能开发中...')
      break
    case 'settings':
      ElMessage.info('系统设置功能开发中...')
      break
    case 'logout':
      ElMessage.success('已退出登录')
      break
  }
}

onMounted(() => {
  console.log('CRM FollowUp System initialized')
})
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #1e3a8a 0%, #3B82F6 50%, #1E90FF 100%);
  color: white;
  position: relative;
  box-shadow: 0 4px 20px rgba(59, 130, 246, 0.2);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.app-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="rgba(255,255,255,0.03)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
  pointer-events: none;
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 64px;
  position: relative;
  z-index: 1;
}

/* 左侧 Logo 区域 */
.header-left {
  display: flex;
  align-items: center;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.app-title {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.025em;
  line-height: 1.2;
}

.app-subtitle {
  font-size: 12px;
  opacity: 0.8;
  font-weight: 400;
  margin-top: 2px;
}


/* 右侧用户信息区域 */
.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.status-indicators {
  display: flex;
  gap: 12px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
}

.status-item.dev-mode {
  background: rgba(245, 158, 11, 0.2);
  border-color: rgba(245, 158, 11, 0.3);
}

.status-icon {
  font-size: 14px;
}

.status-text {
  font-size: 12px;
  font-weight: 500;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.action-btn {
  color: rgba(255, 255, 255, 0.9) !important;
  padding: 8px 12px !important;
  border-radius: 8px !important;
  transition: all 0.2s ease !important;
  border: 1px solid transparent !important;
}

.action-btn:hover {
  color: white !important;
  background: rgba(255, 255, 255, 0.1) !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
  transform: translateY(-1px);
}

.user-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 12px !important;
}

.user-avatar {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
}

/* 开发模式横幅 */
.dev-banner {
  background: linear-gradient(90deg, #F59E0B, #FBBF24);
  color: white;
  padding: 8px 0;
  position: relative;
  z-index: 1;
}

.dev-banner-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 500;
}

.dev-icon {
  font-size: 16px;
}

.close-btn {
  color: white !important;
  padding: 2px 8px !important;
  margin-left: 12px;
  border-radius: 4px !important;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2) !important;
}

.el-main {
  padding: 24px;
  background-color: #FAFAFA;
  min-height: calc(100vh - 64px);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .header-container {
    padding: 0 16px;
  }
}

@media (max-width: 768px) {
  .header-container {
    padding: 0 12px;
    height: 56px;
  }
  
  .app-title {
    font-size: 16px;
  }
  
  .app-subtitle {
    font-size: 11px;
  }
  
  .logo-icon {
    width: 32px;
    height: 32px;
  }
  
  .status-indicators {
    gap: 8px;
  }
  
  .status-item {
    padding: 4px 8px;
  }
  
  .status-text {
    display: none;
  }
  
  .user-name {
    display: none;
  }
  
  .el-main {
    padding: 16px;
    min-height: calc(100vh - 56px);
  }
}

@media (max-width: 480px) {
  .header-container {
    padding: 0 8px;
  }
  
  .logo-section {
    gap: 8px;
  }
  
  .header-actions {
    gap: 4px;
  }
  
  .action-btn {
    padding: 6px 8px !important;
  }
}
</style>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  background-color: #FAFAFA;
}

/* 自定义CSS变量 */
:root {
  --primary-blue: #3B82F6;
  --primary-blue-light: #1E90FF;
  --secondary-gray-light: #F5F5F5;
  --secondary-gray-text: #9CA3AF;
  --secondary-gray-border: #E5E7EB;
  --background-white: #FFFFFF;
  --background-light: #FAFAFA;
  --success-green: #10B981;
  --warning-orange: #F59E0B;
  --error-red: #EF4444;
}

/* Element Plus 组件样式覆盖 */
.el-button--primary {
  background-color: var(--primary-blue);
  border-color: var(--primary-blue);
  border-radius: 8px;
  font-weight: 500;
  padding: 12px 20px;
  transition: all 0.2s ease;
}

.el-button--primary:hover {
  background-color: var(--primary-blue-light);
  border-color: var(--primary-blue-light);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.el-card {
  border-radius: 12px;
  border: 1px solid var(--secondary-gray-border);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.el-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.el-table {
  border-radius: 8px;
  overflow: hidden;
}

.el-table th {
  background-color: var(--secondary-gray-light);
  color: var(--secondary-gray-text);
  font-weight: 600;
  border-bottom: 1px solid var(--secondary-gray-border);
}

.el-input__wrapper {
  border-radius: 8px;
  border: 1px solid var(--secondary-gray-border);
  transition: all 0.2s ease;
}

.el-input__wrapper:hover {
  border-color: var(--primary-blue);
}

.el-input__wrapper.is-focus {
  border-color: var(--primary-blue);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

.el-tag {
  border-radius: 6px;
  font-weight: 500;
  border: none;
}

.el-tag--success {
  background-color: rgba(16, 185, 129, 0.1);
  color: var(--success-green);
}

.el-tag--warning {
  background-color: rgba(245, 158, 11, 0.1);
  color: var(--warning-orange);
}

.el-tag--danger {
  background-color: rgba(239, 68, 68, 0.1);
  color: var(--error-red);
}

.el-tag--info {
  background-color: rgba(59, 130, 246, 0.1);
  color: var(--primary-blue);
}
</style>

