# GyanSetu Educational Mobile Application

**GyanSetu** is a gamified, offline-first educational mobile application developed for students of Classes 1–10 in rural schools. Designed to bridge the digital learning gap, it empowers students with interactive mini-games mapped to their syllabus across **Maths**, **Science**, **English**, and **General Knowledge**.

---

## 🌟 Key Features

1. **Offline-First & Lightweight**
   - Operates completely offline with zero internet dependency using local SQLite storage (`gyansetu.db`).
2. **Curriculum-Aligned Gamification**
   - Classes 1–10 curriculum breakdown mapped to interactive games (Knight vs Dragon, Monkey River Crossing, Science Flashcards, English Vocabulary Master).
3. **Engaging Game Engines**
   - **Knight vs Dragon**: Real-time math combat with difficulty levels (Easy, Medium, Hard), timed auto-attacks, and health tracking.
   - **Monkey River Crossing**: Step-by-step problem-solving stepping stone puzzle.
   - **GK Trivia Quiz**: Local science & general knowledge trivia cards with educational facts.
   - **English Master**: Spoken pronunciation audio and vocabulary matching.
4. **Gamification & Rewards Layer**
   - In-app currency (**Coins**), Level progression, unlocked Badges & Trophies, Daily Reward Tasks, and Cosmetics Store.
5. **Parent & Teacher Progress Board**
   - Comprehensive metrics showing games played, score accuracy, and subject breakdown alongside rural student leaderboards.

---

## 🛠️ Architecture & Tech Stack

- **Frontend Framework**: Kivy (Python cross-platform UI engine)
- **Backend & State**: Python 3.12
- **Database**: SQLite (`gyansetu.db`) for local on-device persistence
- **Audio & Speech**: `pyttsx3` text-to-speech fallback integration

---

## 🚀 How to Run locally

1. Install Python dependencies:
   ```bash
   pip install kivy
   ```
2. Run the application:
   ```bash
   python Main.py
   ```