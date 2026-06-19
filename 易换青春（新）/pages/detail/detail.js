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
        console.log("详情接口完整返回：", res.data)
        // 打印后端实际图片字段 pic
        console.log("当前商品pic图片地址：", res.data.data?.pic)
        let data = res.data.data
        // 兜底防止undefined
        if(!data.pic){
          data.pic = ""
        }
        this.setData({ detail: data })
      },
      fail: () => {
        wx.showToast({title:"加载失败",icon:"none"})
      }
    })
  }
})