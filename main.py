from drafter import *
from drafter.llm import LLMMessage, LLMError, call_gemini
from dataclasses import dataclass
import os
from dotenv import load_dotenv

hide_debug_information()

# INITIAL SETUP & API KEY LOADING

load_dotenv()

# Get the key from the environment and ensure it's used by Drafter/Gemini
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_KEY:
    os.environ['GEMINI_API_KEY'] = GEMINI_KEY 
    print("GEMINI_API_KEY loaded successfully.")
else:
    print("ERROR: GEMINI_API_KEY not found in the environment (check .env file).")


# DATACLASSES

@dataclass
class UserProfile:
    """Static user metrics and health goals"""
    name: str
    height: int
    health_goal: str


@dataclass
class DailyLogEntry:
    """Single day's health tracking data"""
    date: str
    meal: str
    exercise: str
    mood: int
    notes: str


@dataclass
class State:
    """Overarching application state"""
    profile: UserProfile
    log_history: list  # list[DailyLogEntry]
    meal_cache: str
    challenge_cache: str

# AI functions

def analyze_meal_with_ai(meal_description: str) -> str:
    """Use Drafter's call_gemini to analyze a meal"""
    if not GEMINI_KEY:
        return "Analysis failed: GEMINI_API_KEY not set."
        
    prompt = f"""Analyze this meal in detail:
{meal_description}
Provide a clear assessment with:
• Nutritional benefits
• Potential concerns
• Overall health assessment
Keep it concise and friendly."""
    
    try:
        result = call_gemini(
            messages=[
                LLMMessage(role="user", content=prompt)
            ],
            model="gemini-1.5-flash"
        )
        
        # FIX: Check if the result is an error object and use str() to get the error message
        if isinstance(result, LLMError):
            return f"🚫 AI Analysis Failed: {str(result)}"
        
        # If not an error, return the text content
        return result.text
        
    except Exception as e:
        return f"Analysis failed (Internal Error): {str(e)}"


def generate_health_challenge(health_goal: str, mood: int) -> str:
    """Use Drafter's call_gemini to generate a personalized health challenge"""
    if not GEMINI_KEY:
        return "Challenge generation failed: GEMINI_API_KEY not set."
        
    prompt = f"""Create a short, motivating 10-minute health challenge.

User's goal: {health_goal.replace('_', ' ')}
Current mood level: {mood}/10

Make it achievable, fun, and relevant to their goal. Keep it brief and actionable."""
    
    try:
        result = call_gemini(
            messages=[
                LLMMessage(role="user", content=prompt)
            ],
            model="gemini-1.5-flash"
        )
        
        # FIX: Check if the result is an error object and use str() to get the error message
        if isinstance(result, LLMError):
            return f"🚫 Challenge Generation Failed: {str(result)}"
        
        # If not an error, return the text content
        return result.text
        
    except Exception as e:
        return f"Challenge generation failed (Internal Error): {str(e)}"


# CSS styling

CUSTOM_CSS = """
<style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin: 0;
        padding: 20px;
    }
    
    .page-container {
        max-width: 1200px;
        margin: 0 auto;
        background: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    h1, h2 {
        color: #667eea;
        margin-bottom: 20px;
    }
    
    input, textarea, select {
        width: 100%;
        padding: 12px;
        margin: 8px 0;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        font-size: 14px;
        transition: all 0.3s;
    }
    
    input:focus, textarea:focus, select:focus {
        border-color: #667eea;
        outline: none;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
    }
    
    button, a.button {
        background: #667eea;
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
        margin: 5px;
        transition: all 0.3s;
    }
    
    button:hover, a.button:hover {
        background: #5568d3;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102,126,234,0.3);
    }
    
    .grid-2 {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 30px;
        margin-top: 20px;
    }
    
    .card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #667eea;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin: 10px 0;
    }
    
    .stat-value {
        font-size: 36px;
        font-weight: bold;
        margin: 10px 0;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }
    
    table th {
        background: #667eea;
        color: white;
        padding: 12px;
        text-align: left;
    }
    
    table td {
        padding: 12px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    table tr:hover {
        background: #f8f9fa;
    }
    
    .mood-display {
        font-size: 48px;
        text-align: center;
        color: #667eea;
        font-weight: bold;
        margin: 20px 0;
    }
    
    .analysis-box {
        background: white;
        padding: 20px;
        border-radius: 8px;
        margin-top: 15px;
        white-space: pre-wrap;
        line-height: 1.6;
        border: 2px solid #667eea;
    }
    
    @media (max-width: 768px) {
        .grid-2 {
            grid-template-columns: 1fr;
        }
    }
</style>
"""


