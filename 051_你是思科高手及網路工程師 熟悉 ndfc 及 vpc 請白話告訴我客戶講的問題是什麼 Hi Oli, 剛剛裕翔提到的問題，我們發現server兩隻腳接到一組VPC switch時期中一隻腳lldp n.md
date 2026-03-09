# 你是思科高手及網路工程師 熟悉 ndfc 及 vpc
請白話告訴我客戶講的問題是什麼
Hi Oli, 剛剛裕翔提到的問題，我們發現server兩隻腳接到一組VPC switch時期中一隻腳lldp neighbor起不來，switch port status都是connect， 如果關掉有lldp neighbor的那隻腳，neighbor會出現從另一端出現，看起來switch端設定跟拉線沒問題，

**Thread 编号**: 51  
**Slug**: ni-shi-si-ke-gao-shou-ji-wang-2qgePpvVSH2dW3FfNWgBcQ  
**查询次数**: 1  
**最后更新时间**: 2025-09-26T08:57:44.294483  
**模式**: copilot

---

## 内容

### 对话 1

**问题**: 你是思科高手及網路工程師 熟悉 ndfc 及 vpc
請白話告訴我客戶講的問題是什麼
Hi Oli, 剛剛裕翔提到的問題，我們發現server兩隻腳接到一組VPC switch時期中一隻腳lldp neighbor起不來，switch port status都是connect， 如果關掉有lldp neighbor的那隻腳，neighbor會出現從另一端出現，看起來switch端設定跟拉線沒問題，

**回答**:
結論先講：客戶遇到的是伺服器做雙網卡到同一組 vPC（兩台 Nexus）時，LLDP 只會在其中一條上出現，另一條看不到鄰居；把有鄰居的那條關掉後，LLDP 會跑到另一條出現。這屬於在 vPC 環境中常見的「單向可見、交替顯示」現象，多半不是佈線或交換器基本設定錯，而是受 LACP/系統優先序、伺服器 NIC/驅動的 LAG 行為，或 vPC 對 LLDP 展現方式影響所致。

重點用白話整理如下：
- 現象描述：兩條線都 up（connect），但 LLDP 鄰居只在其中一條看到；關掉這條後，LLDP 改在另一條看到。這代表邏輯上 Port-Channel 正常運作，傳輸是單一路徑轉送，並非實體斷線。[一般是正常表現]  
- 為什麼會這樣：  
  - vPC + LACP 下，資料平面與控制平面（含 LLDP）會依雜湊或「主用連結」選擇其中一條傳送，另一條就看不到 LLDP 鄰居，關閉主用連結後，次用連結接手，所以 LLDP 轉移過去。  
  - 伺服器端 LAG 模式與驅動設定（如 LACP active/passive、傳輸雜湊演算法、是否允許單一成員承載控制封包）會影響 LLDP 是否在兩條都可見。  
  - 在 vPC 架構裡，控制協定封包不一定會在每一條成員埠都對稱可見（尤其當伺服器端實作偏向單臂送出），因此只看到一邊並不罕見。  
- 為什麼不像是線或交換器問題：  
  - 兩埠都顯示 connect/up，關掉一條後另一條立即出現 LLDP，符合「通道內接力」邏輯；若是線材/SFP 問題，關閉一條不會讓另一條的 LLDP突然正常。  
- 什麼情況才算異常：  
  - LACP 成員埠顯示 suspended/individual、Port-Channel 不聚合、或伺服器實際流量單邊不通。  
  - vPC consistency 參數不一致、peer-link/keepalive 異常、或 VLAN 設定不對導致實際通訊問題。  
- 建議檢查（最小干擾、務實做法）：  
  - 交換器側：確認該 vPC 埠通道 LACP 是 active、成员埠都 in-Po、無 suspended，且 vPC consistency、peer-link 正常；若有最小成員數（min-links），確認滿足以避免整體 down。  
  - 伺服器側：  
    - LAG 模式設為 802.3ad/LACP active，不要用靜態或廠商私有模式。  
    - 檢查驅動/Team 設定的負載平衡與控制封包處理（不少驅動預設只用單一成員送出 LLDP/CDP/ARP 類封包）。  
    - 若要在兩條都看到 LLDP，可測試把 LACP 都設 active、關閉「suspend individual」的行為（依環境評估）、或調整 hash 讓控制封包不固定綁單一埠（實務上不一定必要）。  
  - 驗證：在不影響業務時段，用伺服器端關閉/開啟單埠交替觀察 LLDP 與 LACP 狀態；以實際流量測試確認連通性正常才是關鍵。  
