const app = getApp()
Page({
  data: {
    username: '',
    password: ''
  },

  inputUsername(e) {
    this.setData({ username: e.detail.value })
  },
  inputPassword(e) {
    this.setData({ password: e.detail.value })
  },

  doLogin() {
    const { username, password } = this.data
    if (!username || !password) {
      wx.showToast({ title: '请输入完整', icon: 'none' })
      return
    }

// 测试账号：test / 123456（本地直接登录）
// ==========================================
if (username === 'test' && password === '123456') {
  let user = {
    userId: 1001,
    username: 'test'
  }
  app.globalData.userInfo = user
  // 新增：存入本地存储，页面切换不丢失
  wx.setStorageSync('userInfo', user)
  // 额外：也存一份单独的 userId，方便后端打印核对
  wx.setStorageSync('userId', user.userId)
  wx.showToast({ title: '登录成功' })
  wx.reLaunch({ url: '/pages/index/index' })
  return
}

    // 其他账号走后端
    wx.request({
      url: app.globalData.baseUrl + '/user/login',
      method: 'POST',
      data: { username, password },
      success: res => {
        if (res.data.code === 200) {
          // 后端用户信息存入全局 + 本地缓存（关键补充）
          const user = res.data.data
          app.globalData.userInfo = user
          wx.setStorageSync('userInfo', user)
          wx.showToast({ title: '登录成功' })
          wx.reLaunch({ url: '/pages/index/index' })
        } else {
          wx.showToast({ title: res.data.msg || '登录失败', icon: 'none' })
        }
      },
      fail: () => {
        wx.showToast({ title: '服务器未启动', icon: 'none' })
      }
    })
  },

  goRegister() {
    wx.navigateTo({ url: '/pages/register/register' })
  }
})