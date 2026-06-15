const app=getApp()
Page({
  data: {
    detail: {}
  },
  onLoad(options) {
    let id=options.id
    this.getGoodsDetail(id)
  },
  getGoodsDetail(id) {
    wx.request({
      url: app.globalData.baseUrl + '/goods/detail',
      data: { id: id },
      success: res => {
        this.setData({ detail: res.data })
      }
    })
  }
})