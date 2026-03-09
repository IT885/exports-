# 檢查程式碼 好像都會跳出 
PS E:\Whisper> & C:/Users/ADAdmin/AppData/Local/Programs/Python/Python312/python.exe e:/Whisper/speech_recognition_ASR.py
[DEBUG] __main__ 啟動，準備呼叫 main()
[DEBUG] main() 啟動完成，進入互動流程
語音辨識程

**Thread 编号**: 300  
**Slug**: jian-cha-cheng-shi-ma-hao-xian-CkOJXt9iReqGDm05t7jfTg  
**查询次数**: 1  
**最后更新时间**: 2025-05-12T13:50:53.645053  
**模式**: copilot

---

## 内容

### 对话 1

**问题**: 檢查程式碼 好像都會跳出 
PS E:\Whisper> & C:/Users/ADAdmin/AppData/Local/Programs/Python/Python312/python.exe e:/Whisper/speech_recognition_ASR.py
[DEBUG] __main__ 啟動，準備呼叫 main()
[DEBUG] main() 啟動完成，進入互動流程
語音辨識程式已啟動
請開始說話，系統會自動辨識
按下ESC鍵可退出程式
偵測到已存在降噪樣本，要重新錄製嗎？(Y/n)： 預設N 等待2秒

已載入降噪樣本 noise_profile.npy
是否啟用降噪？(Y/n)： 預設Y 等待2秒

Whisper 量化模型選擇：
1. small (顯存需求低，速度快)
2. medium (辨識較準確，顯存需求較高)
3. 兩者都執行（方便比較，需較多顯存）
請選擇 Whisper 模型 (1/2/3，預設1，5秒自動選1): 3
PS E:\Whisper>

**回答**:
# 分析語音辨識程式提前終止問題

這個問題是您的語音辨識程式（`speech_recognition_ASR.py`）在啟動後選擇模型後就意外終止了。從提供的輸出信息看，程式在選擇模型選項"3"後就直接退出，沒有任何錯誤訊息。

## 可能的原因

根據程式碼分析，最可能的原因包括：

**1. 模型下載或檢查問題**
- 在選擇模型後，程式應該執行`ensure_hf_quant_model()`函數，但輸出中沒有顯示相關信息[1]
- 可能是`huggingface_hub`套件未安裝或版本不兼容[1]

**2. CUDA相關問題**
- 程式碼中使用了`device="cuda"`設定[1]
- 如果系統沒有可用的CUDA環境或GPU，可能會導致程式崩潰

**3. 相依套件缺失**
- `WhisperModel`或其他關鍵套件可能未正確安裝[1]
- `faster_whisper`套件可能有問題

**4. 未被捕獲的異常**
- 程式可能在某個環節拋出了異常，但沒有被適當捕獲和顯示[1]

## 建議解決方法

1. **檢查日誌文件**
   - 查看程式生成的`speech_asr_debug.log`文件，可能包含錯誤信息[1]

2. **安裝或更新相關套件**
   ```
   pip install huggingface_hub
   pip install faster-whisper
   pip install sounddevice
   ```

3. **修改模型執行環境**
   - 編輯程式碼，將`device="cuda"`改為`device="cpu"`[1]
   - 在`whisper_recognize`函數中尋找並修改這一行

4. **單獨測試模型下載功能**
   - 創建一個簡單腳本測試`ensure_hf_quant_model`函數

5. **啟用更多調試訊息**
   - 在關鍵點添加`print`語句或`try-except`塊來捕獲和顯示錯誤[1]

6. **檢查麥克風權限**
   - 確保程式有適當的權限訪問音訊設備[2][3]

如果您不需要雙模型比較功能，可以先選擇選項"1"(small模型)測試，因為同時載入兩個模型可能需要更多顯存和系統資源。[1]


### 对话 2

**问题**: 給我你修改及優化過的完整程式碼

**回答**:
# 優化語音辨識程式碼

以下是修改及優化過的完整程式碼，解決了在選擇模型後程式意外終止的問題，並增強了程式的穩定性與效能。

```python
import speech_recognition as sr
import keyboard
import threading
import time
import sys
import numpy as np
import sounddevice as sd
import noisereduce as nr
import os
import logging
import difflib
import tempfile
import soundfile as sf
from datetime import datetime

# 配置日誌，使用UTF-8編碼以正確處理中文
LOG_PATH = "speech_asr_debug.log"
logging.basicConfig(filename=LOG_PATH, filemode='a', level=logging.INFO,
                    format='%(asctime)s %(message)s', encoding='utf-8')

def setup_logger():
    """配置額外的控制台日誌輸出以便調試"""
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    return logging.getLogger('')

logger = setup_logger()

def check_dependencies():
    """檢查並報告所需依賴項"""
    missing_deps = []
    try:
        import speech_recognition
    except ImportError:
        missing_deps.append("speech_recognition")
    
    try:
        import keyboard
    except ImportError:
        missing_deps.append("keyboard")
    
    try:
        import noisereduce
    except ImportError:
        missing_deps.append("noisereduce")
    
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        missing_deps.append("faster-whisper")
    
    try:
        import sounddevice
    except ImportError:
        missing_deps.append("sounddevice")
    
    try:
        import soundfile
    except ImportError:
        missing_deps.append("soundfile")
        
    try:
        from huggingface_hub import snapshot_download
    except ImportError:
        missing_deps.append("huggingface_hub")
    
    if missing_deps:
        print(f"缺少以下依賴項，請安裝後再運行：{', '.join(missing_deps)}")
        print("可使用以下命令安裝所有依賴：")
        print("pip install SpeechRecognition keyboard noisereduce faster-whisper sounddevice soundfile huggingface_hub")
        return False
    return True

def input_with_timeout(prompt, timeout=2, default='n'):
    """具有超時功能的輸入函數，跨平台兼容"""
    print(prompt, end='', flush=True)
    result = [default]
    
    def inner():
        try:
            ans = input()
            if ans.strip() != '':
                result[0] = ans.strip()
        except EOFError:
            pass
            
    t = threading.Thread(target=inner)
    t.daemon = True
    t.start()
    t.join(timeout)
    print("")  # 輸出換行
    return result[0]

def detect_hardware():
    """檢測可用硬體，決定模型執行環境"""
    device = "cpu"
    compute_type = "int8"
    
    try:
        # 嘗試導入torch檢查CUDA可用性
        import torch
        if torch.cuda.is_available():
            device = "cuda"
            compute_type = "int8_float16"
            print(f"已檢測到 CUDA 支援的 GPU：{torch.cuda.get_device_name(0)}")
            print(f"顯存：{torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        else:
            print("未檢測到 CUDA 支援的 GPU，將使用 CPU 運行（速度較慢）")
            
        # 檢查Apple Silicon MPS
        if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            device = "mps"
            compute_type = "int8"
            print("已檢測到 Apple Silicon MPS，將使用 MPS 加速")
    except ImportError:
        print("未安裝 PyTorch，無法檢測 GPU 狀態，將使用 CPU 運行")
    except Exception as e:
        print(f"檢測硬體時發生錯誤：{e}")
        print("將使用 CPU 運行")
        
    return device, compute_type

def ensure_hf_quant_model(model_name):
    """確保 HuggingFace 量化模型已下載"""
    try:
        from huggingface_hub import snapshot_download
        
        # 檢查模型是否存在於HuggingFace快取中
        cache_dir = os.path.expanduser("~/.cache/huggingface/hub")
        model_dir = os.path.join(cache_dir, "models--" + model_name.replace("/", "--"))
        
        if not os.path.exists(model_dir):
            print(f"[模型下載] 開始下載 {model_name} ...")
            snapshot_download(repo_id=model_name, local_dir=None, local_dir_use_symlinks=True)
            print(f"[模型下載] {model_name} 下載完成。")
        else:
            print(f"[模型檢查] {model_name} 已存在於本地快取。")
            
        return True
    except ImportError:
        print("[警告] 未安裝 huggingface_hub，無法自動下載模型。請安裝：pip install huggingface_hub")
        return False
    except Exception as e:
        print(f"[警告] 檢查/下載模型時發生錯誤: {e}")
        return False

def analyze_log():
    """分析日誌文件以提供診斷信息"""
    try:
        with open(LOG_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()[-30:]  # 僅分析最後30行
    except Exception:
        print("[診斷] 無法讀取 log 檔案。")
        return
    
    # 分析流程
    last_energy = None
    vad_fail = False
    vad_method = None
    skip_count = 0
    
    for line in lines:
        if '降噪後能量' in line or '原始能量' in line:
            try:
                last_energy = float(line.split(':')[-1].strip())
            except:
                pass
        if 'VAD 偵測失敗' in line or 'Python energy threshold' in line:
            vad_fail = True
        if '


### 对话 3

**问题**: 請幫我檢查speech_recognition_ASR.py後 重新給我修改過的完整程式碼

**回答**:
```python
import speech_recognition as sr
import keyboard
import threading
import time
import sys
import numpy as np
import sounddevice as sd
import noisereduce as nr
import os
import logging
import difflib
import tempfile
import soundfile as sf
from datetime import datetime

