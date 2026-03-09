# EVE-NG 完整有系統性的介紹一下

**Thread 编号**: 40  
**Slug**: eve-ng-wan-zheng-you-xi-tong-x-71JjIMbZRtOQhMzUsdydUw  
**查询次数**: 1  
**最后更新时间**: 2025-10-05T06:10:55.156459  
**模式**: copilot

---

## 内容

### 对话 1

**问题**: EVE-NG 完整有系統性的介紹一下

**回答**:
# EVE-NG 系統性介紹

EVE-NG（Emulated Virtual Environment Next Generation）是一款非常受歡迎的網路模擬平台，被網路工程師、IT 專業人員與培訓機構廣泛採用。它允許用戶在純虛擬環境下，快速建置、測試並管理各種複雜的網路拓撲和裝置。同類工具有 GNS3，但 EVE-NG 在整合多廠商、多種系統虛擬化以及網頁化操作體驗上有明顯優勢。[1][2][3][4][5][6]

**主要特點與架構：**
- 支援 Cisco、Juniper、Fortinet、Palo Alto 等主流設備，以及一般的 Linux、Windows 虛擬機，也能模擬防火牆、負載平衡器、KVM、Docker 等。[3][5][8][1]
- 無客戶端設計，用戶僅需瀏覽器即可操作（HTML5 Web UI），方便在任何作業系統上部署和運用。[2][4][3]
- 高度整合 Dynamips、IOL、QEMU、KVM 等虛擬化技術。[5][3]
- 適合學習認證（如 CCNA/CCNP/CCIE）、新技術驗證、企業研發測試與團隊協作。

**基本運作流程：**
1. 部署 EVE-NG（可安裝於實體主機、VMware、VirtualBox、雲端等,建議下載 OVA/OVF 映像直接導入）。[7][2][5]
2. 首次安裝設置網路、時區等系統參數，開啟後以網頁瀏覽器連線，登入管理介面。
3. 透過 GUI 拖曳網路設備，設置連線，進行組網測試。
4. 可以匯入設備映像檔（像 Cisco IOS、Juniper JunOS、各種 qcow2 虛擬機映像），配合授權後啟動。
5. 可多⼈協同編輯、儲存與分享 LAB 項目。

**版本說明：**
- 社群版（免費，功能豐富，足夠個人與小型團隊實驗室運作）。
- 專業版（收費，增加如多人協作、進階分權、API 支援等強大企業級功能）。[6][5]

***
你希望以哪個角度或用途來深入了解 EVE-NG？例如：
- 入門安裝與基礎操作
- 進階網路模擬應用
- 團隊協作與自動化
還是某一類設備或認證模擬？


### 对话 2

**问题**: 如何創建第一台Cisco NX-OSv 9K

**回答**:
創建第一台 Cisco NX-OSv 9K 節點於 EVE-NG 的步驟如下，涵蓋映像上傳、目錄配置、啟動、以及基礎啟動設定流程：[1][2][3]

### 步驟一：準備映像檔與目錄

1. 下載 Cisco NX-OSv 9K 的 qcow2 映像檔（需合法來源或 Cisco 官網授權）。[2]
2. 使用 SSH 工具（例如 WinSCP/FileZilla）以 root 帳號登入 EVE-NG 伺服器。
3. 在主機 CLI 執行以下指令，創建專用目錄（以 nxosv9k-7.0.3.I7.4 為範例）：
   ```
   mkdir /opt/unetlab/addons/qemu/nxosv9k-7.0.3.I7.4/
   ```
4. 將映像檔上傳至上述目錄後，將檔案重新命名為 sataa.qcow2：
   ```
   cd /opt/unetlab/addons/qemu/nxosv9k-7.0.3.I7.4/
   mv nxosv-final.7.0.3.I7.4.qcow2 sataa.qcow2
   ```
5. 修正映像權限：
   ```
   /opt/unetlab/wrappers/unl_wrapper -a fixpermissions
   ```

### 步驟二：於 EVE-NG 新增 NX-OSv 9K 節點

1. 透過網頁 GUI 登入 EVE-NG。
2. 在專案實驗室（LAB）中新增一個節點，類型選擇 Cisco NX-OSv 9000 Switch（如果正確上傳映像，即可在“新增節點”清單看到 NX-OSv 9K）。
3. 保存並啟動該節點。

### 步驟三：初次設定與開機流程

1. 首次啟動大約需數分鐘，待 Console 連線完成，可以看到類似提示：
   ```
   Abort Auto Provisioning and continue with normal setup ?(yes/no)[n]: yes
   Do you want to enforce secure password standard (yes/no): no
   Enter passwords for admin: admin
   ```