- 結論：這更像是 vPC/LAG 對控制封包的路徑選擇表現，而非異常；只要 LACP 聚合穩定、vPC 一致性與 VLAN 正確、實際流量 OK，就屬於可接受行為。若業務或可觀測性需要讓兩邊都顯示 LLDP，再微調伺服器端 LAG/驅動策略即可。


### 对话 2

**问题**: 確認一下 所以NDFC 跟 VPC 是有關連的嗎 還是不一樣的東西 或是架構 我不太清楚之間的關係

**回答**:
NDFC 和 VPC 是兩個不同層次但有關聯的概念，讓我用白話解釋它們的關係：

## NDFC 和 VPC 的定義

**NDFC (Nexus Dashboard Fabric Controller)** 是思科的**管理平台**，前身是 DCNM (Data Center Network Manager)。它是一個集中式的網路管理工具，用來管理、配置和監控思科的資料中心設備，特別是 Nexus 系列交換器 。[6]

**VPC (Virtual Port Channel)** 是思科 Nexus 設備上的一項**網路虛擬化技術**，讓兩台獨立的交換器可以對下游設備呈現為單一邏輯節點，提供第 2 層多路徑和負載平衡功能 。[5]

## 兩者的關係

NDFC **包含** VPC 的管理功能，關係如下：

- **NDFC 是管理工具**：負責配置、部署和監控 VPC
- **VPC 是被管理的技術**：在 Nexus 交換器上實際運行的功能
- **NDFC 可以一鍵配置 VPC**：提供圖形化介面來建立 VPC pair，簡化複雜的 VPC 設定過程[6]

## 實際應用場景

當你要在兩台 Nexus 交換器之間建立 VPC 時：
- **傳統方式**：需要在每台交換器上手動輸入大量 CLI 指令
- **使用 NDFC**：透過圖形化介面點擊幾下就能完成 VPC 配置[7]

## 限制和注意事項

從搜尋結果發現，在 NDFC 中配置 VPC 有一些限制：
- 如果 Leaf 交換器已經有 overlay 網路或 VRF 配置，VPC 配置選項會變成灰色無法使用
- 需要先移除現有的 overlay 配置才能建立新的 VPC pair[1]

**總結**：NDFC 是管理平台，VPC 是網路技術；NDFC 用來管理和配置 VPC，讓原本複雜的 VPC 部署變得更簡單和自動化。兩者不是對立或平行的概念，而是管理者與被管理者的關係。


### 对话 3

**问题**: 所以回到客戶的問題來看 白話說明

**回答**:
結合剛才對 NDFC 和 VPC 的理解，讓我用白話重新解釋客戶的問題：

## 客戶的環境架構

客戶有：
- **一組 VPC switch**：兩台 Nexus 交換器做成 VPC pair（可能透過 NDFC 管理）
- **一台 server**：用雙網卡分別接到這兩台 VPC 交換器

## 問題現象（白話說明）

**正常情況下應該怎樣**：
- Server 的兩條網路線都接到 VPC 交換器
- 從 VPC 交換器的角度看，這兩條線會合併成一個邏輯通道
- 理論上兩邊都應該看得到 LLDP neighbor

**實際發生什麼**：
- 兩條線的 port status 都顯示 "connect"（物理層 OK）
- 但只有一條線能看到 LLDP neighbor，另一條看不到
- 把有 LLDP neighbor 的那條關掉後，LLDP neighbor 會跳到另一條出現

## 這是什麼問題？

**答案：這不是故障，是 VPC 的正常行為**

**為什麼會這樣**：
1. **VPC 的設計**：兩台獨立交換器要讓 server 以為它們是同一台
2. **LLDP 的特性**：為了避免混淆，VPC 會選擇其中一條做為主要路徑來傳送控制封包（包括 LLDP）
3. **自動切換**：當主要路徑斷掉時，會自動切換到備用路徑

**簡單比喻**：
就像你有兩個門進同一間房間，但房間裡的人只會從其中一個門回應你的敲門聲；如果你把那個門關起來，房間裡的人就會改從另一個門回應。

## 客戶需要擔心嗎？

**不需要擔心**，因為：
- 物理連線正常（都是 connect）
- VPC 功能正常（會自動切換）
- 這是 VPC 環境的標準表現，不是故障

**只要確認**：
- Server 的網路流量正常
- 兩條線的 Port-Channel 聚合狀態正常
- VPC peer-link 和 keepalive 正常

