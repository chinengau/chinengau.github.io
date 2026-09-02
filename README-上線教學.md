# Chin-En Gau 個人網站 — 上線教學（GitHub Pages，完全免費）

## 資料夾內容
```
website/
├── index.html            首頁（全螢幕 Reel 循環播放 + Verticals / Films 兩扇門）
├── verticals/            短劇：index.html 是列表，其餘每部一頁
├── films/                電影：index.html 是列表，其餘每部一頁
├── about.html            關於 + 聯絡
├── assets/style.css      樣式（顏色、字體、版面）
├── assets/site.js        互動（Reel 播放、中英切換、燈箱）
├── img/                  已壓縮的圖片
├── Chin-En_Gau_Resume.pdf
└── _build/               ★ 內容都在這裡：data.py 改內容 → 執行 build.py 重新產生頁面
```

> 直接雙擊 `index.html` 在本機打開時，YouTube 背景影片可能不會自動播放（YouTube 對本機檔案有限制），上到 GitHub Pages 後就會正常。

## 一、建立 GitHub 帳號與 repository（約 5 分鐘）
1. 到 https://github.com 註冊（免費）。使用者名稱之後會變成網址：`https://使用者名稱.github.io`。
2. 右上角 **+** → **New repository**。
3. Repository name 填：`使用者名稱.github.io`（**一定要跟使用者名稱一樣**）。
4. 勾 **Public**，按 **Create repository**。

## 二、上傳網站
1. 在 repo 頁面點 **uploading an existing file**（或 **Add file → Upload files**）。
2. 把 `website` 資料夾**裡面的所有東西**拖進去（含 `verticals`、`films`、`assets`、`img` 四個資料夾）。`_build` 可以不用上傳。
3. 按下方 **Commit changes**。

## 三、開啟 GitHub Pages
1. repo 上方 **Settings** → 左側 **Pages**。
2. Source：**Deploy from a branch**；Branch：**main**、**/(root)**；**Save**。
3. 等 1–2 分鐘重新整理，會出現 `Your site is live at https://使用者名稱.github.io`。

之後改東西：重新上傳覆蓋同名檔案即可，1 分鐘內自動更新。

## 四、之後怎麼改內容
### 方法 A（推薦）：改 `_build/data.py`，再重新產生
1. 用記事本或 VS Code 打開 `_build/data.py`，裡面每一部作品是一個 `dict(...)`，欄位一看就懂（title、year、views、syn_en、syn_zh…）。
2. 新增作品就複製一整個 `dict(...)` 區塊貼在後面改。圖片放進 `img/`，填檔名。
3. 打開終端機／命令提示字元，進到 `_build` 資料夾執行 `python3 build.py`（Windows 可能是 `python build.py`），所有頁面會重新產生。
4. 把整個 website 資料夾重新上傳 GitHub。

沒有 Python 的話：Windows 到 python.org 下載安裝時勾「Add to PATH」即可。或直接把 data.py 傳給我，我幫你重產。

### 方法 B：直接改 HTML
每個頁面都是獨立的 HTML，直接編輯文字即可。但同一段文字會有 `data-en` 和 `data-zh` 兩個版本，兩邊都要改。

### 常見修改對照
| 想改什麼 | 在哪裡 |
|---|---|
| 換 Reel 影片／起始秒數 | `assets/site.js` 最上面 `REEL_ID`、`REEL_START` |
| 首頁兩扇門的文字 | `_build/build.py` 的 HOME 區塊 |
| 自我介紹、學歷、獲獎 | `_build/build.py` 的 ABOUT 區塊 |
| 網站顏色／字體 | `assets/style.css` 最上面的 `:root` 變數 |
| Email / IMDb / LinkedIn | `_build/data.py` 的 `SITE` |

## 五、（選用）自訂網域
買一個網域（約 US$10/年），GitHub Pages 設定頁填 Custom domain，再到網域商加 GitHub 給的 A 紀錄。這是唯一可能花錢的地方。
