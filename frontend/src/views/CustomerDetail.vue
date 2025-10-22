<template>
  <div class="customer-detail">
    <!-- 返回按钮 -->
    <el-button 
      type="info" 
      plain 
      @click="goBack"
      class="back-button"
    >
      <el-icon><ArrowLeft /></el-icon>
      返回客户列表
    </el-button>

    <!-- 客户基本信息 -->
    <el-card class="customer-info-card" v-loading="loading">
      <template #header>
        <div class="card-header">
          <h2>客户信息</h2>
          <div class="header-actions">
            <el-button type="default" @click="goToKPI" class="kpi-btn">
              <el-icon><TrendCharts /></el-icon>
              查看KPI
            </el-button>
            <el-button type="primary" @click="showAddFollowupDialog = true" class="add-followup-btn">
              <el-icon><Plus /></el-icon>
              新增跟进记录
            </el-button>
          </div>
        </div>
      </template>

      <div v-if="customer" class="customer-info">
        <!-- 客户状态栏 -->
        <div class="customer-status-bar">
          <div class="status-left">
            <div class="customer-avatar">
              <el-avatar :size="60" class="customer-avatar-img">
                {{ customer.name.charAt(0) }}
              </el-avatar>
              <div class="status-indicator" :class="getCustomerStatusClass(customer)">
                <el-icon><CircleFilled /></el-icon>
              </div>
            </div>
            <div class="customer-title">
              <h1 class="customer-name">{{ customer.name }}</h1>
              <div class="customer-tags">
                <el-tag type="primary" size="small">活跃客户</el-tag>
                <el-tag type="success" size="small">物流行业</el-tag>
                <el-tag type="warning" size="small">重要客户</el-tag>
              </div>
            </div>
          </div>
          <div class="status-right">
            <div class="quick-actions">
              <el-button type="primary" size="small" @click="handleQuickCall">
                <el-icon><Phone /></el-icon>
                拨打电话
              </el-button>
              <el-button type="success" size="small" @click="handleQuickEmail">
                <el-icon><Message /></el-icon>
                发送邮件
              </el-button>
              <el-button type="warning" size="small" @click="handleCreateTask">
                <el-icon><Calendar /></el-icon>
                创建任务
              </el-button>
            </div>
          </div>
        </div>

        <div class="info-grid">
          <div class="info-item">
            <label>客户名称</label>
            <div class="info-value">
              <el-icon><OfficeBuilding /></el-icon>
              {{ customer.name }}
            </div>
          </div>
          <div class="info-item">
            <label>联系人</label>
            <div class="info-value">
              <el-icon><User /></el-icon>
              {{ customer.contact }}
            </div>
          </div>
          <div class="info-item">
            <label>联系电话</label>
            <div class="info-value">
              <el-icon><Phone /></el-icon>
              {{ customer.phone }}
            </div>
          </div>
          <div class="info-item">
            <label>所属公司</label>
            <div class="info-value">
              <el-icon><Building /></el-icon>
              {{ customer.company }}
            </div>
          </div>
          <div class="info-item">
            <label>国家/地区</label>
            <div class="info-value">
              <el-icon><Location /></el-icon>
              <el-tag :type="getCountryTagType(customer.country)" class="followup-type-tag">
                {{ customer.country }}
              </el-tag>
            </div>
          </div>
          <div class="info-item">
            <label>创建时间</label>
            <div class="info-value">
              <el-icon><Calendar /></el-icon>
              {{ formatDate(customer.created_at) }}
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 智能提醒和任务 -->
    <el-card class="reminder-card">
      <template #header>
        <div class="card-header">
          <h2>智能提醒</h2>
          <el-button type="text" size="small" @click="showAllReminders = !showAllReminders">
            {{ showAllReminders ? '收起' : '展开全部' }}
          </el-button>
        </div>
      </template>

      <div class="reminder-list">
        <div 
          v-for="reminder in reminders" 
          :key="reminder.id"
          class="reminder-item"
          :class="{ 'high-priority': reminder.priority === 'high' }"
        >
          <div class="reminder-icon">
            <el-icon :class="getReminderIconClass(reminder.type)">
              <component :is="getReminderIcon(reminder.type)" />
            </el-icon>
          </div>
          <div class="reminder-content">
            <div class="reminder-title">{{ reminder.title }}</div>
            <div class="reminder-time">{{ formatReminderTime(reminder.time) }}</div>
          </div>
          <div class="reminder-actions">
            <el-button type="text" size="small" @click="handleReminderAction(reminder)">
              处理
            </el-button>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 跟进时间线分析 -->
    <el-card class="timeline-analysis-card">
      <template #header>
        <div class="card-header">
          <h2>跟进时间线分析</h2>
          <div class="analysis-actions">
            <el-button type="text" size="small" @click="exportTimelineData">
              <el-icon><Download /></el-icon>
              导出数据
            </el-button>
          </div>
        </div>
      </template>

      <div class="timeline-analysis-content">
        <div class="analysis-stats-grid">
          <div class="analysis-stat-item">
            <div class="stat-icon">
              <el-icon><TrendCharts /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ timelineAnalysis.avgInterval }}天</div>
              <div class="stat-label">平均跟进间隔</div>
            </div>
          </div>
          
          <div class="analysis-stat-item">
            <div class="stat-icon">
              <el-icon><Calendar /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ timelineAnalysis.totalDays }}天</div>
              <div class="stat-label">跟进总时长</div>
            </div>
          </div>
          
          <div class="analysis-stat-item">
            <div class="stat-icon">
              <el-icon><Clock /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ timelineAnalysis.lastFollowupDays }}天前</div>
              <div class="stat-label">最后跟进时间</div>
            </div>
          </div>
          
          <div class="analysis-stat-item">
            <div class="stat-icon">
              <el-icon><Star /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ timelineAnalysis.bestDay }}</div>
              <div class="stat-label">最佳跟进日</div>
            </div>
          </div>
        </div>

        <!-- 跟进频率图表 -->
        <div class="followup-frequency-chart">
          <h4>跟进频率趋势</h4>
          <div class="frequency-bars">
            <div 
              v-for="(item, index) in timelineAnalysis.frequencyData" 
              :key="index"
              class="frequency-bar"
            >
              <div class="bar-container">
                <div 
                  class="bar" 
                  :style="{ height: `${(item.count / timelineAnalysis.maxFrequency) * 100}%` }"
                ></div>
              </div>
              <div class="bar-label">{{ item.period }}</div>
              <div class="bar-count">{{ item.count }}</div>
            </div>
          </div>
        </div>
      </div>
    </el-card>

     <!-- 客户KPI统计 -->
     <el-card class="customer-kpi-card" v-loading="kpiLoading">
       <template #header>
         <div class="card-header">
           <h2>客户跟进统计</h2>
           <div class="header-controls">
             <div class="kpi-period-selector">
               <el-button-group>
                 <el-button 
                   :type="kpiPeriod === 'daily' ? 'primary' : 'default'"
                   size="small"
                   @click="kpiPeriod = 'daily'; fetchCustomerKPI()"
                 >
                   今日
                 </el-button>
                 <el-button 
                   :type="kpiPeriod === 'weekly' ? 'primary' : 'default'"
                   size="small"
                   @click="kpiPeriod = 'weekly'; fetchCustomerKPI()"
                 >
                   本周
                 </el-button>
                 <el-button 
                   :type="kpiPeriod === 'monthly' ? 'primary' : 'default'"
                   size="small"
                   @click="kpiPeriod = 'monthly'; fetchCustomerKPI()"
                 >
                   本月
                 </el-button>
               </el-button-group>
             </div>
             <el-button 
               type="text" 
               size="small" 
               @click="isKPICollapsed = !isKPICollapsed"
               class="collapse-btn"
             >
               <el-icon>
                 <component :is="isKPICollapsed ? 'ArrowDown' : 'ArrowUp'" />
               </el-icon>
               {{ isKPICollapsed ? '展开' : '收起' }}
             </el-button>
           </div>
         </div>
       </template>

       <div v-show="!isKPICollapsed" class="kpi-content">
         <div class="kpi-stats-grid">
           <div class="kpi-stat-item positive">
             <div class="stat-icon">
               <el-icon><Check /></el-icon>
             </div>
             <div class="stat-content">
               <div class="stat-value">{{ customerKPI.positiveRate }}%</div>
               <div class="stat-label">积极进展率</div>
               <div class="stat-detail">{{ customerKPI.positiveFollowups }}条积极进展</div>
             </div>
           </div>

           <div class="kpi-stat-item pending">
             <div class="stat-icon">
               <el-icon><Clock /></el-icon>
             </div>
             <div class="stat-content">
               <div class="stat-value">{{ customerKPI.pendingRate }}%</div>
               <div class="stat-label">待跟进率</div>
               <div class="stat-detail">{{ customerKPI.pendingFollowups }}条待跟进</div>
             </div>
           </div>

           <div class="kpi-stat-item negative">
             <div class="stat-icon">
               <el-icon><Close /></el-icon>
             </div>
             <div class="stat-content">
               <div class="stat-value">{{ customerKPI.negativeRate }}%</div>
               <div class="stat-label">阻碍率</div>
               <div class="stat-detail">{{ customerKPI.negativeFollowups }}条遇到阻碍</div>
             </div>
           </div>

           <div class="kpi-stat-item">
             <div class="stat-icon">
               <el-icon><Timer /></el-icon>
             </div>
             <div class="stat-content">
               <div class="stat-value">{{ customerKPI.avgDuration }}分钟</div>
               <div class="stat-label">平均时长</div>
             </div>
           </div>

           <div class="kpi-stat-item">
             <div class="stat-icon">
               <el-icon><User /></el-icon>
             </div>
             <div class="stat-content">
               <div class="stat-value">{{ customerKPI.salesUserCount }}</div>
               <div class="stat-label">参与销售</div>
             </div>
           </div>
         </div>
      </div>

      <!-- 跟进结果分布 -->
      <div class="followup-result-stats">
        <h4>跟进结果分布</h4>
        <div class="result-stats-grid">
          <div class="result-category positive-category">
            <div class="category-header">
              <el-icon><Check /></el-icon>
              <span>积极进展</span>
              <span class="category-count">{{ customerKPI.positiveFollowups }}</span>
            </div>
            <div class="category-progress">
              <el-progress 
                :percentage="customerKPI.positiveRate" 
                :stroke-width="8"
                :show-text="false"
                color="#10B981"
              />
              <span class="progress-text">{{ customerKPI.positiveRate }}%</span>
            </div>
          </div>
          
          <div class="result-category pending-category">
            <div class="category-header">
              <el-icon><Clock /></el-icon>
              <span>需要跟进</span>
              <span class="category-count">{{ customerKPI.pendingFollowups }}</span>
            </div>
            <div class="category-progress">
              <el-progress 
                :percentage="customerKPI.pendingRate" 
                :stroke-width="8"
                :show-text="false"
                color="#F59E0B"
              />
              <span class="progress-text">{{ customerKPI.pendingRate }}%</span>
            </div>
          </div>
          
          <div class="result-category negative-category">
            <div class="category-header">
              <el-icon><Close /></el-icon>
              <span>遇到阻碍</span>
              <span class="category-count">{{ customerKPI.negativeFollowups }}</span>
            </div>
            <div class="category-progress">
              <el-progress 
                :percentage="customerKPI.negativeRate" 
                :stroke-width="8"
                :show-text="false"
                color="#EF4444"
              />
              <span class="progress-text">{{ customerKPI.negativeRate }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 跟进类型分布 -->
      <div class="followup-type-stats">
        <h4>跟进类型分布</h4>
        <div class="type-stats-list">
          <div 
            v-for="type in followupTypeStats" 
            :key="type.name"
            class="type-stat-item"
          >
            <div class="type-info">
              <div class="type-icon" :class="type.class">
                <el-icon><component :is="type.icon" /></el-icon>
              </div>
              <span class="type-name">{{ type.name }}</span>
            </div>
            <div class="type-count">{{ type.count }}</div>
          </div>
        </div>
       </div>
    </el-card>

    <!-- 销售漏斗分析 -->
    <el-card class="sales-funnel-card">
      <template #header>
        <div class="card-header">
          <h2>销售漏斗分析</h2>
          <div class="header-controls">
            <div class="funnel-actions">
              <el-button type="text" size="small" @click="exportFunnelData">
                <el-icon><Download /></el-icon>
                导出漏斗数据
              </el-button>
            </div>
            <el-button 
              type="text" 
              size="small" 
              @click="isSalesFunnelCollapsed = !isSalesFunnelCollapsed"
              class="collapse-btn"
            >
              <el-icon>
                <component :is="isSalesFunnelCollapsed ? 'ArrowDown' : 'ArrowUp'" />
              </el-icon>
              {{ isSalesFunnelCollapsed ? '展开' : '收起' }}
            </el-button>
          </div>
        </div>
      </template>

      <div v-show="!isSalesFunnelCollapsed" class="funnel-analysis-content">
        <div class="funnel-stages">
          <div 
            v-for="(stage, index) in salesFunnel.stages" 
            :key="index"
            class="funnel-stage"
            :class="{ 'active': stage.isActive, 'completed': stage.isCompleted }"
          >
            <div class="stage-header">
              <div class="stage-icon">
                <el-icon><component :is="stage.icon" /></el-icon>
              </div>
              <div class="stage-info">
                <div class="stage-name">{{ stage.name }}</div>
                <div class="stage-description">{{ stage.description }}</div>
              </div>
              <div class="stage-status">
                <el-tag 
                  :type="stage.statusType" 
                  size="small"
                  v-if="stage.status"
                >
                  {{ stage.status }}
                </el-tag>
              </div>
            </div>
            <div class="stage-progress">
              <el-progress 
                :percentage="stage.progress" 
                :stroke-width="6"
                :show-text="false"
                :color="stage.progressColor"
              />
              <span class="progress-text">{{ stage.progress }}%</span>
            </div>
            <div class="stage-details">
              <div class="detail-item">
                <span class="detail-label">跟进次数:</span>
                <span class="detail-value">{{ stage.followupCount }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">停留时间:</span>
                <span class="detail-value">{{ stage.duration }}天</span>
              </div>
            </div>
          </div>
        </div>

      </div>
    </el-card>

    <!-- 跟进记录时间线 -->
    <el-card class="followup-card">
      <template #header>
        <div class="card-header">
          <h2>跟进记录</h2>
          <div class="header-controls">
            <div class="followup-actions">
              <el-input
                v-model="followupSearchQuery"
                placeholder="搜索跟进记录..."
                size="small"
                style="width: 200px; margin-right: 12px;"
                clearable
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
              <el-select
                v-model="followupFilterType"
                placeholder="筛选类型"
                size="small"
                style="width: 120px; margin-right: 12px;"
                clearable
              >
                <el-option label="全部" value="" />
                <el-option label="电话沟通" value="电话沟通" />
                <el-option label="线上会议" value="线上会议" />
                <el-option label="上门拜访" value="上门拜访" />
                <el-option label="邮件联系" value="邮件联系" />
              </el-select>
              <el-select
                v-model="followupFilterResult"
                placeholder="筛选结果"
                size="small"
                style="width: 140px; margin-right: 12px;"
                clearable
              >
                <el-option label="全部" value="" />
                <el-option-group label="积极进展">
                  <el-option label="客户有意向" value="客户有意向" />
                  <el-option label="需求明确" value="需求明确" />
                  <el-option label="价格接受" value="价格接受" />
                  <el-option label="决策人接触" value="决策人接触" />
                  <el-option label="合同签署" value="合同签署" />
                </el-option-group>
                <el-option-group label="需要跟进">
                  <el-option label="待客户回复" value="待客户回复" />
                  <el-option label="需要内部讨论" value="需要内部讨论" />
                  <el-option label="预算待确认" value="预算待确认" />
                  <el-option label="技术评估中" value="技术评估中" />
                  <el-option label="竞品对比中" value="竞品对比中" />
                </el-option-group>
                <el-option-group label="遇到阻碍">
                  <el-option label="价格超出预算" value="价格超出预算" />
                  <el-option label="需求不匹配" value="需求不匹配" />
                  <el-option label="决策人未接触" value="决策人未接触" />
                  <el-option label="竞品优势明显" value="竞品优势明显" />
                  <el-option label="客户无需求" value="客户无需求" />
                </el-option-group>
              </el-select>
            </div>
            <el-button 
              type="text" 
              size="small" 
              @click="refreshFollowups"
              :loading="followupLoading"
              class="collapse-btn"
            >
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </div>

        <!-- 分页和显示控制 -->
        <div class="followup-controls" v-if="filteredFollowups.length > 0">
          <div class="display-options">
            <el-select
              v-model="itemsPerPage"
              placeholder="每页显示"
              size="small"
              style="width: 100px; margin-right: 12px;"
              @change="handlePageSizeChange"
            >
              <el-option label="5条" :value="5" />
              <el-option label="10条" :value="10" />
              <el-option label="20条" :value="20" />
              <el-option label="50条" :value="50" />
            </el-select>
            
            <span class="total-count">
              共 {{ filteredFollowups.length }} 条记录
            </span>
          </div>

          <div class="pagination-controls">
            <el-pagination
              :current-page="currentPage"
              :page-size="itemsPerPage"
              :total="filteredFollowups.length"
              layout="prev, pager, next"
              :small="true"
              @current-change="handlePageChange"
            />
          </div>
        </div>
      </template>

      <div v-loading="followupLoading" class="followup-content-wrapper">
        <!-- 标题快速索引导航栏 -->
        <div class="title-index-navigation" v-if="filteredFollowups.length > 0">
          <div class="index-header">
            <h4>标题索引</h4>
            <span class="index-count">{{ filteredFollowups.length }}条记录</span>
          </div>
          <div class="index-search">
            <el-input
              v-model="indexSearchQuery"
              placeholder="搜索标题..."
              size="small"
              clearable
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>
          <div class="index-list">
            <div 
              v-for="(followup, index) in filteredIndexItems" 
              :key="followup.id"
              class="index-item"
              :class="{ 'active': activeIndexId === followup.id }"
              @click="scrollToFollowupByTitle(followup.id)"
            >
              <div class="index-number">{{ index + 1 }}</div>
              <div class="index-content">
                <div class="index-title">{{ followup.title }}</div>
                <div class="index-meta">
                  <span class="index-type">{{ followup.type }}</span>
                  <span class="index-date">{{ formatDate(followup.date) }}</span>
                </div>
                <div class="index-result" v-if="followup.result">
                  <el-tag 
                    :type="getResultTagType(followup.result)" 
                    size="small"
                    class="result-tag-mini"
                  >
                    {{ followup.result }}
                  </el-tag>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 时间线 -->
        <div class="timeline-container" v-if="filteredFollowups.length > 0">
          <el-timeline>
          <el-timeline-item
            v-for="followup in paginatedFollowups"
            :key="followup.id"
            :id="`followup-${followup.id}`"
            :timestamp="formatDateTime(followup.date)"
            placement="top"
            :type="getFollowupType(followup.type)"
            :icon="getFollowupIcon(followup.type)"
          >
            <el-card class="followup-item">
              <div class="followup-header">
                <div class="followup-title" v-if="followup.title">
                  <h4>{{ followup.title }}</h4>
                </div>
                <div class="followup-meta">
                  <el-tag :type="getFollowupTagType(followup.type)" size="small" class="followup-type-tag">
                    {{ followup.type }}
                  </el-tag>
                  <span class="sales-user">录入人：{{ followup.sales_user_name || '未知' }}</span>
                  <span class="followup-duration" v-if="followup.duration">
                    <el-icon><Clock /></el-icon>
                    {{ followup.duration }}分钟
                  </span>
                  <el-tag 
                    :type="getResultTagType(followup.result)" 
                    size="small" 
                    class="result-tag"
                    v-if="followup.result"
                  >
                    {{ followup.result }}
                  </el-tag>
                </div>
                <div class="followup-actions">
                  <el-button 
                    type="text" 
                    size="small"
                    @click="editFollowup(followup)"
                    style="color: var(--primary-blue);"
                  >
                    <el-icon><Edit /></el-icon>
                  </el-button>
                  <el-button 
                    type="text" 
                    size="small"
                    @click="deleteFollowup(followup)"
                    style="color: var(--error-red);"
                  >
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
              </div>
              <div class="followup-content">
                {{ followup.content }}
              </div>
              <div class="followup-footer" v-if="followup.next_action">
                <div class="next-action">
                  <el-icon><ArrowRight /></el-icon>
                  <span class="next-action-label">下一步行动：</span>
                  <span class="next-action-content">{{ followup.next_action }}</span>
                </div>
              </div>
            </el-card>
          </el-timeline-item>
          </el-timeline>
        </div>

        <!-- 空状态 -->
        <el-empty v-else-if="followups.length === 0" description="暂无跟进记录" />
        <el-empty v-else description="没有找到匹配的跟进记录" />

        <!-- 快速导航按钮 -->
        <div class="quick-navigation" v-if="filteredFollowups.length > 10">
          <el-button 
            type="primary" 
            circle 
            size="large"
            @click="scrollToTop"
            class="nav-btn top-btn"
            title="回到顶部"
          >
            <el-icon><Top /></el-icon>
          </el-button>
          
          <el-button 
            type="info" 
            circle 
            size="large"
            @click="scrollToBottom"
            class="nav-btn bottom-btn"
            title="到底部"
          >
            <el-icon><Bottom /></el-icon>
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 新增跟进记录对话框 -->
    <AddFollowupDialog
      v-model="showAddFollowupDialog"
      :customer-id="customerId || 0"
      @success="handleFollowupSuccess"
    />

    <!-- 编辑跟进记录对话框 -->
    <EditFollowupDialog
      v-model="showEditFollowupDialog"
      :followup="editingFollowup"
      @success="handleFollowupSuccess"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { storeToRefs } from 'pinia'
import { useCustomerStore } from '../stores/customer'
import { useFollowupStore } from '../stores/followup'
import dayjs from 'dayjs'
import AddFollowupDialog from '../components/AddFollowupDialog.vue'
import EditFollowupDialog from '../components/EditFollowupDialog.vue'

const props = defineProps({
  id: {
    type: String,
    required: true
  }
})

const router = useRouter()
const customerStore = useCustomerStore()
const followupStore = useFollowupStore()

const customerId = computed(() => {
  const id = parseInt(props.id)
  return isNaN(id) ? null : id
})
const customer = ref(null)
const loading = ref(false)
const followupLoading = ref(false)
const showAddFollowupDialog = ref(false)
const showEditFollowupDialog = ref(false)
const editingFollowup = ref(null)

// KPI相关数据
const kpiLoading = ref(false)
const kpiPeriod = ref('monthly')
const customerKPI = ref({
  totalFollowups: 0,
  successRate: 0,
  avgDuration: 0,
  salesUserCount: 0
})
const followupTypeStats = ref([])

// 时间线分析数据
const timelineAnalysis = ref({
  avgInterval: 0,
  totalDays: 0,
  lastFollowupDays: 0,
  bestDay: '',
  frequencyData: [],
  maxFrequency: 0
})

// 销售漏斗分析数据
const salesFunnel = ref({
  stages: []
})

// 新增的优化功能数据
const showAllReminders = ref(false)
const followupSearchQuery = ref('')
const followupFilterType = ref('')
const followupFilterResult = ref('')

// 分页相关数据
const currentPage = ref(1)
const itemsPerPage = ref(5)

// 标题索引相关数据
const indexSearchQuery = ref('')
const activeIndexId = ref(null)

// 折叠状态控制
const isKPICollapsed = ref(true)
const isSalesFunnelCollapsed = ref(true)
const reminders = ref([
  {
    id: 1,
    type: 'followup',
    title: '需要跟进客户反馈',
    time: new Date(Date.now() + 2 * 60 * 60 * 1000), // 2小时后
    priority: 'high'
  },
  {
    id: 2,
    type: 'call',
    title: '电话回访提醒',
    time: new Date(Date.now() + 24 * 60 * 60 * 1000), // 1天后
    priority: 'medium'
  },
  {
    id: 3,
    type: 'meeting',
    title: '产品演示会议',
    time: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000), // 3天后
    priority: 'high'
  },
  {
    id: 4,
    type: 'email',
    title: '发送报价单',
    time: new Date(Date.now() + 6 * 60 * 60 * 1000), // 6小时后
    priority: 'medium'
  },
  {
    id: 5,
    type: 'task',
    title: '准备合同草稿',
    time: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000), // 2天后
    priority: 'high'
  },
  {
    id: 6,
    type: 'call',
    title: '跟进付款进度',
    time: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000), // 5天后
    priority: 'low'
  }
])