這樣就可以了，LLDP 只在一邊出現是 VPC 的正常保護機制。


### 对话 4

**问题**: 在提供客戶的原話 給你分析 到底客戶 要表達的是甚麼 是否客戶不懂 所以才會這樣提問
還是說 是真的有異常

Hi Oli,
 
剛剛裕翔提到的問題，我們發現server兩隻腳接到一組VPC switch時期中一隻腳lldp neighbor起不來，switch port status都是connect，
 
如果關掉有lldp neighbor的那隻腳，neighbor會出現從另一端出現，看起來switch端設定跟拉線沒問題，
 
看需要提供甚麼資訊請再跟我說，謝謝
 
楚盦

**回答**:
分析客戶的原話，我認為客戶**有一定的網路基礎，但對 VPC 環境下的 LLDP 正常行為不太確定**，所以想要專業確認。

## 客戶的認知程度分析

**客戶懂的部分**：
- 知道 VPC、LLDP、port status 等網路概念[1]
- 會做基本故障排除（檢查 port status、測試切換行為）
- 已經排除了基本的設定和線路問題
- 觀察很仔細，注意到 LLDP neighbor 會在兩邊切換

**客戶不確定的部分**：
- 認為 server 雙網卡接 VPC 時，**兩邊都應該要有 LLDP neighbor**
- 不知道「只有一邊顯示 LLDP neighbor」是否為正常現象

## 客戶的疑慮點

從客戶的描述可以看出，他的**預期** vs **實際情況**有落差：

**預期**：兩條線都應該看到 LLDP neighbor
**實際**：只有一條看到，另一條關掉後才會切換過去

客戶想確認的問題：**這是正常現象還是故障？**

## 客戶需要的答案

客戶其實需要的是**專業確認和解釋**，而不是基本的故障排除指導：

1. **確認這是正常行為**：在 VPC 環境下，LLDP neighbor 只在一邊顯示是標準表現
2. **解釋原因**：VPC 為了避免 loop 和混淆，會選擇單一路徑傳送控制封包
3. **說明何時需要擔心**：只有當 Port-Channel 聚合異常、實際流量有問題時才需要處理

## 結論

客戶**不是不懂網路**，而是對這個特定場景的正常行為沒把握。客戶的觀察和測試都做得很好，只是需要專業確認這個 LLDP 行為是 VPC 的設計特性，不是故障。

**建議回覆客戶**：直接告訴他這是正常現象，並簡單解釋 VPC 的 LLDP 行為，讓他安心。如果他想進一步了解，可以請他提供 `show port-channel summary` 和 `show vpc` 的輸出來確認 VPC 狀態正常。


### 对话 5

**问题**: 請在三的確認 指令沒錯 show port-channel summary 和 show vpc

**回答**:
確認指令完全正確！根據思科官方文件，檢查 VPC 狀態的標準指令就是：

## 基本檢查指令

**`show port-channel summary`** ✅ 正確
- 顯示所有 Port-Channel 的狀態和成員埠
- 確認哪些埠在 Port-Channel 中且狀態為 UP[1][2]

**`show vpc`** ✅ 正確  
- 顯示完整的 VPC 域狀態
- 包含 peer-link、keepalive、role 等所有 VPC 資訊[2][1]

## 進階檢查指令

如果需要更詳細的資訊，還可以加上：

**`show vpc brief`** 
- 簡潔版的 VPC 狀態，快速查看 VPC 成員和狀態[3][1]

**`show vpc consistency-parameters`**
- 檢查 VPC 參數一致性，看是否有 Type-1 或 Type-2 不一致錯誤[2][3]

**`show vpc role`**
- 顯示 VPC 角色狀態（Primary/Secondary/Operational Primary/Operational Secondary）[4]

## 實際建議給客戶的指令

對於客戶的問題，建議先收集：
1. `show port-channel summary` - 確認 Port-Channel 聚合正常
2. `show vpc` - 確認整體 VPC 狀態健康
3. `show vpc brief` - 快速確認問題的 VPC 成員狀態

這些指令可以完整確認 VPC 環境是否正常運作，以及 LLDP 單邊顯示是否為預期行為。


### 对话 6

**问题**: 客戶的回覆 找出問題 提出解決方案

Hi Joe,
 
我們還有其他fabric使用的NDFC server也接在這組switch上，狀態是正常的，所以vpc設定理論上沒問題才對。
 
Show port-channel summary
 
