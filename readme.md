# 📊 Binance Account Balance Viewer (Python)

A simple and secure Python tool that connects to your Binance account and fetches all available crypto balances. It uses the official Binance API, includes logging, and safely handles errors.

---

## 🚀 Features
- Fetches real-time Binance balances  
- Filters out assets with zero balance  
- Logs API status and errors  
- Uses separate `keys.py` for secure key storage  
- Clean and lightweight code  

---

## 📂 Project Structure
project/
│── binance_balance.py
│── keys.py

yaml
Copy code

---

## 🔧 Installation
### 1. Install dependencies
```bash
pip install python-binance
🔐 Add your API keys
Create keys.py:

python
Copy code
user_keys = {
    "kenu": ("YOUR_API_KEY", "YOUR_API_SECRET")
}
▶️ Usage
bash
Copy code
python binance_balance.py
You will see output like:

yaml
Copy code
Testing API Key: xxxxx
Balances: {'BTC': 0.0021, 'USDT': 53.40}
⚠️ Security Notes
Never share your Binance API keys

Use Read Only permissions

Keep keys.py private

📜 License
Free to use. Created by Kenijan.

yaml
Copy code

---

If you want, I can also create:

✅ A professional **banner image** (same style as your previous project)  
✅ A **full installer script**  
✅ A **GUI version** (Tkinter / PyQt)  

Just tell me!