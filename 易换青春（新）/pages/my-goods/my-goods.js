const app = getApp()
Page({
  data: {
    myGoodsList: []
  },

  onLoad() {
    this.getMyGoods()
  },

  getMyGoods() {
    // 后端要求：查询时打印
    console.log("查询用户ID", wx.getStorageSync("userId"))
   // 读取本地存储的登录用户信息
   const userInfo = wx.getStorageSync('userInfo')
   console.log('当前登录用户信息：', userInfo)

   // 校验登录状态
   if (!userInfo || !userInfo.userId) {
     wx.showToast({
       title: '请先登录',
       icon: 'none'
     })
     return
   }

   const userId = userInfo.userId
   console.log('当前用户ID：', userId)

    wx.request({
      url: app.globalData.baseUrl + "/goods/my?userId=" + userId,
      method: "GET",
      success: (res) => {
        // 2. 打印接口返回的完整数据，确认后端返回了什么
        console.log("/goods/my 接口完整返回：", res.data)
        console.log("接口返回的商品列表：", res.data.data)

        // 3. 必须用 res.data.data 解析，不能直接用 res.data
        const goodsList = res.data.data || []
        // 循环打印每一件商品的pic图片地址
        goodsList.forEach(item => {
        console.log(`商品ID:${item.id} 图片字段pic值:`, item.pic)
        })
    
        this.setData({
          myGoodsList: goodsList
        })
      },
      fail: (err) => {
        console.error("请求失败：", err)
        wx.showToast({ title: "加载失败", icon: "none" })
      }
    })
  },

 // 删除商品
 deleteGoods(e) {
  const id = e.currentTarget.dataset.id
  wx.showModal({
    title: "确认删除",
    content: "确定要删除这个商品吗？",
    success: (res) => {
      if (res.confirm) {
        wx.request({
          url: app.globalData.baseUrl + "/goods/delete?id=" + id,
          method: "POST",
          success: (res) => {
            console.log("删除接口返回：", res.data)
            if (res.data.code === 200) {
              wx.showToast({ title: "删除成功" })
              this.getMyGoods()
            } else {
              wx.showToast({ title: "删除失败：" + res.data.msg, icon: "none" })
            }
          }
        })
      }
    }
  })
  }
})