2. 登入管理員帳號：帳號 admin、密碼 admin（如提示）。
3. 執行 `dir bootflash:` 查詢 NX-OS 映像檔。
4. 於 loader 模式輸入：
   ```
   loader > boot nxos.7.0.3.I7.4.bin
   ```
   或於開機後進入全域設定：
   ```
   switch# conf t
   switch(config)# boot nxos bootflash:nxos.7.0.3.I7.4.bin
   end
   copy run start
   ```
5. 節點重啟後，每次開機將會順利進入 NX-OSv 系統。[3][1][2]

***

### 注意事項

- NX-OSv 9K 消耗資源較高，建議配置至少 8GB RAM 及兩顆實體 CPU Core。
- 映像目錄名稱「nxosv9k-版本號」需全小寫，檔案名稱需為 sataa.qcow2。
- 各 NX-OSv 9K 版本或型號需依照官方命名規則建立目錄（可查閱映像兼容表）。

***

如有不同 NX-OSv 版本或進階自動化需求，可進一步延伸。此流程可應用於所有 NX-OSv 9K 映像安裝與啟動。[1][2][3]


### 对话 3

**问题**: Notifications
×Lab has been saved (60023).

**回答**:
這是 EVE-NG 的**成功儲存通知**，表示您的實驗室（Lab）配置已成功保存。[1][2][3]

### 通知說明

**"Lab has been saved (60023)"** 代表以下資訊：
- Lab 的拓撲結構、節點配置、連線關係已儲存至伺服器。
- 括號內的數字 60023 可能是內部儲存操作代碼或時間戳記標識。[4][5]

### 儲存內容包含

當 EVE-NG 儲存 Lab 時，會保存以下項目：
- 拓撲圖中的節點位置與類型
- 節點之間的網路連線
- Lab 名稱、描述、作者等屬性
- 各節點的啟動設定（但不包含設備運行時的 running-config，除非已寫入 NVRAM）

### 後續操作建議

1. **確認設備配置已保存**：對於已完成配置的網路設備（如 Cisco、Juniper 等），需在設備上執行 `copy running-config startup-config` 或 `commit` 指令，才能將設備配置寫入 NVRAM，否則重啟後配置會遺失。[3]

2. **匯出 Lab 備份**：可透過 Lab Details → Export 功能，將整個 Lab 匯出為 ZIP 檔案，作為離線備份或分享用途。[6][7]

3. **關閉節點**：若暫時不使用，可安全地關閉所有節點（Stop all nodes），下次啟動時會從上次儲存的狀態繼續。[3]

此通知確認您的 Lab 環境已安全儲存，可以放心登出或繼續實驗。[1][3]


### 对话 4

**问题**: 有中文化的 EVE-NG

**回答**:
EVE-NG 的介面**官方預設僅支援英文**，但社群與第三方已經開發出多套「中文化（漢化）補丁」可以讓網頁介面、實驗室名稱、部分提示翻譯成中文，流程說明如下：

***

**實現方式：**

- 需下載對應版本的「漢化包」或「中文語言包」，常見都針對 Community 社群版（如 5.x、6.x 系列）[1][2][3][4][5]
- 安裝流程：  
  1. 登入 EVE-NG 主機（root 帳號），將漢化包解壓至 `/opt/unetlab/` 目錄
  2. 覆蓋原本的 html 及 js 資料夾內容（建議先快照或備份原始資料）
  3. 清空瀏覽器快取或強制刷新（ctrl+F5）
  4. 重新打開 EVE-NG 網頁，會看到中文化介面
- 內容涵蓋：登入頁、使用者管理、系統監控、工具條、Lab 新建等主要操作細節皆有中文翻譯[2][3][4][5][1]

***

**使用注意事項：**

- 多數「漢化包」非官方出品，更新版本可能不完全兼容，升級官方新版需重新安裝漢化包
- 最新 6.x 社群版已有人製作新版中文版，用前務必查看是否對應 Ubuntu 版本，常用建議搭配 Ubuntu 20.04
- 建議先備份原版資料，有些網頁 Console 或 JS 翻譯可能影響功能，出現顯示異常可退回原版 html 或清除漢化資料
- 下載來源包含 EVE-NG 中文網、社群論壇（如 emulatedlab、CSDN部落格、B站影片等），需自行辨別安全性

***