const { followups, error: followupError } = storeToRefs(followupStore)

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

// 获取跟进类型
const getFollowupType = (type) => {
  const typeMap = {
    '电话沟通': 'primary',
    '线上会议': 'success',
    '上门拜访': 'warning',
    '邮件联系': 'info'
  }
  return typeMap[type] || 'primary'
}

// 获取跟进标签类型
const getFollowupTagType = (type) => {
  const typeMap = {
    '电话沟通': 'primary',
    '线上会议': 'success',
    '上门拜访': 'warning',
    '邮件联系': 'info'
  }
  return typeMap[type] || 'primary'
}

// 获取跟进结果标签类型
const getResultTagType = (result) => {
  // 积极进展 - 绿色
  const positiveResults = [
    '客户有意向', '需求明确', '价格接受', '决策人接触', '合同签署'
  ]
  
  // 需要跟进 - 橙色
  const pendingResults = [
    '待客户回复', '需要内部讨论', '预算待确认', '技术评估中', '竞品对比中'
  ]
  
  // 遇到阻碍 - 红色
  const negativeResults = [
    '价格超出预算', '需求不匹配', '决策人未接触', '竞品优势明显', '客户无需求'
  ]
  
  // 兼容旧数据
  const legacyResults = {
    '成功': 'success',
    '待跟进': 'warning', 
    '失败': 'danger'
  }
  
  if (legacyResults[result]) {
    return legacyResults[result]
  }
  
  if (positiveResults.includes(result)) {
    return 'success'
  } else if (pendingResults.includes(result)) {
    return 'warning'
  } else if (negativeResults.includes(result)) {
    return 'danger'
  }
  
  return 'info'
}

