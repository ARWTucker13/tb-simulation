from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import json
from datetime import datetime
import os

app = Flask(__name__)
# Configure server-side session storage
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_FILE_DIR'] = './flask_session_data'  # Folder where session files are stored
Session(app)
app.secret_key = 'your-secret-key'

# Load scenes
with open('TB_Mining_Simulation_FullNarratives.json') as f:
    scenes = json.load(f)

# Load archetype profiles
archetype_profiles = {
    "systems_architect": {
        "name": "Systems Architect",
        "description": "You build durable solutions by integrating TB-in-mining services into national systems.",
        "learning_objectives": [
            "Module D: Understand health system functions and UHC policy levers.",
            "Module A: Examine societal structures that influence health systems.",
            "Module B: Use data to guide long-term systems planning."
        ]
    },
    "equity_negotiator": {
        "name": "Equity-Driven Negotiator",
        "description": "You center justice, inclusion, and structural determinants of health.",
        "learning_objectives": [
            "Module C: Analyze upstream social and structural determinants of health.",
            "Lesson 9: Apply human rights-based approaches to health programming.",
            "Lesson 8: Consider historical and political contributors to health inequities."
        ]
    },
    "diplomatic_strategist": {
        "name": "Diplomatic Strategist",
        "description": "You navigate regional politics to build cross-border health solutions.",
        "learning_objectives": [
            "Module A: Understand global governance structures in health.",
            "Module D: Identify tools for regional cooperation.",
            "Lesson 12: Explore global solidarity in public health."
        ]
    },
    "public_health_communicator": {
        "name": "Public Health Communicator",
        "description": "You lead with narrative, empathy, and political framing.",
        "learning_objectives": [
            "Lesson 5: Use storytelling to promote health equity.",
            "Lesson 11: Communicate effectively across audiences.",
            "Module A: Engage public health values of prevention and participation."
        ]
    },
    "evidence_based_strategist": {
        "name": "Evidence-Based Strategist",
        "description": "You prioritize data-driven public health investment and efficiency.",
        "learning_objectives": [
            "Module B: Apply DALYs and epidemiologic data to burden of disease.",
            "Lessons 4–6: Use prevalence and risk factor analysis.",
            "Lesson 10: Evaluate based on cost-effectiveness and impact."
        ]
    }
}

@app.route('/')
def index():
    session.clear()
    return render_template('index.html', scene_count=len(scenes))

@app.route('/scene/<int:scene_id>', methods=['GET', 'POST'])
def scene(scene_id):
    if 'scores' not in session:
        session['scores'] = {k: 0 for k in archetype_profiles}

    if request.method == 'POST':
        selected = request.form['choice']
        choice = next(c for c in scenes[scene_id]['choices'] if c['letter'] == selected)
        session['scores'][choice['archetype']] += choice['points']
        session.modified = True
        return redirect(url_for('scene', scene_id=scene_id + 1))

    if scene_id >= len(scenes):
        return redirect(url_for('results'))

    return render_template('scene.html', scene=scenes[scene_id], scene_id=scene_id)

@app.route('/results')
def results():
    scores = session.get('scores')
    if not scores:
        return redirect(url_for('index'))  # or show a custom error page

    dominant = max(scores, key=scores.get)

    profile = archetype_profiles[dominant]
    return render_template('results.html', profile=profile, scores=scores)

if __name__ == '__main__':
    app.run(debug=True)
