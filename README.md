# project2
在網頁直接執行從google Scholar下在指定主題的摘要資料，如可下載全文pdf則同時下載，最終將摘要彙整成檔案，並連同全文pdf儲存在使用者目錄-paper-主題資料夾
1.在 Google Colab 運行
適用情境：🔹 適合沒有安裝 Python 的使用者
使用方式：只需點擊 Google Colab 連結即可運行你的應用程式。
# 下載 GitHub 上的程式碼
!git clone https://github.com/neako0230/project2.git
%cd project2

# 安裝 Python 套件
!pip install -r requirements.txt

# 執行應用程式
!python app.py

 Google Colab 連結
讓使用者進入 Google Colab
貼上 GitHub 下載代碼
執行程式後，Gradio 會產生一個 Web UI 連結
使用者可以點擊連結 直接操作你的應用程式！

2.在本地端（Windows / Mac）執行
適用情境：🔹 適合會使用 Git 和 Python 的開發者
使用方式：使用者可以在自己的電腦下載並運行你的 app.py。
git clone https://github.com/neako0230/project2.git
cd project2
pip install -r requirements.txt
python app.py
Gradio 會生成一個本地網址，打開瀏覽器即可使用！