// 获取跟进图标
const getFollowupIcon = (type) => {
  const iconMap = {
    '电话沟通': 'Phone',
    '线上会议': 'VideoCamera',
    '上门拜访': 'Location',
    '邮件联系': 'Message'
  }
  return iconMap[type] || 'Document'
}

// 格式化日期
const formatDate = (date) => {
  return dayjs(date).format('YYYY-MM-DD')
}

// 格式化日期时间
const formatDateTime = (date) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

// 返回客户列表
const goBack = () => {
  router.push('/')
}

// 跳转到KPI页面
const goToKPI = () => {
  router.push('/kpi')
}

// 客户状态相关方法
const getCustomerStatusClass = (customer) => {
  // 基于最后跟进时间判断客户状态
  const lastFollowup = followups.value?.[0]
  if (!lastFollowup) return 'inactive'
  
  const daysSinceLastContact = Math.floor((new Date() - new Date(lastFollowup.date)) / (1000 * 60 * 60 * 24))
  if (daysSinceLastContact <= 7) return 'active'
  if (daysSinceLastContact <= 30) return 'warning'
  return 'inactive'
}

// 快速操作方法
const handleQuickCall = () => {
  if (customer.value?.phone) {
    window.open(`tel:${customer.value.phone}`)
  } else {
    ElMessage.warning('客户电话信息不完整')
  }
}

