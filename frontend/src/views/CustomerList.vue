<template>
  <div class="customer-list">
    <!-- 页面标题和操作栏 -->
    <div class="page-header">
      <div class="header-content">
        <h1>客户管理</h1>
        <p>管理您的客户信息和跟进记录</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="handleAddCustomer">
          <el-icon><Plus /></el-icon>
          添加客户
        </el-button>
        <el-button type="default" @click="refreshCustomers">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <!-- 简单搜索栏 -->
    <div class="search-section">
      <el-input
        v-model="searchQuery"
        placeholder="搜索客户名称、联系人、公司或电话..."
        size="large"
        clearable
        @input="handleSearch"
        class="search-input"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <!-- 客户列表内容 -->
    <div v-loading="loading" class="customers-content">
      <!-- 网格视图 -->
      <div v-if="viewMode === 'grid'" class="customers-grid">
        <CustomerCard
          v-for="customer in filteredCustomers"
          :key="customer.id"
          :customer="customer"
          @view="viewCustomer"
          @call="handleQuickCall"
          @email="handleQuickEmail"
          @followup="handleQuickFollowup"
          @edit="handleQuickEdit"
        />
      </div>

      <!-- 列表视图 -->
      <el-card v-else-if="viewMode === 'list'" class="list-view-card">
        <el-table 
          :data="filteredCustomers" 
          stripe
          style="width: 100%"
          @row-click="handleRowClick"
          class="customer-table"
          table-layout="fixed"
        >
          <el-table-column prop="name" label="客户名称" min-width="200" show-overflow-tooltip>
            <template #default="{ row }">
              <div class="customer-name">
                <el-avatar :size="32" class="table-avatar">{{ row.name.charAt(0) }}</el-avatar>
                <div class="name-info">
                  <div class="name-text">{{ row.name }}</div>
                  <div class="company-text">{{ row.company }}</div>
                </div>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="contact" label="联系人" min-width="120" show-overflow-tooltip>
            <template #default="{ row }">
              <div class="contact-info">
                <el-icon><User /></el-icon>
                <span>{{ row.contact }}</span>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="phone" label="联系电话" min-width="160" show-overflow-tooltip>
            <template #default="{ row }">
              <div class="phone-info">
                <el-icon><Phone /></el-icon>
                <span>{{ row.phone }}</span>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="country" label="国家" width="100" align="center">
            <template #default="{ row }">
              <el-tag :type="getCountryTagType(row.country)" size="small">
                <el-icon><Location /></el-icon>
                {{ row.country }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="created_at" label="创建时间" width="120" align="center">
            <template #default="{ row }">
              <div class="date-info">{{ formatDate(row.created_at) }}</div>
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="120" fixed="right" align="center">
            <template #default="{ row }">
              <div class="table-actions">
                <el-button 
                  type="primary" 
                  size="small"
                  @click.stop="viewCustomer(row)"
                >
                  <el-icon><View /></el-icon>
                  查看详情
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <!-- 空状态 -->
      <el-empty v-if="!loading && filteredCustomers.length === 0" description="暂无客户数据" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { storeToRefs } from 'pinia'
import dayjs from 'dayjs'
import { useCustomerStore } from '../stores/customer'
import CustomerCard from '../components/CustomerCard.vue'

const router = useRouter()
const customerStore = useCustomerStore()

const searchQuery = ref('')
const viewMode = ref('grid')
const { customers, loading, error } = storeToRefs(customerStore)

// 过滤后的客户列表
const filteredCustomers = computed(() => {
  let result = customers.value || []
  
  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(customer => 
      customer.name.toLowerCase().includes(query) ||
      customer.contact.toLowerCase().includes(query) ||
      customer.company.toLowerCase().includes(query) ||
      customer.phone.includes(query)
    )
  }
  
  return result
})

// 获取国家标签类型
const getCountryTagType = (country) => {
  const countryTypes = {
    '中国': 'danger',
    '美国': 'warning', 
    '加拿大': 'success',
    '日本': 'info',
    '德国': 'success',
    '英国': 'info',
    '澳大利亚': 'warning',
    '新加坡': 'success',
    '韩国': 'info'
  }
  return countryTypes[country] || ''
}

// 格式化日期
const formatDate = (date) => {
  return dayjs(date).format('YYYY-MM-DD')
}

// 查看客户详情
const viewCustomer = (customer) => {
  router.push(`/customer/${customer.id}`)
}

// 点击行
const handleRowClick = (row) => {
  viewCustomer(row)
}

// 搜索处理
const handleSearch = () => {
  // 搜索逻辑已在computed中处理
}

// 快速操作处理
const handleQuickCall = (customer) => {
  ElMessage.success(`正在拨打 ${customer.phone}`)
}

const handleQuickEmail = (customer) => {
  ElMessage.info(`正在打开邮件客户端，收件人: ${customer.contact}`)
}

