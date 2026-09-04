import random
import time
import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, NoTransition
from kivy.properties import BooleanProperty, StringProperty, NumericProperty, ListProperty, ObjectProperty
from kivy.clock import Clock
from kivy.lang import Builder

import database
import curriculum

# Optional pyttsx3 import for TTS with fallback
try:
    import pyttsx3
    tts_engine = pyttsx3.init()
except Exception:
    tts_engine = None

def speak_text(text):
    if tts_engine:
        try:
            tts_engine.say(text)
            tts_engine.runAndWait()
        except Exception:
            pass

class Manager(ScreenManager):
    pass

class CreateProfilePage(Screen):
    user_name = StringProperty("")
    selected_class = NumericProperty(6)

    def save_profile(self):
        name = self.user_name.strip() if self.user_name.strip() else "Scholar"
        user = database.get_or_create_user(name=name, class_level=int(self.selected_class))
        database.update_user_profile(user["uid"], name, int(self.selected_class))
        
        # Update App state
        app = App.get_running_app()
        app.load_user_data()
        self.manager.current = "home"
        self.manager.transition.direction = "left"

class HomePage(Screen):
    user_name = StringProperty("Scholar")
    user_level = NumericProperty(1)
    user_coins = NumericProperty(100)
    user_title = StringProperty("Beginner Scholar")
    user_avatar = StringProperty("logos/profile.png")

    def on_enter(self):
        app = App.get_running_app()
        app.load_user_data()
        self.user_name = app.user_data.get("name", "Scholar")
        self.user_level = app.user_data.get("level", 1)
        self.user_coins = app.user_data.get("coins", 100)
        self.user_title = app.user_data.get("title", "Beginner Scholar")
        self.user_avatar = app.user_data.get("avatar", "logos/profile.png")

class ProfilePage(Screen):
    user_name = StringProperty("")
    user_uid = StringProperty("")
    user_level = NumericProperty(1)
    user_coins = NumericProperty(0)
    user_title = StringProperty("")
    user_class = NumericProperty(6)
    achievements_count = NumericProperty(0)

    def on_enter(self):
        app = App.get_running_app()
        app.load_user_data()
        u = app.user_data
        self.user_name = u.get("name", "Scholar")
        self.user_uid = u.get("uid", "GS000001")
        self.user_level = u.get("level", 1)
        self.user_coins = u.get("coins", 0)
        self.user_title = u.get("title", "Beginner Scholar")
        self.user_class = u.get("class_level", 6)
        
        achs = database.get_user_achievements(u["uid"])
        self.achievements_count = len(achs)

    def save_changes(self, new_name, new_class):
        app = App.get_running_app()
        uid = app.user_data["uid"]
        cls = int(new_class) if str(new_class).isdigit() else self.user_class
        nm = new_name.strip() if new_name.strip() else self.user_name
        database.update_user_profile(uid, nm, cls)
        app.load_user_data()
        self.on_enter()

class BasicGamesPage(Screen):
    user_coins = NumericProperty(0)

    def on_enter(self):
        app = App.get_running_app()
        self.user_coins = app.user_data.get("coins", 0)

    def launch_game(self, game_name, difficulty):
        if game_name == "Basic_Math_Game_1":
            game_screen = self.manager.get_screen("Basic_Math_Game_1")
            game_screen.difficulty = difficulty
            self.manager.current = "Basic_Math_Game_1"
            self.manager.transition.direction = "up"
        elif game_name == "Monkey_River_Game":
            game_screen = self.manager.get_screen("Monkey_River_Game")
            game_screen.difficulty = difficulty
            self.manager.current = "Monkey_River_Game"
            self.manager.transition.direction = "up"