const handleQuickEmail = () => {
  ElMessage.info('邮件功能开发中...')
}

const handleCreateTask = () => {
  ElMessage.info('任务创建功能开发中...')
}

// 提醒相关方法
const getReminderIcon = (type) => {
  const icons = {
    followup: 'Clock',
    call: 'Phone',
    meeting: 'VideoCamera',
    email: 'Message',
    task: 'Calendar'
  }
  return icons[type] || 'Bell'
}

const getReminderIconClass = (type) => {
  const classes = {
    followup: 'reminder-followup',
    call: 'reminder-call',
    meeting: 'reminder-meeting',
    email: 'reminder-email',
    task: 'reminder-task'
  }
  return classes[type] || 'reminder-default'
}

const formatReminderTime = (time) => {
  const now = new Date()
  const diff = time.getTime() - now.getTime()
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(hours / 24)
  
  if (days > 0) return `${days}天后`
  if (hours > 0) return `${hours}小时后`
  return '即将到期'
}

const handleReminderAction = (reminder) => {
  ElMessage.info(`处理提醒: ${reminder.title}`)
}

// 跟进记录过滤
const filteredFollowups = computed(() => {
  let result = followups.value || []
  
  // 搜索过滤
  if (followupSearchQuery.value) {
    const query = followupSearchQuery.value.toLowerCase()
    result = result.filter(followup => 
      followup.content.toLowerCase().includes(query) ||
      followup.type.toLowerCase().includes(query) ||
      (followup.result && followup.result.toLowerCase().includes(query)) ||
      (followup.sales_user_name && followup.sales_user_name.toLowerCase().includes(query))
    )
  }
  
  // 类型过滤
  if (followupFilterType.value) {
    result = result.filter(followup => followup.type === followupFilterType.value)
  }
  
  // 结果过滤
  if (followupFilterResult.value) {
    result = result.filter(followup => followup.result === followupFilterResult.value)
  }
  
  return result
})

// 分页后的跟进记录
const paginatedFollowups = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredFollowups.value.slice(start, end)
})

// 标题索引项目（用于导航栏显示）
const indexItems = computed(() => {
  return filteredFollowups.value.map(followup => ({
    id: followup.id,
    title: followup.title || '无标题',
    type: followup.type,
    date: followup.date,
    result: followup.result
  }))
})

// 筛选后的索引项目
const filteredIndexItems = computed(() => {
  if (!indexSearchQuery.value) {
    return indexItems.value
  }
  
  const query = indexSearchQuery.value.toLowerCase()
  return indexItems.value.filter(item => 
    item.title.toLowerCase().includes(query) ||
    item.type.toLowerCase().includes(query) ||
    (item.result && item.result.toLowerCase().includes(query))
  )
})

