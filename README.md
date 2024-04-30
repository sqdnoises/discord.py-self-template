<div align="center">

# discord.py bot template

[![](https://img.shields.io/badge/Python-3.10+-FFD43B?labelColor=306998&style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![](https://img.shields.io/badge/License-MIT-009900?style=for-the-badge&labelColor=111111)](LICENSE)

a discord.py bot template that I use for my bots.\
you're free to use this template if you like.

## License
You must have received a copy of the [LICENSE](LICENSE) file with this source code.\
This source code is licensed under the **MIT License**.

</div>

## Setup
Need **Python 3.10+** for this bot template.\
**NOTE:** In this section, `python3` would be `python` or just `py` on **Windows**.

First of all, git clone this repository
```bash
git clone git@github.com:sqdnoises/discord.py-bot-template
```

Then remove `.git` (optional, but highly recommended)
```bash
rm -rf .git # Linux/MacOS
```

`./.env` template
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

### install requirements
```bash
pip install -r requirements.txt
```

### setup the database
```bash
cd src
prisma db push
```

### running
```bash
source .venv/bin/activate # (optional) For Linux/MacOS
cd src
python3 bot.py # py or python bot.py on Windows
```