class Basic_Math_Game_1(Screen):
    difficulty = StringProperty("Easy")
    points = NumericProperty(0)
    ques_text = StringProperty("0")
    ans_text = StringProperty("")
    status_msg = StringProperty("Answer correctly to strike the dragon!")
    
    hero_hp = NumericProperty(60)
    hero_max_hp = NumericProperty(60)
    dragon_hp = NumericProperty(40)
    dragon_max_hp = NumericProperty(40)
    
    inc_point = NumericProperty(10)
    total_ques = NumericProperty(0)
    correct_ques = NumericProperty(0)
    question_ans = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.attack_event = None

    def on_enter(self, *args):
        app = App.get_running_app()
        self.points = 0
        self.total_ques = 0
        self.correct_ques = 0
        self.ans_text = ""
        self.status_msg = "Answer math problems to defeat the dragon!"
        
        if self.difficulty == "Hard":
            self.hero_hp = 40
            self.hero_max_hp = 40
            self.dragon_hp = 60
            self.dragon_max_hp = 60
            self.inc_point = 25
            attack_interval = 2.5
        elif self.difficulty == "Medium":
            self.hero_hp = 50
            self.hero_max_hp = 50
            self.dragon_hp = 50
            self.dragon_max_hp = 50
            self.inc_point = 15
            attack_interval = 3.5
        else:
            self.hero_hp = 60
            self.hero_max_hp = 60
            self.dragon_hp = 40
            self.dragon_max_hp = 40
            self.inc_point = 10
            attack_interval = 5.0
            
        self.generate_question()
        # Schedule dragon auto-attack
        if self.attack_event:
            self.attack_event.cancel()
        self.attack_event = Clock.schedule_interval(self.dragon_auto_attack, attack_interval)

    def on_leave(self, *args):
        if self.attack_event:
            self.attack_event.cancel()
            self.attack_event = None

    def dragon_auto_attack(self, dt):
        if self.hero_hp > 0 and self.dragon_hp > 0:
            dmg = random.randint(4, 8)
            self.hero_hp = max(0, self.hero_hp - dmg)
            self.status_msg = f"Dragon strikes! Hero took {dmg} damage!"
            if self.hero_hp <= 0:
                self.end_game(won=False)

    def generate_question(self):
        op = random.choice(["+", "-", "*", "/"])
        if self.difficulty == "Easy":
            a, b = random.randint(1, 12), random.randint(1, 12)
        elif self.difficulty == "Medium":
            a, b = random.randint(10, 50), random.randint(2, 20)
        else:
            a, b = random.randint(20, 100), random.randint(5, 30)

        if op == "+":
            self.ques_text = f"{a} + {b}"
            self.question_ans = a + b
        elif op == "-":
            a, b = max(a, b), min(a, b)
            self.ques_text = f"{a} - {b}"
            self.question_ans = a - b
        elif op == "*":
            a, b = random.randint(2, 10), random.randint(2, 10)
            self.ques_text = f"{a} × {b}"
            self.question_ans = a * b
        elif op == "/":
            b = random.randint(2, 10)
            mult = random.randint(1, 10)
            a = b * mult
            self.ques_text = f"{a} ÷ {b}"
            self.question_ans = mult

    def keypad(self, val):
        if len(self.ans_text) < 6:
            self.ans_text += str(val)

    def uni_opera(self):
        if self.ans_text:
            if self.ans_text.startswith("-"):
                self.ans_text = self.ans_text[1:]
            else:
                self.ans_text = "-" + self.ans_text

    def delete(self):
        self.ans_text = self.ans_text[:-1]

    def enter(self):
        if not self.ans_text.strip():
            return
        try:
            val = float(self.ans_text)
            self.total_ques += 1
            if abs(val - self.question_ans) < 0.01:
                self.correct_ques += 1
                dmg = random.randint(10, 18)
                self.dragon_hp = max(0, self.dragon_hp - dmg)
                self.points += self.inc_point
                self.status_msg = f"CRITICAL HIT! Dealt {dmg} damage to Dragon!"
                if self.dragon_hp <= 0:
                    self.end_game(won=True)
                    return
            else:
                self.status_msg = f"Incorrect! Answer was {self.question_ans}"
        except Exception:
            self.status_msg = "Invalid input!"

        self.ans_text = ""
        self.generate_question()

    def end_game(self, won):
        if self.attack_event:
            self.attack_event.cancel()
            self.attack_event = None
            
        app = App.get_running_app()
        uid = app.user_data["uid"]
        earned_coins = database.save_game_progress(
            uid=uid,
            game_id="kvd_math",
            subject="Maths",
            class_num=app.user_data.get("class_level", 6),
            chapter="Arithmetic Combat",
            score=self.points,
            max_score=100
        )
        app.load_user_data()
        
        self.status_msg = f"GAME OVER! You {'WON' if won else 'LOST'}. Earned {earned_coins} coins!"
        Clock.schedule_once(lambda dt: self.return_to_menu(), 2.5)

    def return_to_menu(self):
        self.manager.current = "Basic_Games"
        self.manager.transition.direction = "down"