// 计算时间线分析
const calculateTimelineAnalysis = () => {
  const currentFollowups = followups.value || []
  if (currentFollowups.length === 0) return

  // 按时间排序跟进记录
  const sortedFollowups = [...currentFollowups].sort((a, b) => new Date(a.date) - new Date(b.date))
  
  // 计算平均跟进间隔
  let totalInterval = 0
  let intervalCount = 0
  for (let i = 1; i < sortedFollowups.length; i++) {
    const prevDate = new Date(sortedFollowups[i - 1].date)
    const currDate = new Date(sortedFollowups[i].date)
    const interval = Math.floor((currDate - prevDate) / (1000 * 60 * 60 * 24))
    totalInterval += interval
    intervalCount++
  }
  const avgInterval = intervalCount > 0 ? Math.round(totalInterval / intervalCount) : 0

  // 计算跟进总时长
  const firstDate = new Date(sortedFollowups[0].date)
  const lastDate = new Date(sortedFollowups[sortedFollowups.length - 1].date)
  const totalDays = Math.floor((lastDate - firstDate) / (1000 * 60 * 60 * 24))

  // 计算最后跟进时间
  const now = new Date()
  const lastFollowupDate = new Date(sortedFollowups[sortedFollowups.length - 1].date)
  const lastFollowupDays = Math.floor((now - lastFollowupDate) / (1000 * 60 * 60 * 24))

  // 分析最佳跟进日
  const dayStats = {}
  sortedFollowups.forEach(followup => {
    const day = new Date(followup.date).getDay()
    const dayNames = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
    const dayName = dayNames[day]
    dayStats[dayName] = (dayStats[dayName] || 0) + 1
  })
  const bestDay = Object.keys(dayStats).reduce((a, b) => dayStats[a] > dayStats[b] ? a : b, '周一')

  // 计算跟进频率数据（按周）
  const frequencyData = []
  const weekStats = {}
  sortedFollowups.forEach(followup => {
    const date = new Date(followup.date)
    const weekStart = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay())
    const weekKey = weekStart.toISOString().split('T')[0]
    weekStats[weekKey] = (weekStats[weekKey] || 0) + 1
  })

  // 转换为图表数据
  Object.entries(weekStats).forEach(([week, count]) => {
    const weekDate = new Date(week)
    const period = `${weekDate.getMonth() + 1}/${weekDate.getDate()}`
    frequencyData.push({ period, count })
  })

  const maxFrequency = Math.max(...frequencyData.map(item => item.count), 1)

  timelineAnalysis.value = {
    avgInterval,
    totalDays,
    lastFollowupDays,
    bestDay,
    frequencyData: frequencyData.slice(-8), // 显示最近8周
    maxFrequency
  }
}

// 导出时间线数据
const exportTimelineData = () => {
  const data = {
    customer: customer.value?.name,
    analysis: timelineAnalysis.value,
    followups: followups.value?.map(f => ({
      date: f.date,
      type: f.type,
      result: f.result,
      duration: f.duration,
      sales_user: f.sales_user_name
    }))
  }
  
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${customer.value?.name || '客户'}_时间线分析_${new Date().toISOString().split('T')[0]}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  
  ElMessage.success('时间线数据导出成功')
}

// 计算销售漏斗分析
const calculateSalesFunnel = () => {
  const currentFollowups = followups.value || []
  if (currentFollowups.length === 0) return

  // 定义销售漏斗阶段
  const funnelStages = [
    {
      name: '初步接触',
      description: '首次接触客户，了解基本需求',
      icon: 'User',
      results: ['客户有意向', '需求明确'],
      statusType: 'primary'
    },
    {
      name: '需求确认',
      description: '深入了解客户需求，确认合作意向',
      icon: 'Document',
      results: ['价格接受', '决策人接触'],
      statusType: 'warning'
    },
    {
      name: '方案制定',
      description: '制定详细方案，进行商务谈判',
      icon: 'Edit',
      results: ['技术评估中', '竞品对比中'],
      statusType: 'info'
    },
    {
      name: '合同签署',
      description: '完成合同签署，建立合作关系',
      icon: 'Check',
      results: ['合同签署'],
      statusType: 'success'
    }
  ]

  // 分析每个阶段的状态
  const stages = funnelStages.map((stage, index) => {
    const stageFollowups = currentFollowups.filter(f => 
      stage.results.includes(f.result)
    )
    
    const isCompleted = stageFollowups.length > 0
    const isActive = index === 0 || funnelStages[index - 1].isCompleted
    
    // 计算进度
    let progress = 0
    if (isCompleted) {
      progress = 100
    } else if (isActive) {
      // 根据跟进次数计算进度
      const totalFollowups = currentFollowups.length
      const stageProgress = Math.min((stageFollowups.length / totalFollowups) * 100, 100)
      progress = Math.round(stageProgress)
    }

    // 计算停留时间
    const stageDates = stageFollowups.map(f => new Date(f.date))
    const duration = stageDates.length > 0 ? 
      Math.floor((new Date() - Math.min(...stageDates)) / (1000 * 60 * 60 * 24)) : 0

    return {
      ...stage,
      isCompleted,
      isActive,
      progress,
      followupCount: stageFollowups.length,
      duration,
      status: isCompleted ? '已完成' : isActive ? '进行中' : '未开始',
      progressColor: isCompleted ? '#10B981' : isActive ? '#3B82F6' : '#E5E7EB'
    }
  })

  salesFunnel.value = {
    stages
  }
}

// 导出销售漏斗数据
const exportFunnelData = () => {
  const data = {
    customer: customer.value?.name,
    funnel: salesFunnel.value,
    followups: followups.value?.map(f => ({
      date: f.date,
      type: f.type,
      result: f.result,
      duration: f.duration,
      sales_user: f.sales_user_name
    }))
  }
  
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${customer.value?.name || '客户'}_销售漏斗分析_${new Date().toISOString().split('T')[0]}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  
  ElMessage.success('销售漏斗数据导出成功')
}

// 分页相关方法
const handlePageChange = (page) => {
  currentPage.value = page
  // 滚动到跟进记录区域顶部
  scrollToFollowupSection()
}

const handlePageSizeChange = (size) => {
  itemsPerPage.value = size
  currentPage.value = 1
  // 滚动到跟进记录区域顶部
  scrollToFollowupSection()
}

