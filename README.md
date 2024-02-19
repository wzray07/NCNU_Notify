# NCNU_Notify 暨大最新公告通知系統 2.0
## 開發緣由
- 還記得剛入學暨大的我，使用了學長所寫的 Line Notify ，這幫助我即時接收了許多學校的重要公告，不過學校的相關網站更新，這個系統也無法提供服務，詢問計中人員也表示目前已經由外包廠商進行網站的處理，舊的 API 也預計將於今年 (2024) 移除，於是趁這次寒假比較沒事做，來寫一個 2.0 改版供大家使用。

## 使用及測試說明
> 使用環境：Docker
### /climb 
- 爬資料相關
- `record_today` 今天所爬到的資料
    - 搭配 crontab 進行每日清除
- `all_token` 需發送的對象 token
- `error_token` 發送失敗的 token（用戶解除綁定會無法發送，即該 token 失效）
    - 搭配 crontab 進行每日 token 更新
### /nginx
- nginx 設定檔
### /oauth
- 用戶進行綁定之網頁
- `new_token_list` 綁定完成的 token
### 使用測試
> 僅提供測試使用，測試前需先申請一組服務 [傳送門](https://notify-bot.line.me/my/services/)</p>
> 如需進行用戶授權綁定，[點擊這裡](https://notifyoauth.wzray07.studio/)
- 完成申請後，將會獲得 `client_id` 與 `client sercret`
- 將 `client_id` 與 `secret` 更新到 `oauth.py`（第 6、7 行）
- in Terminal => `cd NCNU_Notify` `docker-compose up`
- in Browser => `127.0.0.1`

