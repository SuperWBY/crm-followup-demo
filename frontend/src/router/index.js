import { createRouter, createWebHistory } from 'vue-router'
import CustomerList from '../views/CustomerList.vue'
import CustomerDetail from '../views/CustomerDetail.vue'

const routes = [
  {
    path: '/',
    name: 'CustomerList',
    component: CustomerList
  },
  {
    path: '/customer/:id',
    name: 'CustomerDetail',
    component: CustomerDetail,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

