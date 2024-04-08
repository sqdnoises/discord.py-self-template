# discord.py bot template

## Setup
Need **Python 3.10+** for this bot template.\
**NOTE:** In this section, `python3` would be `python` or just `py` on **Windows**.

`./`**`.env`** template
```python
TOKEN="Bot token"
```

### venv (optional) (For Linux/MacOS)
On `bash`:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### venv (optional) (For Windows)
On `powershell`:
```powershell
py -m venv venv
& .\venv\Scripts\activate
```

### pip requirements
```bash
pip install -r requirements.txt
```

### running
```bash
source .venv/bin/activate # For Linux/MacOS
cd src
prisma db push
python3 bot.py
```