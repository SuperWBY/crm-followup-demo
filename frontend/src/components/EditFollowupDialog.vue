<template>
  <el-dialog
    v-model="dialogVisible"
    title="编辑跟进记录"
    width="600px"
    :before-close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
      label-position="left"
    >
      <el-form-item label="跟进标题" prop="title">
        <el-input
          v-model="form.title"
          placeholder="请输入跟进记录标题，如：客户需求沟通会议"
          maxlength="200"
          show-word-limit
        />
        <div class="form-tip">建议使用简洁明了的标题，便于快速识别跟进内容</div>
      </el-form-item>

      <el-form-item label="跟进类型" prop="type">
        <el-select
          v-model="form.type"
          placeholder="请选择跟进类型"
          style="width: 100%"
        >
          <el-option
            v-for="type in followupTypes"
            :key="type.value"
            :label="type.label"
            :value="type.value"
          >
            <div class="option-content">
              <el-icon :class="type.iconClass">
                <component :is="type.icon" />
              </el-icon>
              <span>{{ type.label }}</span>
            </div>
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="跟进时间" prop="date">
        <el-date-picker
          v-model="form.date"
          type="datetime"
          placeholder="选择跟进时间"
          style="width: 100%"
          format="YYYY-MM-DD HH:mm"
          value-format="YYYY-MM-DDTHH:mm:ss"
        />
      </el-form-item>

      <el-form-item label="录入人" prop="sales_user_id">
        <el-select
          v-model="form.sales_user_id"
          placeholder="请选择销售人员"
          style="width: 100%"
        >
          <el-option
            v-for="user in salesUsers"
            :key="user.id"
            :label="user.name"
            :value="user.id"
          >
            <div class="option-content">
              <el-icon><User /></el-icon>
              <span>{{ user.name }} ({{ user.position }})</span>
            </div>
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="跟进时长" prop="duration">
        <el-input-number
          v-model="form.duration"
          :min="0"
          :max="480"
          placeholder="跟进时长（分钟）"
          style="width: 100%"
        />
        <div class="form-tip">请输入跟进时长，单位：分钟</div>
      </el-form-item>

      <el-form-item label="跟进结果" prop="result">
        <el-select
          v-model="form.result"
          placeholder="请选择跟进结果"
          style="width: 100%"
        >
          <el-option-group label="积极进展">
            <el-option label="✅ 客户有意向" value="客户有意向" />
            <el-option label="✅ 需求明确" value="需求明确" />
            <el-option label="✅ 价格接受" value="价格接受" />
            <el-option label="✅ 决策人接触" value="决策人接触" />
            <el-option label="✅ 合同签署" value="合同签署" />
          </el-option-group>
          <el-option-group label="需要跟进">
            <el-option label="⏳ 待客户回复" value="待客户回复" />
            <el-option label="⏳ 需要内部讨论" value="需要内部讨论" />
            <el-option label="⏳ 预算待确认" value="预算待确认" />
            <el-option label="⏳ 技术评估中" value="技术评估中" />
            <el-option label="⏳ 竞品对比中" value="竞品对比中" />
          </el-option-group>
          <el-option-group label="遇到阻碍">
            <el-option label="❌ 价格超出预算" value="价格超出预算" />
            <el-option label="❌ 需求不匹配" value="需求不匹配" />
            <el-option label="❌ 决策人未接触" value="决策人未接触" />
            <el-option label="❌ 竞品优势明显" value="竞品优势明显" />
            <el-option label="❌ 客户无需求" value="客户无需求" />
          </el-option-group>
        </el-select>
      </el-form-item>

      <el-form-item label="跟进内容" prop="content">
        <el-input
          v-model="form.content"
          type="textarea"
          :rows="4"
          placeholder="请详细描述跟进内容..."
          maxlength="500"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="下一步行动" prop="next_action">
        <el-input
          v-model="form.next_action"
          type="textarea"
          placeholder="请描述下一步行动计划"
          :rows="2"
          maxlength="200"
          show-word-limit
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button 
          type="primary" 
          @click="handleSubmit"
          :loading="loading"
        >
          确定
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useFollowupStore } from '../stores/followup'
import dayjs from 'dayjs'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  followup: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'success'])