class MonkeyRiverGame(Screen):
    difficulty = StringProperty("Easy")
    score = NumericProperty(0)
    current_step = NumericProperty(0)
    question_text = StringProperty("Help Monkey step across the river!")
    stone_1 = StringProperty("1")
    stone_2 = StringProperty("2")
    stone_3 = StringProperty("3")
    stone_4 = StringProperty("4")
    correct_stone = NumericProperty(1)
    status_msg = StringProperty("Select the correct stepping stone!")

    def on_enter(self):
        self.score = 0
        self.current_step = 0
        self.generate_step()

    def generate_step(self):
        if self.current_step >= 5:
            self.end_game()
            return
            
        op = random.choice(["+", "-"])
        a, b = random.randint(1, 10), random.randint(1, 10)
        if op == "+":
            ans = a + b
            self.question_text = f"Step {self.current_step + 1}/5: {a} + {b} = ?"
        else:
            a, b = max(a, b), min(a, b)
            ans = a - b
            self.question_text = f"Step {self.current_step + 1}/5: {a} - {b} = ?"
            
        # Generate 4 choices
        choices = {ans}
        while len(choices) < 4:
            choices.add(ans + random.choice([-3, -2, -1, 1, 2, 3]))
        c_list = list(choices)
        random.shuffle(c_list)
        
        self.stone_1 = str(c_list[0])
        self.stone_2 = str(c_list[1])
        self.stone_3 = str(c_list[2])
        self.stone_4 = str(c_list[3])
        self.correct_stone = c_list.index(ans) + 1

    def select_stone(self, idx):
        if idx == self.correct_stone:
            self.score += 20
            self.current_step += 1
            self.status_msg = "Monkey hopped safely!"
            speak_text("Great job!")
            self.generate_step()
        else:
            self.status_msg = "Splash! Wrong stone, try again!"

    def end_game(self):
        app = App.get_running_app()
        uid = app.user_data["uid"]
        earned = database.save_game_progress(
            uid=uid,
            game_id="monkey_river",
            subject="Maths",
            class_num=app.user_data.get("class_level", 6),
            chapter="River Hop Puzzle",
            score=self.score,
            max_score=100
        )
        app.load_user_data()
        self.status_msg = f"River Crossed! Earned {earned} Coins!"
        Clock.schedule_once(lambda dt: self.exit_game(), 2.0)

    def exit_game(self):
        self.manager.current = "Basic_Games"
        self.manager.transition.direction = "down"