# JAVASCRIPT - Interactive Features

MOOD_SLIDER_JS = """
<script>
    function updateMoodDisplay() {
        const slider = document.getElementById('mood-slider');
        const display = document.getElementById('mood-value');
        if (slider && display) {
            display.textContent = slider.value;
        }
    }
    
    // Initialize on load
    window.addEventListener('DOMContentLoaded', function() {
        updateMoodDisplay();
    });
</script>
"""

# ROUTES - Application Pages

@route
def index(state: State) -> Page:
    """Main entry point"""
    if state.profile.name == "":
        return setup(state)
    return dashboard(state)


@route
def setup(state: State) -> Page:
    """Profile setup with enhanced styling"""
    return Page(
        state,
        content=[
            CUSTOM_CSS,
            "<div class='page-container'>",
            "<h1>👤 Welcome to Your Holistic Health Hub</h1>",
            "<p>Let's set up your profile to get started on your wellness journey.</p>",
            "<br>",
            "<label><strong>Your Name:</strong></label>",
            TextBox(name="name", default_value=""),
            "<label><strong>Height (cm):</strong></label>",
            TextBox(name="height", default_value="", kind="number"),
            "<label><strong>Health Goal:</strong></label>",
            SelectBox(
                name="health_goal",
                options=["weight_loss", "muscle_gain", "maintenance", "energy_boost", "flexibility"],
                default_value="weight_loss"
            ),
            "<br>",
            Button(text="🚀 Start Your Journey", url="/save_profile"),
            "</div>",
        ],
    )


@route
def save_profile(state: State, name: str, height: str, health_goal: str) -> Page:
    """Save profile and redirect"""
    state.profile = UserProfile(
        name=name,
        height=int(height) if height else 0,
        health_goal=health_goal
    )
    return dashboard(state)


@route
def dashboard(state: State) -> Page:
    """Main dashboard with daily logging"""
    return Page(
        state,
        content=[
            CUSTOM_CSS,
            MOOD_SLIDER_JS,
            "<div class='page-container'>",
            f"<h1>Hello, {state.profile.name}! 👋</h1>",
            f"<p><strong>Goal:</strong> {state.profile.health_goal.replace('_', ' ').title()} | <strong>Height:</strong> {state.profile.height}cm</p>",
            "<hr>",
            "<h2>📅 Daily Log Entry</h2>",
            "<div class='card'>",
            "<label><strong>Date:</strong></label>",
            TextBox(name="log_date", default_value="2024-12-06", kind="date"),
            "<label><strong>Meal Description:</strong></label>",
            TextArea(name="meal", default_value="", placeholder="What did you eat today?"),
            "<label><strong>Exercise:</strong></label>",
            TextBox(name="exercise", default_value="", placeholder="e.g., Running, Yoga"),
            "<label><strong>Mood (1-10):</strong></label>",
            "<div class='mood-display' id='mood-value'>5</div>",
            "<input type='range' id='mood-slider' name='mood' min='1' max='10' value='5' oninput='updateMoodDisplay()' style='width: 100%;'>",
            "<label><strong>Notes:</strong></label>",
            TextArea(name="notes", default_value="", placeholder="Any additional thoughts..."),
            Button(text="💾 Save Daily Log", url="/save_daily_log"),
            "</div>",
            "<br>",
            "<div class='grid-2'>",
            "<div>",
            Button(text="✨ Analyze Meal (AI)", url="/analyze_meal_page"),
            Button(text="🎯 Generate Challenge (AI)", url="/challenge_page"),
            "</div>",
            "<div>",
            Button(text="📊 View History", url="/history"),
            Button(text="📈 View Progress", url="/progress"),
            "</div>",
            "</div>",
            "</div>",
        ],
    )


