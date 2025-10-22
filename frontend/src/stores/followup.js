import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api'

export const useFollowupStore = defineStore('followup', () => {
  const followups = ref([])
  const loading = ref(false)
  const error = ref(null)

  // 获取客户跟进记录
  const fetchFollowups = async (customerId, forceRefresh = false) => {
    loading.value = true
    error.value = null
    try {
      // 添加时间戳参数强制刷新
      const url = forceRefresh ? `/customers/${customerId}/followups?_t=${Date.now()}` : `/customers/${customerId}/followups`
      const response = await api.get(url)
      followups.value = response.data
      console.log('跟进记录数据已更新:', response.data.length, '条记录')
    } catch (err) {
      error.value = err.message || '获取跟进记录失败'
      console.error('Error fetching followups:', err)
    } finally {
      loading.value = false
    }
  }

  // 创建跟进记录
  const createFollowup = async (customerId, followupData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.post(`/customers/${customerId}/followups`, followupData)
      // 强制刷新跟进记录列表
      await fetchFollowups(customerId, true)
      console.log('新跟进记录已创建，数据已刷新')
      return response.data
    } catch (err) {
      error.value = err.message || '创建跟进记录失败'
      console.error('Error creating followup:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // 更新跟进记录
  const updateFollowup = async (followupId, followupData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.put(`/followups/${followupId}`, followupData)
      // 强制刷新跟进记录列表
      const customerId = followups.value.find(f => f.id === followupId)?.customer_id
      if (customerId) {
        await fetchFollowups(customerId, true)
        console.log('跟进记录已更新，数据已刷新')
      }
      return response.data
    } catch (err) {
      error.value = err.message || '更新跟进记录失败'
      console.error('Error updating followup:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // 删除跟进记录
  const deleteFollowup = async (followupId) => {
    loading.value = true
    error.value = null
    try {
      await api.delete(`/followups/${followupId}`)
      // 重新获取跟进记录列表
      const customerId = followups.value.find(f => f.id === followupId)?.customer_id
      if (customerId) {
        await fetchFollowups(customerId)
      }
    } catch (err) {
      error.value = err.message || '删除跟进记录失败'
      console.error('Error deleting followup:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    followups,
    loading,
    error,
    fetchFollowups,
    createFollowup,
    updateFollowup,
    deleteFollowup
  }
})

