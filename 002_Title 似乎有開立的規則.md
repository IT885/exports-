# Title 似乎有開立的規則

**Thread 编号**: 1  
**Slug**: title-si-hu-you-kai-li-de-gui-L3FY5xJbRpar.6Y.rI3e9w  
**查询次数**: 1  
**最后更新时间**: 2025-10-26T03:15:40.077538  
**模式**: copilot

---

## 内容

### 对话 1

**问题**: Title 似乎有開立的規則

**回答**:
根據目前頁面的資訊，「Support Case Manager」主要負責開立和管理支援案件，提供 Genesis TAC 專案（如 TSMC 專案）的案件建立、狀態追蹤與過濾功能。在案件列表區，有明確的篩選規則與選項，包括：

- 顯示「Open Cases」（開啟中的案件）、Draft Cases（草稿案件）及 Closed Cases（已結案案件）
- 可依「Created」（建立日期）或「Updated」（更新日期）及「Sev」（等級）等條件進階篩選
- 案件標題有明確命名規則，一般格式如「[專案/系統] 問題描述」：例「[TSMC-H-OA] F2/5 subfab iphone wifi issue」或「[FET] C8200-1N-4T CpuCatastrophicError」
- 案件狀態包括：Cisco Pending、Customer Pending、Service Order Pending、Not Submitted、Close Pending 等

整體而言，此平台有完整的案件開立與管理流程，並確實區分案件狀態和標題命名規則。如果你要查找特定案件或規則，可以利用「Show Advanced Filters」進一步篩選，也可匯出 Excel 檔進行後續分析。

如需更細緻規則說明，請指定要查詢的案件類型或範例，我可協助進行更深層分析。


### 对话 2

**问题**: 我是說 這一頁的Title 好像有規則

**回答**:
依據 Support Case Manager 這一頁的案件標題，確實存在明顯的命名規則與格式慣例，主要可歸納如下：

- 大部分標題會以「[專案/客戶名/系統]」作為前綴，置於中括號內，如 [TSMC-H-OA]、[FET]、[ITRI]、[MXIC]、[UMC-TN]。
- 客戶名稱/專案代碼之後，常接地點或系統型號資訊，例如 F2/5、93108、C8200-1N-4T。
- 接下來是主要設備或問題描述，像是「iphone wifi issue」、「CpuCatastrophicError」、「Jabber推播異常」、「GUI Loading很久」、「RF Profile setting not taking effect」等。
- RMA 案件多改用「RMA + 型號」方式，如「RMA CP-7841-NC-K9=」
- 部分長標題可能包含國際地點/多地資訊，以及故障現象與需求說明（如「Germany and Taiwan dial Belgium abnormally」、「need support for switch device between old and new」）。

**常見標題格式範例如下：**
- [TSMC-H-OA] F2/5 subfab iphone wifi issue
- [FET] C8200-1N-4T CpuCatastrophicError
- [ITRI] Jabber推播異常，現已恢復，請協助確認原因
- [MXIC] Voice Message Forwarding Issue
- [UMC-TN] Cat9K version 17.12.5 critical Bug verify
- RMA CP-7841-NC-K9=
- TSMC-H-DC F12P4 9504 設備異常

**規則歸納：**
- 前綴以「[專案/客戶/系統]」中括號表示
- 地點/分類/型號於括號後，常用空格/符號隔開
- 描述以英文或中英文混合簡述問題現象、維護需求或設備型號
- RMA案件有特殊命名（RMA xxxxx型號）

如果你需要萃取格式作為自動化生成規則，可採用：
`[專案/客戶/系統] 地點/型號 問題或現象描述`

這個規則通用於 Genesis/Cisco/TSMC 系統案件管理。[1]


### 对话 3

**问题**: 如果是這個 RT18-18P7Z3Y17-4-24-BDR-MS 命名會是怎樣

**回答**:
依據目前 Support Case Manager 的命名慣例，你給的「RT18-18P7Z3Y17-4-24-BDR-MS」屬於設備/位置詳細編碼，可以直接套用既有格式作標題。建議如下：

### 範例一（精簡型）
[TSMC-T-DC] RT18-18P7Z3Y17-4-24-BDR-MS failure

- `[TSMC-T-DC]`：專案/地區前綴（台積電台南資料中心）
- `RT18-18P7Z3Y17-4-24-BDR-MS`：完整設備編碼
- `failure`：問題描述（可依實際狀況替換）

### 範例二（細節型）
[TSMC-T-DC] F18P7 RT18-18P7Z3Y17-4-24-BDR-MS switch connectivity issue

- `[TSMC-T-DC]`：前綴
- `F18P7`：簡稱樓層/廠區（若編碼中有代表意義可補充）
- `RT18-18P7Z3Y17-4-24-BDR-MS`：設備編碼
- `switch connectivity issue`：具體問題說明

**各欄位意義推導：**
- `RT18`：類型（可能是Router/交換機）
- `18P7Z3Y17`：場域、樓層或設備區域
- `4-24`：機架/端口序號
- `BDR-MS`：角色（如Border/Main Switch）

這樣的命名完全符合 Genesis/Cisco/TSMC 案件標題習慣。[1]


### 对话 4

**问题**: 讀取Contact Information 所有的資訊

**回答**:
Contact Information 區塊內容如下：

- **名稱 (NAME)：** genesis tac
- **商務電話 (BUSINESS PHONE)：** +886981293269
- **首選聯絡方式 (PREFERRED CONTACT METHOD)：** Email
- **案件通知 (CASE NOTIFICATIONS)：** Off

- **電子郵件 (EMAIL)：** joe_huang@genesis.com.tw
- **副本清單 (CC LIST)：**
  - Joe_Huang@genesis.com.tw
  - Oli_Chen@genesis.com.tw
  - tsmc-bcs@cisco.com

- **RADKIT 服務 ID (RADKIT SERVICE ID)：** [可編輯，未顯示具體值]

此區域完整列出案件聯絡窗口、信箱與副本群組，涵蓋電話、主要聯絡管道，以及案件通知狀態設定。這些資訊適合用於 Cisco TAC 溝通、直接聯繫或技術支援協調。[1]



---

**来源**: [Perplexity AI](https://www.perplexity.ai/search/title-si-hu-you-kai-li-de-gui-L3FY5xJbRpar.6Y.rI3e9w)