class LessonsPage(Screen):
    selected_class = NumericProperty(6)
    selected_subject = StringProperty("Maths")
    chapters_list = ListProperty([])
    user_coins = NumericProperty(0)

    def on_enter(self):
        app = App.get_running_app()
        self.user_coins = app.user_data.get("coins", 0)
        self.selected_class = app.user_data.get("class_level", 6)
        self.load_chapters()

    def select_class(self, class_num):
        self.selected_class = int(class_num)
        self.load_chapters()

    def select_subject(self, subject):
        self.selected_subject = subject
        self.load_chapters()

    def load_chapters(self):
        self.chapters_list = curriculum.get_chapters(self.selected_class, self.selected_subject)

    def start_chapter_game(self, game_type):
        if game_type == "kvd":
            g = self.manager.get_screen("Basic_Math_Game_1")
            g.difficulty = "Medium"
            self.manager.current = "Basic_Math_Game_1"
        elif game_type == "monkey":
            g = self.manager.get_screen("Monkey_River_Game")
            g.difficulty = "Medium"
            self.manager.current = "Monkey_River_Game"
        elif game_type == "gk_quiz":
            g = self.manager.get_screen("GK_Quiz_Game")
            self.manager.current = "GK_Quiz_Game"
        elif game_type == "english_vocab":
            g = self.manager.get_screen("English_Vocab_Game")
            self.manager.current = "English_Vocab_Game"
        self.manager.transition.direction = "left"

class GKQuizGame(Screen):
    question_title = StringProperty("General Knowledge Quiz")
    question_text = StringProperty("")
    option_a = StringProperty("")
    option_b = StringProperty("")
    option_c = StringProperty("")
    option_d = StringProperty("")
    correct_idx = NumericProperty(0)
    explanation = StringProperty("")
    score = NumericProperty(0)
    q_index = NumericProperty(0)

    questions = [
        {
            "q": "Which is the largest organ in the human body?",
            "opts": ["Heart", "Brain", "Skin", "Liver"],
            "ans": 2,
            "exp": "Skin is the largest organ of the human body!"
        },
        {
            "q": "What process do plants use to make food from sunlight?",
            "opts": ["Respiration", "Photosynthesis", "Evaporation", "Digestion"],
            "ans": 1,
            "exp": "Photosynthesis uses light, CO2, and water to produce sugar."
        },
        {
            "q": "Which planet is known as the Red Planet?",
            "opts": ["Venus", "Jupiter", "Mars", "Saturn"],
            "ans": 2,
            "exp": "Mars appears red due to iron oxide (rust) on its surface."
        },
        {
            "q": "What is the capital of India?",
            "opts": ["Mumbai", "New Delhi", "Kolkata", "Chandigarh"],
            "ans": 1,
            "exp": "New Delhi is the official national capital of India."
        }
    ]

    def on_enter(self):
        self.score = 0
        self.q_index = 0
        self.load_question()

    def load_question(self):
        if self.q_index >= len(self.questions):
            self.end_game()
            return
        q = self.questions[self.q_index]
        self.question_title = f"Question {self.q_index + 1} of {len(self.questions)}"
        self.question_text = q["q"]
        self.option_a = q["opts"][0]
        self.option_b = q["opts"][1]
        self.option_c = q["opts"][2]
        self.option_d = q["opts"][3]
        self.correct_idx = q["ans"]
        self.explanation = ""

    def choose_option(self, idx):
        if idx == self.correct_idx:
            self.score += 25
            self.explanation = "CORRECT! " + self.questions[self.q_index]["exp"]
            speak_text("Correct!")
        else:
            self.explanation = "WRONG! " + self.questions[self.q_index]["exp"]
            
        Clock.schedule_once(lambda dt: self.next_q(), 2.0)

    def next_q(self):
        self.q_index += 1
        self.load_question()

    def end_game(self):
        app = App.get_running_app()
        uid = app.user_data["uid"]
        earned = database.save_game_progress(
            uid=uid,
            game_id="gk_quiz",
            subject="GK",
            class_num=app.user_data.get("class_level", 6),
            chapter="General Knowledge",
            score=self.score,
            max_score=100
        )
        app.load_user_data()
        self.question_text = f"Quiz Complete! Scored {self.score}/100. Earned {earned} Coins!"
        Clock.schedule_once(lambda dt: self.exit_quiz(), 2.0)

    def exit_quiz(self):
        self.manager.current = "lessons"
        self.manager.transition.direction = "right"

