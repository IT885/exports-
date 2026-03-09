# 你是思科產品高手 請幫我解析問題出在那邊 請先思考理解郵件問題後 再開始搜尋答案
Critical <System> ms4.scinopharm.com: An application fault occurred: ('query/api.py searchData|465...
IronPort C300V Alert<alert@ms4.scinopharm.com>


​it2 <it

**Thread 编号**: 22  
**Slug**: ni-shi-si-ke-chan-pin-gao-shou-dO1UZHzuShiVDZgeJzoHdg  
**查询次数**: 1  
**最后更新时间**: 2025-10-13T05:46:17.817665  
**模式**: copilot

---

## 内容

### 对话 1

**问题**: 你是思科產品高手 請幫我解析問題出在那邊 請先思考理解郵件問題後 再開始搜尋答案
Critical <System> ms4.scinopharm.com: An application fault occurred: ('query/api.py searchData|465...
IronPort C300V Alert<alert@ms4.scinopharm.com>


​it2 <it2@scinopharm.com>​
Alert: External mail
 
The Critical message is:
 
An application fault occurred: ('query/api.py searchData|4652', "<type 'exceptions.AttributeError'>", "'NoneType' object has no attribute '__len__'", '[util/Aquarium.py screenLoop|412] [util/InternalLibrary.py inverseExtend|328] [util/InternalLibrary.py __call__|769] [screen/Controller.py __call__|30] [util/InternalLibrary.py __call__|769] [screen/CommonController.py __call__|49] [util/InternalLibrary.py __call__|769] [screen/AppController.py __call__|214] [util/InternalLibrary.py __call__|771] [monitor/message_tracking.py __call__|308] [screen/Controller.py executeAction|73] [monitor/message_tracking.py doSearchAction|1251] [monitor/message_tracking.py _querySearch|2814] [query/api.py searchData|208] [query/api.py sequence_query|294] [query/api.py searchData|4652]')
 
Version: 16.0.1-017
Serial Number: 420EA0FDF49A77105369-DD12E432498E
Timestamp: 13 Oct 2025 09:19:57 +0800
 
To learn more about alerts, visit our support community and troubleshooting site.  In many cases, you can find more information about this specific alert.
For troubleshooting, see the following URL :
[https://www.Cisco.com/c/en/us/support/security/email-security-appliance/products-tech-notes-list.html](https://www.cisco.com/c/en/us/support/security/email-security-appliance/products-tech-notes-list.html)
For ESA Support, see the Cisco Support Community site :
[https://supportforums.cisco.com/t5/email-security/bd-p/5756-discussions-email-security](https://supportforums.cisco.com/t5/email-security/bd-p/5756-discussions-email-security)
 
If you desire further information, please contact your support provider.
 
To open a support request for this issue, access the IronPort C300V
and issue the "supportrequest" command. The command sends an email with
diagnostic information directly to Cisco IronPort Customer Support to
facilitate a rapid diagnosis of the problem.
 
 
Thank you.

**回答**:
這是一個思科 IronPort C300V 電子郵件安全設備（Email Security Appliance，ESA）的系統警示，報告了在執行郵件追蹤（message_tracking）相關操作時，應用程式遇到了一個錯誤。問題重點在於 Python 代碼發生了 AttributeError："'NoneType' object has no attribute '__len__'"。這表明系統在處理搜尋查詢（searchData/sequence_query）時，某個變數本應是一個有長度的物件（如列表、字串等），但其實是 None。

### 問題原因解析

- 系統嘗試對一個值為 None 的物件執行 __len__ 操作，通常是想取得長度（例如列表、字串），但該物件尚未正確初始化。
- 堆疊訊息顯示錯誤發生在 query/api.py 的 searchData 函數中，與 message_tracking.py 相關聯，可能是在郵件追蹤查詢的資料或參數異常（例如查詢條件未正確傳遞、資料庫回傳空值等）。
- 發生於 Version: 16.0.1-017，代表可能是該軟體版本的已知漏洞或需更新修正。

### 可能的觸發情境

- 一個郵件查詢或者追蹤要求，傳入了有問題的參數（如查詢值為 None）。
- 資料庫查詢失敗或回傳空物件。
- 某個 API 或內部函式沒有處理資料缺失的異常情況。

### 解決建議

- 依據堆疊訊息，先檢查 query/api.py searchData、sequence_query 等函式，是否正確處理 None 值與查詢條件。
- 檢查 message_tracking 相關的輸入資料是否正確，或是否有新近的操作導致查詢物件異常。
- 建議參考思科官方技術文件或到支援論壇搜尋 'NoneType object has no attribute __len__' 關鍵字，有機會找到已知案例和修補建議。
- 若系統允許，可使用 supportrequest 指令回報、取得更詳細的診斷資訊。

### 參考資源

- 思科官方電子郵件安全技術說明（可搜尋關鍵字）。
- 思科支援論壇，尋找 IronPort 電子郵件安全相關討論及案例。

此問題根本原因是查詢資料異常導致 NoneType 無法運算，建議檢查查詢邏輯與邊界判斷，或諮詢官方修補建議。


### 对话 2

**问题**: Critical <System> ms4.scinopharm.com: An application fault occurred: ('query/api.py searchData|465...
IronPort C300V Alert<alert@ms4.scinopharm.com>


​it2 <it2@scinopharm.com>​
Alert: External mail
 
The Critical message is:
 
An application fault occurred: ('query/api.py searchData|4652', "<type 'exceptions.AttributeError'>", "'NoneType' object has no attribute '__len__'", '[util/Aquarium.py screenLoop|412] [util/InternalLibrary.py inverseExtend|328] [util/InternalLibrary.py __call__|769] [screen/Controller.py __call__|30] [util/InternalLibrary.py __call__|769] [screen/CommonController.py __call__|49] [util/InternalLibrary.py __call__|769] [screen/AppController.py __call__|214] [util/InternalLibrary.py __call__|771] [monitor/message_tracking.py __call__|308] [screen/Controller.py executeAction|73] [monitor/message_tracking.py doSearchAction|1251] [monitor/message_tracking.py _querySearch|2814] [query/api.py searchData|208] [query/api.py sequence_query|294] [query/api.py searchData|4652]')
 
Version: 16.0.1-017
Serial Number: 420EA0FDF49A77105369-DD12E432498E
Timestamp: 13 Oct 2025 09:19:57 +0800
 
To learn more about alerts, visit our support community and troubleshooting site.  In many cases, you can find more information about this specific alert.
For troubleshooting, see the following URL :
[https://www.Cisco.com/c/en/us/support/security/email-security-appliance/products-tech-notes-list.html](https://www.cisco.com/c/en/us/support/security/email-security-appliance/products-tech-notes-list.html)
For ESA Support, see the Cisco Support Community site :
[https://supportforums.cisco.com/t5/email-security/bd-p/5756-discussions-email-security](https://supportforums.cisco.com/t5/email-security/bd-p/5756-discussions-email-security)
 
If you desire further information, please contact your support provider.
 
To open a support request for this issue, access the IronPort C300V
and issue the "supportrequest" command. The command sends an email with
diagnostic information directly to Cisco IronPort Customer Support to
facilitate a rapid diagnosis of the problem.
 
 
Thank you.

**回答**:
經過分析與相關資料查證，這個錯誤來自於 Cisco IronPort C300V (ESA) 啟用了郵件查詢（message tracking）時，API 查詢程式 query/api.py 的 searchData 函式遇到物件是 None（即未取得預期資料）卻被執行 __len__ 長度運算，所以拋出 "AttributeError: 'NoneType' object has no attribute '__len__'"。[1][2]

### 錯誤成因詳細說明

- 軟體堆疊表明，系統在處理郵件追蹤或查詢 API 時，某個輸入變數或回傳資料並未被正確初始化或帶入（為 None），導致內部對其呼叫 .__len__ 觸發錯誤。[2][1]
- 這常見於查詢參數遺失、資料庫中未查出資料、或物件建立失敗而未有異常保護。[1]
- 依據程式錯誤堆疊與 Python 社群經驗，這種錯誤多半與執行邏輯未處理 None 值或是傳入空值有關（如未檢查輸入合法性）。[1]

### 與現有軟體版本的關聯

- 系統版本為 AsyncOS 16.0.1-017，根據該版釋出說明文件，並未出現與 message tracking API 直接相關的已知重大 Bug，但 release notes 也指出應該回報任何出現應用程式錯誤以便取得後續診斷。[3]
- 有一些已知案例顯示 IronPort 類產品若郵件佇列、查詢參數異常，也可能觸發類似 Application Fault。[4]

### 處理與建議步驟

- 檢查是否有異常查詢操作、或最近有 API 整合、SMTP 查詢條件誤植，導致 message tracking 查詢資料是 None。[2][1]
- 如可行，檢查 IronPort Web UI 或 CLI 錯誤日誌，追蹤是否每次查詢均出現，或僅有特定參數值時觸發。
- 建議執行官方建議的 supportrequest 指令（於 CLI 上），讓 Cisco 支援團隊分析更詳細的例外診斷紀錄。[3]
- 若近期有系統升級或設定變動，建議比對設定及日誌，排查有無版本兼容或資料異常遺漏。
- 若能重現錯誤，可於查詢前預先檢查輸入資料非 None，自行或請原廠補丁強化異常保護。[2]

### 參考資源
- Cisco AsyncOS 16.0.1 Release Notes（版本重大問題與官方支援回報管道說明）[3]
- Python 社群與專案常見 NoneType 運算錯誤說明[1][2]
- 鐵盒 ESA Application Fault 案例[4]

結論：此現象為應用查詢時資料異常，強烈建議比對條件與系統日誌，並依官方程序回報，以便獲取更實務的修補與說明。[4][3]


### 对话 3

**问题**: SR 699889185 : [神隆] 告警信件問題
Ryan Hsu -X (ryahsu)<ryahsu@cisco.com>


​Oli_Chen(陳昶丞);​Joe_Huang(黃昭穎)​
[​attach@cisco.com](mailto:​attach@cisco.com);​tac​
Dear Oli、Joe，您們好。
 
感謝您們連絡思科技術支援中心(Cisco TAC)，我是台灣Security隊的Ryan Hsu，由我來協助您們的案件，您們的案件編號：699889185。
 
 
經由您們提供的問題描述，我理解您們遇到的問題如下：
「客戶收到以下錯誤訊息，想知道其起因及如何處理：
Alert: External mail
 
The Critical message is:
 
An application fault occurred: ('query/api.py searchData|4652', "<type 'exceptions.AttributeError'>", "'NoneType' object has no attribute '__len__'", '[util/Aquarium.py screenLoop|412] [util/InternalLibrary.py inverseExtend|328] [util/InternalLibrary.py __call__|769] [screen/Controller.py __call__|30] [util/InternalLibrary.py __call__|769] [screen/CommonController.py __call__|49] [util/InternalLibrary.py __call__|769] [screen/AppController.py __call__|214] [util/InternalLibrary.py __call__|771] [monitor/message_tracking.py __call__|308] [screen/Controller.py executeAction|73] [monitor/message_tracking.py doSearchAction|1251] [monitor/message_tracking.py _querySearch|2814] [query/api.py searchData|208] [query/api.py sequence_query|294] [query/api.py searchData|4652]')
 
Version: 16.0.1-017
Serial Number: 420EA0FDF49A77105369-DD12E432498E
Timestamp: 13 Oct 2025 09:19:57 +0800
 
To learn more about alerts, visit our support community and troubleshooting site.  In many cases, you can find more information about this specific alert.
For troubleshooting, see the following URL :
[https://www.Cisco.com/c/en/us/support/security/email-security-appliance/products-tech-notes-list.html](https://www.cisco.com/c/en/us/support/security/email-security-appliance/products-tech-notes-list.html)
For ESA Support, see the Cisco Support Community site :
[https://supportforums.cisco.com/t5/email-security/bd-p/5756-discussions-email-security](https://supportforums.cisco.com/t5/email-security/bd-p/5756-discussions-email-security)
 
If you desire further information, please contact your support provider.
 
To open a support request for this issue, access the IronPort C300V
and issue the "supportrequest" command. The command sends an email with
diagnostic information directly to Cisco IronPort Customer Support to
facilitate a rapid diagnosis of the problem.
 
 
Thank you.」
 
若我對本案件的理解有誤差，請讓我知道。
 
 
從該錯誤訊息得知，其與Message Tracking／tracking service(服務)有關。為了更進一步了解本案情，若可取得，請您們協助提供下列資訊：
 
請問目前客戶用Message Tracking時，有無其他問題呢？
 
該ESA/SMA/WSA之遠端存取(Remote Access)／隧道(TUNNEL)資訊，可參考下列 link-->
[Cisco ESA/WSA/SMA 遠端存取的常見問題技術說明 - Cisco](https://apc01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fwww.cisco.com%2Fc%2Fzh_tw%2Fsupport%2Fdocs%2Fsecurity%2Femail-security-appliance%2F117873-faq-esa-00.html&data=05%7C02%7Coli_chen%40genesis.com.tw%7Cb14020e8095c48617bdb08de0a1b7769%7C41641633d15446f589596539058bede9%7C0%7C0%7C638959310264178397%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C0%7C%7C%7C&sdata=ufB6cHqTqycBF7f0kfc9K%2BkvWlHwMCQsn5hyonrC2ds%3D&reserved=0)
遠端存取(Remote Access)／隧道(TUNNEL)資訊包含「產品序號(Serial Number)」及「種子字串(Seed String)」。若情況允許，請複製、貼上該資訊中字元於e-mail 上。
 
 
 
 
我的聯絡方式及值班時段在下方的信件簽名檔中。若您有任何疑問或需協助的地方，歡迎連絡我。謝謝您～
 
 
 
 
徐帥斌(Ryan Hsu)
台灣區技術顧問工程師(Technical Consulting Engineer TW)
.:|:..:|:. | <CX Centre>
標準上班時間: 9:00a.m.～5:00p.m.
電子信件及Webex地址: [ryahsu@cisco.com](mailto:ryahsu@cisco.com)
連絡電話: +886237257611
---------------------------------------------------
組長: John Wang
電子信件: [linhwang@cisco.com](mailto:linhwang@cisco.com)
連絡電話: +886237257622
直屬主管: Chad Chang
電子信件: [chenycha@cisco.com](mailto:chenycha@cisco.com)
連絡電話: +886237257620
______________________________________
外部聯絡上班時間，惠請採用下列連結：
Cisco全球支援聯繫: [https://www.cisco.com/c/en/us/support/web/tsd-cisco-worldwide-contacts.html](https://apc01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fwww.cisco.com%2Fc%2Fen%2Fus%2Fsupport%2Fweb%2Ftsd-cisco-worldwide-contacts.html&data=05%7C02%7Coli_chen%40genesis.com.tw%7Cb14020e8095c48617bdb08de0a1b7769%7C41641633d15446f589596539058bede9%7C0%7C0%7C638959310264208983%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C0%7C%7C%7C&sdata=603JX%2FK7RyZJl%2Fk%2B2u4PnCVrP5x7thTApRpVJrKONw4%3D&reserved=0)
更新您的案件(需要支援聯繫): [https://mycase.cloudapps.cisco.com/](https://apc01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fmycase.cloudapps.cisco.com%2F&data=05%7C02%7Coli_chen%40genesis.com.tw%7Cb14020e8095c48617bdb08de0a1b7769%7C41641633d15446f589596539058bede9%7C0%7C0%7C638959310264231194%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C0%7C%7C%7C&sdata=alQ%2BmX0m%2BM9IXDKsIPaGiVN7Ycchbei0WKE78vVP4gs%3D&reserved=0)
透過TAC聯繫機器人，體驗自助服務: [https://tacconnect.cisco.com/](https://apc01.safelinks.protection.outlook.com/?url=https%3A%2F%2Ftacconnect.cisco.com%2F&data=05%7C02%7Coli_chen%40genesis.com.tw%7Cb14020e8095c48617bdb08de0a1b7769%7C41641633d15446f589596539058bede9%7C0%7C0%7C638959310264240393%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C0%7C%7C%7C&sdata=1rUxC%2F81%2Bw1Hb1b0V6ItK5t91n5NyrPISXopQLZKiMo%3D&reserved=0)
顧客資訊為高度機密。
懇請從下列工具上傳資訊以保護您的資訊。
支援案件管理器Support Case Manager (SCM): [https://mycase.cloudapps.cisco.com/case](https://apc01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fmycase.cloudapps.cisco.com%2Fcase&data=05%7C02%7Coli_chen%40genesis.com.tw%7Cb14020e8095c48617bdb08de0a1b7769%7C41641633d15446f589596539058bede9%7C0%7C0%7C638959310264248631%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C0%7C%7C%7C&sdata=4LqWUmLNmn4q3dwTli9MDAKex47bvYYxW0mwLUIzg5w%3D&reserved=0)>

**回答**:
根據 TAC 工程師 Ryan Hsu 的回覆郵件，可以看出思科已經正式接手案件並開始初步診斷。以下是郵件重點分析與後續建議：[1][2]

### TAC 的問題判斷

Ryan 工程師已經確認錯誤與 **Message Tracking 服務**相關。Message Tracking 是 ESA 的郵件追蹤功能，允許管理員搜尋特定郵件或符合條件的郵件群組，用於郵件流向分析和故障排除。這次的 AttributeError 錯誤發生在執行查詢 API（query/api.py）時，系統試圖處理 None 物件，導致程式崩潰。[2][3][1]

### TAC 要求提供的資訊

**Message Tracking 使用狀況**

工程師詢問使用 Message Tracking 時是否有其他問題，目的是了解：是否每次查詢都出錯、特定條件才觸發、或僅偶發性發生。思科有記錄到類似的間歇性應用程式錯誤案例（如 Bug CSCvv36665），與從隔離區頁面執行追蹤查詢有關。[3][4]

**遠端存取（Remote Access）資訊**

TAC 需要「產品序號」和「種子字串（Seed String）」來建立遠端診斷隧道。這是思科支援團隊標準的故障排除程序，允許工程師直接連線到設備進行深入分析，檢視系統日誌、設定檔和即時運作狀態。[5]

### 建議回應重點

**關於 Message Tracking 問題**

需回答：這個錯誤是否每次使用 Message Tracking 都會發生、還是在特定條件下（例如搜尋特定日期範圍、使用特定篩選條件、從隔離區介面查詢）才出現。若能提供觸發時間點和操作步驟，有助於加速診斷。[4][3]

**提供 Remote Access 資訊**

依據 Ryan 提供的連結，可從 ESA CLI 或 Web GUI 取得遠端存取資訊（包含序號和種子字串）。這是安全的診斷方式，TAC 透過加密隧道連線，不會影響正常運作。[5]

### 可能的解決方向

根據搜尋結果，類似問題可能與以下因素相關：Message Tracking 資料庫初始化問題、特定查詢參數異常、或軟體版本已知臭蟲。TAC 可能會檢查資料庫狀態、查詢日誌、並評估是否需要套用修補程式或升級 AsyncOS 版本。[6][3][4]

此案件已進入正式技術支援流程，建議盡快提供 TAC 要求的資訊，讓工程師能建立遠端連線深入分析，這是最有效率的解決途徑。[4][5]



---

**来源**: [Perplexity AI](https://www.perplexity.ai/search/ni-shi-si-ke-chan-pin-gao-shou-dO1UZHzuShiVDZgeJzoHdg)
