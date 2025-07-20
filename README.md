Sure Megh! Below is your complete, **beautifully formatted and simple** `README.md` file content. You can **copy-paste** it directly into your project as `README.md`.

---

```markdown
# 🏏 IPL Flask API

This is a simple and powerful **Flask-based REST API** that gives detailed stats about the Indian Premier League (IPL) from 2008 to 2022. It uses **Python, Pandas, and Flask** to serve IPL data like team records, player stats, points tables, and much more.

---

## 🔥 Key Features

- Get all IPL teams
- Compare any two teams head-to-head
- See which captains played the most finals
- Player-wise stats season-by-season
- Purple Cap and Orange Cap winners
- Points table by season
- Highest batting partnerships
- Fully working REST API ready to deploy!

---

## 📁 Project Structure

```

ipl\_flask\_api/
├── data/
│   ├── IPL\_Matches\_2008\_2022.csv
│   ├── IPL\_Ball\_by\_Ball\_2008\_2022.csv
│   └── ipl\_deliveries.csv
├── backend.py            # Main Flask app and API routes
├── ipl.py                # All IPL data functions using Pandas
├── Testing.ipynb         # Used for testing and experimenting
├── requirements.txt      # List of required Python libraries
├── Procfile              # For deployment (e.g. Render.com)
└── README.md             # This file

````

---

## ⚙️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/MeghOffical/ipl_flask_api.git
   cd ipl_flask_api
````

2. **Create a virtual environment (optional but recommended)**

   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate  # Mac/Linux
   ```

3. **Install all requirements**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask app**

   ```bash
   set FLASK_APP=backend.py    # Windows
   export FLASK_APP=backend.py # Mac/Linux
   flask run
   ```

5. **Visit in browser:**
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔗 API Endpoints

| URL                                        | Description                      |
| ------------------------------------------ | -------------------------------- |
| `/`                                        | Home route / Welcome message     |
| `/api/teams`                               | List of all IPL teams            |
| `/api/teamVteam?team1=CSK&team2=MI`        | Compare two teams head-to-head   |
| `/api/team_winning_record`                 | Overall win % of all teams       |
| `/api/most_final_played`                   | Captains with most finals played |
| `/api/name_of_batsmens`                    | List of all batsmen              |
| `/api/name_of_bowlers`                     | List of all bowlers              |
| `/api/batsman_details?batsman=Virat Kohli` | Batsman’s season stats           |
| `/api/bowler_details?bowler=J Bumrah`      | Bowler’s season stats            |
| `/api/purple_cap`                          | Top wicket takers per season     |
| `/api/orange_cap`                          | Top run scorers per season       |
| `/api/point_table?season=2020`             | Points table for a given season  |
| `/api/Player_Of_Match`                     | Most Player of the Match winners |
| `/api/batting_pair`                        | Top batting partnerships         |


---


## ☁️ Deploy on Render (Free Hosting)

1. Push your project to GitHub
2. Go to [https://render.com](https://render.com)
3. Create a new Web Service and connect your repo
4. Set **Build Command**: `pip install -r requirements.txt`
5. Set **Start Command**: `gunicorn backend:app`
6. Click Deploy 🎉

---

## 💡 Future Improvements

* Add player vs player comparisons
* Add live match prediction using ML
* Add frontend with charts using React.js or Streamlit
* Add rate limiting and API keys for public use

---


## 📝 License

This project is open source — use it freely.

---

*Built with ❤️ using Python, Pandas, and Flask.*

---

## 🙋 About Me

Hi, I'm **Megh Bavarva**, the creator of this project!
This was built as a personal project to learn API design, Flask, and Pandas while exploring IPL data.
Feel free to fork it, star it, or reach out for collaboration!

🔗 GitHub: [@MeghOffical](https://github.com/MeghOffical)