class EnglishVocabGame(Screen):
    word_text = StringProperty("")
    definition_text = StringProperty("")
    opt1 = StringProperty("")
    opt2 = StringProperty("")
    opt3 = StringProperty("")
    correct_opt = NumericProperty(0)
    score = NumericProperty(0)
    q_count = NumericProperty(0)
    status_msg = StringProperty("Match the English word to its meaning!")

    words_db = [
        {"word": "Abundant", "def": "Plentiful, existing in large quantities", "opts": ["Scarce", "Plentiful", "Tiny"], "ans": 1},
        {"word": "Benevolent", "def": "Kind, well-meaning, and helpful", "opts": ["Kind & Helpful", "Cruel", "Noisy"], "ans": 0},
        {"word": "Diligent", "def": "Showing care and effort in work", "opts": ["Lazy", "Hardworking", "Sleepy"], "ans": 1},
        {"word": "Resilient", "def": "Able to withstand or recover quickly", "opts": ["Fragile", "Strong & Flexible", "Slow"], "ans": 1}
    ]

    def on_enter(self):
        self.score = 0
        self.q_count = 0
        self.load_word()

    def load_word(self):
        if self.q_count >= len(self.words_db):
            self.end_game()
            return
        item = self.words_db[self.q_count]
        self.word_text = item["word"]
        self.definition_text = f"What is the meaning of '{item['word']}'?"
        self.opt1 = item["opts"][0]
        self.opt2 = item["opts"][1]
        self.opt3 = item["opts"][2]
        self.correct_opt = item["ans"]
        self.status_msg = "Tap audio icon to hear pronunciation!"

    def play_audio(self):
        speak_text(self.word_text)

    def check_answer(self, idx):
        if idx == self.correct_opt:
            self.score += 25
            self.status_msg = "Excellent! Correct vocabulary match."
            speak_text("Excellent!")
        else:
            self.status_msg = f"Not quite! Correct: {self.words_db[self.q_count]['def']}"
            
        self.q_count += 1
        Clock.schedule_once(lambda dt: self.load_word(), 1.8)

    def end_game(self):
        app = App.get_running_app()
        uid = app.user_data["uid"]
        earned = database.save_game_progress(
            uid=uid,
            game_id="english_vocab",
            subject="English",
            class_num=app.user_data.get("class_level", 6),
            chapter="Vocabulary Master",
            score=self.score,
            max_score=100
        )
        app.load_user_data()
        self.word_text = "Lesson Complete!"
        self.status_msg = f"Scored {self.score}/100! Earned {earned} coins!"
        Clock.schedule_once(lambda dt: self.exit_game(), 2.0)

    def exit_game(self):
        self.manager.current = "lessons"
        self.manager.transition.direction = "right"

class AchievementsPage(Screen):
    achievements_list = ListProperty([])

    def on_enter(self):
        app = App.get_running_app()
        uid = app.user_data["uid"]
        achs = database.get_user_achievements(uid)
        
        # Merge with default list for display
        default_achs = [
            {"title": "First Steps", "desc": "Completed your very first game.", "unlocked": False},
            {"title": "Master Mind", "desc": "Scored 80+ points in a combat game.", "unlocked": False},
            {"title": "Coin Collector", "desc": "Accumulated 200+ total coins.", "unlocked": app.user_data.get("coins", 0) >= 200},
            {"title": "Polymath", "desc": "Completed lessons across 3 different subjects.", "unlocked": False}
        ]
        unlocked_titles = {a["title"] for a in achs}
        for d in default_achs:
            if d["title"] in unlocked_titles:
                d["unlocked"] = True
                
        self.achievements_list = default_achs

