# telegram_bot_for_irent

irent 路邊租還找車服務

# 用途

透過 Telegram Bot 即時提醒附近是否有路邊租還車輛可供選擇，還可以自行修改搜車半徑


# 參數說明

這服務不需要登入，只需要自己申請 Telegram Bot 的 access token   

`telegram_bot_token` 請輸入自己從 https://telegram.me/BotFather 申請來的 token
`search_radius_km` 表示搜車的公里半徑，預設設定 1.5 公里，可自行修改


# 使用方式
    * 直接分享 Location 給 bot 
    * 在輸入框先輸入 `/address ` 後加上地址

系統會每 30 秒搜尋一次，直到找到車為止。

目前還沒實做停止功能，如果要停止現有搜尋，可以直接把 bot 停用後再啟用


# 效果

![](demo.gif)

# Todo
    - [ ] 實做停止功能
    - [ ] 地址轉經緯度的網頁爬重穩定度


* 參考資料
    * [Geocoding - 批量處理地址轉換經緯度](https://medium.com/%E8%8A%B1%E5%93%A5%E7%9A%84%E5%A5%87%E5%B9%BB%E6%97%85%E7%A8%8B/geocoding-%E6%89%B9%E9%87%8F%E8%99%95%E7%90%86%E5%9C%B0%E5%9D%80%E8%BD%89%E6%8F%9B%E7%B6%93%E7%B7%AF%E5%BA%A6-721ab2564c88)
    * [The haversine formula](http://evoling.net/code/haversine/)
    * [Python Telegram Bot 教學](https://hackmd.io/@truckski/HkgaMUc24)
