# 🎓 GyanSetu - Digital Learning Platform for Rural Schools

[![Theme](https://img.shields.io/badge/Theme-Smart%20Education-brightgreen.svg)]()
[![Problem Statement](https://img.shields.io/badge/PS%20ID-25019-blue.svg)]()
[![Category](https://img.shields.io/badge/Category-Software-orange.svg)]()
[![Offline First](https://img.shields.io/badge/Offline--First-100%25-success.svg)]()
[![Target Audience](https://img.shields.io/badge/Classes-1%20to%2010-purple.svg)]()

> **Team Name:** Terminal Velocity  
> **Problem Statement Title:** Digital Learning Platform for Rural Schools/Students  
> **Focus:** Equal learning access, girls' education retention, rote-learning reduction, offline playability.

---

## 📌 Overview

**GyanSetu** is a gamified, offline-first educational mobile application designed to deliver quality education in Maths, Science, English, and General Knowledge to students of **Classes 1–10** in rural areas. 

Instead of passive reading or rote memorization, learning takes place through engaging, curriculum-aligned mini-games that run seamlessly on low-end devices without requiring internet connectivity.

---

## 🎯 Challenges Addressed in Rural Education

1. **Lack of Internet Access:** Fully functional on-device offline operations after initial installation.
2. **Low-Spec Hardware:** Lightweight Python/Kivy architecture optimized for low resource utilization.
3. **Rote Learning Culture:** Problem-solving game mechanics that encourage critical thinking over memorization.
4. **Student Engagement & Motivation:** Coin rewards, badges, level progress, cosmetics store, and leaderboards.
5. **Teacher/Parent Visibility:** Dedicated **Progress Board** aggregating learning history, accuracy rates, and time spent.
6. **Inclusivity:** Multi-language support (English, Punjabi, Hindi) empowering rural students and girls at risk of school dropout.

---

## ✨ Key Features & Game Modules

### 1. ⚔️ Knight vs Dragon (Arithmetic Battle Engine)
- **Mechanics:** Fast-paced math arithmetic combat (+, −, ×, ÷).
- **Time Pressure:** The dragon automatically strikes the hero every few seconds, compelling speed + accuracy.
- **Difficulty Modes:** Easy (single digits), Medium (double digits), Hard (multi-operator & time compression).
- **Health System:** Real-time health bars for Hero and Dragon, awarding bonus coins upon victory.

### 2. 🐒 Monkey River Crossing (Problem Solving Puzzle)
- **Mechanics:** Help a monkey hop across river stepping stones by solving sequence and geometry equations.
- **Critical Thinking:** Reinforces multi-step logical reasoning and pattern recognition.

### 3. 🧠 GK Quiz & Science Trivia
- **Mechanics:** Interactive flashcard quiz covering environmental science, Indian heritage, geography, and agriculture.
- **Educational Feedback:** Instant explanations provided after every question.

### 4. 🔤 English Vocab Master & Audio Pronunciation
- **Mechanics:** Matching vocabulary definitions, synonyms, and parts of speech.
- **Text-to-Speech (TTS):** Audio button allowing students to hear native English pronunciation.

---

## 🎮 Gamification & Analytics Layer

| Feature | Description |
|---------|-------------|
| 🪙 **Coins & Level Progression** | Earn coins for completing games and leveling up your profile. |
| 🏅 **Badges & Gallery** | Showcase unlocked trophies, milestones, and accomplishment medals. |
| 🎁 **Daily Reward Tasks** | Daily incentive tasks (e.g., "Complete 1 Math Game", "Score 50 in GK"). |
| 🛍️ **Cosmetic Store** | Spend earned coins on custom profile titles, avatars, and app themes. |
| 📊 **Progress Board** | Aggregated performance metrics for parents and teachers to track student growth. |
| 🏆 **Offline Leaderboard** | Local & regional leaderboard ranking student achievements against peers. |

---

## 📚 Curriculum Structure

GyanSetu includes dynamic curriculum mapping across **Classes 1 through 10**:

```
Class (1–10)
 └── Subject (Maths / Science / English / GK)
        └── Chapter (e.g., Ch 1: Number Line, Ch 2: Photosynthesis, Ch 3: Vocabulary)
               └── Interactive Game Engine (Knight vs Dragon / River Hop / Quiz / Vocab)
```

---

## 🏗️ Architecture & Tech Stack

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                   │
│          Kivy Responsive UI Screens (gyansetu.kv)       │
└────────────────────────────┬────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────┐
│                    Application Layer                    │
│    Python Core Game Engines, Randomization & Logic      │
│            Text-to-Speech (pyttsx3 / Fallback)           │
└────────────────────────────┬────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────┐
│                       Data Layer                        │
│             SQLite Local Database (gyansetu.db)         │
│     Stores: User Profile, Progress, Daily Tasks, Store  │
└─────────────────────────────────────────────────────────┘
```

- **Core Language:** Python 3.12
- **UI Framework:** Kivy 2.3.1 (Cross-platform GUI engine)
- **Database:** SQLite (`database.py` - zero external database setup needed)
- **Asset Interop:** Canvas vector layouts + custom iconography (`logos/`)

---

## 📂 Project Directory Structure

```
GYANSETU-app/
├── Main.py                 # Application entry point & ScreenManager logic
├── gyansetu.kv             # Kivy markup stylesheet & responsive layouts
├── database.py             # SQLite database layer & persistence helpers
├── curriculum.py           # Class 1-10 curriculum mapping & data engine
├── gyansetu.db             # Local SQLite database instance (auto-generated)
├── README.md               # Project documentation
├── logos/                  # UI button icons & graphics
└── ICON/                   # Application assets & logos
```

---

## ⚡ Quick Start Guide

### Prerequisites
- Python 3.8 or higher installed on your system.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Anany1014/GYANSETU-app.git
   cd GYANSETU-app
   ```

2. Install dependencies:
   ```bash
   pip install kivy
   ```

3. Launch the application:
   ```bash
   python Main.py
   ```

---

## 🗺️ Roadmap & Future Enhancements

- 📡 **Offline Peer-to-Peer Distribution:** Integration with native Android Quick Share via PyJNIus bridge.
- ☁️ **Cloud Sync:** Optional background synchronization when internet connectivity becomes available.
- 📱 **Native Mobile Migration:** Long-term migration plan to Kotlin/Java for smaller APK footprint on ultra low-spec hardware.
- 🌐 **Expanded Localization:** Additional regional language dialects for rural communities.

---

## 📄 License & Acknowledgments

Developed by **Team Terminal Velocity** for the Smart Education hackathon initiative. Graphics and icons sourced from open assets. Built with love for accessible digital education! ❤️