const app = getApp()
Page({
  data: {
    userInfo: {}
  },

  onShow() {
    // 先从本地存储取数据（兜底）
    let userInfo = wx.getStorageSync('userInfo') || {}
    // 同步到全局变量
    app.globalData.userInfo = userInfo
    this.setData({
      userInfo: userInfo
    })
  },

  // 我的发布
  goMyGoods() {
    wx.navigateTo({
      url: '/pages/my-goods/my-goods'
    })
  },

  // 退出登录
  logout() {
    // 清空全局 + 本地存储
    app.globalData.userInfo = null
    wx.removeStorageSync('userInfo')
    wx.removeStorageSync('token')

    wx.reLaunch({
      url: '/pages/login/login'
    })
  }
})