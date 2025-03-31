from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import asyncio
import aiohttp

app = FastAPI()

# 允許跨域請求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 數據庫設置
SQLALCHEMY_DATABASE_URL = "sqlite:///./restaurants.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 數據模型
class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    menu = Column(JSON)
    last_updated = Column(String)

# 創建數據庫表
Base.metadata.create_all(bind=engine)

# 爬蟲函數
async def fetch_menu(session, restaurant):
    try:
        # 這裡需要根據實際餐廳網站修改爬蟲邏輯
        # 這是一個示例，實際使用時需要替換為真實的網站 URL
        url = f"https://example.com/restaurant/{restaurant['name']}"
        async with session.get(url) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                # 這裡需要根據實際網站結構修改選擇器
                menu_items = [item.text for item in soup.select('.menu-item')]
                return menu_items
    except Exception as e:
        print(f"Error fetching menu for {restaurant['name']}: {str(e)}")
    return []

# 更新菜單的函數
async def update_menus():
    db = SessionLocal()
    try:
        # 獲取所有餐廳
        restaurants = db.query(Restaurant).all()
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for restaurant in restaurants:
                tasks.append(fetch_menu(session, {
                    'name': restaurant.name
                }))
            
            results = await asyncio.gather(*tasks)
            
            for restaurant, menu in zip(restaurants, results):
                if menu:
                    restaurant.menu = menu
                    restaurant.last_updated = datetime.now().isoformat()
            
            db.commit()
    finally:
        db.close()

# API 路由
@app.get("/api/restaurants")
async def get_restaurants():
    db = SessionLocal()
    try:
        restaurants = db.query(Restaurant).all()
        return [{"name": r.name, "menu": r.menu, "last_updated": r.last_updated} for r in restaurants]
    finally:
        db.close()

@app.get("/api/restaurants/{restaurant_name}")
async def get_restaurant(restaurant_name: str):
    db = SessionLocal()
    try:
        restaurant = db.query(Restaurant).filter(Restaurant.name == restaurant_name).first()
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        return {"name": restaurant.name, "menu": restaurant.menu, "last_updated": restaurant.last_updated}
    finally:
        db.close()

@app.post("/api/update-menus")
async def trigger_menu_update():
    await update_menus()
    return {"message": "Menu update triggered"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 