const app=getApp()
Page({
  data: {
    keyword: '',
    goodsList: []
  },
  inputKeyword(e) {
    this.setData({ keyword: e.detail.value })
  },
  doSearch() {
    wx.request({
      url: app.globalData.baseUrl + '/goods/search',
      data: { keyword: this.data.keyword },
      success: res => {
        this.setData({ goodsList: res.data })
      }
    })
  },
  goDetail(e) {
    let id=e.currentTarget.dataset.id
    wx.navigateTo({ url: '/pages/detail/detail?id='+id })
  }
})