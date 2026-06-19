const app=getApp()
Page({
  data: {
    username: '',
    password: '',
    repassword: ''
  },
  inputUsername(e) {
    this.setData({ username: e.detail.value })
  },
  inputPassword(e) {
    this.setData({ password: e.detail.value })
  },
  inputRepassword(e) {
    this.setData({ repassword: e.detail.value })
  },
  doRegister() {
    if (!this.data.username || !this.data.password) {
      wx.showToast({ title: '请输入完整', icon: 'none' })
      return
    }
    if (this.data.password !== this.data.repassword) {
      wx.showToast({ title: '两次密码不一致', icon: 'none' })
      return
    }
    wx.request({
      url: app.globalData.baseUrl + '/user/register',
      method: 'POST',
      data: {
        username: this.data.username,
        password: this.data.password
      },
      success: res => {
        if (res.data.code === 200) {
          wx.showToast({ title: '注册成功' })
          setTimeout(() => wx.navigateBack(), 1500)
        } else {
          wx.showToast({ title: res.data.msg, icon: 'none' })
        }
      }
    })
  }
})