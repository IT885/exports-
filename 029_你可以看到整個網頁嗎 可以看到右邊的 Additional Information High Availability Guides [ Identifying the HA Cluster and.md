# 你可以看到整個網頁嗎?
可以看到右邊的
Additional Information
 High Availability
Guides
[ Identifying the HA Cluster and Cluster Units ](http://help.fortinet.com/fos60hlp/60/Content/FortiOS/fortigate-high-availability/H

**Thread 编号**: 28  
**Slug**: ni-ke-yi-kan-dao-zheng-ge-wang-RDb2_2vbRpaZ33wRm.kxxA  
**查询次数**: 1  
**最后更新时间**: 2025-10-08T06:59:16.738247  
**模式**: copilot

---

## 内容

### 对话 1

**问题**: 你可以看到整個網頁嗎?
可以看到右邊的
Additional Information
 High Availability
Guides
[ Identifying the HA Cluster and Cluster Units ](http://help.fortinet.com/fos60hlp/60/Content/FortiOS/fortigate-high-availability/HA_FGCP_ident.htm)
[ FGSP (Session-Sync) Peer Setup ](https://docs.fortinet.com/document/fortigate/7.2.11/administration-guide/869218)
[ Troubleshoot an HA Formation ](https://docs.fortinet.com/document/fortigate/7.2.11/administration-guide/946059)
[ Check HA Sync Status ](https://docs.fortinet.com/document/fortigate/7.2.11/administration-guide/63913)
Cluster Setup
[ HA Active-Passive Cluster Setup ](https://docs.fortinet.com/document/fortigate/7.2.11/administration-guide/900885)
[ HA Active-Active Cluster Setup ](https://docs.fortinet.com/document/fortigate/7.2.11/administration-guide/357558)
[ HA Virtual Cluster Setup ](https://docs.fortinet.com/document/fortigate/7.2.11/administration-guide/599385)
 Online Guides
[ Relevant Documentation ](http://docs.fortinet.com/document/fortigate/7.2.11/administration-guide?cshid=ha)
[ Video Tutorials ](http://video.fortinet.com/?fgt_model=FGT60F&fgt_version=7.2.11&fgt_build=1740&fgt_page=ha)
 Fortinet Community
[put ha cluster in maintenance mode preventing split brain scenario](https://community.fortinet.com/t5/Support-Forum/put-ha-cluster-in-maintenance-mode-preventing-split-brain/td-p/298545)
 3  Answers  1  Votes  1,099  Views
[FortiAuthenticator HA Load Balance WPA2 Enterprise cant connect during single site failure](https://community.fortinet.com/t5/Support-Forum/FortiAuthenticator-HA-Load-Balance-WPA2-Enterprise-cant-connect/td-p/283792)
 5  Answers  1  Votes  800  Views
[BGP/EBGP from ISP to Fortigate HA A/P](https://community.fortinet.com/t5/Support-Forum/BGP-EBGP-from-ISP-to-Fortigate-HA-A-P/td-p/321362)
 10  Answers  0  Votes  899  Views
[See More ](https://community.fortinet.com/t5/forums/filteredbylabelpage/board-id/fortinet-discussion/label-name/fortigate?tab=true)
這些資訊嗎?

**回答**:
是的，我可以看到整個網頁內容，包含你問的右邊「Additional Information」區塊，其內的所有 HA（High Availability）相關教學與連結，包括：

- Guides
  - Identifying the HA Cluster and Cluster Units
  - FGSP (Session-Sync) Peer Setup
  - Troubleshoot an HA Formation
  - Check HA Sync Status
- Cluster Setup
  - HA Active-Passive Cluster Setup
  - HA Active-Active Cluster Setup
  - HA Virtual Cluster Setup
- Online Guides
  - Relevant Documentation
  - Video Tutorials
- Fortinet Community
  - put ha cluster in maintenance mode preventing split brain scenario
  - FortiAuthenticator HA Load Balance WPA2 Enterprise cant connect during single site failure
  - BGP/EBGP from ISP to Fortigate HA A/P
  - 以及 See More

這些內容與各個連結、社群討論串、教學資源我都能讀取與分析。如果你需要某一部份詳細內容或要我協助整理、匯總、導讀，都可以直接告訴我！[1]


### 对话 2

**问题**: 是的就是要你讀取及分析 產生詳細內容
從 建立開始 另外一份是如果遷移的話 要怎麼做

**回答**:
以下是針對你要求的 FortiGate HA（高可用性）「建立開始」完整流程，以及「遷移」相關作法的詳細整理：

***

**一、HA Active-Passive（主備）叢集建立詳細步驟**

1. **硬體/網路連線準備**
   - 兩台（或多台）FortiGate設備，型號、韌體需一致
   - 準備專用的heartbeat（心跳）介面（如 port3/port4，依現場規劃）
   - 內外網等實際業務介面依需求接入交換機

2. **初次設定（建議流程）**
   - **主設備先設定（例如防火牆1）**
     - 登入GUI，前往「系統管理 > 高可靠性（HA）」：
       - 模式選「Active-Passive」
       - 設備優先權（priority）建議設定較高（如 250）
       - 群組名稱（Group Name）自訂
       - 密碼自行設定一組
       - 選擇 heartbeat 介面（如 internal4 與 internal5）
       - 其他維持預設即可
     - 完成後，**先不要接heartbeat纜線**
   - **次要設備設定（如防火牆2）**
     - 建議恢復出廠值
     - 也需設定管理IP
     - 進入HA設定，模式與主設備相同（Active-Passive）、群組名稱、密碼、heartbeat介面等都要一樣
     - 設備優先權比主設備低（如 100）
   - **接上Heartbeat線纜**，這時次要設備會自動加入叢集，狀態欄位會顯示同步完成。

3. **確認同步/狀態**
   - GUI介面下可直接觀看狀態
   - CLI 下可用 `get system ha status` 或 `diagnose sys ha status` 查詢
   - 若需主動同步： `execute ha synchronize start`

4. **勾選注意事項**
   - 叢集中所有參數一致，包括 group id、密碼、heartbeat等，否則無法正確合併
   - 主設備狀態正常時，備設備所有設定會自動同步
   - 建議部署前先備份好各自config檔案

***

**二、HA叢集遷移流程與注意事項**

假設遷移情境：要換掉叢集中的一台防火牆，或全數換新機種

1. **提前備份現有主機設定**  
   - 在主機備份全機設定檔（含策略、物件、網路等）

2. **準備新機**
   - 將新設備升級至與現有叢集相同版本、韌體
   - 修改新設備 port 名稱與舊設備匹配（若必要）
   - 恢復預設值（或僅保留最基本的管理設定）

3. **設定 HA 參數**
   - 依前述叢集建立步驟設定HA，group name、group id、heartbeat介面、密碼等全部要相同

4. **接入心跳線纜，加入叢集**
   - 新設備連上heartbeat，會自動識別並同步設定

5. **移除待替換舊設備**
   - 在Web或CLI觀察狀態正常後，關閉並移除舊設備

6. **驗證與測試**
   - 必要時重新reboot，新設備會以備機身份加入，以後如有故障會自動接手

7. **全機群換（機型升級/整組替換）時要點**
   - 建議規劃維護時段
   - 設定檔需根據新設備接口命名調整
   - 逐台替換方式最穩，最後一台主動切換主機
   - 相關說明與用戶經驗參考：[Reddit原廠論壇遷移經驗整理]、[社群技巧分享][1][2]

***

如需 CLI 詳細指令範例、中文接口畫面解說、或特殊主備切換操作方式（如「execute ha failover」與強制主控切換），都可以進一步提供！如果還要針對你的現場環境或特定拓撲需求討論，請補充細節。[2][3][4][5]


### 对话 3

**问题**: 依據你看到的畫面 重新給我一次 詳細的做法及流程

**回答**:
根據你「HA叢集設定」畫面（FortiGate 7.2.11 TN_LAB_Firewall），以下整理操作細節與完整流程：

***

**一、建立 HA 叢集（以 GUI 畫面為主）**

1. **進入 HA 叢集設定**
   - 位置：系統管理 → High Availability
   - 畫面會有：
     - Mode（模式）：選擇 ▸ Standalone / Active-Active / Active-Passive
     - Device priority（裝置優先權）：數字越大越容易成為主機，建議主設備設高、備機設低
     - Group ID：數字編號，要所有叢集設備一致
     - Group name：自訂名字，同樣需一致
     - Password：共用密碼，確保安全
     - Session pickup：決定故障轉移時是否保留現有連線（可勾選）
     - Monitor interfaces：指定業務介面監控
     - Heartbeat interfaces：指定心跳線(同步/健康監控)
     - Management Interface Reservation（管理介面保留）

2. **主設備設定步驟**
   - Mode 選「Active-Passive」或「Active-Active」（多數為 Active-Passive）
   - Device Priority 輸入如 250
   - Group ID選一組數字（如1，整組統一）
   - Group Name填組名（如 TN_HA1）
   - Password請自行輸入並記錄
   - Session pickup可選擇是否啟用（根據需求）
   - 選擇需監控的interface（如port1、WAN/內網）
   - Heartbeat interface指定埠口（如port4、port5，實際埠名依硬體而定）
   - 如需要，管理介面可保留勾選
   - 按「OK」完成

3. **備機設定步驟**
   - 依主機相同方式，Mode/Group ID/Group Name/Password都一致
   - 優先權設低（如100）
   - 配置相同的heartbeat
   - 確認同版本韌體、同網段可管理IP

4. **設備連線與啟用**
   - 先各自完成設定再插上heartbeat纜線
   - 管理介面加入同一交換機/網段
   - 連線後，備機自動偵測並加入叢集，主機完成同步

5. **驗證狀態**
   - 觀察HA monitoring畫面，即可看到主/備角色、同步進度
   - CLI可用 `diagnose sys ha status`查詢

***

**二、HA遷移（更換設備/移動機器）流程**

1. **備份現有主機設定**
   - 在主設備「系統 > 設定 > 備份」，存檔至本地

2. **新設備準備**
   - 初始化新機，升級韌體至與原本同版本
   - 做好基礎管理IP/網路連線

3. **設定 HA 參數**
   - 在新機同樣進入HA設定，照上述步驟設好各參數（mode/group/password/heartbeat等）

4. **插入heartbeat線纜使新設備加入叢集**
   - 主機自動同步至新設備

5. **故障切換/移除舊設備**
   - 如要替換，移除舊設備，或可直接重啟新設備主動成為主機
   - GUI畫面下可直接移除裝置，也可用CLI強制切換

6. **驗證同步與流量轉移**
   - 確認新主機狀態正常，業務流量可正常接收

***

**延伸補充與建議：**
- *所有需要叢集參數完全一致：mode、group id/group name、password及heartbeat介面！*
- *變更設備時多做管理介面、內外網IP調整規劃，避免因叢集同步覆蓋掉新設備IP導致管理失效*

如要CLI指令、特殊情境如同型號換機/跨型號遷移、手動同步細節，再告知即可給最適合流程！


### 对话 4

**问题**: 接線的方式?

**回答**:
根據你現有的 FortiGate HA 叢集設定畫面，「接線方式」請依如下方式操作：

***

**HA叢集常見接線方式說明：**

1. **業務介面（如WAN/LAN等）：**
   - 主/備機的所有業務介面（如 port1/WAN/內網口等）都連到「同一交換機」或「同一台路由器」
   - 目的：無論哪台為主（Master），業務流量都能即時切換且不中斷

2. **Heartbeat介面（心跳線）：**
   - 需要至少 1 組專用接口（如 port4、port5），建議用 2 組以提升可靠性
   - 當有兩組 heartbeat port，可分別獨立接線（例如直連、或經由交換機但不混用業務流量）
   - 心跳線通常「雙機間直連」（例如主的 port4 直接連到備的 port4）
   - 若機器位置相隔遠，可使用專用 VLAN 或獨立交換機來橋接 heartbeat 接口

3. **管理介面（可選）：**
   - 若需要獨立管理，每台機器的管理口建議分開且分配不同管理 IP
   - 或者統一經交換機或管理 VLAN，便於運維

***

**圖解式文字說明（典型2機HA主備）：**

- 主機 port1(WAN) <-> 上層交換機/路由器
- 備機 port1(WAN) <-> 上層交換機/路由器
- 主機 port2(LAN) <-> 內部交換機
- 備機 port2(LAN) <-> 內部交換機
- 主機 port4(heartbeat1) <-> 備機 port4(heartbeat1)
- 主機 port5(heartbeat2) <-> 備機 port5(heartbeat2)
- 主/備機管理口可各接內部管理用交換機

***

**重點注意：**

- Heartbeat接口一定不要和業務流量混用，專線直連（或獨立switch也可）
- 若有3台以上，Heartbeat可全部直連一條獨立switch即可
- 若只一組heartbeat，若有故障就無法判斷主機健康，建議至少兩組
- 緊急時請依介面LED/CLI檢查heartbeat通訊正常 `diagnose sys ha status`、`diagnose hardware deviceinfo heartbeat`

***

如果需要更詳細插線圖或指定型號接口分配（如 FGT60F/FGT100F 各port用法、接口映射建議），請補充設備型號！


### 对话 5

**问题**: 若只一組heartbeat，若有故障就無法判斷主機健康，建議至少兩組 所以
主機 port4(heartbeat1) <-> 備機 port4(heartbeat1)
主機 port5(heartbeat2) <-> 備機 port5(heartbeat2)
這樣才有效果 說說看如果只有一組的話

**回答**:
你的理解完全正確！  
**若只有一組heartbeat**（例如只用 port4 這一對，主 port4 <-> 備 port4）：  

- **風險：**  
  - 若這條heartbeat線路或接口（port4）發生故障（如纜線鬆脫/壞掉、介面異常、Switch發生問題甚至故意拔除），整個HA叢集**將失去彼此健康狀態監控能力**。
  - 在這種情況下，「主備雙方都無法得知對方存活」，就會同時認為**對方已經故障**，導致**Split Brain（腦裂）**——兩台設備都搶著成為主機，此時將造成：  
    - 兩台同時放流量/對外動作，IP、MAC發生衝突
    - 造成網路大亂、服務不正常或封包衝突

- **防範建議：**
  - 應**至少兩組heartbeat線**（例如port4、port5同時有heartbeat），這樣即使有一組失效，還有另一組能持續完成設備健康監控與同步任務。
  - 叢集判斷「至少有一組heartbeat暢通」時，才會維持正常主備關係
  - 只有當**所有heartbeat都失效**時，才會進入腦裂危機

***

**總結（只有一組heartbeat的缺點）：**  
- 單一heartbeat斷線，無備援，易導致腦裂與故障轉移錯亂。
- 設計建議一定要用**雙heartbeat**（若有更多可用接口，甚至三組），並且heartbeat專線不要與業務流量或一般交換機混用，優先考慮設備直接point-to-point相連。
- FortiGate的HA設定畫面通常會有明顯警告提示「僅設一組heartbeat時有風險」，務必遵守官方建議。

如果你現場只剩一組可用接口，“非不得已”才建議這樣做，並加強現場運維監控；若方便，請追加一組專用線來避免故障時大範圍影響。


### 对话 6

**问题**: 詳細白話說明這一頁

**回答**:
這個頁面是 FortiGate 防火牆的「編輯防火牆規則（Policy）」畫面，專門用來設定、防護與流量控管。白話重點說明如下：

***

**1. 規則基本資訊**
- **名稱 (Name)：**  
  這條Policy取名為 `SSLVPN_client` — 方便辨識這是給 SSLVPN 用戶通過的流量規則。

- **Incoming Interface (來源介面)：**  
  設為 `internal1`，即用戶端流量進入防火牆的來源埠口。

- **Outgoing Interface (目的介面)：**  
  設為 `SSL-VPN tunnel interface (ssl.root)`，代表網頁上的流量要「從內網」經過這條規則，送往SSL VPN的虛擬介面。

***

**2. 流量來源與目的地**
- **Source (來源位址)：**  
  包含多個來源物件（如 DCNM_LAB_10_198_236、F22LAB、GST_lab、TSMC-10.11.116.0、Vlan_2/4/5/6），這些代表允許哪些設備或VLAN的流量能被這條規則處理。

- **Destination (目的位址)：**  
  目標對象是 `SSLVPN`，即連至SSL VPN的虛擬群組。

- **Schedule (時段)：**  
  設為 `always`，這條policy任何時候都有效。

- **Service (服務類型)：**  
  設為 `ALL`，代表所有協定和埠號（如HTTP, HTTPS, RDP, SSH等）都允許通過。

***

**3. 行為設定**
- **Action (行為)：**  
  勾選 `ACCEPT`，意味著這條規則「放行」上述來源至目的地的流量。

***

**4. 防火牆/安全功能**
- **NAT（來源/目的位址轉換）：**  
  可選擇是否開啟，避免內部IP曝光（此處看不到有打勾）。

- **Security Profiles（安全防護）：**  
  可按需求開關多種防護：
  - AntiVirus（防毒）
  - Web Filter（網頁過濾）
  - DNS Filter（DNS過濾）
  - Application Control（已勾選，啟用應用程式辨識控管）
  - IPS（入侵防護）
  - File Filter（檔案過濾）
  - SSL Inspection（SSL偵測）

  目前只開了 Application Control，其他安控模組未啟用。

***

**5. 日誌與狀態**
- **Log Allowed Traffic（允許流量日誌）：**  
  有打勾，代表所有Suppose允許通過此rule的session都進行日誌記錄。

- **統計資訊**  
  - ID這條是第9條Policy
  - 最近一次使用：5天前
  - 命中（Hit）次數：70
  - 流量總量：3.91 GB
  - 活動連線數：0

***

**6. 其他附加資訊與快速功能**
- 可備註、查看API範例、直接切換CLI編輯，等。
- 附有官方文件/教學影片連結。

***

**整體總結（白話）：**  
這條規則是要讓你「內部多個網段/設備」可透過 `internal1` 介面通過這條防火牆，進入到 SSLVPN （ssl.root）介面且所有服務都開放、時段不限，而且「開啟應用程式控管」與完整日誌留存。這是典型的SSL VPN放行規則設計，方便統一控管與追蹤VPN進出的所有活動。

如要進階解釋（比如流量路徑、安控行為背後原理、最佳實務），或要比較不同策略寫法再詢問即可！[1]



---

**来源**: [Perplexity AI](https://www.perplexity.ai/search/ni-ke-yi-kan-dao-zheng-ge-wang-RDb2_2vbRpaZ33wRm.kxxA)