T-14P8_Z3_Y17-D93180-71-39-TOR-NDFC# show port-channel summary
Flags:  D - Down        P - Up in port-channel (members)
        I - Individual  H - Hot-standby (LACP only)
        s - Suspended   r - Module-removed
        b - BFD Session Wait
        S - Switched    R - Routed
        U - Up (port-channel)
        p - Up in delay-lacp mode (member)
        M - Not in use. Min-links not met
--------------------------------------------------------------------------------
Group Port-       Type     Protocol  Member Ports
      Channel
--------------------------------------------------------------------------------
1     Po1(SU)     Eth      LACP      Eth1/53(P)   Eth1/54(P)  
T-14P8_Z3_Y17-D93180-71-39-TOR-NDFC#
 
T-14P8_Z3_Y19-D93180-71-40-TOR-NDFC# show port-channel summary
Flags:  D - Down        P - Up in port-channel (members)
        I - Individual  H - Hot-standby (LACP only)
        s - Suspended   r - Module-removed
        b - BFD Session Wait
        S - Switched    R - Routed
        U - Up (port-channel)
        p - Up in delay-lacp mode (member)
        M - Not in use. Min-links not met
--------------------------------------------------------------------------------
Group Port-       Type     Protocol  Member Ports
      Channel
--------------------------------------------------------------------------------
1     Po1(SU)     Eth      LACP      Eth1/53(P)   Eth1/54(P)  
T-14P8_Z3_Y19-D93180-71-40-TOR-NDFC#
 
 
Show vpc brief
 
T-14P8_Z3_Y17-D93180-71-39-TOR-NDFC# show vpc brief
Legend:
                (*) - local vPC is down, forwarding via vPC peer-link
 
vPC domain id                     : 148
Peer status                       : peer adjacency formed ok     
vPC keep-alive status             : peer is alive                
Configuration consistency status  : success
Per-vlan consistency status       : success                      
Type-2 consistency status         : success
vPC role                          : primary                      
Number of vPCs configured         : 0  
Peer Gateway                      : Disabled
Dual-active excluded VLANs        : -
Graceful Consistency Check        : Enabled
Auto-recovery status              : Enabled, timer is off.(timeout = 240s)
Delay-restore status              : Timer is off.(timeout = 240s)
Delay-restore SVI status          : Timer is off.(timeout = 10s)
Operational Layer3 Peer-router    : Disabled
Virtual-peerlink mode             : Disabled
 
vPC Peer-link status
---------------------------------------------------------------------
id    Port   Status Active vlans   
--    ----   ------ -------------------------------------------------
1     Po1    up     1,101,108,111,114,117 
 
T-14P8_Z3_Y19-D93180-71-40-TOR-NDFC# show vpc brief
Legend:
                (*) - local vPC is down, forwarding via vPC peer-link
 
vPC domain id                     : 148
Peer status                       : peer adjacency formed ok     
vPC keep-alive status             : peer is alive                
Configuration consistency status  : success
Per-vlan consistency status       : success                      
Type-2 consistency status         : success
vPC role                          : secondary                    
Number of vPCs configured         : 0  
Peer Gateway                      : Disabled
Dual-active excluded VLANs        : -
Graceful Consistency Check        : Enabled
Auto-recovery status              : Enabled, timer is off.(timeout = 240s)
Delay-restore status              : Timer is off.(timeout = 240s)
Delay-restore SVI status          : Timer is off.(timeout = 10s)
Operational Layer3 Peer-router    : Disabled
Virtual-peerlink mode             : Disabled
 
vPC Peer-link status
---------------------------------------------------------------------
id    Port   Status Active vlans   
--    ----   ------ -------------------------------------------------
1     Po1    up     1,101,108,111,114,117
 
 
我們幫這組新的NDFC新增了一個vlan 117來做L2打通，設定在vpc兩端與server對接共6個port上
舉例其中一台的三個port設定如下 :
 
interface Ethernet1/17
  description F14-TSM
  switchport
  switchport access vlan 117
  spanning-tree port type edge
  spanning-tree bpduguard enable
  mtu 9216
  storm-control broadcast level 0.03
  no shutdown
 
interface Ethernet1/18
  description F14-TSM
  switchport
  switchport access vlan 117
  spanning-tree port type edge
  spanning-tree bpduguard enable
  mtu 9216
  storm-control broadcast level 0.03
  no shutdown
 