// 滚动到跟进记录区域
const scrollToFollowupSection = () => {
  const followupSection = document.querySelector('.followup-card')
  if (followupSection) {
    followupSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

// 快速导航方法
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const scrollToBottom = () => {
  window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
}

// 通过标题索引滚动到指定跟进记录
const scrollToFollowupByTitle = (followupId) => {
  activeIndexId.value = followupId
  
  // 找到目标跟进记录所在的页面
  const targetFollowup = filteredFollowups.value.find(f => f.id === followupId)
  if (!targetFollowup) return
  
  const targetIndex = filteredFollowups.value.findIndex(f => f.id === followupId)
  const targetPage = Math.floor(targetIndex / itemsPerPage.value) + 1
  
  // 如果目标记录不在当前页，先切换到目标页
  if (targetPage !== currentPage.value) {
    currentPage.value = targetPage
    // 等待页面更新后再滚动
    setTimeout(() => {
      scrollToTargetFollowup(followupId)
    }, 100)
  } else {
    scrollToTargetFollowup(followupId)
  }
}

// 滚动到目标跟进记录
const scrollToTargetFollowup = (followupId) => {
  const targetElement = document.getElementById(`followup-${followupId}`)
  if (targetElement) {
    targetElement.scrollIntoView({ 
      behavior: 'smooth', 
      block: 'center' 
    })
    
    // 3秒后清除高亮状态
    setTimeout(() => {
      activeIndexId.value = null
    }, 3000)
  }
}

// 获取客户KPI统计
const fetchCustomerKPI = async () => {
  if (!customerId.value) return
  
  kpiLoading.value = true
  try {
    // 计算客户相关的KPI数据
    const currentFollowups = followups.value || []
    
    // 根据时间周期筛选跟进记录
    const now = new Date()
    let startDate = new Date()
    
    if (kpiPeriod.value === 'daily') {
      startDate.setHours(0, 0, 0, 0)
    } else if (kpiPeriod.value === 'weekly') {
      const dayOfWeek = now.getDay()
      startDate = new Date(now.getTime() - dayOfWeek * 24 * 60 * 60 * 1000)
      startDate.setHours(0, 0, 0, 0)
    } else if (kpiPeriod.value === 'monthly') {
      startDate = new Date(now.getFullYear(), now.getMonth(), 1)
    }
    
    const filteredFollowups = currentFollowups.filter(followup => 
      new Date(followup.date) >= startDate
    )
    
    // 计算KPI指标 - 基于新的跟进结果分类
    const totalFollowups = filteredFollowups.length
    
    // 积极进展的跟进结果
    const positiveResults = ['客户有意向', '需求明确', '价格接受', '决策人接触', '合同签署']
    const positiveFollowups = filteredFollowups.filter(f => positiveResults.includes(f.result)).length
    
    // 需要跟进的跟进结果
    const pendingResults = ['待客户回复', '需要内部讨论', '预算待确认', '技术评估中', '竞品对比中']
    const pendingFollowups = filteredFollowups.filter(f => pendingResults.includes(f.result)).length
    
    // 遇到阻碍的跟进结果
    const negativeResults = ['价格超出预算', '需求不匹配', '决策人未接触', '竞品优势明显', '客户无需求']
    const negativeFollowups = filteredFollowups.filter(f => negativeResults.includes(f.result)).length
    
    // 兼容旧数据
    const legacySuccessFollowups = filteredFollowups.filter(f => f.result === '成功').length
    const legacyPendingFollowups = filteredFollowups.filter(f => f.result === '待跟进').length
    const legacyFailedFollowups = filteredFollowups.filter(f => f.result === '失败').length
    
    // 计算综合成功率（积极进展 + 旧的成功数据）
    const totalPositiveFollowups = positiveFollowups + legacySuccessFollowups
    const successRate = totalFollowups > 0 ? (totalPositiveFollowups / totalFollowups * 100) : 0
    
    const totalDuration = filteredFollowups.reduce((sum, f) => sum + (f.duration || 0), 0)
    const avgDuration = totalFollowups > 0 ? (totalDuration / totalFollowups) : 0
    
    // 统计参与销售人员数量
    const salesUserIds = new Set(filteredFollowups.map(f => f.sales_user_id))
    const salesUserCount = salesUserIds.size
    
    customerKPI.value = {
      totalFollowups,
      successRate: Math.round(successRate * 100) / 100,
      avgDuration: Math.round(avgDuration * 100) / 100,
      salesUserCount,
      // 新增详细统计
      positiveFollowups: totalPositiveFollowups,
      pendingFollowups: pendingFollowups + legacyPendingFollowups,
      negativeFollowups: negativeFollowups + legacyFailedFollowups,
      positiveRate: totalFollowups > 0 ? Math.round((totalPositiveFollowups / totalFollowups * 100) * 100) / 100 : 0,
      pendingRate: totalFollowups > 0 ? Math.round(((pendingFollowups + legacyPendingFollowups) / totalFollowups * 100) * 100) / 100 : 0,
      negativeRate: totalFollowups > 0 ? Math.round(((negativeFollowups + legacyFailedFollowups) / totalFollowups * 100) * 100) / 100 : 0
    }
    
    // 统计跟进类型分布
    const typeStats = {}
    filteredFollowups.forEach(followup => {
      const type = followup.type
      typeStats[type] = (typeStats[type] || 0) + 1
    })
    
    const typeIcons = {
      '电话沟通': { icon: 'Phone', class: 'phone' },
      '线上会议': { icon: 'VideoCamera', class: 'meeting' },
      '上门拜访': { icon: 'Location', class: 'visit' },
      '邮件联系': { icon: 'Message', class: 'email' }
    }
    
    followupTypeStats.value = Object.entries(typeStats).map(([name, count]) => ({
      name,
      count,
      ...typeIcons[name] || { icon: 'Document', class: 'other' }
    }))
    
  } catch (error) {
    console.error('Error fetching customer KPI:', error)
    ElMessage.error('获取KPI数据失败')
  } finally {
    kpiLoading.value = false
  }
}

// 刷新跟进记录
const refreshFollowups = async () => {
  await followupStore.fetchFollowups(customerId.value, true)
  if (followupError.value) {
    ElMessage.error(followupError.value)
  }
}

// 编辑跟进记录
const editFollowup = (followup) => {
  editingFollowup.value = followup
  showEditFollowupDialog.value = true
}

// 删除跟进记录
const deleteFollowup = async (followup) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这条跟进记录吗？',
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await followupStore.deleteFollowup(followup.id)
    ElMessage.success('删除成功')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 处理跟进记录成功
const handleFollowupSuccess = () => {
  refreshFollowups()
  fetchCustomerKPI() // 刷新KPI数据
}

// 获取客户详情
const fetchCustomer = async () => {
  loading.value = true
  try {
    customer.value = await customerStore.fetchCustomer(customerId.value)
  } catch (error) {
    ElMessage.error('获取客户详情失败')
  } finally {
    loading.value = false
  }
}

// 监听客户ID变化
watch(customerId, () => {
  if (customerId.value) {
    fetchCustomer()
    refreshFollowups()
    fetchCustomerKPI() // 获取KPI数据
  }
}, { immediate: true })

// 监听跟进记录变化，自动更新KPI、时间线分析和销售漏斗
watch(followups, () => {
  fetchCustomerKPI()
  calculateTimelineAnalysis()
  calculateSalesFunnel()
}, { deep: true })

// 组件挂载时获取数据
onMounted(async () => {
  await fetchCustomer()
  await refreshFollowups()
  await fetchCustomerKPI()
})
</script>

<style scoped>
.customer-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0;
}

.back-button {
  margin-bottom: 24px;
}

.back-button .el-button {
  background: var(--background-white);
  border: 1px solid var(--secondary-gray-border);
  color: var(--secondary-gray-text);
  border-radius: 8px;
  padding: 10px 16px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.back-button .el-button:hover {
  border-color: var(--primary-blue);
  color: var(--primary-blue);
  background: rgba(59, 130, 246, 0.05);
}

.customer-info-card,
.followup-card {
  margin-bottom: 24px;
  background: var(--background-white);
  border: 1px solid var(--secondary-gray-border);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0;
}

.card-header h2 {
  margin: 0;
  color: #1F2937;
  font-size: 20px;
  font-weight: 600;
  letter-spacing: -0.025em;
}

.customer-info {
  padding: 20px 0;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-item label {
  font-size: 13px;
  color: var(--secondary-gray-text);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.info-value {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
  color: #1F2937;
  font-weight: 500;
}

.info-value .el-icon {
  color: var(--primary-blue);
  font-size: 18px;
}


.followup-item {
  margin-bottom: 16px;
  transition: all 0.3s ease;
}


/* 跟进记录标题样式 */
.followup-title {
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--secondary-gray-border);
}

.followup-title h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1F2937;
  line-height: 1.4;
}

.followup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.followup-meta {
  display: flex;
  align-items: center;
  gap: 16px;
}

.followup-type-tag {
  font-weight: 600;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
}

.sales-user {
  font-size: 13px;
  color: var(--secondary-gray-text);
  font-weight: 500;
  background: var(--secondary-gray-light);
  padding: 4px 10px;
  border-radius: 12px;
}

.followup-actions {
  display: flex;
  gap: 8px;
}

.followup-actions .el-button {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
}

/* 分页控制样式 */
.followup-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid var(--secondary-gray-border);
  margin-bottom: 16px;
}

.display-options {
  display: flex;
  align-items: center;
  gap: 12px;
}

.total-count {
  font-size: 14px;
  color: var(--secondary-gray-text);
  font-weight: 500;
}

.pagination-controls {
  display: flex;
  align-items: center;
}

/* 快速导航按钮样式 */
.quick-navigation {
  position: fixed;
  right: 30px;
  bottom: 30px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  z-index: 1000;
}

.nav-btn {
  width: 50px;
  height: 50px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

.nav-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.top-btn {
  background: var(--primary-blue);
  border-color: var(--primary-blue);
}

.bottom-btn {
  background: #909399;
  border-color: #909399;
}

/* 跟进记录内容包装器 */
.followup-content-wrapper {
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

/* 标题索引导航栏 */
.title-index-navigation {
  width: 320px;
  flex-shrink: 0;
  background: var(--secondary-gray-light);
  border-radius: 12px;
  padding: 16px;
  position: sticky;
  top: 20px;
  max-height: 80vh;
  overflow-y: auto;
}

.index-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--secondary-gray-border);
}

.index-header h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1F2937;
}

