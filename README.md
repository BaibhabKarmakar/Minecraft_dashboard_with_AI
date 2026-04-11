# ⛏️ Minecraft Wrapped

> *Your survival story, told in data.*

A **Minecraft stats dashboard** built with Python — upload your world's stats JSON and get beautiful interactive charts, a personalized playstyle profile, and AI-powered analysis of your gameplay. Think Spotify Wrapped, but for Minecraft.

![Python](https://img.shields.io/badge/Python-3.8+-5dff8a?style=flat-square&logo=python&logoColor=white&labelColor=080c10)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-5dff8a?style=flat-square&logo=streamlit&logoColor=white&labelColor=080c10)
![Plotly](https://img.shields.io/badge/Plotly-5.x-5dff8a?style=flat-square&logo=plotly&logoColor=white&labelColor=080c10)
![Groq](https://img.shields.io/badge/Groq_AI-Free-5dff8a?style=flat-square&logoColor=white&labelColor=080c10)

---

## 📸 What It Looks Like

The dashboard has 7 sections:

| Section | What You See |
|---|---|
| 📊 Overview | Playtime, blocks mined, kills, deaths, jumps, distance |
| 🎭 Playstyle Profile | Radar chart + your playstyle label (Miner / Fighter / Explorer / Chaos Agent) |
| ⛏️ Mining Report | Top 15 blocks mined, ore breakdown with color coding |
| ⚔️ Combat Report | Mobs killed, cause of death pie chart, damage ratio, trauma score |
| 🗺️ Movement Report | Distance by type, real-world comparisons |
| 🔨 Crafting Report | Top items crafted |
| 🤖 AI Analysis | Roast, Story, Coach, and Death Prediction powered by Groq AI |

---

## 🤖 AI Features

Connect a free **Groq API key** to unlock four AI-powered tabs:

- **🔥 Roast Me** — A savage, funny roast of your gameplay using your actual stats
- **📖 My Story** — A dramatic fantasy narrative of your session
- **🧠 Coach** — Real tactical advice for your next session based on your patterns
- **🔮 Predict My Doom** — Predicts what will probably kill you next time and why

> Groq AI is completely free. Get your key at [console.groq.com](https://console.groq.com)

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/BaibhabKarmakar/minecraft-wrapped.git
cd minecraft-wrapped
```

### 2. Install dependencies

```bash
pip install streamlit plotly pandas groq
```

### 3. Find your Minecraft stats file

```
Windows:
C:\Users\YourName\AppData\Roaming\.minecraft\saves\YourWorldName\stats\

Mac:
~/Library/Application Support/minecraft/saves/YourWorldName/stats/

Linux:
~/.minecraft/saves/YourWorldName/stats/
```

> ⚠️ Always exit your world with **Save and Quit to Title** before uploading — this ensures the stats file is properly saved.

### 4. Run the app

```bash
streamlit run app.py
```

### 5. Upload your stats file and explore!

---

## 📁 Project Structure

```
minecraft-wrapped/
├── app.py          # Main Streamlit application
├── README.md       # You are here
└── requirements.txt
```

---

## 📦 Requirements

Create a `requirements.txt` with:

```
streamlit
plotly
pandas
groq
```

---

## 🧠 How It Works

Minecraft saves your gameplay stats as a **JSON file** automatically every session. The file tracks everything — every block mined, every mob killed, every death, every jump, every meter walked.

This app reads that file, processes it with **Pandas**, visualizes it with **Plotly**, and wraps it in a **Streamlit** web interface. The AI features send a summary of your stats to **Groq's LLaMA 3.3 70B model** which generates personalized responses.

No external APIs needed for the core dashboard. The AI features are optional and use Groq's free tier.

---

## 💡 Things That Might Surprise You In Your Stats

- `fly_one_cm` tracks **all airborne movement** — not just elytra. Sprint jumping counts.
- `damage_dealt` and `damage_taken` are in **half-hearts** (so 20 = 10 hearts)
- `play_time` is in **game ticks** — divide by 20 for seconds, 72000 for hours
- Stats only update when you **properly exit** the world — not on Alt+F4

---

## 🗺️ Roadmap

- [ ] Multi-world comparison (compare across different saves)
- [ ] Session-by-session tracking over time
- [ ] Shareable stats card (image export)
- [ ] Multiplayer server stats support
- [ ] Mobile-friendly layout

---

## 🛠️ Built With

- [Streamlit](https://streamlit.io) — Web app framework for Python
- [Plotly](https://plotly.com) — Interactive charts
- [Pandas](https://pandas.pydata.org) — Data processing
- [Groq](https://groq.com) — Free, fast AI inference (LLaMA 3.3 70B)

---

## 👤 Author

Built by a Data Science student who started this project to avoid doom scrolling Instagram reels about passive income. 
Turns out playing Minecraft is legitimate data collection. Mom was wrong.

---

## 📄 License

MIT License — use it, fork it, build on it, share it.

---

## ⭐ If you found this useful

Give it a star on GitHub and share your stats with the Minecraft community!

Post your dashboard screenshot on Reddit at [r/Minecraft](https://reddit.com/r/Minecraft) — the community loves this kind of thing.
