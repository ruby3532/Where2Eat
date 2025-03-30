from backend import SessionLocal, Restaurant
import json

def init_db():
    db = SessionLocal()
    try:
        # 從現有的餐廳數據初始化數據庫
        restaurants_data = [
            {
                "name": "八方雲集",
                "menu": ["鍋貼", "水餃", "麵食", "湯品"]
            },
            {
                "name": "麥當勞",
                "menu": ["漢堡", "薯條", "雞塊", "飲料"]
            },
            {
                "name": "Subway",
                "menu": ["潛艇堡", "沙拉", "湯品", "餅乾"]
            },
            {
                "name": "吉野家",
                "menu": ["牛丼", "豬丼", "咖哩飯", "味噌湯"]
            },
            {
                "name": "摩斯漢堡",
                "menu": ["漢堡", "米漢堡", "沙拉", "飲料"]
            }
        ]

        for restaurant_data in restaurants_data:
            restaurant = Restaurant(
                name=restaurant_data["name"],
                menu=restaurant_data["menu"],
                last_updated="2024-01-01T00:00:00"
            )
            db.add(restaurant)

        db.commit()
        print("數據庫初始化完成！")
    except Exception as e:
        print(f"初始化數據庫時出錯：{str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 