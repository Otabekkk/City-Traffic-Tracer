# 🚦 Smart Traffic Simulator for Bishkek

A platform for testing traffic light configurations
using real microscopic traffic simulation (SUMO).

![Demo](screenshots/ui.png)

## 🚀 Problem
Traffic light changes are usually applied directly in real cities,
which is risky and expensive.

## 💡 Solution
We provide a platform where traffic engineers can:
- configure traffic light phases
- simulate traffic behavior
- compare metrics before deployment

## 🔍 Before / After
![Comparison](screenshots/compare.png)

Queue length and waiting time can be reduced by **up to 40%**.

## ▶ Simulation Playback
![Playback](screenshots/playback.png)

Playback helps understand *why* a configuration works better.

## 🧠 Architecture
![Architecture](screenshots/architecture.png)

SUMO runs inside Docker, backend exposes an API, frontend is optional.

## 🏙 Focus
The project is focused on **Bishkek**, but can be adapted to any city.

## 👥 Team
- Backend / Simulation
- Frontend / UX
- Pitch / Design
