# VXlan FortiGate

**Thread 编号**: 6  
**Slug**: vxlan-fortigate-GDRl6bNwSBuBjr62ci3X8Q  
**查询次数**: 1  
**最后更新时间**: 2025-10-22T07:11:10.432355  
**模式**: copilot

---

## 内容

### 对话 1

**问题**: VXlan FortiGate

**回答**:
# VXLAN 在 FortiGate 上的實作

VXLAN（Virtual Extensible LAN）是 FortiGate 支援的網路虛擬化技術，主要用於在 Layer 3 網路上延伸 Layer 2 網段，特別適合跨數據中心或異地站點的網路整合。[2][5]

## 版本與支援

FortiOS 5.4 版本開始支援 VXLAN 功能，但建議使用 5.6.2 以上版本，因為該版本對 VXLAN 有大幅改進，包括更完善的 VLAN trunking 和 multicast 支援。FortiOS 7.4+ 版本則進一步改善了 loopback 介面的 jumbo frame 支援，對 VXLAN 部署更為友善。[1][5][6]

## 基本配置架構

FortiGate 的 VXLAN 通常透過 IPsec VPN 架構實作，配置方式如下：[5][2]

```
config system vxlan
    edit <name>
    set interface <string>
    set vni <integer>
    set remote-ip <IP_address>
    set dstport <integer>
    next
end
```

關鍵參數包括 VNI（VXLAN Network ID）、remote-ip（遠端 VTEP 位址）和預設的 UDP port 4789。[2]

## 常見拓撲與應用

**點對點 VXLAN**：兩個 FortiGate 作為 VTEP，透過 port1 建立 VXLAN 介面，並與 port2 組成 software switch 或 virtual wire pair，實現跨站點的 L2 延伸。[8][2]

**支援 Wildcard VLAN**：可透過 virtual wire pair 讓 VLAN tag 透過 VXLAN 封裝傳輸，使多個 VLAN 跨不同交換器延伸。[2]

**FortiLink over VXLAN**：支援 FortiGate 到 FortiSwitch 的 FortiLink 連線透過 VXLAN 建立。[2]

## 重要技術考量

**MTU 設定**：VXLAN 封裝會增加額外的 header，MTU 議題需特別注意。在 7.4 之前的版本，loopback 介面無法啟用 jumbo frame，可能導致效能或連線問題。[6][7]

**效能限制**：VXLAN 功能透過 IPsec VPN 架構進行，但無法透過硬體加速晶片加速，流量過大時需評估 CPU 負載。[1]

**多站點部署**：若需建立一對多的 VXLAN 架構，建議使用 loopback 介面作為 VTEP，並在 IPsec phase 2 選擇器中包含 loopback 位址，這在 hub-and-spoke 拓撲中特別有用。[6][8]

**Multicast 支援**：較新版本的 FortiOS 支援 multicast 流量透過 VXLAN 傳輸，適合需要廣播或群播的應用場景。[7][5]

## 實務部署建議

配置時需同時設定 IPsec phase1 和 phase2，並將 VXLAN 介面加入 software switch 或 virtual wire pair 中。若 IPsec tunnel 介面未設定 IP 位址（unnumbered），建議使用 loopback 介面作為 VTEP endpoint，以簡化路由和多點部署。FortiGate 也可與其他廠商的 VXLAN 設備互通，提供良好的異構網路整合能力。[6][2]


### 对话 2

**问题**: 查找更多相關資訊並且驗證你的來源 我要準確的訊息

**回答**:
# FortiGate VXLAN 完整技術資訊（官方文檔驗證版）

根據 Fortinet 官方技術文檔（FortiOS 7.6.4），以下是經過驗證的準確資訊。[1][2]

## 技術原理

VXLAN（Virtual Extensible LAN）是一種網路虛擬化技術，透過將 Layer 2 乙太網路封包封裝在 Layer 3 IP 封包內，使用 **UDP port 4789** 進行傳輸。VXLAN 終端設備稱為 VTEP（VXLAN Tunnel Endpoint），可以是虛擬或實體交換器埠。[1]

**封裝結構**：VXLAN 使用 3 bytes（24 bits）的 VNID（VXLAN Network ID）來識別 VXLAN 區段，理論上可支援 **16,777,215 個不同的 VNID**，遠超過傳統 VLAN 的 4096 個限制。[1]

**封包開銷**：VXLAN 封裝會增加 **50 bytes overhead**，包含 14B 乙太網路標頭 + 20B IPv4 標頭 + 8B UDP 標頭 + 8B VXLAN 標頭。因此建議將 MTU 調整為 **1550 bytes 以上**，或在防火牆政策中降低 TCP MSS 大小，避免封包分片。[1]

## 標準配置指令

```
config system vxlan
    edit <name>
    set interface <string>
    set vni <integer>
    set ip-version {ipv4-unicast | ipv6-unicast | ipv4-multicast | ipv6-multicast}
    set dstport <integer>
    set remote-ip <IP_address>
    set remote-ip6 <IP_address>
    next
end
```

**關鍵參數說明**：[2]

- **interface**：VXLAN 封裝流量的本地輸出介面
- **vni**：VXLAN 網路 ID（識別碼）
- **ip-version**：IP 版本，預設為 ipv4-unicast，支援 IPv4/IPv6 單播與多播
- **dstport**：VXLAN 目的埠，預設 4789
- **remote-ip/remote-ip6**：遠端 VXLAN endpoint 的 IP 位址

## L2 網路連接方式

FortiGate 支援兩種方式將 VXLAN 介面與內部介面連接到同一 L2 網路：[2]

### Software Switch

