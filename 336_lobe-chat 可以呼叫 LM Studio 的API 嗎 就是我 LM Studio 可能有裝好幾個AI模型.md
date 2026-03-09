# lobe-chat 可以呼叫 LM Studio 的API 嗎 就是我 LM Studio 可能有裝好幾個AI模型

**Thread 编号**: 335  
**Slug**: lobe-chat-ke-yi-hu-jiao-lm-stu-9fDWugULRfWnQR2ZDkRsMg  
**查询次数**: 1  
**最后更新时间**: 2025-05-01T15:17:08.634982  
**模式**: copilot

---

## 内容

### 对话 1

**问题**: lobe-chat 可以呼叫 LM Studio 的API 嗎 就是我 LM Studio 可能有裝好幾個AI模型

**回答**:
是的，LobeChat 可以呼叫 LM Studio 的 API，並且能夠使用您在 LM Studio 中安裝的多個 AI 模型。

LobeChat 具有連接多種 AI 模型的能力，包括本地運行的大型語言模型。根據提供的資訊，LobeChat 與 LM Studio 的整合有以下幾點要點：

1. LobeChat 整合了多個頂尖 AI 模型，包括 ChatGPT、Claude、Gemini、Groq、Ollama 等，為用戶提供了極大的靈活性和選擇。[2]

2. LM Studio 採用了與 OpenAI 相容的接口，這意味著 LobeChat 可以透過 OpenAI 連接器來實現與 LM Studio 的連接，無需特定的 LM Studio 接口。[5]

3. 在 2025 年 1 月 15 日，LobeChat 的開發團隊已經在一個 PR（Pull Request）中正式添加了對 LM Studio 的支持。考慮到現在已是 2025 年 5 月，這個功能很可能已經正式上線。[5]

4. 您可以透過 Docker 部署 LobeChat，然後將其連接到由 LM Studio 運行的本地模型。具體來說，您需要：[5]
   - 在 LM Studio 中啟動模型服務
   - 在 LobeChat 的設置中配置一個 OpenAI 語言模型，並指向 LM Studio 的 API 地址

值得注意的是，某些模型（如文中提到的 DeepSeek R1）可能不支持 Function Calling 功能，這會導致無法使用 LobeChat 中的插件功能。[5]

與 ChatGPT Plus 不同，LobeChat 明確支持「存取多個 LLM」和「運行本地 LLM」的功能，這正是您想要的功能-在 LM Studio 中安裝多個 AI 模型並通過 LobeChat 呼叫它們。[2]

總結來說，LobeChat 確實可以呼叫 LM Studio 的 API，並且能夠訪問您在 LM Studio 中安裝的多個 AI 模型，這為您提供了更加靈活且強大的 AI 對話體驗。


### 对话 2

**问题**: LibreChat 也可以嗎

**回答**:
是的，LibreChat 也可以呼叫 LM Studio 的 API，並使用您在 LM Studio 中安裝的多個 AI 模型。

根據搜尋結果，LibreChat 的主要特點之一就是支援多種 AI 模型，不僅包括雲端服務如 OpenAI、Google Vertex AI、Anthropic Claude 等，還兼容多種本地 AI 服務。[2]

具體來說，LibreChat 可以與 LM Studio 整合的方式如下：

1. 首先，您需要在 LM Studio 中啟用伺服器模式（Server Mode），這在預設情況下是停用的。LM Studio 提供了一個本地伺服器，讓您可以透過 API 呼叫所載入的模型。[1][3][4]

2. 在 LibreChat 中，您需要在 `librechat.yaml` 配置文件中添加 LM Studio 的連接信息。一個具體的配置範例如下：[4]
   ```
   name: "Mistral 7B"
   apiKey: "sk-1234"  # 可以使用任何虛擬密鑰
   baseURL: "http://localhost:1234/v1"
   models:
     default: [ "local-model", ]
   ```

3. 值得注意的是，您需要提供一個虛擬的 API 密鑰（可以是任何字串，如 "sk-1234"），並將 baseURL 設定為 LM Studio 的本地伺服器地址（通常是 http://localhost:1234/v1）。[4]

4. 在 LM Studio 中，您可以載入多個不同的模型，然後通過上述配置在 LibreChat 中使用這些模型。[3][1]

LibreChat 的這種靈活性讓您可以根據不同任務選擇最適合的模型，或者比較不同模型的表現，這與您想要的功能（在 LM Studio 中安裝多個 AI 模型並通過 LibreChat 呼叫它們）完全吻合。[2]

此外，LibreChat 還提供了豐富的功能，如對話歷史保存、消息搜索、自定義預設、多模態對話（支持圖像分析）、語音交互等，進一步增強了用戶體驗。[2]


### 对话 3

**问题**: 那我如果有要分析 影片 或是生成語音撥放 還是要做語音轉文字 或是文字轉語音 模型我用 多模態的
Qwen2.5-Omni 語言模型 上述的 LibreChat 及LobeChat都可以上傳檔案 去處理嗎?
但是我記得LobeChat好像要SERVER DB版的才可以上傳沒錯吧 一般的LobeChat好像不行上傳副檔沒錯吧