class GalleryPage(Screen):
    badges_list = ListProperty([])

    def on_enter(self):
        app = App.get_running_app()
        uid = app.user_data["uid"]
        inventory = database.get_user_inventory(uid)
        
        base_badges = [
            {"name": "Bronze Medalist", "desc": "Awarded for completing Class 6 level", "icon": "logos/tasks.png"},
            {"name": "Silver Trophy", "desc": "Awarded for earning 150 coins", "icon": "logos/achievements.png"},
            {"name": "Gold Scholar", "desc": "Awarded for high accuracy", "icon": "logos/gallery.png"}
        ]
        
        for item in inventory:
            base_badges.append({"name": item["item_name"], "desc": "Purchased item", "icon": "logos/store.png"})
            
        self.badges_list = base_badges

class RewardsPage(Screen):
    tasks_list = ListProperty([])
    user_coins = NumericProperty(0)

    def on_enter(self):
        app = App.get_running_app()
        uid = app.user_data["uid"]
        self.user_coins = app.user_data.get("coins", 0)
        self.tasks_list = database.get_daily_tasks(uid)

    def claim_reward(self, task_id):
        app = App.get_running_app()
        uid = app.user_data["uid"]
        success, reward = database.complete_daily_task(uid, task_id)
        if success:
            app.load_user_data()
            self.on_enter()

class StorePage(Screen):
    user_coins = NumericProperty(0)
    status_msg = StringProperty("Spend your hard-earned coins on cosmetics!")

    store_items = [
        {"id": "bg_cyber", "type": "theme", "name": "Dark Galaxy Theme", "cost": 50},
        {"id": "av_knight", "type": "avatar", "name": "Golden Knight Avatar", "cost": 80},
        {"id": "title_master", "type": "title", "name": "Grand Scholar Title", "cost": 100}
    ]

    def on_enter(self):
        app = App.get_running_app()
        self.user_coins = app.user_data.get("coins", 0)

    def buy_item(self, item_id, item_type, item_name, cost):
        app = App.get_running_app()
        uid = app.user_data["uid"]
        success, msg = database.buy_inventory_item(uid, item_id, item_type, item_name, cost)
        self.status_msg = msg
        if success:
            if item_type == "title":
                database.update_user_profile(uid, app.user_data["name"], app.user_data["class_level"], title=item_name)
            app.load_user_data()
            self.on_enter()

class StatsPage(Screen):
    user_coins = NumericProperty(0)
    subject_stats = ListProperty([])
    leaderboard = ListProperty([])

    def on_enter(self):
        app = App.get_running_app()
        uid = app.user_data["uid"]
        self.user_coins = app.user_data.get("coins", 0)
        self.subject_stats = database.get_subject_stats(uid)
        self.leaderboard = database.get_leaderboard()

class SettingsPage(Screen):
    selected_lang = StringProperty("English")

    def change_language(self, lang):
        self.selected_lang = lang

    def reset_progress(self):
        app = App.get_running_app()
        if os.path.exists(database.DB_PATH):
            try:
                os.remove(database.DB_PATH)
            except Exception:
                pass
        database.init_db()
        app.load_user_data()
        self.manager.current = "create_profile"

class HelpPage(Screen):
    help_text = StringProperty("""Welcome to GyanSetu!

1. Offline-First Learning:
All mini-games and curriculum chapters (Classes 1–10) run on your device without internet connection.

2. Curriculum Games:
- Knight vs Dragon: Practice arithmetic calculations under timed combat pressure.
- Monkey River Crossing: Solve problem-solving math puzzles to hop stones across the river.
- GK Quiz: Test your knowledge in science, geography, and Indian heritage.
- English Master: Learn new vocabulary and practice pronunciation.

3. Progress Board:
Parents and teachers can review learning activity, score accuracy, and game stats on the Progress Board.

4. Gamification:
Earn coins for every completed game, unlock achievements, collect badges in your gallery, and buy store cosmetics!""")


class GyanSetuApp(App):
    user_data = ObjectProperty({})

    def build(self):
        database.init_db()
        self.load_user_data()
        return Builder.load_file("gyansetu.kv")

    def load_user_data(self):
        self.user_data = database.get_or_create_user()

if __name__ == "__main__":
    GyanSetuApp().run()
