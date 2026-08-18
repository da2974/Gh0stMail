# Gh0stMail — Temporary Email Desktop Client

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![PySide6](https://img.shields.io/badge/PySide6-6.6%2B-41CD52?logo=qt)
![License](https://img.shields.io/badge/license-MIT-green)

A lightweight Python desktop application for creating temporary email addresses, receiving messages and automatically detecting verification codes.

## 📸 Screenshots

<img width="1918" height="1078" alt="Screenshot 2026-08-17 024334" src="https://github.com/user-attachments/assets/f5662978-0a63-41bb-ae45-fc7df134198c" />

## ✨ Features

- Address creation with **3 providers** (mail.tm, Guerrilla Mail, 1secMail), with automatic
  provider switching if one fails ("Automatic" mode)
- **Provider selector in Settings** → General → "Mail provider" to choose based on your needs
- Inbox with search/filter by sender or subject
- Automatic verification code detection, with a customizable
  pattern (regular expression) from Settings
- Local message history per address, independent of the
  live inbox
- Desktop notifications that can be toggled on/off + optional sound
- System tray icon; the app can keep running in the background
  when the window is closed (configurable)
- Light or dark theme
- Spanish or English language, selectable from Settings
- Export an address (and its password, if applicable) to a text file
- Configurable auto-refresh and wait intervals
- **Encryption at rest** for the accounts file (Fernet/AES)
- **Estimated expiration notice** in the address list

## Email providers

| Provider | Best for | Duration |
|-----------|------------|----------|
| **mail.tm** (recommended default) | **Use for days/weeks**: 2FA, password recovery, future notifications, anything that needs to arrive tomorrow or next week | Days / weeks (depending on use) |
| **Guerrilla Mail** | **Code NOW**: quick sign-up, immediate verification, "I need the code right now" | ~60 min if unused (renews on request) |
| **1secMail** | **Backup** if the two above fail or are slow | Indefinite (not published) |

## 🌐 Languages

The application is available in **Spanish** and **English**. You can change
the language at any time from Settings → General → Language; the change
applies instantly, without restarting the application.

## 🚀 Installation

```bash
git clone https://github.com/da2974/Gh0stMail.git
cd Gh0stMail
pip install -r requirements.txt
```

> On Linux, some distributions may need `pip` installed separately, e.g. `sudo apt install python3-pip` (Debian/Ubuntu).
> On macOS, if Python isn't installed, you can get it via [Homebrew](https://brew.sh): `brew install python`.

## ▶️ Usage

**Windows:**
```bash
pythonw main.py
```

**Linux / macOS:**
```bash
python3 main.py
```


## 📁 Project structure

| File/Folder | Description |
|---|---|
| `main.py` | Main window and interface logic |
| `dialogo_ajustes.py` | Settings modal window |
| `gestor_proveedores.py` | Provider selection and automatic failover (3 providers) |
| `proveedores/` | Implementations for mail.tm, Guerrilla Mail and 1secMail |
| `tareas.py` | Network operations in threads (QThread) |
| `configuracion.py` / `almacenamiento.py` | JSON persistence (accounts encrypted with Fernet) |
| `notificaciones.py` | Desktop notifications via system tray (+ sound) |
| `utilidades.py` | Code detection, HTML→text, date formatting, expiration |
| `idiomas.py` | Interface text in Spanish and English |
| `tema_claro.qss` / `tema_oscuro.qss` | Stylesheets |

## 🤝 Contributing

Contributions are welcome. If you'd like to propose a change:

1. Fork the repository
2. Create a branch for your change (`git checkout -b my-improvement`)
3. Commit your changes
4. Open a Pull Request

## ☕ Support the project

If you find it useful, you can buy me a coffee:

[![PayPal](https://img.shields.io/badge/PayPal-Donate-00457C?logo=paypal)](https://paypal.me/Davidnt20)

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
