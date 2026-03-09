# Whisper 量化模型來源：HuggingFace 量化模型（small-int8/medium-int8）
如本地無模型將自動下載。來源：guillaumekln/faster-whisper-small-int8/medium-int8
1. small-int8 (顯存最低，速度最快)
2. medium-int8 (辨識較準確，顯存較高)
3. 兩者都執行（需較多顯存）
請選擇 Hugg

**Thread 编号**: 301  
**Slug**: whisper-liang-hua-mo-xing-lai-gvKukwmXSOakCYBfnJxQuw  
**查询次数**: 1  
**最后更新时间**: 2025-05-12T12:54:10.797277  
**模式**: copilot

---

## 内容

### 对话 1

**问题**: Whisper 量化模型來源：HuggingFace 量化模型（small-int8/medium-int8）
如本地無模型將自動下載。來源：guillaumekln/faster-whisper-small-int8/medium-int8
1. small-int8 (顯存最低，速度最快)
2. medium-int8 (辨識較準確，顯存較高)
3. 兩者都執行（需較多顯存）
請選擇 HuggingFace 量化模型 (1/2/3，預設1)：3
[自動下載] 檢查 small-int8 量化模型...
[自動下載] 從 HuggingFace 下載 guillaumekln/faster-whisper 子資料夾 small-int8 ...
[自動下載失敗] small-int8：404 Client Error. (Request ID: Root=1-6821eecf-05cf7b411f9f98317c6f55c2;46abdbc9-3016-4917-9fbe-12ebda6756ce)

Repository Not Found for url: https://huggingface.co/api/models/guillaumekln/faster-whisper/revision/main.
Please make sure you specified the correct `repo_id` and `repo_type`.
If you are trying to access a private or gated repo, make sure you are authenticated. For more details, see https://huggingface.co/docs/huggingface_hub/authentication  
請檢查網路、HuggingFace 是否可連線，或手動下載 small-int8 資料夾放到本目錄。        
如在中國大陸，建議設置代理或使用鏡像。
Traceback (most recent call last):
  File "C:\Users\ADAdmin\AppData\Local\Programs\Python\Python312\Lib\site-packages\huggingface_hub\utils\_http.py", line 409, in hf_raise_for_status
    response.raise_for_status()
  File "C:\Users\ADAdmin\AppData\Local\Programs\Python\Python312\Lib\site-packages\requests\models.py", line 1021, in raise_for_status
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 404 Client Error: Not Found for url: https://huggingface.co/api/models/guillaumekln/faster-whisper/revision/main

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "e:\Whisper\speech_recognition_ASR.py", line 462, in <module>
    main()
  File "e:\Whisper\speech_recognition_ASR.py", line 215, in main
    ensure_hf_quant_model(m)
  File "e:\Whisper\speech_recognition_ASR.py", line 30, in ensure_hf_quant_model    
    local_dir = snapshot_download(
                ^^^^^^^^^^^^^^^^^^
  File "C:\Users\ADAdmin\AppData\Local\Programs\Python\Python312\Lib\site-packages\huggingface_hub\utils\_validators.py", line 114, in _inner_fn
    return fn(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\ADAdmin\AppData\Local\Programs\Python\Python312\Lib\site-packages\huggingface_hub\_snapshot_download.py", line 233, in snapshot_download
    raise api_call_error
  File "C:\Users\ADAdmin\AppData\Local\Programs\Python\Python312\Lib\site-packages\huggingface_hub\_snapshot_download.py", line 155, in snapshot_download
    repo_info = api.repo_info(repo_id=repo_id, repo_type=repo_type, revision=revision, token=token)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\ADAdmin\AppData\Local\Programs\Python\Python312\Lib\site-packages\huggingface_hub\utils\_validators.py", line 114, in _inner_fn
    return fn(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\ADAdmin\AppData\Local\Programs\Python\Python312\Lib\site-packages\huggingface_hub\hf_api.py", line 2816, in repo_info
    return method(
           ^^^^^^^
  File "C:\Users\ADAdmin\AppData\Local\Programs\Python\Python312\Lib\site-packages\huggingface_hub\utils\_validators.py", line 114, in _inner_fn
    return fn(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\ADAdmin\AppData\Local\Programs\Python\Python312\Lib\site-packages\huggingface_hub\hf_api.py", line 2601, in model_info
    hf_raise_for_status(r)
  File "C:\Users\ADAdmin\AppData\Local\Programs\Python\Python312\Lib\site-packages\huggingface_hub\utils\_http.py", line 459, in hf_raise_for_status
    raise _format(RepositoryNotFoundError, message, response) from e
huggingface_hub.errors.RepositoryNotFoundError: 404 Client Error. (Request ID: Root=1-6821eecf-05cf7b411f9f98317c6f55c2;46abdbc9-3016-4917-9fbe-12ebda6756ce)

Repository Not Found for url: https://huggingface.co/api/models/guillaumekln/faster-whisper/revision/main.
Please make sure you specified the correct `repo_id` and `repo_type`.
If you are trying to access a private or gated repo, make sure you are authenticated. For more details, see https://huggingface.co/docs/huggingface_hub/authentication  
PS E:\Whisper>

**回答**:
# 關於 Faster-Whisper 模型下載問題分析與解決方案

根據您的錯誤提示，問題出在嘗試下載 `guillaumekln/faster-whisper/small-int8` 時發生 404 錯誤。經分析，這是由於模型路徑設置不正確所致。

## 問題原因

您嘗試的下載路徑 `guillaumekln/faster-whisper/small-int8` 格式不正確。根據 Hugging Face 的存儲庫結構，正確的模型應該是：[4]

- `guillaumekln/faster-whisper-small`[1]
- `guillaumekln/faster-whisper-medium`[2]

## 正確使用方法

Faster-Whisper 中的量化是通過加載模型時設置 `compute_type` 參數實現的，而非下載特定的量化版本。[4]

**正確的使用方式：**

```python
from faster_whisper import WhisperModel

# 使用 small 模型並設置 INT8 量化
model = WhisperModel("small", device="cuda", compute_type="int8_float16")  # GPU 上運行
# 或
model = WhisperModel("small", device="cpu", compute_type="int8")  # CPU 上運行
```

## 建議修改

需修改您的代碼，將模型路徑改為：

1. `guillaumekln/faster-whisper-small`
2. `guillaumekln/faster-whisper-medium`

然後在加載模型時設置量化參數：

```python
# 例如加載 small 模型並使用 INT8 量化
model = WhisperModel("guillaumekln/faster-whisper-small", device="cuda", compute_type="int8_float16")
```

## 其他注意事項

1. 確保網絡連接暢通，可訪問 Hugging Face[3]
2. 如果在中國大陸，可能需要設置代理或使用鏡像站點
3. 可以考慮手動下載模型並本地加載，以避免網絡問題[4]

若要使用多種模型大小，可分別加載不同模型並設置相應的量化參數，而不是嘗試下載特定的 `-int8` 版本。[4]



---

**来源**: [Perplexity AI](https://www.perplexity.ai/search/whisper-liang-hua-mo-xing-lai-gvKukwmXSOakCYBfnJxQuw)
