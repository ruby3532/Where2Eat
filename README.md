# NTU午餐決策工具

這是一個幫助台大學生選擇午餐的網頁應用程序。

## 功能特點

- 根據步行時間和餐廳類型進行篩選
- 在地圖上顯示餐廳位置
- 查看餐廳詳細信息
- 支持自定義餐廳類型
- 整合 Google Maps 功能

## 技術棧

- React
- Tailwind CSS
- Google Maps API

## 本地開發

1. 克隆倉庫：
```bash
git clone [your-repository-url]
cd Where2Eat
```

2. 使用本地服務器運行：
```bash
python -m http.server 8000
```

3. 在瀏覽器中訪問：
```
http://localhost:8000
```

## 部署

本項目使用 GitHub Pages 進行部署。

### 部署步驟

1. 確保你的倉庫設置中已啟用 GitHub Pages：
   - 進入倉庫設置（Settings）
   - 找到 "Pages" 選項
   - 在 "Source" 下選擇 "GitHub Actions"

2. 推送代碼到 main 分支後，GitHub Actions 會自動部署到 GitHub Pages

3. 部署完成後，可以通過以下地址訪問：
   ```
   https://[你的GitHub用戶名].github.io/Where2Eat
   ```

### 注意事項

- 確保 Google Maps API 密鑰已正確配置
- 在 Google Cloud Console 中添加 GitHub Pages 域名到允許的來源
- 如果遇到跨域問題，需要配置適當的 CORS 設置 