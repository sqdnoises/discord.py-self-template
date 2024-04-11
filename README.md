# discord.py bot template
a discord.py bot template that I use for my bots.

you're free to use this template if you like.

## Setup
Need **Python 3.10+** for this bot template.\
**NOTE:** In this section, `python3` would be `python` or just `py` on **Windows**.

First of all, git clone this repository
```bash
git clone https://github.com/sqdnoises/discord.py-bot-template.git
```

Then remove `.git` (optional, but highly recommended)
```bash
rm -rf .git # Linux/MacOS
```

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

### install the bot
```bash
pip install -e .
```

### setup the database
```bash
prisma db push
```

### running
```bash
source .venv/bin/activate # (optional) For Linux/MacOS
run-bot
```