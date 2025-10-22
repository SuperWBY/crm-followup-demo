<template>
  <div class="customer-card" @click="handleCardClick">
    <!-- 客户状态指示器 -->
    <div class="status-indicator" :class="statusClass"></div>
    
    <!-- 卡片头部 -->
    <div class="card-header">
      <div class="customer-avatar">
        <el-avatar :size="48" :src="customerAvatar">
          {{ customer.name.charAt(0) }}
        </el-avatar>
      </div>
      <div class="customer-basic-info">
        <h3 class="customer-name">{{ customer.name }}</h3>
        <p class="customer-company">{{ customer.company }}</p>
      </div>
      <div class="quick-actions">
        <el-dropdown trigger="click" @command="handleQuickAction">
          <el-button type="text" class="more-btn">
            <el-icon><MoreFilled /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="call" icon="Phone">拨打电话</el-dropdown-item>
              <el-dropdown-item command="email" icon="Message">发送邮件</el-dropdown-item>
              <el-dropdown-item command="followup" icon="Edit">添加跟进</el-dropdown-item>
              <el-dropdown-item command="edit" icon="EditPen">编辑信息</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <!-- 卡片内容 -->
    <div class="card-content">
      <!-- 联系人信息 -->
      <div class="info-row">
        <div class="info-item">
          <el-icon class="info-icon"><User /></el-icon>
          <span class="info-label">联系人</span>
          <span class="info-value">{{ customer.contact }}</span>
        </div>
      </div>

      <!-- 电话信息 -->
      <div class="info-row">
        <div class="info-item">
          <el-icon class="info-icon"><Phone /></el-icon>
          <span class="info-label">电话</span>
          <span class="info-value">{{ customer.phone }}</span>
        </div>
      </div>

      <!-- 地区信息 -->
      <div class="info-row">
        <div class="info-item">
          <el-icon class="info-icon"><Location /></el-icon>
          <span class="info-label">地区</span>
          <el-tag :type="getCountryTagType(customer.country)" size="small" class="country-tag">
            {{ customer.country }}
          </el-tag>
        </div>
      </div>

      <!-- 创建时间 -->
      <div class="info-row">
        <div class="info-item">
          <el-icon class="info-icon"><Calendar /></el-icon>
          <span class="info-label">创建时间</span>
          <span class="info-value">{{ formatDate(customer.created_at) }}</span>
        </div>
      </div>
    </div>

    <!-- 卡片底部 -->
    <div class="card-footer">
      <div class="followup-info">
        <el-icon class="followup-icon"><Clock /></el-icon>
        <span class="followup-text">最近跟进: {{ getLastFollowupTime() }}</span>
      </div>
      <el-button type="primary" size="small" @click.stop="viewDetails" class="view-btn">
        查看详情
      </el-button>
    </div>

    <!-- 悬停时的快速操作 -->
    <div class="hover-actions">
      <el-button type="primary" size="small" circle @click.stop="quickCall">
        <el-icon><Phone /></el-icon>
      </el-button>
      <el-button type="success" size="small" circle @click.stop="quickFollowup">
        <el-icon><Edit /></el-icon>
      </el-button>
      <el-button type="info" size="small" circle @click.stop="viewDetails">
        <el-icon><View /></el-icon>
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'

