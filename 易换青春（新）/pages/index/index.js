const app = getApp()
Page({
  data: {
    keyword: '',
    // 分类列表：名称+emoji图标，两行四列布局
    cateList: [
      { name: '数码电子', icon: '📱' },
      { name: '图书教材', icon: '📚' },
      { name: '运动器材', icon: '⚽' },
      { name: '生活用品', icon: '🛒' },
      { name: '服装配饰', icon: '👕' },
      { name: '美妆护肤', icon: '💄' },
      { name: '宠物用品', icon: '🐱' },
      { name: '全部分类', icon: '🧩' }
    ],
    goodsList: [],
    activeCate: "" // 记录当前筛选的分类名，页面做提示
  },

  onLoad() {
    this.getGoodsList()
  },
  // 切回首页自动刷新商品
  onShow() {
    this.getGoodsList()
  },

  // 获取全部商品（全部分类调用）
  getGoodsList() {
    wx.showLoading({ title: '加载中...' })
    wx.request({
      url: app.globalData.baseUrl + '/goods/list',
      method: "GET",
      header: { "Content-Type": "application/json" },
      success: res => {
        wx.hideLoading()
        console.log("全部商品列表", res.data)
        const list = res.data.data || []
        this.setData({
          goodsList: list,
          activeCate: "" // 清空筛选标记
        })
      },
      fail: () => {
        wx.hideLoading()
        wx.showToast({ title: '请求商品失败', icon: 'none' })
      }
    })
  },

  // 搜索输入框赋值
  inputSearch(e) {
    this.setData({ keyword: e.detail.value })
  },

  // 点击搜索框跳转搜索页面
  doSearch() {
    wx.navigateTo({
      url: '/pages/search/search'
    })
  },

  // 点击分类项筛选商品
  selectCate(e) {
    const cateName = e.currentTarget.dataset.cate
    // 判断：点的是【全部分类】直接加载全部商品
    if (cateName === "全部分类") {
      this.getGoodsList()
      return
    }

    // 普通分类，调用分类筛选接口
    wx.showLoading({ title: '加载中...' })
    wx.request({
      url: app.globalData.baseUrl + '/goods/category',
      method: "GET",
      header: { "Content-Type": "application/json" },
      data: { category: cateName },
      success: res => {
        wx.hideLoading()
        console.log("分类返回", res.data)
        const list = res.data.data || []
        this.setData({
          goodsList: list,
          activeCate: cateName
        })
      },
      fail: () => {
        wx.hideLoading()
        wx.showToast({ title: '分类查询失败', icon: 'none' })
      }
    })
  },

  // 跳转商品详情
  goDetail(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: '/pages/detail/detail?id=' + id
    })
  }
})