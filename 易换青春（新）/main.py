"""
使用前需要输入cpolar http 8000，然后在前端哪里改代码https://xxxx.cpolar.top
"""
import os
import json
import base64
import sqlite3
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI(
    api_key="ark-1f44d553-d578-4b5d-aecd-fd801c3976b6-d88b2",
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

class UserAuth(BaseModel):
    username: str
    password: str

def init_db():
    conn = sqlite3.connect("market.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            title TEXT,
            description TEXT,
            price REAL,
            image_path TEXT
            user_id INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            avatar TEXT,
            role TEXT
        )
    """)
    
    cursor.execute("SELECT COUNT(*) FROM items")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO items (category, title, description, price, image_path) VALUES (?, ?, ?, ?, ?)",
            ("\u4e66\u7c4d\u8d44\u6599", "\u7b97\u6cd5\u5bfc\u8bba\u7b2c\u4e09\u7248", "\u4e5d\u6210\u65b0\uff0c\u65e0\u7b14\u8bb0\u3002", 25.0, "https://img.yzcdn.cn/vant/ipad.jpeg")
        )
        cursor.execute(
            "INSERT INTO items (category, title, description, price, image_path) VALUES (?, ?, ?, ?, ?)",
            ("\u6570\u7801\u4ea7\u54c1", "\u4e8c\u624b iPad Air", "\u5e26\u539f\u88c5\u5145\u7535\u5668\uff0c\u529f\u80fd\u5b8c\u597d\u3002", 1200.0, "https://img.yzcdn.cn/vant/ipad.jpeg")
        )
        cursor.execute(
            "INSERT INTO items (category, title, description, price, image_path) VALUES (?, ?, ?, ?, ?)",
            ("\u4ee3\u6b65\u5de5\u5177", "\u6821\u56ed\u4e8c\u624b\u81ea\u884c\u8f66", "\u525a\u6362\u7684\u8f6e\u80ce\uff0c\u597d\u9aa4\u8f6b\u3002", 80.0, "https://img.yzcdn.cn/vant/ipad.jpeg")
        )
        
    conn.commit()
    conn.close()

init_db()


@app.post("/user/register")
async def register(auth: UserAuth):
    try:
        conn = sqlite3.connect("market.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, avatar, role) VALUES (?, ?, ?, ?)",
            (auth.username, auth.password, "https://img.yzcdn.cn/vant/cat.jpeg", "student")
        )
        conn.commit()
        return {"status": "success", "code": 200, "message": "User registered successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    finally:
        cursor.close()
        conn.close()

@app.post("/user/login")
async def login(auth: UserAuth):
    conn = sqlite3.connect("market.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, avatar, role FROM users WHERE username = ? AND password = ?",
        (auth.username, auth.password)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user:
        return {
            "status": "success",
            "code": 200,
            "data": {
                "userId": user[0],
                "username": user[1],
                "avatar": user[2],
                "role": user[3]
            }
        }
    else:
        raise HTTPException(status_code=400, detail="Invalid username or password")

@app.get("/goods/list")
async def get_goods_list(request: Request):
    try:
        base_url = str(request.base_url)
        conn = sqlite3.connect("market.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, category, title, description, price, image_path FROM items")
        rows = cursor.fetchall()
        
        goods_list = []
        for row in rows:
            img_path = row[5]
            full_img_url = f"{base_url}{img_path}" if img_path and not img_path.startswith("http") else img_path
            goods_list.append({
                "id": row[0],
                "category": row[1],
                "categoryName": row[1],
                "goodsCategory": row[1],
                "title": row[2],
                "name": row[2],
                "goodsName": row[2],
                "goods_name": row[2],
                "description": row[3],
                "desc": row[3],
                "goodsDesc": row[3],
                "detail": row[3],
                "price": row[4],
                "goodsPrice": row[4],
                "goods_price": row[4],
                "image_path": full_img_url,
                "image": full_img_url,
                "imgUrl": full_img_url,
                "img": full_img_url,
                "cover": full_img_url,
                "goodsCover": full_img_url
            })
        return {"status": "success", "code": 200, "data": goods_list}
    except Exception as e:
        return {"status": "error", "code": 500, "message": str(e)}
    finally:
        cursor.close()
        conn.close()

@app.get("/goods/my")
async def get_my_goods(userId: int):

    conn = sqlite3.connect("market.db")
    cursor = conn.cursor()

    try:

        cursor.execute("""
        SELECT
            id,
            user_id,
            category,
            title,
            description,
            price,
            image_path

        FROM items

        WHERE user_id = ?

        ORDER BY id DESC
        """,
        (userId,))


        rows = cursor.fetchall()


        goods = []


        for row in rows:

            image = row[6]


            # 如果数据库存的是相对路径
            if image and not image.startswith("http"):

                image = "http://你的后端地址:8000/" + image


            goods.append({

                "id": row[0],

                "user_id": row[1],

                "category": row[2],

                "title": row[3],

                "description": row[4],

                "price": row[5],


                # 前端需要的字段
                "pic": image

            })


        return {

            "code":200,

            "status":"success",

            "data":goods

        }


    except Exception as e:

        print("goods/my错误:",e)

        return {

            "code":500,

            "message":str(e)

        }


    finally:

        conn.close()
@app.get("/goods/category")
async def get_goods_by_category(category: str):

    conn = sqlite3.connect("market.db")
    cursor = conn.cursor()

    try:

        # 统一分类规则
        cate_map = {

            "数码电子": [
                "数码",
                "电子",
                "手机",
                "电脑",
                "平板",
                "耳机",
                "键盘"
            ],


            "图书教材": [
                "图书",
                "教材",
                "书",
                "课本",
                "小说"
            ],


            # 修改这里
            "运动器材": [
                "运动",
                "球类",
                "健身",
                "器材",
                "自行车",
                "单车",
                "滑板",
                "轮滑",
                "瑜伽"
            ],


            "生活用品": [
                "生活",
                "用品",
                "日用",
                "收纳",
                "家具"
            ],


            "服装配饰": [
                "服装",
                "衣服",
                "鞋",
                "包",
                "帽子"
            ],


            "美妆护肤": [
                "美妆",
                "护肤",
                "化妆品"
            ],


            "宠物用品": [
                "宠物",
                "猫",
                "狗",
                "宠物粮"
            ]

        }


        keywords = cate_map.get(
            category,
            [category]
        )


        conditions = []

        params = []


        for word in keywords:

            conditions.append(
                "category LIKE ?"
            )

            params.append(
                "%" + word + "%"
            )


        sql = """
        SELECT
            id,
            title,
            price,
            category,
            description,
            image_path

        FROM items

        WHERE
        """


        sql += " OR ".join(conditions)


        sql += " ORDER BY id DESC"


        cursor.execute(
            sql,
            params
        )


        rows = cursor.fetchall()


        goods = []


        for row in rows:


            pic = row[5]


            if pic and not pic.startswith("http"):

                pic = "http://你的cpolar地址/" + pic



            goods.append({

                "id": row[0],

                "title": row[1],

                "price": row[2],

                "category": row[3],

                "description": row[4],

                "pic": pic

            })


        return {

            "code":200,

            "data":goods

        }



    except Exception as e:

        print("分类查询错误:", e)

        return {

            "code":500,

            "message":str(e)

        }


    finally:

        conn.close()
@app.get("/goods/list")
async def get_goods_list():

    conn = sqlite3.connect("market.db")
    cursor = conn.cursor()

    try:

        cursor.execute("""
        SELECT
            id,
            title,
            price,
            category,
            description,
            image_path

        FROM items

        ORDER BY id DESC
        """)


        rows = cursor.fetchall()


        goods = []


        for row in rows:

            pic = row[5]


            # 图片地址处理
            if pic and not pic.startswith("http"):

                pic = "http://76d37cf6.r40.cpolar.top/" + pic


            goods.append({

                "id": row[0],

                "title": row[1],

                "price": row[2],

                "category": row[3],

                "description": row[4],

                "pic": pic

            })


        return {

            "code":200,

            "status":"success",

            "data":goods

        }


    except Exception as e:

        print("goods/list错误:",e)

        return {

            "code":500,

            "message":str(e)

        }


    finally:

        conn.close()
@app.get("/goods/detail")
async def goods_detail(id:int):

    conn=sqlite3.connect("market.db")
    cursor=conn.cursor()


    cursor.execute("""
    SELECT
        id,
        title,
        price,
        category,
        description,
        image_path

    FROM items

    WHERE id=?
    """,(id,))


    row=cursor.fetchone()

    conn.close()


    if not row:

        return {
            "code":404
        }


    image = row[5]


    # 转成前端可以访问的地址
    if image and not image.startswith("http"):

        image = "http://你的服务器地址:8000/" + image


    return {

        "code":200,

        "data":{

            "id":row[0],

            "title":row[1],

            "price":row[2],

            "category":row[3],

            "description":row[4],

            "pic":image

        }

    }
@app.get("/goods/search")
async def search_goods(keyword: str):

    conn = sqlite3.connect("market.db")
    cursor = conn.cursor()

    try:

        key = "%" + keyword + "%"


        cursor.execute("""
        SELECT
            id,
            title,
            price,
            category,
            description,
            image_path

        FROM items

        WHERE
            title LIKE ?
            OR category LIKE ?
            OR description LIKE ?

        ORDER BY id DESC

        """,
        (
            key,
            key,
            key
        ))


        rows = cursor.fetchall()


        goods = []


        for row in rows:

            pic = row[5]


            if pic and not pic.startswith("http"):

                pic = "http://你的cpolar地址/" + pic


            goods.append({

                "id": row[0],

                "title": row[1],

                "price": row[2],

                "category": row[3],

                "description": row[4],

                "pic": pic

            })


        return {

            "code":200,

            "data":goods

        }


    except Exception as e:

        print("搜索错误:",e)

        return {

            "code":500,

            "message":str(e)

        }


    finally:

        conn.close()
@app.post("/goods/add")
async def add_goods(request: Request):

    conn = sqlite3.connect("market.db")
    cursor = conn.cursor()

    try:

        # 接收前端 JSON
        data = await request.json()


        user_id = 1001


        title = (
            data.get("title")
            or data.get("goodsName")
            or data.get("name")
            or "untitled"
        )


        price = (
            data.get("price")
            or data.get("goodsPrice")
            or 0
        )


        category = (
            data.get("category")
            or data.get("goodsCate")
            or "其他"


        )


        description = (
            data.get("description")
            or data.get("goodsDesc")
            or ""
        )


        image_path = (
            data.get("image_path")
            or data.get("image")
            or data.get("pic")
            or ""
        )


        cursor.execute("""
        INSERT INTO items
        (
            user_id,
            category,
            title,
            description,
            price,
            image_path
        )
        VALUES
        (?,?,?,?,?,?)
        """,
        (
            user_id,
            category,
            title,
            description,
            price,
            image_path
        ))


        conn.commit()


        return {

            "code":200,
            "message":"发布成功"

        }


    except Exception as e:

        conn.rollback()

        print("goods/add错误:",e)

        return {

            "code":500,
            "message":str(e)

        }


    finally:

        conn.close()
@app.post("/ai/recognize")
async def ai_recognize(file: UploadFile = File(...)):
    fallback_data = {
        "category": "\u4e66\u7c4d\u8d44\u6599",
        "title": "\u7b97\u6cd5\u5bfc\u8bba\u7b2c\u4e09\u7248",
        "description": "\u4e5d\u6210\u65b0\uff0c\u65e0\u7b14\u8bb0\uff0c\u5b66\u671f\u7ed3\u671f\u4f4e\u4ef7\u51fa\u7ed9\u9700\u8981\u7685\u540c\u5b66\u3002",
        "price": 25.0
    }
    try:
        contents = await file.read()
        if not contents:
            return {"status": "success", "code": 200, "data": fallback_data}
            
        image_data = base64.b64encode(contents).decode("utf-8")
        prompt = "Analyze this campus second-hand item. Return ONLY a JSON object with keys: category, title, description, price. Values must be in Chinese."
        
        response = client.chat.completions.create(
            model="doubao-seed-2-0-mini-260428",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                        },
                    ],
                }
            ]
        )
        
        raw_content = response.choices[0].message.content.strip()
        if raw_content.startswith("```"):
            lines = raw_content.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            raw_content = "\n".join(lines).strip()
            
        try:
            parsed_json = json.loads(raw_content)
            if not parsed_json or not isinstance(parsed_json, dict) or len(parsed_json) == 0:
                parsed_json = fallback_data
        except:
            parsed_json = fallback_data
            
        return {
            "status": "success",
            "code": 200,
            "data": parsed_json
        }
    except Exception as e:
        return {
            "status": "success",
            "code": 200,
            "data": fallback_data
        }
@app.post("/goods/delete")
async def delete_goods(id: int):

    conn = sqlite3.connect("market.db")
    cursor = conn.cursor()


    try:

        # 删除指定商品
        cursor.execute(
            """
            DELETE FROM items
            WHERE id = ?
            """,
            (id,)
        )


        conn.commit()


        # 判断是否真的删除
        if cursor.rowcount == 0:

            return {
                "status":"error",
                "code":404,
                "message":"商品不存在"
            }


        return {

            "status":"success",
            "code":200,
            "message":"删除成功"

        }


    except Exception as e:

        conn.rollback()

        print("删除失败:")
        print(e)


        return {

            "status":"error",
            "code":500,
            "message":str(e)

        }


    finally:

        conn.close()
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