# 配置日誌，使用UTF-8編碼以正確處理中文
LOG_PATH = "speech_asr_debug.log"
logging.basicConfig(filename=LOG_PATH, filemode='a', level=logging.INFO,
                    format='%(asctime)s %(message)s', encoding='utf-8')

def setup_logger():
    """配置額外的控制台日誌輸出以便調試"""
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    return logging.getLogger('')

logger = setup_logger()

def check_dependencies():
    """檢查並報告所需依賴項"""
    missing_deps = []
    try:
        import speech_recognition
    except ImportError:
        missing_deps.append("speech_recognition")
    
    try:
        import keyboard
    except ImportError:
        missing_deps.append("keyboard")
    
    try:
        import noisereduce
    except ImportError:
        missing_deps.append("noisereduce")
    
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        missing_deps.append("faster-whisper")
    
    try:
        import sounddevice
    except ImportError:
        missing_deps.append("sounddevice")
    
    try:
        import soundfile
    except ImportError:
        missing_deps.append("soundfile")
        
    try:
        from huggingface_hub import snapshot_download
    except ImportError:
        missing_deps.append("huggingface_hub")
    
    if missing_deps:
        print(f"缺少以下依賴項，請安裝後再運行：{', '.join(missing_deps)}")
        print("可使用以下命令安裝所有依賴：")
        print("pip install SpeechRecognition keyboard noisereduce faster-whisper sounddevice soundfile huggingface_hub")
        return False
    return True

