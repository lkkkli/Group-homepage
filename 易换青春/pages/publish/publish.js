const app = getApp();
Page({
  data: {
    pic: "",
    name: "",
    category: "",
    desc: "",
    price: "",
    contact: "",
    cateList: ["数码电子", "图书教材", "运动器材", "生活用品", "服装配饰", "美妆护肤", "宠物用品", "全部分类"],
    cateIndex: 0
  },

  choosePic() {
    wx.chooseImage({
      count: 1,
      sizeType: ["compressed"],
      sourceType: ["album", "camera"],
      success: (res) => {
        this.setData({ pic: res.tempFilePaths[0] });
      }
    });
  },

  onName(e) { this.setData({ name: e.detail.value }); },
  onDesc(e) { this.setData({ desc: e.detail.value }); },
  onPrice(e) { this.setData({ price: e.detail.value }); },
  onContact(e) { this.setData({ contact: e.detail.value }); },

  onCateChange(e) {
    const index = e.detail.value;
    this.setData({
      cateIndex: index,
      category: this.data.cateList[index]
    });
  },

  aiRecognize() {
    const { pic } = this.data;
    if (!pic) {
      wx.showToast({ title: "请先上传图片", icon: "none" });
      return;
    }
  
    wx.showLoading({ title: "AI识别中..." });
  
    wx.uploadFile({
      url: app.globalData.baseUrl + "/ai/recognize",
      filePath: pic,
      name: "file",
      success: (res) => {
        wx.hideLoading();
        console.log("【后端真实返回】", res.data);
        try {
          const data = JSON.parse(res.data);
          console.log("【解析后完整数据】", data);
          if (data.code === 200 && data.data) {
            let info = data.data;
            // 直接回填AI识别的分类文本
            this.setData({
              name: info.title || info.name || "",
              category: info.category || this.data.category,
              desc: info.description || ""
            });
            wx.showToast({ title: "识别成功" });
          } else {
            wx.showToast({ title: "识别失败", icon: "none" });
          }
        } catch (e) {
          wx.showToast({ title: "解析错误", icon: "none" });
        }
      },
      fail: () => {
        wx.hideLoading();
        wx.showToast({ title: "上传失败", icon: "none" });
      }
    });
  },

    // 【核心修改点】发布提交 
    submit() { 
      // 后端要求：发布时打印 
      console.log("发布用户ID", wx.getStorageSync("userId")) 
      // 只定义一次 user，优先缓存，再全局
      const user = wx.getStorageSync('userInfo') || app.globalData.userInfo; 
      const { pic, name, category, price, desc, contact } = this.data; 
  
      console.log("登录用户：", user); 
      console.log("提交userId：", user?.userId); 
  
      if (!user || !user.userId) { 
        wx.showToast({ title: "请先登录", icon: "none" }); 
        return; 
      } 
      if (!pic || !name || !category || !price || !contact) { 
        wx.showToast({ title: "请完善所有信息", icon: "none" }); 
        return; 
      } 
  
      wx.showLoading({ title: "发布中..." }); 
  
      wx.request({ 
        url: app.globalData.baseUrl + "/goods/add", 
        method: "POST", 
        header: { "Content-Type": "application/json" }, 
        data: { 
          image_path: pic,
          title: name,
          price: price, 
          category: category, 
          description: desc, 
          contact: contact, 
          userId: user.userId 
        }, 
        success: (res) => { 
          wx.hideLoading(); 
          console.log("发布接口返回：", res.data); 
  
          //根据后端真实返回判断是否成功 
          if (res.data.code === 200 || res.data.status === "success") { 
            wx.showToast({ title: "发布成功" }); 
  
            // 清空表单 
            this.setData({ 
              pic: "", 
              name: "", 
              price: "", 
              category: "", 
              desc: "", 
              contact: "", 
              cateIndex: 0 
            }); 
  
            setTimeout(() => { 
              wx.navigateBack(); 
            }, 1500); 
          } else { 
            // 后端返回错误状态，提示真实信息 
            const errMsg = res.data.message || "发布失败，请重试"; 
            wx.showToast({ title: errMsg, icon: "none" }); 
          } 
        }, 
        fail: (err) => { 
          wx.hideLoading(); 
          console.error("发布请求失败：", err); 
          // 网络错误/500错误时，提示服务器错误 
          wx.showToast({ title: "发布失败：服务器错误", icon: "none" }); 
        } 
      }); 
    } 
});