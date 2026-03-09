# username nwadmin privilege 15 secret 9 $9$3V.F2V6D3V6J2.$DsGe5l2KZh5Ut5.96PWtg0mLMX4Hi2rTFFbuzmdfKq2
username ap_gnms_crawler privilege 15 secret 9 $9$2lEJ3F.J4/AK3k$RwaW3Ge/GPFPSU13SE09jYCacoKOlohaBn

**Thread 编号**: 147  
**Slug**: username-nwadmin-privilege-15-lXNwtGs4Q2O6oUlwUl_9tQ  
**查询次数**: 1  
**最后更新时间**: 2025-07-04T05:32:17.040637  
**模式**: copilot

---

## 内容

### 对话 1

**问题**: username nwadmin privilege 15 secret 9 $9$3V.F2V6D3V6J2.$DsGe5l2KZh5Ut5.96PWtg0mLMX4Hi2rTFFbuzmdfKq2
username ap_gnms_crawler privilege 15 secret 9 $9$2lEJ3F.J4/AK3k$RwaW3Ge/GPFPSU13SE09jYCacoKOlohaBnUEsa79c1o
!
確認一下這樣對嗎 secret 9 
的意思

**回答**:
**Cisco IOS `secret 9` 密碼型態說明**

在 Cisco IOS 設定中，`secret 9` 代表該密碼是以「Type 9」加密方式儲存。這種加密方式使用 scrypt 演算法，是目前 Cisco 裝置中安全性最高的密碼雜湊類型之一。

### `secret 9` 的意義

- **Type 9 密碼**：採用 scrypt 演算法進行單向雜湊（hash），並加入隨機 salt 值與多次迭代，極大提升破解難度。
- **安全性**：scrypt 設計目的是讓暴力破解（brute-force）成本極高，即使使用大量 GPU 或 ASIC 也很難破解。[1][2]
- **格式**：`secret 9` 後面接的字串（如 `$9$3V.F2V6D3V6J2.$DsGe5l2KZh5Ut5.96PWtg0mLMX4Hi2rTFFbuzmdfKq2`）就是經過 scrypt 雜湊後的密碼，不可逆，無法還原成明文。

### 常見密碼型態比較

| 類型 | 說明                | 加密演算法      | 安全性         |
|------|---------------------|-----------------|----------------|
| 0    | 明文                | 無              | 極低           |
| 7    | 可逆加密            | Cisco專用簡單算法 | 低             |
| 5    | MD5雜湊             | MD5 + salt      | 中（已不建議） |
| 8    | PBKDF2雜湊          | PBKDF2 + salt   | 高             |
| 9    | scrypt雜湊          | scrypt + salt   | 極高           |

### 實際範例說明

```plaintext
username nwadmin privilege 15 secret 9 $9$3V.F2V6D3V6J2.$DsGe5l2KZh5Ut5.96PWtg0mLMX4Hi2rTFFbuzmdfKq2
username ap_gnms_crawler privilege 15 secret 9 $9$2lEJ3F.J4/AK3k$RwaW3Ge/GPFPSU13SE09jYCacoKOlohaBnUEsa79c1o
```

- 這兩行設定表示：建立了兩個本地帳號，權限等級 15（最高），密碼以 Type 9（scrypt）加密儲存。
- 這種寫法完全正確，且是目前 Cisco 建議的安全做法。[2][3][1]

### 補充

- 若要設定 Type 9 密碼，建議使用 `algorithm-type scrypt` 參數，例如：
  ```
  username <帳號> privilege 15 algorithm-type scrypt secret <密碼>
  ```
- 若直接貼入密文（如你範例），則格式必須正確，且密文需來自合法的 scrypt hash 產生器。

**結論**  
`secret 9` 代表密碼以 scrypt（Type 9）加密，安全性極高，建議用於所有重要帳號。你的設定方式正確，完全符合 Cisco 安全建議。[3][1][2]


### 对话 2

**问题**: 所以 用戶有實際未加密的密碼就可以登入沒錯吧

**回答**:
沒錯，你的理解是正確的。  
**當你在 Cisco 設備上設定 `username xxx secret 9 ...` 時，實際登入時用戶只需要輸入「原始明文密碼」即可登入**。設備會將用戶輸入的密碼經過相同的 scrypt（Type 9）演算法雜湊後，與配置檔中的密文做比對，只要一致就允許登入。[1][2][6][8]

- **密碼在配置檔中是加密（雜湊）儲存**，用戶登入時輸入的是「明文密碼」。
- **設備不會要求用戶輸入密文**，也無法用密文直接登入。
- **無論密碼是 Type 5、8、9，只要用戶知道原始密碼即可登入**，加密只是為了保護密碼不被直接讀取。

這也是為什麼密碼型態越安全（如 Type 9），就算有人取得配置檔，也無法還原出明文密碼。  
**登入時永遠是用明文密碼，而不是加密後的密文**。[2][6][8][1]



---

**来源**: [Perplexity AI](https://www.perplexity.ai/search/username-nwadmin-privilege-15-lXNwtGs4Q2O6oUlwUl_9tQ)