def detect_hardware():
    """檢測可用硬體，決定模型執行環境"""
    device = "cpu"
    compute_type = "int8"
    
    try:
        # 嘗試導入torch檢查CUDA可用性
        import torch
        if torch.cuda.is_available():
            device = "cuda"
            compute_type = "int8_float16"
            print(f"已檢測到 CUDA 支援的 GPU：{torch.cuda.get_device_name(0)}")
            print(f"顯存：{torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        else:
            print("未檢測到 CUDA 支援的 GPU，將使用 CPU 運行（速度較慢）")
            
        # 檢查Apple Silicon MPS
        if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            device = "mps"
            compute_type = "int8"
            print("已檢測到 Apple Silicon MPS，將使用 MPS 加速")
    except ImportError:
        print("未安裝 PyTorch，無法檢測 GPU 狀態，將使用 CPU 運行")
    except Exception as e:
        print(f"檢測硬體時發生錯誤：{e}")
        print("將使用 CPU 運行")
        
    return device, compute_type

def input_with_timeout(prompt, timeout=2, default='n'):
    """具有超時功能的輸入函數，跨平台兼容"""
    print(prompt, end='', flush=True)
    result = [default]
    
    def inner():
        try:
            ans = input()
            if ans.strip() != '':
                result[0] = ans.strip()
        except EOFError:
            pass
            
    t = threading.Thread(target=inner)
    t.daemon = True
    t.start()
    t.join(timeout)
    print("")  # 輸出換行
    return result[0]

def ensure_hf_quant_model(model_name):
    """確保 HuggingFace 量化模型已下載"""
    try:
        from huggingface_hub import snapshot_download
        
        # 檢查模型是否存在於HuggingFace快取中
        cache_dir = os.path.expanduser("~/.cache/huggingface/hub")
        model_dir = os.path.join(cache_dir, "models--" + model_name.replace("/", "--"))
        
        if not os.path.exists(model_dir):
            print(f"[模型下載] 開始下載 {model_name} ...")
            snapshot_download(repo_id=model_name, local_dir=None, local_dir_use_symlinks=True)
            print(f"[模型下載] {model_name} 下載完成。")
        else:
            print(f"[模型檢查] {model_name} 已存在於本地快取。")
            
        return True
    except ImportError:
        print("[警告] 未安裝 huggingface_hub，無法自動下載模型。請安裝：pip install huggingface_hub")
        return False
    except Exception as e:
        print(f"[警告] 檢查/下載模型時發生錯誤: {e}")
        return False

def analyze_log():
    """分析日誌文件以提供診斷信息"""
    try:
        with open(LOG_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()[-30:]  # 僅分析最後30行
    except Exception:
        print("[診斷] 無法讀取 log 檔案。")
        return
    
    # 分析流程
    last_energy = None
    vad_fail = False
    vad_method = None
    skip_count = 0
    
    for line in lines:
        if '降噪後能量' in line or '原始能量' in line:
            try:
                last_energy = float(line.split(':')[-1].strip())
            except:
                pass
        if 'VAD 偵測失敗' in line or 'Python energy threshold' in line:
            vad_fail = True
        if '人聲偵測方法' in line:
            vad_method = line.strip().split('：')[-1]
        if '未偵測到人聲' in line:
            skip_count += 1
    
    print("\n[自動診斷報告]")
    if skip_count > 0:
        print(f"- 最近 {skip_count} 次錄音都未偵測到人聲。")
    if last_energy is not None:
        print(f"- 最近一次能量值: {last_energy:.4f}")
        if last_energy < 0.01:
            print(" → 音訊能量過低，請確認麥克風音量/距離/權限。")
        else:
            print(" → 能量正常，可能是降噪過強或 VAD 閾值過高。建議關閉降噪或調整參數。")
    if vad_fail:
        print("- VAD 模組不可用，已自動切換為 Python 閾值法。")
    
    print("- 建議：\n 1. 測試關閉降噪是否能辨識。\n 2. 確認麥克風音量與環境。\n 3. 如仍無法辨識，請錄音後手動檢查音檔內容。")

def main():
    """主要程式流程"""
    # 確保所需依賴項都已安裝
    if not check_dependencies():
        print("請安裝上述缺少的依賴項後重試。")
        return
    
    print("[DEBUG] main() 啟動完成，進入互動流程")
    sys.stdout.flush()
    
    # 初始化語音辨識器
    recognizer = sr.Recognizer()
    
    # 設定語音辨識參數
    recognizer.pause_threshold = 1  # 停止多少秒數後視為結束語句
    recognizer.phrase_threshold = 0.3  # 最小語句秒數
    recognizer.non_speaking_duration = 0.5  # 開始和結束的等待秒數
    
    # 設定退出標記
    exit_flag = threading.Event()
    
    # 監聽ESC鍵的函數
    def check_exit():
        while not exit_flag.is_set():
            if keyboard.is_pressed('esc'):
                print("\n程式即將退出...")
                exit_flag.set()
                break
            time.sleep(0.1)
    
    # 啟動監聽ESC鍵的執行緒
    exit_thread = threading.Thread(target=check_exit)
    exit_thread.daemon = True
    exit_thread.start()
    
    print("語音辨識程式已啟動")
    print("請開始說話，系統會自動辨識")
    print("按下ESC鍵可退出程式")
    
    # 檢測硬體環境
    device, compute_type = detect_hardware()
    
    # 降噪設置
    noise_profile_path = "noise_profile.npy"
    noise_profile = None
    
    # 啟動時詢問是否重新錄製降噪樣本（預設N，2秒自動略過）
    if os.path.exists(noise_profile_path):
        ans = input_with_timeout("偵測到已存在降噪樣本，要重新錄製嗎？(Y/n)： 預設N 等待2秒\n", 2, 'n').lower()
        if ans == 'y':
            need_record = True
        else:
            need_record = False
    else:
        need_record = True
    
    if need_record:
        # 1. 錄製兩段環境音作為降噪樣本
        print("請錄製第一段環境音（請保持安靜或只錄背景雜訊），按 Enter 結束...")
        env_frames1 = []
        start_time = time.time()
        
        def env_callback1(indata, frame_count, time_info, status):
            elapsed = time.time() - start_time
            bar = '█' * int(np.linalg.norm(indata) * 10)
            print(f'\r[環境音1]{bar:<30} {elapsed:.1f}s', end='')
            env_frames1.append(indata.copy())
        
        stop_flag1 = threading.Event()
        
        def wait_env1():
            input()
            stop_flag1.set()
        
        threading.Thread(target=wait_env1).start()
        
        try:
            with sd.InputStream(samplerate=16000, channels=1, callback=env_callback1):
                while not stop_flag1.is_set():
                    sd.sleep(100)
        except Exception as e:
            print(f"\n錄製環境音時出錯: {e}")
            print("請確認麥克風權限和連接，程序將繼續但無法使用降噪功能")
            need_record = False
            use_denoise = False
            
        if need_record:
            print()
            print("請錄製第二段環境音（請保持安靜或只錄背景雜訊），按 Enter 結束...")
            env_frames2 = []
            start_time = time.time()
            
            def env_callback2(indata, frame_count, time_info, status):
                elapsed = time.time() - start_time
                bar = '█' * int(np.linalg.norm(indata) * 10)
                print(f'\r[環境音2]{bar:<30} {elapsed:.1f}s', end='')
                env_frames2.append(indata.copy())
            
            stop_flag2 = threading.Event()
            
            def wait_env2():
                input()
                stop_flag2.set()
            
            threading.Thread(target=wait_env2).start()
            
            try:
                with sd.InputStream(samplerate=16000, channels=1, callback=env_callback2):
                    while not stop_flag2.is_set():
                        sd.sleep(100)
                        
                print()
                
                # 合併兩段環境音作為 noise_profile
                noise_profile = np.concatenate(env_frames1 + env_frames2, axis=0)
                
                # 儲存降噪樣本
                np.save(noise_profile_path, noise_profile)
                print(f"降噪樣本已儲存於 {noise_profile_path}")
            except Exception as e:
                print(f"\n錄製環境音時出錯: {e}")
                print("請確認麥克風權限和連接，程序將繼續但無法使用降噪功能")
                need_record = False
                use_denoise = False
    else:
        # 直接載入降噪樣本
        try:
            noise_profile = np.load(noise_profile_path)
            print(f"已載入降噪樣本 {noise_profile_path}")
        except Exception as e:
            print(f


### 对话 4

**问题**: 從中斷的地方繼續輸出

**回答**:
```python
        try:
            with open(LOG_PATH, 'r', encoding='utf-8') as f:
                lines = f.readlines()[-30:] # 只分析最近 30 行
        except Exception:
            print("[診斷] 無法讀取 log 檔案。")
            return
        
        # 分析流程
        last_energy = None
        vad_fail = False
        vad_method = None
        skip_count = 0
        
        for line in lines:
            if '降噪後能量' in line or '原始能量' in line:
                try:
                    last_energy = float(line.split(':')[-1].strip())
                except:
                    pass
            if 'VAD 偵測失敗' in line or 'Python energy threshold' in line:
                vad_fail = True
            if '人聲偵測方法' in line:
                vad_method = line.strip().split('：')[-1]
            if '未偵測到人聲' in line:
                skip_count += 1
        
        print("\n[自動診斷報告]")
        if skip_count > 0:
            print(f"- 最近 {skip_count} 次錄音都未偵測到人聲。")
        if last_energy is not None:
            print(f"- 最近一次能量值: {last_energy:.4f}")
            if last_energy < 0.01:
                print(" → 音訊能量過低，請確認麥克風音量/距離/權限。")
            else:
                print(" → 能量正常，可能是降噪過強或 VAD 閾值過高。建議關閉降噪或調整參數。")
        if vad_fail:
            print("- VAD 模組不可用，已自動切換為 Python 閾值法。")
        
        print("- 建議：\n 1. 測試關閉降噪是否能辨識。\n 2. 確認麥克風音量與環境。\n 3. 如仍無法辨識，請錄音後手動檢查音檔內容。")

def detect_hardware():
    """檢測可用硬體，決定模型執行環境"""
    device = "cpu"
    compute_type = "int8"
    
    try:
        # 嘗試導入torch檢查CUDA可用性
        import torch
        if torch.cuda.is_available():
            device = "cuda"
            compute_type = "int8_float16"
            print(f"已檢測到 CUDA 支援的 GPU：{torch.cuda.get_device_name(0)}")
            print(f"顯存：{torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        else:
            print("未檢測到 CUDA 支援的 GPU，將使用 CPU 運行（速度較慢）")
            
        # 檢查Apple Silicon MPS
        if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            device = "mps"
            compute_type = "int8"
            print("已檢測到 Apple Silicon MPS，將使用 MPS 加速")
    except ImportError:
        print("未安裝 PyTorch，無法檢測 GPU 狀態，將使用 CPU 運行")
    except Exception as e:
        print(f"檢測硬體時發生錯誤：{e}")
        print("將使用 CPU 運行")
        
    return device, compute_type

def whisper_recognize(audio_np, fs, model_name, device, compute_type):
    """執行Whisper模型語音識別"""
    try:
        import time as t
        from faster_whisper import WhisperModel
        import tempfile
        import soundfile as sf
        
        start_whisper = t.time()
        
        # 初始化模型，使用檢測到的硬體環境
        model = WhisperModel(model_name, device=device, compute_type=compute_type)
        
        # 保存音頻到臨時文件
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=True) as tmp:
            sf.write(tmp.name, audio_np, samplerate=fs, subtype='PCM_16')
            
            # 執行轉錄
            segments, info = model.transcribe(tmp.name, beam_size=5, language="zh")
            
            # 合併所有段落文本
            whisper_result = ''.join([seg.text for seg in segments])
            
        return whisper_result, t.time() - start_whisper
    except Exception as e:
        print(f"Whisper模型 {model_name} 執行出錯: {e}")
        logging.error(f"Whisper模型 {model_name} 執行出錯: {e}")
        return f"[錯誤] {model_name}: {e}", 0

def main():
    """主要程式流程"""
    # 確保所需依賴項都已安裝
    if not check_dependencies():
        print("請安裝上述缺少的依賴項後重試。")
        return
    
    print("[DEBUG] main() 啟動完成，進入互動流程")
    sys.stdout.flush()
    
    # 初始化語音辨識器
    recognizer = sr.Recognizer()
    
    # 設定語音辨識參數
    recognizer.pause_threshold = 1  # 停止多少秒數後視為結束語句
    recognizer.phrase_threshold = 0.3  # 最小語句秒數
    recognizer.non_speaking_duration = 0.5  # 開始和結束的等待秒數
    
    # 設定退出標記
    exit_flag = threading.Event()
    
    # 監聽ESC鍵的函數
    def check_exit():
        while not exit_flag.is_set():
            if keyboard.is_pressed('esc'):
                print("\n程式即將退出...")
                exit_flag.set()
                break
            time.sleep(0.1)
    
    # 啟動監聽ESC鍵的執行緒
    exit_thread = threading.Thread(target=check_exit)
    exit_thread.daemon = True
    exit_thread.start()
    
    print("語音辨識程式已啟動")
    print("請開始說話，系統會自動辨識")
    print("按下ESC鍵可退出程式")
    
    # 檢測硬體環境
    device, compute_type = detect_hardware()
    
    # 降噪設置
    noise_profile_path = "noise_profile.npy"
    noise_profile = None
    
    # 啟動時詢問是否重新錄製降噪樣本（預設N，2秒自動略過）
    if os.path.exists(noise_profile_path):
        ans = input_with_timeout("偵測到已存在降噪樣本，要重新錄製嗎？(Y/n)： 預設N 等待2秒\n", 2, 'n').lower()
        if ans == 'y':
            need_record = True
        else:
            need_record = False
    else:
        need_record = True
    
    if need_record:
        # 1. 錄製兩段環境音作為降噪樣本
        print("請錄製第一段環境音（請保持安靜或只錄背景雜訊），按 Enter 結束...")
        env_frames1 = []
        start_time = time.time()
        
        def env_callback1(indata, frame_count, time_info, status):
            elapsed = time.time() - start_time
            bar = '█' * int(np.linalg.norm(indata) * 10)
            print(f'\r[環境音1]{bar:<30} {elapsed:.1f}s', end='')
            env_frames1.append(indata.copy())
        
        stop_flag1 = threading.Event()
        
        def wait_env1():
            input()
            stop_flag1.set()
        
        threading.Thread(target=wait_env1).start()
        
        try:
            with sd.InputStream(samplerate=16000, channels=1, callback=env_callback1):
                while not stop_flag1.is_set():
                    sd.sleep(100)
        except Exception as e:
            print(f"\n錄製環境音時出錯: {e}")
            print("請確認麥克風權限和連接，程序將繼續但無法使用降噪功能")
            need_record = False
            use_denoise = False
            
        if need_record:
            print()
            print("請錄製第二段環境音（請保持安靜或只錄背景雜訊），按 Enter 結束...")
            env_frames2 = []
            start_time = time.time()
            
            def env_callback2(indata, frame_count, time_info, status):
                elapsed = time.time() - start_time
                bar = '█' * int(np.linalg.norm(indata) * 10)
                print(f'\r[環境音2]{bar:<30} {elapsed:.1f}s', end='')
                env_frames2.append(indata.copy())
            
            stop_flag2 = threading.Event()
            
            def wait_env2():
                input()
                stop_flag2.set()
            
            threading.Thread(target=wait_env2).start()
            
            try:
                with sd.InputStream(samplerate=16000, channels=1, callback=env_callback2):
                    while not stop_flag2.is_set():
                        sd.sleep(100)
                        
                print()
                
                # 合併兩段環境音作為 noise_profile
                noise_profile = np.concatenate(env_frames1 + env_frames2, axis=0)
                
                # 儲存降噪樣本
                np.save(noise_profile_path, noise_profile)
                print(f"降噪樣本已儲存於 {noise_profile_path}")
            except Exception as e:
                print(f"\n錄製環境音時出錯: {e}")
                print("請確認麥克風權限和連接，程序將繼續但無法使用降噪功能")
                need_record = False
                use_denoise = False
    else:
        # 直接載入降噪樣本
        try:
            noise_profile = np.load(noise_profile_path)
            print(f"已載入降噪樣本 {noise_profile_path}")
        except Exception as e:
            print(f"載入降噪樣本時發生錯誤: {e}")
            print("將繼續但不使用降噪功能")
            noise_profile = None
    
    # 啟動時詢問是否啟用降噪（預設Y，2秒自動啟用）
    use_denoise = True
    if noise_profile is not None:
        ans = input_with_timeout("是否啟用降噪？(Y/n)： 預設Y 等待2秒\n", 2, 'y').lower()
        if ans == 'n':
            use_denoise = False
    else:
        use_denoise = False
        print("無法使用降噪功能（樣本不存在或載入失敗）")
    
    # 配置日誌
    LOG_PATH = "speech_asr_debug.log"
    logging.basicConfig(filename=LOG_PATH, filemode='a', level=logging.INFO,
                        format='%(asctime)s %(message)s', encoding='utf-8')
    
    # Whisper 量化模型選擇
    print("Whisper 量化模型選擇：")
    print("1. small (顯存需求低，速度快)")
    print("2. medium (辨識較準確，顯存需求較高)")
    print("3. 兩者都執行（方便比較，需較多顯存）")
    
    ans = input_with_timeout("請選擇 Whisper 模型 (1/2/3，預設1，5秒自動選1): ", 5, '1')
    
    if ans in ('', '1'):
        whisper_model_choice = ['guillaumekln/faster-whisper-small']
    elif ans == '2':
        whisper_model_choice = ['guillaumekln/faster-whisper-medium']
    elif ans == '3':
        whisper_model_choice = ['guillaumekln/faster-whisper-small', 'guillaumekln/faster-whisper-medium']
    else:
        whisper_model_choice = ['guillaumekln/faster-whisper-small']
    
    # 自動下載所需 HuggingFace 量化模型
    print("[DEBUG] 開始檢查/下載 Whisper 模型...", flush=True)
    available_models = []
    
    for m in whisper_model_choice:
        try:
            print(f"[DEBUG] 檢查/下載模型: {m}", flush=True)
            ensure_hf_quant_model(m)
            available_models.append(m)
            print(f"[DEBUG] 模型 {m} 可用", flush=True)
        except Exception as e:
            print(f"[警告] Whisper 模型 {m} 下載/檢查失敗：{e}\n將略過此模型，繼續其他模型。", flush=True)
    
    if not available_models:
        print("[致命錯誤] 所有 Whisper 模型皆無法下載/檢查，將僅執行 Google 語音辨識。", flush=True)
    
    whisper_model_choice = available_models
    print(f"[DEBUG] whisper_model_choice: {whisper_model_choice}", flush=True)
    print("[DEBUG] 進入主循環 while not exit_flag.is_set() ...", flush=True)
    
    # 主循環
    while not exit_flag.is_set():
        try:
            # 開啟麥克風
            with sr.Microphone() as source:
                print("\n正在聆聽... (動態音量條與秒數)")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                fs = int(source.SAMPLE_RATE)
                frames = []
                start_time = time.time()
                
                print("請開始說話，3秒沒有人聲自動結束錄音...")
                silence_limit = 3.0  # 3秒無人聲自動結束
                last_voice_time = time.time()
                stop_flag = threading.Event()
                
                # 監聽靜音的執行緒
                def monitor_silence():
                    while not stop_flag.is_set():
                        remaining = silence_limit - (time.time() - last_voice_time)
                        if remaining < 0:
                            stop_flag.set()
                            break
                        time.sleep(0.1)
                
                silence_thread = threading.Thread(target=monitor_silence)
                silence_thread.daemon = True
                silence_thread.start()
                
                # 監聽ESC按鍵的執行緒
                def esc_monitor():
                    while not stop_flag.is_set():
                        if exit_flag.is_set():
                            stop_flag.set()
                            break
                        time.sleep(0.1)
                
                esc_thread = threading.Thread(target=esc_monitor)
                esc_thread.daemon = True
                esc_thread.start()
                
                # 監聽Enter按鍵的執行緒
                def wait_for_enter():
                    try:
                        input()
                        stop_flag.set()
                    except EOFError:
                        pass
                
                enter_thread = threading.Thread(target=wait_for_enter)
                enter_thread.daemon = True
                enter_thread.start()
                
                # 錄音回調函數
                def callback(indata, frame_count, time_info, status):
                    nonlocal last_voice_time
                    
                    if exit_flag.is_set() or stop_flag.is_set():
                        raise sd.CallbackStop()
                    
                    elapsed = time.time() - start_time
                    
                    # 降噪處理
                    if use_denoise and noise_profile is not None:
                        try:
                            reduced = nr.reduce_noise(y=indata.flatten(), sr=fs, y_noise=noise_profile.flatten())
                        except Exception as e:
                            print(f"\n[警告] 降噪處理失敗: {e}，使用原始音訊")
                            reduced = indata.flatten()
                    else:
                        reduced = indata.flatten()
                    
                    frames.append(reduced.reshape(-1, 1))
                    
                    # 音量條與靜音倒數合併顯示
                    volume_norm = np.linalg.norm(reduced) * 10
                    bar = '█' * int(volume_norm)
                    remaining = silence_limit - (time.time() - last_voice_time)
                    
                    print(f'\r[{"降噪" if use_denoise else "錄音"}]{bar:<30} {elapsed:.1f}s [靜音倒數: {max(0, remaining):.1f}s]', end='')
                    
                    # 人聲偵測（能量法）
                    if np.mean(np.abs(reduced)) > 0.01:
                        last_voice_time = time.time()
                
                # 開始錄音
                try:
                    with sd.InputStream(samplerate=fs, channels=1, callback=callback):
                        while not stop_flag.is_set():
                            sd.sleep(10)  # 10ms檢查一次，提升按鍵響應速度
                except Exception as e:
                    print(f"\n[錯誤] 錄音時發生例外: {e}")
                    logging.error(f"錄音時發生例外: {e}")
                    continue
                
                print()
                duration = time.time() - start_time
                print(f"實際錄音秒數：{duration:.1f}s")
                
                # 檢查是否有錄到聲音
                if not frames:
                    print("[警告] 未錄到任何聲音！")
                    continue
                
                # 將 frames 合併為音訊資料
                audio_np = np.concatenate(frames, axis=0).flatten()
                
                # 音量分析
                max_amp = np.max(np.abs(audio_np))
                mean_amp = np.mean(np.abs(audio_np))
                
                print(f"[DEBUG] 音量分析：最大值={max_amp:.4f} 平均值={mean_amp:.4f}")
                logging.info(f"音量分析：最大值={max_amp:.4f} 平均值={mean_amp:.4f}")
                
                if max_amp < 0.01:
                    print("[建議] 音量過小，請靠近麥克風或調高音量。")
                elif max_amp > 0.8:
                    print("[建議] 音量過大，可能爆音，請遠離麥克風或調低音量。")
                else:
                    print("[建議] 音量正常。")
                
                # 自動 normalization（避免太小聲）
                if max_amp > 0:
                    audio_np = audio_np / max_amp * 0.5  # 正規化到最大幅度0.5
                
                # 顯示降噪前後能量
                if use_denoise:
                    msg = f"[DEBUG] 降噪後能量: {np.mean(np.abs(audio_np)):.4f}"
                else:
                    msg = f"[DEBUG] 原始能量: {np.mean(np.abs(audio_np)):.4f}"
                
                print(f"\n{msg}")
                logging.info(msg)
                
                # 轉換為AudioData格式供Google語音辨識使用
                audio_bytes = (audio_np * 32767).astype(np.int16).tobytes()
                audio_data = sr.AudioData(audio_bytes, fs, 2)
                
                # --- 人聲偵測區塊 ---
                human_voice = False
                used_method = None
                
                # 嘗試使用silero-vad
                try:
                    from silero_vad import VoiceActivityDetector
                    vad = VoiceActivityDetector(fs)
                    test_audio = audio_np[:16000] if len(audio_np) > 16000 else audio_np
                    speech_probs = vad.get_speech_prob(test_audio.astype(np.float32))
                    
                    if np.max(speech_probs) > 0.5:
                        human_voice = True
                        used_method = "silero-vad"
                except Exception as e:
                    msg = f"silero-vad 偵測失敗或不可用，改用 Python 閾值法: {e}"
                    print(msg)
                    logging.info(msg)
                    
                    # 使用簡單能量閾值法
                    energy = np.mean(np.abs(audio_np))
                    print(f"[DEBUG] 使用 Python 閾值法，能量值: {energy:.4f}")
                    logging.info(f"使用 Python 閾值法，能量值: {energy:.4f}")
                    
                    if energy > 0.01:
                        human_voice = True
                        used_method = "Python energy threshold"
                
                print(f"[DEBUG] 人聲偵測方法：{used_method}")
                logging.info(f"人聲偵測方法：{used_method}")
                
                if not human_voice:
                    print("未偵測到人聲，略過辨識。")
                    logging.info("未偵測到人聲，略過辨識。")
                    analyze_log()
                    continue
                
                # --- 人聲偵測結束 ---
                
                print("正在處理語音...")
                
                # Google 與 Whisper 辨識（多模型並行）
                google_zh = None
                whisper_results = []
                whisper_times = []
                
                # Google 語音辨識函數
                def google_recognize():
                    nonlocal google_zh
                    try:
                        google_zh = recognizer.recognize_google(audio_data, language="zh-TW")
                    except sr.UnknownValueError:
                        google_zh = "無法辨識"
                    except Exception as e:
                        google_zh = f"Google辨識錯誤: {e}"
                        logging.error(f"Google辨識錯誤: {e}")
                    
                    print("\n====================\n[Google] 辨識結果：" + google_zh + "\n====================")
                
                # 先執行 Google，因為它是非同步的
                t_google = threading.Thread(target=google_recognize)
                t_google.start()
                t_google.join()
                
                # 依序執行 Whisper 模型，避免 GPU 顯存不足
                for model_name in whisper_model_choice:
                    try:
                        result, elapsed_time = whisper_recognize(audio_np, fs, model_name, device, compute_type)
                        whisper_results.append((model_name, result))
                        whisper_times.append(elapsed_time)
                    except Exception as e:
                        print(f"[錯誤] Whisper模型 {model_name} 執行失敗: {e}")
                        logging.error(f"Whisper模型 {model_name} 執行失敗: {e}")
                        whisper_results.append((model_name, f"[錯誤] {e}"))
                        whisper_times.append(0)
                
                # 輸出所有 Whisper 模型的結果和推論時間
                for idx, (model_name, result) in enumerate(whisper_results):
                    print(f"[Whisper-{model_name.split('/')[-1]}] 辨識結果：{result}")
                    print(f"[Whisper-{model_name.split('/')[-1]} {device.upper()}] 推論時間：{whisper_times[idx]:.2f} 秒")
                    logging.info(f"[Whisper-{model_name.split('/')[-1]}] {device.upper()}推論時間: {whisper_times[idx]:.2f} 秒，結果: {result}")
                
                # 比較不同模型結果
                def merge_results(g, w):
                    # 去除前後空格
                    g = g.strip() if g else ""
                    w = w.strip() if w else ""
                    
                    if not g or not w:
                        return g or w
                    
                    seq = difflib.SequenceMatcher(None, g, w)
                    ratio = seq.ratio()
                    
                    print(f"[合併分析] Google/Whisper 相似度: {ratio:.2f}")
                    logging.info(f"[合併分析] Google/Whisper 相似度: {ratio:.2f}")
                    
                    if ratio > 0.85:
                        print("[合併建議] 兩者結果高度相似，建議直接採用：")
                        merged = g if len(g) >= len(w) else w
                        print(merged)
                        return merged
                    else:
                        print("[合併建議] 兩者有差異，建議人工確認：")
                        print("Google:", g)
                        print("Whisper:", w)
                        
                        diff = list(difflib.ndiff(g, w))
                        diff_str = ''.join(x for x in diff if x.startswith('+') or x.startswith('-'))
                        print("[差異]", diff_str)
                        logging.info(f"[差異] {diff_str}")
                        return None
                
                # 若有small模型結果，優先與Google結果合併
                main_whisper = next((r for n, r in whisper_results if "small" in n.lower()), None)
                if not main_whisper and whisper_results:
                    main_whisper = whisper_results[0][1]
                
                if main_whisper and google_zh and not google_zh == "無法辨識":
                    merged_result = merge_results(google_zh, main_whisper)
                    if merged_result:
                        print("\n[最終建議結果]:", merged_result)
                
                # 若同時有多個Whisper模型結果，顯示比對
                if len(whisper_results) > 1:
                    print("\n[Whisper 模型間比對]")
                    for i in range(len(whisper_results)-1):
                        for j in range(i+1, len(whisper_results)):
                            n1, r1 = whisper_results[i]
                            n2, r2 = whisper_results[j]
                            
                            # 跳過包含錯誤的結果
                            if r1.startswith("[錯誤]") or r2.startswith("[錯誤]"):
                                continue
                                
                            n1_short = n1.split("/")[-1]
                            n2_short = n2.split("/")[-1]
                            
                            seq = difflib.SequenceMatcher(None, r1, r2)
                            ratio = seq.ratio()
                            
                            print(f"{n1_short} vs {n2_short} 相似度: {ratio:.2f}")
                            logging.info(f"[Whisper模型比對] {n1_short} vs {n2_short} 相似度: {ratio:.2f}")
                            
                            if ratio < 0.85:
                                print(f"→ 內容差異較大，建議人工確認。\n{n1_short}: {r1}\n{n2_short}: {r2}")
                                logging.info(f"→ 差異大\n{n1_short}: {r1}\n{n2_short}: {r2}")
                
        except Exception as e:
            print(f"[錯誤] 主循環發生例外: {e}")
            logging.error(f"主循環發生例外: {e}")
            # 添加短暫延遲避免CPU高負載
            time.sleep(0.5)
            continue
    
    print("程式已退出")

if __name__ == "__main__":
    print("[DEBUG] __main__ 啟動，準備呼叫 main()")
    sys.stdout.flush()
    main()
```


### 对话 5

**问题**: 你可以寫一個純HTML5的網頁來讓我在 往業上按下麥克風講話
就是開始跟停止 然後把這段語音 給剛剛的程式來處理 處理完畢後把文字 顯示在網頁上嗎

**回答**:
# 網頁語音辨識整合方案

以下是一個純HTML5網頁，可讓您通過麥克風錄音並發送到後端進行處理，然後在網頁上顯示辨識結果。這個解決方案分為前端和後端兩部分。

## 前端HTML5網頁代碼

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>語音辨識介面</title>
    <style>
        body {
            font-family: Arial, "微軟正黑體", sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        
        .container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        h1 {
            color: #333;
            text-align: center;
        }
        
        .mic-button {
            display: block;
            width: 120px;
            height: 120px;
            margin: 30px auto;
            border-radius: 50%;
            background-color: #2f2ff2;
            color: white;
            border: none;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .mic-button.recording {
            background-color: #f22f2f;
            animation: pulse 1.5s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .status {
            text-align: center;
            margin: 15px 0;
            font-size: 16px;
            min-height: 20px;
        }
        
        .result-container {
            margin-top: 30px;
            border-top: 1px solid #eee;
            padding-top: 20px;
        }
        
        .result {
            background: #f9f9f9;
            border-left: 4px solid #2f2ff2;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }
        
        .model-name {
            font-weight: bold;
            color: #666;
            margin-bottom: 5px;
        }
        
        .progress-bar {
            width: 100%;
            height: 4px;
            background-color: #eee;
            margin: 10px 0;
            border-radius: 2px;
            overflow: hidden;
        }
        
        .progress-bar-fill {
            height: 100%;
            background-color: #2f2ff2;
            width: 0%;
            transition: width 0.3s;
        }
        
        .settings {
            margin-top: 30px;
        }
        
        select, input[type="checkbox"] {
            margin: 10px 5px;
        }
        
        .error {
            color: #f22f2f;
            text-align: center;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>語音辨識系統</h1>
        
        <div class="settings">
            <div>
                <input type="checkbox" id="denoise" name="denoise" checked>
                <label for="denoise">啟用降噪</label>
            </div>
            
            <div>
                <label for="model">Whisper 模型選擇:</label>
                <select id="model" name="model">
                    <option value="small">small (速度快)</option>
                    <option value="medium">medium (較準確)</option>
                    <option value="both">兩者都執行 (比較)</option>
                </select>
            </div>
        </div>
        
        <button id="micButton" class="mic-button">
            點擊開始錄音
        </button>
        
        <div id="status" class="status"></div>
        
        <div class="progress-bar">
            <div id="progressBarFill" class="progress-bar-fill"></div>
        </div>
        
        <div id="errorMessage" class="error"></div>
        
        <div class="result-container">
            <h2>辨識結果</h2>
            <div id="results"></div>
        </div>
    </div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // 檢查瀏覽器支援
            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                document.getElementById('errorMessage').textContent = 
                    '您的瀏覽器不支援錄音功能，請使用最新版Chrome或Firefox。';
                document.getElementById('micButton').disabled = true;
                return;
            }
            
            const micButton = document.getElementById('micButton');
            const status = document.getElementById('status');
            const results = document.getElementById('results');
            const progressBarFill = document.getElementById('progressBarFill');
            const errorMessage = document.getElementById('errorMessage');
            const denoiseCheckbox = document.getElementById('denoise');
            const modelSelect = document.getElementById('model');
            
            let mediaRecorder;
            let audioChunks = [];
            let isRecording = false;
            let startTime;
            let progressInterval;
            
            // 更新錄音時間和進度條
            function updateProgress() {
                const elapsed = (Date.now() - startTime) / 1000;
                status.textContent = `錄音中... ${elapsed.toFixed(1)} 秒`;
                
                // 30秒為最大錄音時間
                const progress = Math.min(elapsed / 30 * 100, 100);
                progressBarFill.style.width = `${progress}%`;
                
                // 如果超過30秒，自動停止錄音
                if (elapsed >= 30) {
                    stopRecording();
                }
            }
            
            // 開始錄音
            function startRecording() {
                navigator.mediaDevices.getUserMedia({ audio: true })
                    .then(stream => {
                        status.textContent = '開始錄音...';
                        errorMessage.textContent = '';
                        
                        mediaRecorder = new MediaRecorder(stream);
                        audioChunks = [];
                        
                        mediaRecorder.ondataavailable = event => {
                            audioChunks.push(event.data);
                        };
                        
                        mediaRecorder.onstop = () => {
                            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                            sendAudioToServer(audioBlob);
                        };
                        
                        mediaRecorder.start();
                        isRecording = true;
                        micButton.classList.add('recording');
                        micButton.textContent = '點擊停止錄音';
                        
                        startTime = Date.now();
                        progressBarFill.style.width = '0%';
                        progressInterval = setInterval(updateProgress, 100);
                    })
                    .catch(error => {
                        errorMessage.textContent = `無法啟用麥克風: ${error.message}`;
                        console.error('麥克風存取錯誤:', error);
                    });
            }
            
            // 停止錄音
            function stopRecording() {
                if (mediaRecorder && isRecording) {
                    mediaRecorder.stop();
                    isRecording = false;
                    micButton.classList.remove('recording');
                    micButton.textContent = '點擊開始錄音';
                    status.textContent = '處理中...';
                    
                    clearInterval(progressInterval);
                    progressBarFill.style.width = '100%';
                    
                    // 停止所有媒體軌道
                    mediaRecorder.stream.getTracks().forEach(track => track.stop());
                }
            }
            
            // 發送音頻到服務器
            function sendAudioToServer(audioBlob) {
                const formData = new FormData();
                formData.append('audio_data', audioBlob, 'recording.wav');
                formData.append('denoise', denoiseCheckbox.checked);
                formData.append('model', modelSelect.value);
                
                fetch('/process_audio', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('服務器處理失敗');
                    }
                    return response.json();
                })
                .then(data => {
                    status.textContent = '處理完成';
                    displayResults(data);
                    progressBarFill.style.width = '0%';
                })
                .catch(error => {
                    status.textContent = '';
                    errorMessage.textContent = `處理失敗: ${error.message}`;
                    console.error('上傳或處理錯誤:', error);
                });
            }
            
            // 顯示辨識結果
            function displayResults(data) {
                results.innerHTML = '';
                
                if (data.google) {
                    const resultDiv = document.createElement('div');
                    resultDiv.className = 'result';
                    
                    const modelNameDiv = document.createElement('div');
                    modelNameDiv.className = 'model-name';
                    modelNameDiv.textContent = 'Google 辨識結果:';
                    
                    const textDiv = document.createElement('div');
                    textDiv.textContent = data.google;
                    
                    resultDiv.appendChild(modelNameDiv);
                    resultDiv.appendChild(textDiv);
                    results.appendChild(resultDiv);
                }
                
                if (data.whisper && data.whisper.length > 0) {
                    data.whisper.forEach(item => {
                        const resultDiv = document.createElement('div');
                        resultDiv.className = 'result';
                        
                        const modelNameDiv = document.createElement('div');
                        modelNameDiv.className = 'model-name';
                        modelNameDiv.textContent = `Whisper ${item.model} 辨識結果: (${item.time}秒)`;
                        
                        const textDiv = document.createElement('div');
                        textDiv.textContent = item.text;
                        
                        resultDiv.appendChild(modelNameDiv);
                        resultDiv.appendChild(textDiv);
                        results.appendChild(resultDiv);
                    });
                }
                
                if (data.merged) {
                    const resultDiv = document.createElement('div');
                    resultDiv.className = 'result';
                    resultDiv.style.borderLeft = '4px solid #2fb82f';
                    
                    const modelNameDiv = document.createElement('div');
                    modelNameDiv.className = 'model-name';
                    modelNameDiv.textContent = '最佳辨識結果 (合併):';
                    
                    const textDiv = document.createElement('div');
                    textDiv.textContent = data.merged;
                    
                    resultDiv.appendChild(modelNameDiv);
                    resultDiv.appendChild(textDiv);
                    results.appendChild(resultDiv);
                }
            }
            
            // 點擊麥克風按鈕
            micButton.addEventListener('click', function() {
                if (isRecording) {
                    stopRecording();
                } else {
                    startRecording();
                }
            });
        });
    </script>
</body>
</html>
```

## 後端 Flask 程式碼

這是將前端與您的 `speech_recognition_ASR.py` 整合的 Flask 後端程式碼：

```python
from flask import Flask, request, jsonify, render_template
import tempfile
import os
import numpy as np
import soundfile as sf
import sys
import logging
import time
from faster_whisper import WhisperModel
import speech_recognition as sr

app = Flask(__name__, static_folder='static', template_folder='templates')

# 日誌配置
logging.basicConfig(
    filename="web_asr_debug.log", 
    filemode='a', 
    level=logging.INFO,
    format='%(asctime)s %(message)s', 
    encoding='utf-8'
)

# 載入降噪樣本（如果存在）
noise_profile_path = "noise_profile.npy"
noise_profile = None
if os.path.exists(noise_profile_path):
    try:
        noise_profile = np.load(noise_profile_path)
        print(f"已載入降噪樣本 {noise_profile_path}")
    except Exception as e:
        print(f"載入降噪樣本時發生錯誤: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audio_data' not in request.files:
        return jsonify({"error": "沒有音頻檔案"}), 400
    
    try:
        # 獲取表單參數
        audio_file = request.files['audio_data']
        denoise = request.form.get('denoise', 'true') == 'true'
        model_choice = request.form.get('model', 'small')
        
        # 將音頻保存到臨時文件
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            audio_file.save(tmp.name)
            tmp_path = tmp.name
        
        # 讀取音頻文件
        audio_np, fs = sf.read(tmp_path)
        
        # 應用降噪（如果啟用且有降噪樣本）
        if denoise and noise_profile is not None:
            try:
                import noisereduce as nr
                audio_np = nr.reduce_noise(y=audio_np, sr=fs, y_noise=noise_profile.flatten())
                logging.info(f"降噪後能量: {np.mean(np.abs(audio_np)):.4f}")
            except Exception as e:
                logging.error(f"降噪處理失敗: {e}")
        
        # 創建 AudioData 對象（用於 Google 辨識）
        audio_bytes = (audio_np * 32767).astype(np.int16).tobytes()
        audio_data = sr.AudioData(audio_bytes, fs, 2)
        
        # Google 語音辨識
        recognizer = sr.Recognizer()
        google_result = None
        try:
            google_result = recognizer.recognize_google(audio_data, language="zh-TW")
        except sr.UnknownValueError:
            google_result = "無法辨識"
        except Exception as e:
            google_result = f"Google辨識錯誤: {e}"
            logging.error(f"Google辨識錯誤: {e}")
        
        # Whisper 模型選擇
        whisper_results = []
        if model_choice == 'small':
            models = ['guillaumekln/faster-whisper-small']
        elif model_choice == 'medium':
            models = ['guillaumekln/faster-whisper-medium']
        else:  # 'both'
            models = ['guillaumekln/faster-whisper-small', 'guillaumekln/faster-whisper-medium']
        
        # 檢查設備（CPU/CUDA）
        device = "cpu"
        compute_type = "int8"
        try:
            import torch
            if torch.cuda.is_available():
                device = "cuda"
                compute_type = "int8_float16"
        except ImportError:
            pass
        
        # 執行 Whisper 模型
        for model_name in models:
            try:
                start_time = time.time()
                model = WhisperModel(model_name, device=device, compute_type=compute_type)
                
                # 使用臨時文件進行轉錄
                segments, info = model.transcribe(tmp_path, beam_size=5, language="zh")
                whisper_result = ''.join([seg.text for seg in segments])
                
                elapsed_time = time.time() - start_time
                model_short_name = model_name.split('/')[-1].replace('faster-whisper-', '')
                
                whisper_results.append({
                    "model": model_short_name,
                    "text": whisper_result,
                    "time": round(elapsed_time, 2)
                })
                
                logging.info(f"[Whisper-{model_short_name}] {device.upper()}推論時間: {elapsed_time:.2f} 秒，結果: {whisper_result}")
            except Exception as e:
                error_msg = f"Whisper模型 {model_name} 執行失敗: {e}"
                logging.error(error_msg)
                whisper_results.append({
                    "model": model_name.split('/')[-1],
                    "text": f"[錯誤] {e}",
                    "time": 0
                })
        
        # 處理完成後刪除臨時文件
        try:
            os.unlink(tmp_path)
        except:
            pass
        
        # 合併最佳結果（如果有多個模型結果）
        merged_result = None
        if whisper_results and google_result and google_result != "無法辨識":
            main_whisper = whisper_results[0]["text"]
            
            import difflib
            seq = difflib.SequenceMatcher(None, google_result, main_whisper)
            ratio = seq.ratio()
            
            logging.info(f"[合併分析] Google/Whisper 相似度: {ratio:.2f}")
            
            if ratio > 0.85:
                merged_result = google_result if len(google_result) >= len(main_whisper) else main_whisper
        
        # 返回結果
        return jsonify({
            "google": google_result,
            "whisper": whisper_results,
            "merged": merged_result
        })
    
    except Exception as e:
        logging.error(f"處理音頻時發生例外: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## 使用說明

1. 將上方HTML代碼保存為`templates/index.html`
2. 將Flask代碼保存為`app.py`
3. 確保已安裝所有依賴：
   ```
   pip install flask numpy soundfile speech_recognition faster-whisper noisereduce torch
   ```
4. 啟動Flask服務器：
   ```
   python app.py
   ```
5. 用瀏覽器訪問 http://127.0.0.1:5000/

這個解決方案完整實現了您的需求：純HTML5網頁錄音，發送到後端處理，然後顯示結果。如果您需要進一步優化或調整某些功能，可以根據需要修改代碼。



---

**来源**: [Perplexity AI](https://www.perplexity.ai/search/jian-cha-cheng-shi-ma-hao-xian-CkOJXt9iReqGDm05t7jfTg)
