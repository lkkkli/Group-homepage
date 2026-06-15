const app = getApp()
Page({
  data: {
    keyword: '',
    // 分类列表+图标：UI结构固定，名称可由后端返回替换
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
    goodsList: [] // 商品列表
  },

  onLoad() {
    // 对接后端时，注释上面模拟数据，启用下方接口
    this.getGoodsList()
  },

  // 请求后端：获取全部商品
  getGoodsList() {
    wx.request({
      url: app.globalData.baseUrl + '/goods/list',
      success: res => {
        console.log("商品列表", res.data)
        this.setData({
          goodsList: res.data.data
        })
      },
      fail: () => {
        wx.showToast({
          title: '请求商品失败',
          icon: 'none'
        })
      }
    })
  },

  // 搜索输入
  inputSearch(e) {
    this.setData({ keyword: e.detail.value })
  },

  // 跳转搜索页
  doSearch() {
    if (!this.data.keyword) {
      wx.showToast({ title: '请输入搜索内容', icon: 'none' })
      return
    }
    wx.navigateTo({
      url: '/pages/search/search?keyword=' + this.data.keyword
    })
  },

  // 按分类筛选商品（对接后端分类接口）
  selectCate(e) {
    const cate = e.currentTarget.dataset.cate
    wx.request({
      url: app.globalData.baseUrl + '/goods/category',
      data: {
        category: cate
      },
      success: res => {
        console.log("分类返回", res.data)
        this.setData({ goodsList: res.data.data })
      },
      fail: () => {
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