@route
def save_daily_log(state: State, log_date: str, meal: str, exercise: str, mood: str, notes: str) -> Page:
    """Save log entry"""
    new_entry = DailyLogEntry(
        date=log_date,
        meal=meal,
        exercise=exercise,
        mood=int(mood) if mood else 5,
        notes=notes
    )
    state.log_history.append(new_entry)
    
    return Page(
        state,
        content=[
            CUSTOM_CSS,
            "<div class='page-container'>",
            "<h1>✅ Log Saved Successfully!</h1>",
            "<div class='card'>",
            "<p><strong>Date:</strong> " + log_date + "</p>",
            "<p><strong>Meal:</strong> " + meal[:50] + "...</p>",
            "<p><strong>Exercise:</strong> " + exercise + "</p>",
            "<p><strong>Mood:</strong> " + mood + "/10</p>",
            "</div>",
            "<br>",
            Button(text="← Back to Dashboard", url="/dashboard"),
            Button(text="📊 View History", url="/history"),
            "</div>",
        ],
    )


@route
def analyze_meal_page(state: State) -> Page:
    """AI meal analysis form page"""
    return Page(
        state,
        content=[
            CUSTOM_CSS,
            "<div class='page-container'>",
            "<h1>✨ AI Meal Analysis</h1>",
            "<div class='card'>",
            "<label><strong>Describe your meal:</strong></label>",
            TextArea(name="meal_to_analyze", default_value="", placeholder="Enter detailed meal description..."),
            "<br>",
            Button(text="🤖 Analyze with AI", url="/analyze_meal_result"),
            "</div>",
            "<br>",
            Button(text="← Back to Dashboard", url="/dashboard"),
            "</div>",
        ],
    )


@route
def analyze_meal_result(state: State, meal_to_analyze: str) -> Page:
    """Display AI meal analysis result"""
    if not meal_to_analyze.strip():
        analysis_text = "Please enter a meal description to analyze."
    else:
        analysis_text = analyze_meal_with_ai(meal_to_analyze)
    
    return Page(
        state,
        content=[
            CUSTOM_CSS,
            "<div class='page-container'>",
            "<h1>✨ AI Meal Analysis Result</h1>",
            "<div class='analysis-box'>",
            analysis_text,
            "</div>",
            "<br>",
            Button(text="← Back", url="/analyze_meal_page"),
            Button(text="🏠 Dashboard", url="/dashboard"),
            "</div>",
        ],
    )


@route
def challenge_page(state: State) -> Page:
    """AI challenge generator form page"""
    latest_mood = 5
    if len(state.log_history) > 0:
        latest_mood = state.log_history[-1].mood
    
    return Page(
        state,
        content=[
            CUSTOM_CSS,
            "<div class='page-container'>",
            "<h1>🎯 Daily Challenge Generator</h1>",
            "<div class='card'>",
            f"<p><strong>Your Goal:</strong> {state.profile.health_goal.replace('_', ' ').title()}</p>",
            f"<p><strong>Recent Mood:</strong> {latest_mood}/10</p>",
            "<br>",
            Button(text="🎲 Generate Challenge", url="/challenge_result"),
            "</div>",
            "<br>",
            Button(text="← Back to Dashboard", url="/dashboard"),
            "</div>",
        ],
    )