.index-count {
  font-size: 12px;
  color: var(--secondary-gray-text);
  background: rgba(59, 130, 246, 0.1);
  padding: 4px 8px;
  border-radius: 12px;
  font-weight: 500;
}

.index-search {
  margin-bottom: 16px;
}

.index-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.index-item {
  padding: 12px;
  background: var(--background-white);
  border-radius: 8px;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.index-item:hover {
  border-color: var(--primary-blue);
  background: rgba(59, 130, 246, 0.05);
  transform: translateY(-1px);
}

.index-item.active {
  border-color: var(--primary-blue);
  background: rgba(59, 130, 246, 0.1);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
}

.index-number {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--primary-blue);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.index-item.active .index-number {
  background: var(--primary-blue-light);
}

.index-content {
  flex: 1;
  min-width: 0;
}

.index-title {
  font-size: 14px;
  font-weight: 600;
  color: #1F2937;
  line-height: 1.4;
  margin-bottom: 6px;
  word-break: break-word;
}

.index-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.index-type {
  font-size: 11px;
  color: var(--primary-blue);
  background: rgba(59, 130, 246, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 500;
}

.index-date {
  font-size: 11px;
  color: var(--secondary-gray-text);
  font-weight: 500;
}

.index-result {
  display: flex;
  align-items: center;
}

.result-tag-mini {
  font-size: 9px;
  padding: 1px 4px;
  border-radius: 3px;
}

/* 时间线容器 */
.timeline-container {
  flex: 1;
  min-width: 0;
}

.followup-content {
  line-height: 1.7;
  color: #374151;
  font-size: 14px;
  background: var(--secondary-gray-light);
  padding: 16px;
  border-radius: 8px;
  border-left: 4px solid var(--primary-blue);
}

.followup-duration {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--secondary-gray-text);
  background: rgba(59, 130, 246, 0.1);
  padding: 4px 8px;
  border-radius: 12px;
  font-weight: 500;
}

.followup-duration .el-icon {
  font-size: 12px;
  color: var(--primary-blue);
}

.result-tag {
  font-weight: 600;
  border: none;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
}

.followup-footer {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--secondary-gray-border);
}

.next-action {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #374151;
}

.next-action .el-icon {
  color: var(--primary-blue);
  font-size: 14px;
}

.next-action-label {
  font-weight: 600;
  color: var(--secondary-gray-text);
}

.next-action-content {
  color: #1F2937;
  font-weight: 500;
}

.el-icon {
  color: var(--secondary-gray-text);
}

.el-timeline-item__timestamp {
  color: var(--secondary-gray-text);
  font-size: 13px;
  font-weight: 500;
}

.el-timeline-item__node {
  background: var(--primary-blue);
  border-color: var(--primary-blue);
}

.el-timeline-item__tail {
  border-left-color: var(--secondary-gray-border);
}

.add-followup-btn {
  background: var(--primary-blue);
  border-color: var(--primary-blue);
  border-radius: 8px;
  padding: 12px 20px;
  font-weight: 600;
  transition: all 0.2s ease;
}

.add-followup-btn:hover {
  background: var(--primary-blue-light);
  border-color: var(--primary-blue-light);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

/* 空状态样式 */
.el-empty {
  margin: 40px 0;
  padding: 40px;
}

.el-empty :deep(.el-empty__description) {
  color: var(--secondary-gray-text);
  font-size: 14px;
}

/* 客户状态栏样式 */
.customer-status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-radius: 12px;
  margin-bottom: 24px;
}

.status-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.customer-avatar {
  position: relative;
}

.customer-avatar-img {
  background: var(--primary-blue);
  color: white;
  font-weight: 700;
  font-size: 24px;
}

.status-indicator {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 2px solid white;
}

.status-indicator.active {
  background: var(--success-green);
}

.status-indicator.warning {
  background: var(--warning-orange);
}

.status-indicator.inactive {
  background: var(--secondary-gray-text);
}

.customer-title {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.customer-name {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #1F2937;
}

.customer-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.status-right {
  display: flex;
  align-items: center;
}

.quick-actions {
  display: flex;
  gap: 12px;
}

.quick-actions .el-button {
  border-radius: 8px;
  font-weight: 500;
}

/* 提醒卡片样式 */
.reminder-card {
  background: var(--background-white);
  border: 1px solid var(--secondary-gray-border);
  margin-bottom: 24px;
}

.reminder-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.reminder-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: var(--secondary-gray-light);
  border-radius: 8px;
  transition: all 0.2s ease;
}

.reminder-item:hover {
  background: rgba(59, 130, 246, 0.05);
}

.reminder-item.high-priority {
  border-left: 4px solid var(--error-red);
  background: rgba(239, 68, 68, 0.05);
}

.reminder-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.reminder-icon .reminder-followup {
  background: rgba(59, 130, 246, 0.1);
  color: var(--primary-blue);
}

.reminder-icon .reminder-call {
  background: rgba(16, 185, 129, 0.1);
  color: var(--success-green);
}

.reminder-icon .reminder-meeting {
  background: rgba(245, 158, 11, 0.1);
  color: var(--warning-orange);
}

.reminder-icon .reminder-email {
  background: rgba(239, 68, 68, 0.1);
  color: var(--error-red);
}

.reminder-icon .reminder-task {
  background: rgba(139, 92, 246, 0.1);
  color: #8B5CF6;
}

.reminder-content {
  flex: 1;
}

.reminder-title {
  font-weight: 600;
  color: #1F2937;
  margin-bottom: 4px;
}

.reminder-time {
  font-size: 12px;
  color: var(--secondary-gray-text);
}

.reminder-actions {
  display: flex;
  gap: 8px;
}

/* 时间线分析卡片样式 */
.timeline-analysis-card {
  background: var(--background-white);
  border: 1px solid var(--secondary-gray-border);
  margin-bottom: 24px;
}

.timeline-analysis-content {
  padding: 0;
}

.analysis-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.analysis-stat-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--secondary-gray-light);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.analysis-stat-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.analysis-stat-item .stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
  background: rgba(59, 130, 246, 0.1);
  color: var(--primary-blue);
}

.analysis-stat-item .stat-content {
  flex: 1;
}

.analysis-stat-item .stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #1F2937;
  line-height: 1;
  margin-bottom: 4px;
}

.analysis-stat-item .stat-label {
  font-size: 14px;
  color: var(--secondary-gray-text);
  font-weight: 500;
}

/* 跟进频率图表样式 */
.followup-frequency-chart {
  margin-top: 24px;
}

