import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api'

export const useCustomerStore = defineStore('customer', () => {
  const customers = ref([])
  const loading = ref(false)
  const error = ref(null)

  // 获取客户列表
  const fetchCustomers = async (forceRefresh = false) => {
    loading.value = true
    error.value = null
    try {
      // 添加时间戳参数强制刷新
      const url = forceRefresh ? `/customers?_t=${Date.now()}` : '/customers'
      const response = await api.get(url)
      customers.value = response.data
      console.log('客户数据已更新:', response.data.length, '个客户')
    } catch (err) {
      error.value = err.message || '获取客户列表失败'
      console.error('Error fetching customers:', err)
    } finally {
      loading.value = false
    }
  }

  // 获取客户详情
  const fetchCustomer = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/customers/${id}`)
      return response.data
    } catch (err) {
      error.value = err.message || '获取客户详情失败'
      console.error('Error fetching customer:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    customers,
    loading,
    error,
    fetchCustomers,
    fetchCustomer
  }
})