interface Ethernet1/19
  description F14-TSM
  switchport
  switchport access vlan 117
  spanning-tree port type edge
  spanning-tree bpduguard enable
  mtu 9216
  storm-control broadcast level 0.03
  no shutdown
 
 
再麻煩幫忙看看，謝謝
 
楚盦

**回答**:
分析客戶提供的資訊，我發現了**核心問題**：

## 問題診斷

從 `show vpc brief` 看到關鍵資訊：
- **Number of vPCs configured: 0** ❌

這表示雖然 VPC peer-link 正常，但**沒有任何 vPC 成員被配置**！

## 實際狀況

客戶目前的配置：
- Server 的線分別接到兩台 switch 的 Eth1/17, 1/18, 1/19
- 這些 port 都配置為**獨立的 access port**，不是 vPC 成員
- 所以 server 看到的是**兩個獨立的 switch**，不是一個邏輯 vPC

## 解決方案

需要將 server 對接的 port 配置為 **vPC**，而不是獨立 access port：

### 步驟 1：在兩台 switch 上配置相同的 vPC

**Switch 1 (Primary):**
```
interface port-channel10
  switchport
  switchport access vlan 117
  spanning-tree port type edge
  mtu 9216
  vpc 10

interface Ethernet1/17
  description F14-TSM
  switchport
  switchport access vlan 117
  channel-group 10 mode active
  no shutdown

interface Ethernet1/18  
  description F14-TSM
  switchport
  switchport access vlan 117
  channel-group 10 mode active
  no shutdown

interface Ethernet1/19
  description F14-TSM  
  switchport
  switchport access vlan 117
  channel-group 10 mode active
  no shutdown
```

**Switch 2 (Secondary):** 
- 配置**完全相同**的指令（vPC 要求兩邊配置一致）

### 步驟 2：驗證配置

配置完成後檢查：
```
show vpc brief
show port-channel summary  
show vpc 10
```

應該會看到：
- `Number of vPCs configured: 1`
- `vpc 10` 狀態正常
- Server 的三個 port 聚合在 Po10 中

## 為什麼之前 LLDP 只在一邊出現？

因為沒有 vPC，server 看到兩個獨立 switch，可能因為：
- Server 端的 NIC teaming/bonding 配置
- LACP 或其他聚合協定的行為
- 導致流量只走其中一條路徑

配置成正確的 vPC 後，這個問題就會解決。


### 对话 7

**问题**: 你要去驗證及反查 剛剛給的答案是對的 因為客戶是台X電 你應該知道不能隨便解答 瞎掰 及亂回答

**回答**:
你說得對，我需要更仔細驗證。讓我重新分析客戶提供的資訊：

## 重新分析客戶狀況

### 客戶環境確認
- **VPC Domain 148** 已建立且正常運作
- **Peer-link (Po1)** 狀態正常，承載 vlan 1,101,108,111,114,117
- **VPC keep-alive** 正常
- **但關鍵：Number of vPCs configured: 0**

### 客戶描述分析
客戶說：**"我們還有其他fabric使用的NDFC server也接在這組switch上，狀態是正常的"**

這句話可能有幾種解釋：
1. **其他 NDFC server 可能用單邊連接**（不是 vPC）
2. **其他 server 可能在不同的 port 上**，沒有在當前檢查的範圍內
3. **客戶對"正常"的定義**可能是指連通性正常，而非 vPC 配置正常

### 目前新 NDFC 的配置狀況
從客戶提供的配置看：
- **Eth1/17, 1/18, 1/19** 配置為獨立的 **access port**（vlan 117）
- **沒有 port-channel 配置**
- **沒有 vpc 成員配置**

## 初步結論與建議

**問題根因**：新的 NDFC server 並未配置為 vPC，而是配置為獨立的 access port，這解釋了為什麼 LLDP 行為不如預期。

**但在給解決方案前，需要向客戶確認**：
1. **其他正常的 NDFC server 是如何連接的？** 是用 vPC 還是單邊連接？
2. **這個新的 NDFC server 是否需要 vPC？** 還是單邊連接就足夠？
3. **目前 server 端是否有做 NIC teaming/bonding？**

**建議客戶先提供**：
- `show run interface ethernet1/XX`（其他正常 NDFC server 連接的 port 配置）
- 確認 server 端的網卡配置需求

這樣才能給出準確的解決方案，避免不必要的配置變更風險。



---

**来源**: [Perplexity AI](https://www.perplexity.ai/search/ni-shi-si-ke-gao-shou-ji-wang-2qgePpvVSH2dW3FfNWgBcQ)