.followup-frequency-chart h4 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #1F2937;
}

.frequency-bars {
  display: flex;
  align-items: end;
  gap: 12px;
  height: 120px;
  padding: 0 8px;
}

.frequency-bar {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.bar-container {
  width: 100%;
  height: 80px;
  display: flex;
  align-items: end;
  justify-content: center;
}

.bar {
  width: 100%;
  background: linear-gradient(to top, var(--primary-blue), var(--primary-blue-light));
  border-radius: 4px 4px 0 0;
  min-height: 4px;
  transition: all 0.3s ease;
}

.bar:hover {
  background: linear-gradient(to top, var(--primary-blue-light), var(--primary-blue));
  transform: scaleY(1.1);
}

.bar-label {
  font-size: 12px;
  color: var(--secondary-gray-text);
  font-weight: 500;
}

.bar-count {
  font-size: 14px;
  color: #1F2937;
  font-weight: 600;
}

/* 销售漏斗分析卡片样式 */
.sales-funnel-card {
  background: var(--background-white);
  border: 1px solid var(--secondary-gray-border);
  margin-bottom: 24px;
}

.funnel-analysis-content {
  padding: 0;
}

.funnel-stages {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.funnel-stage {
  padding: 20px;
  border-radius: 12px;
  background: var(--secondary-gray-light);
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.funnel-stage.active {
  border-color: var(--primary-blue);
  background: rgba(59, 130, 246, 0.05);
}

.funnel-stage.completed {
  border-color: #10B981;
  background: rgba(16, 185, 129, 0.05);
}

.stage-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.stage-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
  background: rgba(59, 130, 246, 0.1);
  color: var(--primary-blue);
}

.funnel-stage.completed .stage-icon {
  background: rgba(16, 185, 129, 0.1);
  color: #10B981;
}

.stage-info {
  flex: 1;
}

.stage-name {
  font-size: 18px;
  font-weight: 600;
  color: #1F2937;
  margin-bottom: 4px;
}

.stage-description {
  font-size: 14px;
  color: var(--secondary-gray-text);
}

.stage-status {
  flex-shrink: 0;
}

.stage-progress {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.stage-progress .el-progress {
  flex: 1;
}

.progress-text {
  font-size: 14px;
  font-weight: 600;
  color: #1F2937;
  min-width: 40px;
}

.stage-details {
  display: flex;
  gap: 24px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-label {
  font-size: 14px;
  color: var(--secondary-gray-text);
  font-weight: 500;
}

.detail-value {
  font-size: 14px;
  color: #1F2937;
  font-weight: 600;
}


/* KPI卡片样式 */
.customer-kpi-card {
  background: var(--background-white);
  border: 1px solid var(--secondary-gray-border);
  margin-bottom: 24px;
}

.customer-kpi-card .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-controls {
  display: flex;
  align-items: center;
  gap: 16px;
}

.collapse-btn {
  color: #6B7280;
  font-size: 14px;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.collapse-btn:hover {
  color: #374151;
  background-color: #F3F4F6;
}

.customer-kpi-card .card-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1F2937;
}

.kpi-period-selector {
  display: flex;
  align-items: center;
  gap: 8px;
}

.kpi-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.kpi-stat-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--secondary-gray-light);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.kpi-stat-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.kpi-stat-item .stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
  background: rgba(59, 130, 246, 0.1);
  color: var(--primary-blue);
}

.kpi-stat-item .stat-content {
  flex: 1;
}

.kpi-stat-item .stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #1F2937;
  line-height: 1;
  margin-bottom: 4px;
}

.kpi-stat-item .stat-label {
  font-size: 14px;
  color: var(--secondary-gray-text);
  font-weight: 500;
}

.kpi-stat-item .stat-detail {
  font-size: 12px;
  color: var(--secondary-gray-text);
  margin-top: 4px;
}

/* KPI统计项特殊样式 */
.kpi-stat-item.positive .stat-icon {
  background: rgba(16, 185, 129, 0.1);
  color: #10B981;
}

.kpi-stat-item.pending .stat-icon {
  background: rgba(245, 158, 11, 0.1);
  color: #F59E0B;
}

.kpi-stat-item.negative .stat-icon {
  background: rgba(239, 68, 68, 0.1);
  color: #EF4444;
}

/* 跟进结果分布样式 */
.followup-result-stats {
  margin-top: 24px;
}

.followup-result-stats h4 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #1F2937;
}

.result-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.result-category {
  padding: 16px;
  border-radius: 12px;
  background: var(--secondary-gray-light);
  transition: all 0.3s ease;
}

.result-category:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.positive-category {
  border-left: 4px solid #10B981;
}

.pending-category {
  border-left: 4px solid #F59E0B;
}

.negative-category {
  border-left: 4px solid #EF4444;
}

.category-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-weight: 600;
  color: #1F2937;
}

.category-header .el-icon {
  font-size: 16px;
}

.positive-category .category-header .el-icon {
  color: #10B981;
}

.pending-category .category-header .el-icon {
  color: #F59E0B;
}

.negative-category .category-header .el-icon {
  color: #EF4444;
}

.category-count {
  margin-left: auto;
  font-size: 18px;
  font-weight: 700;
  color: #1F2937;
}

.category-progress {
  display: flex;
  align-items: center;
  gap: 12px;
}

.progress-text {
  font-size: 14px;
  font-weight: 600;
  color: #1F2937;
  min-width: 40px;
}

.followup-type-stats {
  margin-top: 24px;
}

.followup-type-stats h4 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #1F2937;
}

.type-stats-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.type-stat-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: var(--secondary-gray-light);
  border-radius: 8px;
  transition: all 0.2s ease;
}

.type-stat-item:hover {
  background: rgba(59, 130, 246, 0.05);
}

.type-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.type-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.type-icon.phone {
  background: rgba(59, 130, 246, 0.1);
  color: var(--primary-blue);
}

.type-icon.meeting {
  background: rgba(16, 185, 129, 0.1);
  color: var(--success-green);
}

.type-icon.visit {
  background: rgba(245, 158, 11, 0.1);
  color: var(--warning-orange);
}

.type-icon.email {
  background: rgba(239, 68, 68, 0.1);
  color: var(--error-red);
}

.type-name {
  font-weight: 500;
  color: #1F2937;
  font-size: 14px;
}

.type-count {
  font-size: 16px;
  font-weight: 700;
  color: var(--primary-blue);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .customer-detail {
    padding: 0 16px;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .followup-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .followup-meta {
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
  }
  
  .kpi-stats-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .type-stats-list {
    grid-template-columns: 1fr;
  }
  
  .customer-kpi-card .card-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .customer-status-bar {
    flex-direction: column;
    gap: 20px;
    align-items: flex-start;
  }
  
  .status-left {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .quick-actions {
    flex-wrap: wrap;
  }
  
  .followup-actions {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .followup-actions .el-input,
  .followup-actions .el-select {
    width: 100% !important;
    margin-right: 0 !important;
  }
  
  /* 移动端分页控制调整 */
  .followup-controls {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .display-options {
    justify-content: center;
  }
  
  .pagination-controls {
    justify-content: center;
  }
  
  /* 移动端快速导航调整 */
  .quick-navigation {
    right: 20px;
    bottom: 20px;
  }
  
  .nav-btn {
    width: 45px;
    height: 45px;
  }
  
  /* 移动端标题索引导航栏调整 */
  .followup-content-wrapper {
    flex-direction: column;
    gap: 16px;
  }
  
  .title-index-navigation {
    width: 100%;
    position: static;
    max-height: none;
    order: 2;
  }
  
  .timeline-container {
    order: 1;
  }
  
  .index-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 8px;
  }
  
}
</style>

