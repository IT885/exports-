# 我要請VSCODE安裝 關於您提到的 "Serena" 和 "MCP" 套件
你說明一下

**Thread 编号**: 102  
**Slug**: wo-yao-qing-vscodean-zhuang-gu-E7aYOWQ0TEm33nTbmaGrfQ  
**查询次数**: 1  
**最后更新时间**: 2025-07-25T09:54:46.693697  
**模式**: copilot

---

## 内容

### 对话 1

**问题**: 我要請VSCODE安裝 關於您提到的 "Serena" 和 "MCP" 套件
你說明一下

**回答**:
# VSCode「Serena」與「MCP」套件說明

## 什麼是 Serena？

- **Serena** 是一套專為 Visual Studio Code（VSCode）環境設計的強大 AI 編碼代理工具包，能把大型語言模型（LLM）變成具備「資料夾與程式碼層級操作」的智慧代理人，直接與你的專案程式碼互動。[1][2][3]
- Serena 的「MCP Server」本質上是一個標準協議（Model Context Protocol, MCP）的伺服器，讓 LLM 或其他 MCP 客戶端能夠用自然語言指令，請求讀寫、更改、檢查整個程式碼庫，進行像人類開發者般的編輯、瀏覽、診斷等動作。[2]

### Serena MCP Server 的能力特色

- **語意搜尋**、**語法結構分析**、**快速檢索工程架構**。
- 支援直接使用 VSCode 核心 API：如檔案/資料夾瀏覽、文件結構、符號搜尋、取得函式定義、編輯檔案、替換特定區段、錯誤診斷等。[2]
- 免費開源，安裝彈性高，不綁定特定 LLM 平台。[2]

### Serena 安裝與啟用簡要流程

1. 透過 GitHub Clone 專案檔案（範例指令）：  
   ```bash
   git clone https://github.com/oraios/serena.git
   cd serena
   ```
2. 使用工具（如 `uvx`）啟動 Serena MCP 伺服器：  
   ```bash
   uvx --from git+https://github.com/oraios/serena serena-mcp-server
   ```
3. 可針對大型專案預先建立索引以提升效能。[2]

## 什麼是 MCP？VSCode MCP Server 簡介

- **MCP（Model Context Protocol）** 是一套標準協議，讓 AI 助手透過統一介面與 VSCode 或第三方工具深度整合。[4][5][6]
- **VSCode MCP Server** 是官方或第三方開發的套件，能將你的 VSCode 啟用為 MCP 伺服器。安裝此擴充套件後，MCP 客戶端（如 Claude、Copilot 或 Serena）將可直接控制 VSCode 的檔案瀏覽、讀寫、自動化程式碼維護與測試等。[6][7][8][4]

### MCP Server 的功能

- **列出資料夾/檔案內容**、**讀取/編輯檔案**、**搜尋符號**、**取得錯誤診斷**、**執行終端機命令**等。
- 可設置獨立網路埠，並動態管理啟停與安全性。
- 支援工作區配置 `.vscode/mcp.json`、用戶全域設置、指令式安裝，與多種自動發現（例如可同步 Claude Desktop 配置）。[5][7][8][4][6]

### VSCode MCP Server 安裝方法

1. 直接從 VSCode 擴充套件市集搜尋並安裝「MCP Server」相關套件。
2. 或從官方介紹頁面，點選「Install」加入 VSCode。[8][5]
3. 進階用戶可以 `npm install`、`npm run compile` 自行安裝編譯。[7][9]

## Serena 與 MCP 的關係

- Serena 是功能完整的 MCP Server 典範，代表「MCP 協議」＋「智慧 AI 編碼工具集」的結合，適合高階開發者與自建 LLM 工作流。[3][2]
- MCP Server 的 VSCode 套件則讓更多 AI 助手（如 Claude、Copilot）可以在 VSCode 如同原生外掛般協作與共用。[5][6][7]

## 注意事項與安全提醒

- MCP / Serena 伺服器會讓 AI 客戶端取得 VSCode 的檔案系統和終端機控制權，請僅使用並信任來源可靠之客戶端或代理。[7][5][2]
- 若有進階流程需求，請詳細參閱各自官方文件以自訂專屬開發或部屬方案。

### 相關參考

- Serena GitHub: [oraios/serena][1]
- VSCode MCP Server: [vscode-mcp-server][8][7]
- 微軟官方 MCP 文件：[MCP developer guide]、[VSCode MCP使用介紹][4][5]
- 中文 MCP 概覽：[Lobehub MCP說明][6]

註：如需安裝與設定進一步教學，歡迎提出您的具體需求。



---

**来源**: [Perplexity AI](https://www.perplexity.ai/search/wo-yao-qing-vscodean-zhuang-gu-E7aYOWQ0TEm33nTbmaGrfQ)