```
config system switch-interface
    edit <name>
    set member <member_1> <member_2> ... <member_n>
    set intra-switch-policy {implicit | explicit}
    next
end
```

- **implicit 模式**：switch 成員間流量隱式允許
- **explicit 模式**：需明確防火牆政策，但可卸載至 SOC4/SOC5/NP6/NP7 處理器加速[2]

### Virtual Wire Pair

```
config system virtual-wire-pair
    edit <name>
    set member <member_1> <member_2>
    set wildcard-vlan {enable | disable}
    set vlan-filter <filter>
    next
end
```

**wildcard-vlan** 功能允許 VLAN tag 透過 virtual wire pair 傳遞，實現多個 VLAN 跨 VXLAN 延伸。使用 virtual wire pair 時需配置雙向防火牆政策允許成員間流量。[2]

## 標準部署拓撲

### 點對點 VXLAN
兩個 VTEP 透過 port1 建立 VXLAN 介面，remote-ip 指向對方 port1，VXLAN 介面與 port2 組成 software switch 或 virtual wire pair，底下的 L2 交換器設備可互通。[2]

### Wildcard VLAN 支援
使用 virtual wire pair 搭配 wildcard-vlan 功能，允許 VLAN tag 封裝在 VXLAN 內傳輸，讓不同交換器上的 VLAN 可跨 VXLAN 延伸。[2]

### VXLAN over IPsec
當 VTEP 位於不同站點需加密時，VXLAN 介面使用 IPsec 介面作為輸出介面，remote-ip 設為遠端 IPsec gateway 的 IP。VXLAN 介面可與 port2 組成 software switch 或 virtual wire pair。[2]

### Hub-and-Spoke 多點拓撲
在既有 IPsec VPN hub-and-spoke 架構上，每個 spoke 建立 VXLAN 連線至 hub，hub 允許私有網路與各 spoke 的 VXLAN 介面互連，使所有 spoke 後端網路實際上位於同一 L2 網路。[2]

## 互通性與應用

FortiGate 可與其他廠商的 VXLAN 設備互通，只要其中一個 VTEP 是 FortiGate 即可。應用場景包括 FortiLink 連線透過 VXLAN 延伸至 FortiSwitch、FortiGate LAN extension、FortiExtender 整合等。[2]

## 技術標準

VXLAN 技術詳細規範請參考 **RFC 7348**。[1]


### 对话 3

**问题**: 請確認我提供的 conf 是否有包含 VXLAN

**回答**:
根據您提供的 FortiGate 配置檔案（FG101ETK19007343M_7-0_0682_202510211824-2.conf）分析結果，**此配置檔案中沒有包含 VXLAN 相關設定**。[1]

## 檢查結果

搜尋了以下 VXLAN 相關的配置關鍵字：[1]

- `config system vxlan`：無此配置區段
- `vxlan`：未出現在配置檔案中
- `vni`（VXLAN Network ID）：未找到相關設定

## 檔案基本資訊

您提供的配置檔案屬於以下設備：[1]

- **型號**：FortiGate FG-101E（現使用 FGT81F 韌體）
- **序號**：FG101ETK19007343M
- **FortiOS 版本**：7.0.17-FW-build0682
- **匯出時間**：2025年10月21日 18:24

## 現有配置特點

此設備目前配置包含：[1]

- IPsec VPN tunnel（lj2hq-p1、lj2hq-wan2-p2）
- 多個實體介面（wan1、wan2、internal1-6、modem 等）
- Hard-switch（sw0）
- SSL VPN 配置
- 防火牆政策與地址物件
- FortiAnalyzer 連線設定

## 建議

如果您計劃在此設備上實作 VXLAN 功能，FortiOS 7.0.17 版本完全支援 VXLAN 特性。您需要新增 `config system vxlan` 配置區段，並依照先前提供的標準配置語法進行設定。建議搭配現有的 IPsec VPN tunnel 來建立 VXLAN over IPsec 架構。[2]


### 对话 4

**问题**: 這個conf 有嗎

**回答**:
根據搜尋您第二個配置檔案（TC-FG-01_7-0_0682_202510131447.conf）的結果，**此配置檔案同樣沒有包含 VXLAN 相關設定**。[1]

## 檢查結果

針對以下 VXLAN 相關關鍵字進行搜尋：[1]

- `config system vxlan`：無此配置區段
- `vxlan`：未在配置中找到
- `vni`（VXLAN Network ID）：無相關設定

## 檔案基本資訊

此配置檔案屬於：[1]

- **設備名稱**：TC-FG-01
- **型號**：FortiGate FG-101E
- **FortiOS 版本**：7.0.17-FW-build0682
- **匯出時間**：2025年10月13日 14:47
- **管理者**：scottko1004

## 現有配置特點

此設備配置包含：[1]

- IPsec VPN tunnel（tc2hq-p1）
- 多個介面（dmz、mgmt、wan1、wan2、lan、fortilink 等）
- Hard-switch（sw0）與 virtual-switch 配置
- DHCP server 服務
- SSL VPN 設定
- 防火牆政策與大量地址物件
- FortiAnalyzer 連線（192.168.250.80）
- Syslog 配置（多個 syslog server）

## 總結

您提供的兩個 FortiGate 配置檔案中**都沒有 VXLAN 配置**。兩台設備都是 FG-101E 型號，運行 FortiOS 7.0.17 版本，該版本完全支援 VXLAN 功能。如果您計劃在這兩台設備之間建立 VXLAN 連線，可以參考先前提供的官方配置語法進行設定。[2][1]



---

**来源**: [Perplexity AI](https://www.perplexity.ai/search/vxlan-fortigate-GDRl6bNwSBuBjr62ci3X8Q)