const followupStore = useFollowupStore()
const formRef = ref()
const loading = ref(false)
const salesUsers = ref([])

// 跟进类型选项
const followupTypes = [
  {
    value: '电话沟通',
    label: '电话沟通',
    icon: 'Phone',
    iconClass: 'phone-icon'
  },
  {
    value: '线上会议',
    label: '线上会议',
    icon: 'VideoCamera',
    iconClass: 'video-icon'
  },
  {
    value: '上门拜访',
    label: '上门拜访',
    icon: 'Location',
    iconClass: 'location-icon'
  },
  {
    value: '邮件联系',
    label: '邮件联系',
    icon: 'Message',
    iconClass: 'message-icon'
  }
]

// 表单数据
const form = ref({
  title: '',
  type: '',
  date: '',
  sales_user_id: null,
  duration: null,
  result: '',
  content: '',
  next_action: ''
})

// 表单验证规则
const rules = {
  title: [
    { required: true, message: '请输入跟进标题', trigger: 'blur' },
    { min: 2, max: 200, message: '标题长度在 2 到 200 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择跟进类型', trigger: 'change' }
  ],
  date: [
    { required: true, message: '请选择跟进时间', trigger: 'change' }
  ],
  sales_user_id: [
    { required: true, message: '请选择销售人员', trigger: 'change' }
  ],
  duration: [
    { required: true, message: '请输入跟进时长', trigger: 'blur' }
  ],
  result: [
    { required: true, message: '请选择跟进结果', trigger: 'change' }
  ],
  content: [
    { required: true, message: '请输入跟进内容', trigger: 'blur' },
    { min: 10, max: 500, message: '跟进内容长度在 10 到 500 个字符', trigger: 'blur' }
  ]
}

// 对话框显示状态
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 获取销售人员列表
const fetchSalesUsers = async () => {
  try {
    const response = await fetch('/api/sales-users')
    if (response.ok) {
      salesUsers.value = await response.json()
    }
  } catch (error) {
    console.error('获取销售人员列表失败:', error)
  }
}

// 监听对话框打开，填充表单数据
watch(dialogVisible, (visible) => {
  if (visible && props.followup) {
    fillForm()
    fetchSalesUsers()
  }
})

// 监听跟进记录变化
watch(() => props.followup, (newFollowup) => {
  if (newFollowup && dialogVisible.value) {
    fillForm()
  }
})

// 填充表单数据
const fillForm = () => {
  if (props.followup) {
    form.value = {
      title: props.followup.title || '',
      type: props.followup.type,
      date: dayjs(props.followup.date).format('YYYY-MM-DDTHH:mm:ss'),
      sales_user_id: props.followup.sales_user_id,
      duration: props.followup.duration,
      result: props.followup.result,
      content: props.followup.content,
      next_action: props.followup.next_action
    }
  }
}

// 关闭对话框
const handleClose = () => {
  dialogVisible.value = false
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value || !props.followup) return

  try {
    const valid = await formRef.value.validate()
    if (!valid) return

    loading.value = true
    
    const followupData = {
      ...form.value,
      date: new Date(form.value.date).toISOString()
    }

    await followupStore.updateFollowup(props.followup.id, followupData)
    
    ElMessage.success('跟进记录更新成功')
    emit('success')
    handleClose()
    
  } catch (error) {
    console.error('Error updating followup:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.option-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
  line-height: 1.4;
}

.phone-icon {
  color: #409eff;
}

.video-icon {
  color: #67c23a;
}

.location-icon {
  color: #e6a23c;
}

.message-icon {
  color: #909399;
}

.dialog-footer {
  text-align: right;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}
</style>