const props = defineProps({
  customer: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['view', 'call', 'email', 'followup', 'edit'])

const router = useRouter()

// 计算客户头像
const customerAvatar = computed(() => {
  // 这里可以集成头像服务，暂时返回null使用默认头像
  return null
})

// 计算状态样式
const statusClass = computed(() => {
  // 根据客户状态返回不同的样式类
  const daysSinceCreated = dayjs().diff(dayjs(props.customer.created_at), 'days')
  if (daysSinceCreated <= 7) return 'status-new'
  if (daysSinceCreated <= 30) return 'status-active'
  return 'status-normal'
})

// 获取国家标签类型
const getCountryTagType = (country) => {
  const countryTypes = {
    '中国': 'danger',
    '美国': 'warning', 
    '加拿大': 'success',
    '日本': 'info'
  }
  return countryTypes[country] || 'info'
}

// 格式化日期
const formatDate = (date) => {
  return dayjs(date).format('YYYY-MM-DD')
}

// 获取最近跟进时间
const getLastFollowupTime = () => {
  // 这里应该从跟进记录中获取最近时间，暂时返回模拟数据
  return '2天前'
}

// 卡片点击事件
const handleCardClick = () => {
  viewDetails()
}

// 快速操作处理
const handleQuickAction = (command) => {
  emit(command, props.customer)
}

// 查看详情
const viewDetails = () => {
  router.push(`/customer/${props.customer.id}`)
  emit('view', props.customer)
}

// 快速拨号
const quickCall = () => {
  ElMessage.success(`正在拨打 ${props.customer.phone}`)
  emit('call', props.customer)
}

// 快速跟进
const quickFollowup = () => {
  emit('followup', props.customer)
}
</script>

<style scoped>
.customer-card {
  position: relative;
  background: var(--background-white);
  border: 1px solid var(--secondary-gray-border);
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.customer-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border-color: var(--primary-blue);
}

.status-indicator {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  border-radius: 12px 12px 0 0;
}

.status-indicator.status-new {
  background: linear-gradient(90deg, #10B981, #34D399);
}

.status-indicator.status-active {
  background: linear-gradient(90deg, #3B82F6, #60A5FA);
}

.status-indicator.status-normal {
  background: linear-gradient(90deg, #9CA3AF, #D1D5DB);
}

.card-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 20px;
}

.customer-avatar {
  flex-shrink: 0;
}

.customer-basic-info {
  flex: 1;
  min-width: 0;
}

.customer-name {
  margin: 0 0 4px 0;
  font-size: 18px;
  font-weight: 600;
  color: #1F2937;
  line-height: 1.3;
}

.customer-company {
  margin: 0;
  font-size: 14px;
  color: var(--secondary-gray-text);
  line-height: 1.4;
}

.quick-actions {
  flex-shrink: 0;
}

.more-btn {
  color: var(--secondary-gray-text);
  padding: 4px;
}

.more-btn:hover {
  color: var(--primary-blue);
  background: rgba(59, 130, 246, 0.1);
}

.card-content {
  margin-bottom: 20px;
}

.info-row {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.info-row:last-child {
  margin-bottom: 0;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 0;
}

.info-icon {
  color: var(--secondary-gray-text);
  font-size: 16px;
  flex-shrink: 0;
}

.info-label {
  font-size: 12px;
  color: var(--secondary-gray-text);
  font-weight: 500;
  min-width: 60px;
  flex-shrink: 0;
}

.info-value {
  font-size: 14px;
  color: #1F2937;
  font-weight: 500;
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.country-tag {
  font-weight: 500;
  border: none;
  padding: 2px 8px;
  font-size: 12px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid var(--secondary-gray-border);
}

.followup-info {
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
}

.followup-icon {
  color: var(--secondary-gray-text);
  font-size: 14px;
}

.followup-text {
  font-size: 12px;
  color: var(--secondary-gray-text);
}

.view-btn {
  background: var(--primary-blue);
  border-color: var(--primary-blue);
  font-weight: 500;
  padding: 6px 16px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.view-btn:hover {
  background: var(--primary-blue-light);
  border-color: var(--primary-blue-light);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.hover-actions {
  position: absolute;
  top: 50%;
  right: 20px;
  transform: translateY(-50%) translateX(100px);
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: all 0.3s ease;
  opacity: 0;
}

.customer-card:hover .hover-actions {
  transform: translateY(-50%) translateX(0);
  opacity: 1;
}

.hover-actions .el-button {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .customer-card {
    padding: 16px;
  }
  
  .card-header {
    gap: 12px;
    margin-bottom: 16px;
  }
  
  .customer-name {
    font-size: 16px;
  }
  
  .info-row {
    margin-bottom: 10px;
  }
  
  .hover-actions {
    display: none;
  }
  
  .card-footer {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .followup-info {
    justify-content: center;
  }
}
</style>