**參考連結及資源：**
- [EVE-NG 中文網漢化版教學與下載][1]
- [CSDN 漢化包教學][5][6][2]
- [EmulatedLab 漢化補丁（6.2.0-4 社群版）][3]
- [社群分享安裝步驟][4][7][8]

***

**總結：**  
EVE-NG 只要安裝社群漢化包，即可輕鬆切換為中文界面，大幅降低第一次使用的學習門檻。不過，使用漢化包時，建議保留英文原版快照，確保日後升級與兼容性。


### 对话 5

**问题**: 列出流程

**回答**:
## EVE-NG 中文化安裝完整流程

### 前置準備

**必要工具與檔案：**
1. SSH/SFTP 連線工具（例如：MobaXterm、Xshell、WinSCP、FileZilla）[1][2]
2. 對應版本的漢化包（例如：5.0.1-13 或 6.2.0-4 社群版漢化包）[2][3][4]
3. 建議先對 EVE-NG 虛擬機進行快照備份[3][1][2]

**版本兼容性注意事項：**
- EVE-NG 6.2.0-4 官方建議搭配 Ubuntu 20.04 LTS[5][1]
- Ubuntu 22.04 可能導致漢化後無法登入或相容性問題[1][5]
- 現有漢化包主要針對 5.0.1-13 或 6.2.0-4 版本，6.x 官方尚未正式發布漢化包[4][1]

***

### 安裝步驟

**步驟 1：建立系統快照（強烈建議）**
在進行任何操作前，先對 EVE-NG 虛擬機建立快照，以便失敗時可快速還原。[6][2][3]

**步驟 2：連線至 EVE-NG 主機**
使用 SSH/SFTP 工具連線到 EVE-NG 伺服器：
- 帳號：`root`
- 密碼：預設為 `eve`（或安裝時設定的密碼）[2][1]

**步驟 3：下載與解壓縮漢化包**
從可信賴來源下載對應版本的漢化包，並在本地解壓縮（通常為 ZIP 或 TAR.GZ 格式）。[3][4][2]

**步驟 4：備份原始檔案（選用但建議）**
在 EVE-NG 主機執行以下指令備份原始目錄：
```bash
cp -r /opt/unetlab /opt/unetlab_backup
```

**步驟 5：上傳漢化包至 EVE-NG**
透過 SFTP 工具（如 WinSCP、MobaXterm）將解壓後的 `opt` 資料夾直接拖曳上傳至 EVE-NG 根目錄（`/`），選擇「覆蓋」原有檔案。[6][1][2]

具體路徑為：將 `opt` 資料夾內的內容覆蓋至 `/opt/unetlab/` 目錄。[2][3]

**步驟 6：修正檔案權限（選用）**
在 SSH 終端執行以下指令確保檔案權限正確：
```bash
/opt/unetlab/wrappers/unl_wrapper -a fixpermissions
```

**步驟 7：清除瀏覽器快取並刷新**
1. 回到瀏覽器，按下 `Ctrl + F5`（Windows）或 `Cmd + Shift + R`（macOS）強制刷新頁面[4][2]
2. 或手動清除瀏覽器快取後重新登入[2]

**步驟 8：驗證中文化介面**
重新登入 EVE-NG 網頁介面（預設帳號：`admin`，密碼：`eve`），確認介面已變更為中文。[1][2]

***

### 常見問題排除

**問題 1：漢化後無法登入或登入無響應**
- **原因**：使用 Ubuntu 22.04 版本，與漢化包不相容[5][1]
- **解決方案**：重新安裝 EVE-NG，選擇 Ubuntu 20.04 LTS 版本後再進行漢化[5][1]

**問題 2：漢化後部分功能異常**
- **原因**：漢化包版本與 EVE-NG 版本不匹配[1]
- **解決方案**：還原快照，或手動刪除 `/opt/unetlab/html` 目錄後重新安裝官方檔案[3]

**問題 3：漢化包下載來源失效**
- 建議從 EVE-NG 中文網、EmulatedLab 論壇、或 CSDN 部落格等社群資源取得[7][4][3][2]

***

### 還原至英文版

若需還原至官方英文版本：
1. 刪除漢化的 `/opt/unetlab/html` 目錄
2. 重新安裝 EVE-NG 或從快照還原[3][2]

***

此流程適用於 EVE-NG 社群版 5.x 與 6.x 系列，建議依照版本選擇對應漢化包，並在操作前務必建立快照備份。[4][1][2][3]



---

**来源**: [Perplexity AI](https://www.perplexity.ai/search/eve-ng-wan-zheng-you-xi-tong-x-71JjIMbZRtOQhMzUsdydUw)