**回答**:
是的，關於您的問題，我可以提供以下資訊：

## 關於 LobeChat 的檔案上傳功能

您的記憶是正確的。LobeChat 確實需要使用伺服器端資料庫版本才能支援檔案上傳功能：

- LobeChat 在客戶端資料庫模式下，資料僅儲存在用戶的本地裝置上，不支援檔案上傳和知識庫等進階功能。[10]
- 官方文件明確指出：「客戶端資料庫模式...不支援檔案上傳和知識庫等進階功能」。[10]
- 若要使用檔案上傳功能，您需要部署具有伺服器端資料庫的版本。[10]

當您成功部署伺服器端資料庫版本後，LobeChat 確實支援多種檔案的上傳和處理：

- LobeChat 支援上傳各種類型的檔案，包括文件、圖像、音訊和影片。[7][9]
- 這些功能已在 2024 年 8 月 31 日正式發布，可用於開源版本和雲端版本。[5]

## 關於 LibreChat 的檔案上傳功能

LibreChat 也支援檔案上傳，但有一些注意事項：

- 根據 Reddit 上的討論，有用戶報告 LibreChat 只接受圖像格式，而對其他格式（如 PDF、CSV、docx 等）會顯示「Error processing file」錯誤。[8]
- 解決方法是使用 LibreChat 的「Assistants」功能，並確保 RAG（檢索增強生成）功能正在運行。[8]
- 您需要使用最新的 Docker 映像和 compose 檔案來確保 RAG 正常運行。[8]

## 關於 Qwen2.5-Omni 多模態處理能力

Qwen2.5-Omni 確實是一個功能強大的多模態模型：

- 它設計用於感知多種模態，包括文字、圖像、音訊和影片。[2]
- 它支援即時語音和影片聊天、自然語音生成等功能。[2]
- 它採用了名為「Thinker-Talker」的架構，可以同時處理多種模態並產生文字和自然語音回應。[2]

總結來說，如果您想使用 Qwen2.5-Omni 模型來分析影片、生成語音、進行語音轉文字或文字轉語音，兩個平台都可以支援，但您需要：

1. 對於 LobeChat：部署伺服器端資料庫版本
2. 對於 LibreChat：確保使用最新版本並正確設定 Assistants 功能和 RAG


### 对话 4

**问题**: 除了上述還有其他的開源項目嗎?

**回答**:
是的，除了之前提到的 LobeChat、LibreChat、LM Studio、Ollama、GPT4ALL 和 Jan.ai 外，還有許多值得關注的開源多模態 AI 項目：

## 多模態模型

**CogVLM**：2023 年被公認為最先進的開源多模態模型，在理解和回答跨文本和圖像的問題方面表現優異，超越許多同類型模型。[1]

**LLaVA 1.5**：開源的 ChatGPT 替代品，讓用戶能夠使用圖像和文本進行對話，設計專注於通過視覺輸入增強用戶互動。[1]

**Adept's Fuyu**：以解釋圖表、文檔和用戶界面的能力著稱，代表多模態 AI 能力的重要進步。[1]

**Meta 的貢獻**：推出了 **ImageBind** 和 **AnyMAL** 等模型，進一步豐富了開源生態系統，這些模型旨在整合各種數據類型，增強它們在現實世界場景中的適用性。[1]

## 應用平台與框架

**Local Multimodal AI Chat**：一個整合各種 AI 模型的多模態聊天應用，可在單一界面中無縫管理音頻、圖像和 PDF，使用 Whisper AI 處理音頻，LLaVA 管理圖像，以及 Chroma DB 處理 PDF。[3]

**Streamlit Multimodal Chat Input**：一個 Streamlit 組件，啟用多模態聊天界面，允許用戶在 Streamlit 應用程序中輸入文本和上傳圖像。[7]

## 語音與音頻工具

**Coqui.ai**：使用 TensorFlow 和 PyTorch 框架的開源項目，具有改進的自然語言處理模型，為視頻遊戲、後期製作、配音等生成 AI 語音。特色包括語音克隆、生成式語音和語音控制。[5]

## 完全本地化多模態系統

還有一個完全開源、本地部署的多模態 AI 助手項目，結合了：
- **Whisper**：用於語音轉文本
- **Qwen2.5-VL**：用於多模態理解和生成
- **Kokoro**：用於文本轉語音
所有這些通過 Python WebSocket 服務器進行協調。[10]

這些項目展示了開源社區在多模態 AI 領域的蓬勃發展，提供了從模型到應用框架的完整解決方案，滿足各種需求和使用場景。



---

**来源**: [Perplexity AI](https://www.perplexity.ai/search/lobe-chat-ke-yi-hu-jiao-lm-stu-9fDWugULRfWnQR2ZDkRsMg)
