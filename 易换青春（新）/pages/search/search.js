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
    const keyword = this.data.keyword
    if(!keyword) {
      wx.showToast({title:"请输入搜索关键词",icon:"none"})
      return
    }
    wx.showLoading({title:"搜索中"})
    wx.request({
      url: app.globalData.baseUrl + '/goods/search',
      method: "GET",
      header: {"Content-Type": "application/json"},
      data: { keyword: keyword },
      success: res => {
        wx.hideLoading()
        console.log("搜索完整返回：", res.data)
        // 关键：取res.data.data里的商品数组
        const list = res.data.data || []
        this.setData({ goodsList: list })
      },
      fail: () => {
        wx.hideLoading()
        wx.showToast({title:"搜索请求出错",icon:"none"})
      }
    })
  },
  goDetail(e) {
    let id=e.currentTarget.dataset.id
    wx.navigateTo({ url: '/pages/detail/detail?id='+id })
  }
})