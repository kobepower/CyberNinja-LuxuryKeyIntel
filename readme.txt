# 🔑 CyberNinja Luxury Key Intelligence

Professional BMW / Mercedes-Benz / Audi key programming reference tool for automotive locksmiths.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey.svg)

---

## 🎯 What It Does

Instantly tells you everything you need to know before accepting a luxury vehicle key job:

- **Platform / Chassis** — F30, G20, G05, etc.
- **Immobilizer System** — CAS4+, FEM, BDC
- **Key Type & Blade** — What to order, what to cut
- **Programming Method** — OBD vs Bench, based on key status
- **Module Removal** — Do you need to pull the dash?
- **AKL Support** — Can you do all keys lost?
- **Risk Level** — Green/Yellow/Red job assessment
- **⚠️ EEPROM Backup Warnings** — Critical info that saves you from bricking modules

---

## 🖥️ Screenshot

```
┌─────────────────────────────────────────────────────────────────┐
│  🔑 CYBERNINJA LUXURY KEY INTELLIGENCE                          │
│     BMW • MERCEDES • AUDI                                       │
├──────────────────┬──────────────────────────────────────────────┤
│  VEHICLE INPUT   │  VEHICLE SECURITY OVERVIEW                   │
│                  │                                              │
│  Make: BMW       │  Platform: G05                               │
│  Model: X5       │  Immobilizer: BDC                            │
│  Year: 2020      │  Key Blade: HU100R                           │
│  Key Status: AKL │  Programming: Bench (BDC removal)            │
│                  │  Module Removal: Yes                         │
│  VIN: [______]   │  Risk Level: HIGH                            │
│                  │  EEPROM: 95256 (256kb)                       │
│                  │  ⚠️ BACKUP WARNING: CRITICAL - 95256 backup  │
│                  │     MANDATORY before any work!               │
└──────────────────┴──────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Requirements
- Python 3.8+
- CustomTkinter
- Pillow

### Install & Run

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/CyberNinja-LuxuryKeyIntel.git
cd CyberNinja-LuxuryKeyIntel

# Install dependencies (auto-installs on first run, or manually)
pip install customtkinter pillow

# Run
python CyberNinja_LuxuryKeyIntel.py
```

---

## 📁 Project Structure

```
CyberNinja-LuxuryKeyIntel/
├── CyberNinja_LuxuryKeyIntel.py   # Main application
├── data/
│   ├── bmw.json                    # BMW database (12+ models)
│   ├── benz.json                   # Mercedes-Benz (coming soon)
│   └── audi.json                   # Audi (coming soon)
├── Key_Images/                     # Your reference photos
└── README.md
```

---

## 🔧 Features

| Feature | Description |
|---------|-------------|
| **VIN Decoder** | Auto-detects make from VIN, validates format |
| **Key Status Logic** | Results change based on Has Key / 1 Key / AKL |
| **EEPROM Warnings** | Shows chip type (95128/95256) and backup procedures |
| **Risk Assessment** | Color-coded job risk (Low/Medium/High/Very High) |
| **Image Library** | Attach module/key reference photos per vehicle |
| **JSON Database** | Easy to update, expand, and customize |

---

## 📊 Supported Vehicles

### BMW (Full Support)
| Model | Years | System |
|-------|-------|--------|
| 1 Series | 2012-2026 | FEM / BDC |
| 2 Series | 2014-2026 | FEM / BDC |
| 3 Series | 2012-2026 | CAS4+ / BDC |
| 4 Series | 2014-2026 | FEM / BDC |
| 5 Series | 2011-2026 | CAS4+ / BDC |
| 7 Series | 2012-2026 | CAS4+ / BDC |
| X1 | 2012-2026 | CAS4 / FEM / BDC |
| X3 | 2011-2026 | CAS4+ / BDC |
| X5 | 2014-2026 | CAS4+ / BDC |
| X6 | 2015-2026 | CAS4+ / BDC |
| Z4 | 2019-2026 | BDC |
| i4 | 2022-2026 | BDC |
| iX | 2022-2026 | BDC+ |

### Mercedes-Benz — Coming Soon
### Audi — Coming Soon

---

## ⚠️ EEPROM Backup Guide

**DO NOT SKIP THIS** — This is why locksmiths brick modules.

| System | Chip | Backup Tool |
|--------|------|-------------|
| FEM | 95128 (128kb) | VVDI Prog, Orange5, Multi-Prog |
| BDC | 95256 (256kb) | VVDI Prog, Orange5, Multi-Prog |
| CAS4+ | Internal | VVDI Prog CAS4+ adapter |

**Correct workflow:**
1. OBD backup coding data FIRST
2. Remove module
3. Read EEPROM chip (95128 or 95256)
4. **SAVE THAT FILE** — this is your recovery
5. Do your key programming
6. If anything fails → write original EEPROM back

---

## 🤝 Contributing

Got data for Mercedes or Audi? PRs welcome!

JSON format:
```json
{
  "BMW": {
    "Model Name": {
      "2020-2026": {
        "platform": "G05",
        "immobilizer": "BDC",
        "key_type": "BMW G-Series Smart Key",
        "key_blade": "HU100R",
        "programming": {
          "has_key": "OBD",
          "one_key": "OBD",
          "akl": "Bench (BDC removal)"
        },
        "module_removal": {
          "has_key": false,
          "one_key": false,
          "akl": true
        },
        "akl_supported": "Limited",
        "risk_level": "High",
        "notes": "Your notes here",
        "eeprom_info": {
          "backup_required": true,
          "chip_type": "95256 (256kb)",
          "backup_method": "OBD coding + 95256 EEPROM backup",
          "warning": "⚠️ CRITICAL: Backup mandatory!"
        }
      }
    }
  }
}
```

---

## 📜 License

MIT License — Use it, modify it, make money with it. Just don't blame me if you brick a BDC. 😉

---

## 👨‍💻 Author

**Kobe's Keys** — Mobile Locksmith, GTA  
Built with the CyberNinja toolkit 🥷

---

## ⭐ Support

If this tool saved you from a bricked module or helped you quote jobs faster, drop a ⭐ on the repo!