@route
def challenge_result(state: State) -> Page:
    """Display AI challenge result"""
    latest_mood = 5
    if len(state.log_history) > 0:
        latest_mood = state.log_history[-1].mood
    
    challenge_text = generate_health_challenge(state.profile.health_goal, latest_mood)
    
    return Page(
        state,
        content=[
            CUSTOM_CSS,
            "<div class='page-container'>",
            "<h1>🎯 Your Challenge</h1>",
            "<div class='analysis-box'>",
            challenge_text,
            "</div>",
            "<br>",
            Button(text="← Back", url="/challenge_page"),
            Button(text="🏠 Dashboard", url="/dashboard"),
            "</div>",
        ],
    )


@route
def history(state: State) -> Page:
    """History table view"""
    if len(state.log_history) == 0:
        return Page(
            state,
            content=[
                CUSTOM_CSS,
                "<div class='page-container'>",
                "<h1>📊 Log History</h1>",
                "<p>No logs yet. Start logging your daily activities!</p>",
                "<br>",
                Button(text="← Back to Dashboard", url="/dashboard"),
                "</div>",
            ],
        )
    
    table_rows = []
    for entry in state.log_history:
        meal_short = entry.meal[:40] + "..." if len(entry.meal) > 40 else entry.meal
        table_rows.append([
            entry.date,
            meal_short,
            entry.exercise,
            f"{entry.mood}/10",
            entry.notes if entry.notes else "-"
        ])
    
    return Page(
        state,
        content=[
            CUSTOM_CSS,
            "<div class='page-container'>",
            "<h1>📊 Log History</h1>",
            f"<p><strong>Total Entries:</strong> {len(state.log_history)}</p>",
            Table(
                headers=["Date", "Meal", "Exercise", "Mood", "Notes"],
                rows=table_rows
            ),
            "<br>",
            Button(text="← Back to Dashboard", url="/dashboard"),
            Button(text="📈 View Progress", url="/progress"),
            "</div>",
        ],
    )


@route
def progress(state: State) -> Page:
    """Progress analytics"""
    if len(state.log_history) == 0:
        return Page(
            state,
            content=[
                CUSTOM_CSS,
                "<div class='page-container'>",
                "<h1>📈 Progress Analytics</h1>",
                "<p>No data yet. Start logging to see your progress!</p>",
                "<br>",
                Button(text="← Back to Dashboard", url="/dashboard"),
                "</div>",
            ],
        )
    
    # Calculate stats
    total_logs = len(state.log_history)
    total_mood = sum(entry.mood for entry in state.log_history)
    avg_mood = total_mood / total_logs
    
    # Mood-activity correlation
    exercise_moods = {}
    for entry in state.log_history:
        exercise = entry.exercise.lower()
        if exercise not in exercise_moods:
            exercise_moods[exercise] = []
        exercise_moods[exercise].append(entry.mood)
    
    correlation_content = []
    for exercise, moods in exercise_moods.items():
        avg = sum(moods) / len(moods)
        correlation_content.append(f"<div class='card'><strong>{exercise.title()}:</strong> {avg:.1f} average mood ❤️</div>")
    
    return Page(
        state,
        content=[
            CUSTOM_CSS,
            "<div class='page-container'>",
            "<h1>📈 Progress Analytics</h1>",
            "<div class='grid-2'>",
            f"<div class='stat-card'><div>Total Logs</div><div class='stat-value'>{total_logs}</div></div>",
            f"<div class='stat-card'><div>Average Mood</div><div class='stat-value'>{avg_mood:.1f}</div></div>",
            "</div>",
            "<br>",
            "<h2>Mood-Activity Correlation</h2>",
            *correlation_content,
            "<br>",
            Button(text="← Back to Dashboard", url="/dashboard"),
            Button(text="📊 View History", url="/history"),
            "</div>",
        ],
    )


# INITIALIZATION

start_server(State(
    profile=UserProfile(name="", height=0, health_goal="weight_loss"),
    log_history=[],
    meal_cache="",
    challenge_cache=""
))