const handleQuickFollowup = (customer) => {
  router.push(`/customer/${customer.id}?action=followup`)
}

const handleQuickEdit = (customer) => {
  ElMessage.info('编辑功能开发中...')
}

// 操作处理
const handleAddCustomer = () => {
  ElMessage.info('添加客户功能开发中...')
}

// 刷新客户列表
const refreshCustomers = async () => {
  await customerStore.fetchCustomers(true)
  if (error.value) {
    ElMessage.error(error.value)
  } else {
    ElMessage.success('客户列表刷新成功')
  }
}

// 组件挂载时获取数据
onMounted(async () => {
  // 强制刷新数据
  await customerStore.fetchCustomers(true)
  if (error.value) {
    ElMessage.error(error.value)
  }
})
</script>

<style scoped>
.customer-list {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0;
}

/* 页面标题样式 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 24px;
  background: var(--background-white);
  border: 1px solid var(--secondary-gray-border);
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.header-content h1 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 700;
  color: #1F2937;
}

.header-content p {
  margin: 0;
  font-size: 14px;
  color: var(--secondary-gray-text);
}

.header-actions {
  display: flex;
  gap: 12px;
}

/* 搜索栏样式 */
.search-section {
  margin-bottom: 24px;
}

.search-input {
  width: 100%;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: 8px;
  border: 2px solid var(--secondary-gray-border);
  transition: all 0.2s ease;
}

.search-input :deep(.el-input__wrapper:hover) {
  border-color: var(--primary-blue);
}

.search-input :deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-blue);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

.customers-content {
  min-height: 400px;
}

/* 网格视图样式 */
.customers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

/* 列表视图样式 */
.list-view-card {
  background: var(--background-white);
  border: 1px solid var(--secondary-gray-border);
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.list-view-card :deep(.el-card__body) {
  padding: 0;
}

.customer-table {
  cursor: pointer;
  width: 100%;
}

.customer-table :deep(.el-table__row:hover) {
  background-color: #F8FAFC;
}

.customer-table :deep(.el-table__row) {
  border-bottom: 1px solid var(--secondary-gray-border);
}

.customer-table :deep(.el-table__row:last-child) {
  border-bottom: none;
}

.customer-table :deep(.el-table th) {
  background-color: var(--secondary-gray-light);
  color: var(--secondary-gray-text);
  font-weight: 600;
  border-bottom: 1px solid var(--secondary-gray-border);
  text-align: center;
}

.customer-table :deep(.el-table td) {
  padding: 12px 8px;
  border-bottom: 1px solid var(--secondary-gray-border);
}

.customer-table :deep(.el-table__body-wrapper) {
  overflow-x: auto;
}

.customer-table :deep(.el-table__header-wrapper) {
  overflow-x: auto;
}

.customer-name {
  display: flex;
  align-items: center;
  gap: 12px;
}

.table-avatar {
  background: var(--primary-blue);
  color: white;
  font-weight: 600;
  flex-shrink: 0;
}

.name-info {
  min-width: 0;
  flex: 1;
}

.name-text {
  font-weight: 600;
  color: #1F2937;
  font-size: 15px;
  line-height: 1.3;
  margin-bottom: 2px;
}

.company-text {
  font-size: 13px;
  color: var(--secondary-gray-text);
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.contact-info,
.phone-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.contact-info .el-icon,
.phone-info .el-icon {
  color: var(--secondary-gray-text);
  font-size: 16px;
  flex-shrink: 0;
}

.date-info {
  font-size: 13px;
  color: var(--secondary-gray-text);
  font-weight: 500;
}

.table-actions .el-button {
  background: var(--primary-blue);
  border-color: var(--primary-blue);
  font-weight: 500;
  border-radius: 6px;
  padding: 6px 12px;
  transition: all 0.2s ease;
}

.table-actions .el-button:hover {
  background: var(--primary-blue-light);
  border-color: var(--primary-blue-light);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

/* 空状态样式 */
.el-empty {
  margin: 60px 0;
  padding: 60px 20px;
}

.el-empty :deep(.el-empty__description) {
  color: var(--secondary-gray-text);
  font-size: 14px;
}

/* 加载状态样式 */
.customers-content :deep(.el-loading-mask) {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(2px);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .customers-grid {
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .customer-list {
    padding: 0 16px;
  }
  
  .customers-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .customer-name {
    gap: 10px;
  }
  
  .name-text {
    font-size: 14px;
  }
  
  .company-text {
    font-size: 12px;
  }
  
  .contact-info,
  .phone-info {
    gap: 6px;
  }
  
  .contact-info .el-icon,
  .phone-info .el-icon {
    font-size: 14px;
  }
  
  .table-actions .el-button {
    padding: 4px 8px;
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .customer-list {
    padding: 0 12px;
  }
  
  .customers-grid {
    gap: 12px;
  }
  
  .list-view-card {
    border-radius: 8px;
  }
}
</style>

