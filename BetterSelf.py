import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from analytics import MillionaireAnalytics
from ml_engine import SuccessRoadmapEngine

# ==========================================
# 1. PAGE CONFIGURATION & CACHED ENGINES
# ==========================================
st.set_page_config(page_title="Orphan Rise Roadmap", page_icon="🏆", layout="wide", initial_sidebar_state="expanded")

@st.cache_resource
def get_engines():
    return MillionaireAnalytics('optimized_dataset.csv'), SuccessRoadmapEngine('ML_dataset.csv')

stats_engine, ml_engine = get_engines()

# ==========================================
# 2. REUSABLE UI & STYLING FUNCTIONS
# ==========================================
def apply_custom_css():
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                background-image: radial-gradient(circle at 50% 50%, #1c1c1e 0%, #0c0c0d 80%) !important;
                background-color: #0c0c0d !important;
            }
            /* Force the outer Streamlit button wrapper to span 100% of the sidebar */
            [data-testid="stSidebar"] div.stButton {
                width: 100% !important;
                display: block !important;
            }
            [data-testid="stSidebar"] div.stButton > button {
                width: 100% !important;
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                background: linear-gradient(135deg, #BF953F 0%, #FCF6BA 25%, #B38728 50%, #FBF5B7 75%, #AA771C 100%) !important;
                color: #1A120B !important;
                font-weight: 900 !important;
                font-size: 1rem !important;
                padding: 12px !important;
                border-radius: 8px !important;
                border: 2px solid #AA771C !important;
                box-shadow: 0px 4px 0px #7A5210, 0px 6px 10px rgba(0, 0, 0, 0.6) !important;
                margin-bottom: 8px !important;
            }
            [data-testid="stSidebar"] div.stButton > button:hover {
                border: 2px solid #FFFFFF !important;
                box-shadow: 0px 4px 0px #7A5210, 0px 0px 14px rgba(212, 175, 55, 0.85) !important;
            }
        </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    st.sidebar.markdown("<h1 style='text-align: center; color: #D4AF37; margin-bottom: 0px;'>🏆 Success Road</h1>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center; color: #FFFFFF; font-size: 0.9rem; font-weight: bold; margin-bottom: 15px;'>The Orphan Wealth Roadmap</p>", unsafe_allow_html=True)
    try:
        st.sidebar.image("Images/Success.jpg", use_container_width=True)
    except TypeError:
        st.sidebar.image("Images/Success.jpg", use_column_width=True)

    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"

    with st.sidebar:
        st.write("")
        if st.button("🏠 Home & Mission Story", key="nav_home"):
            st.session_state.current_page = "Home"
        if st.button("💰 Millionaire Statistics", key="nav_stats"):
            st.session_state.current_page = "Stats"
        if st.button("🔮 Success Roadmap (ML Engine)", key="nav_roadmap"):
            st.session_state.current_page = "Roadmap"

def create_circle_badge(main_value: str, label_html: str) -> str:
    return (
        f'<div style="width: 145px; height: 145px; border-radius: 50%; background-color: #2C2C2E; '
        f'border: 3px solid #D4AF37; box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.28); '
        f'display: flex; flex-direction: column; justify-content: center; align-items: center; '
        f'text-align: center; padding: 10px; font-family: sans-serif; margin: 4px auto;">'
        f'<span style="color: #D4AF37; font-size: 1.45rem; font-weight: 900; line-height: 1.1;">{main_value}</span>'
        f'<span style="color: #D4AF37; font-size: 0.75rem; font-weight: 700; margin-top: 6px; line-height: 1.2;">{label_html}</span>'
        f'</div>'
    )

# ==========================================
# 3. PAGE RENDERING FUNCTIONS
# ==========================================
def render_home_page():
    st.markdown("<h1 style='text-align: center; color: #D4AF37; margin-bottom: 5px;'>🏆 Orphan Rise Roadmap</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #333333; font-weight: 500; margin-bottom: 20px;'>The Digital Mindset and Wealth Prescriptive Engine</h3>", unsafe_allow_html=True)

    left_col, center_col, right_col = st.columns([1.0, 2.2, 1.0])

    with left_col:
        st.markdown(
            '<div style="display: flex; flex-direction: column; align-items: center; gap: 12px;">'
            + create_circle_badge(f"{stats_engine.get_average_books_read()}", "Avg Books Read<br>Per Year")
            + create_circle_badge(f"{stats_engine.get_wakeup_range()['average_clock']}", "Average<br>Wake-Up Time")
            + create_circle_badge(f"${stats_engine.get_average_charity_amount():,.0f}", "Avg Annual<br>Charity Money")
            + '</div>', unsafe_allow_html=True
        )

    with center_col:
        st.markdown('<div style="padding-top: 25px;"></div>', unsafe_allow_html=True)
        try:
            st.image("Images/illustration.png", use_container_width=True)
        except TypeError:
            st.image("Images/illustration.png", use_column_width=True)

    with right_col:
        st.markdown(
            '<div style="display: flex; flex-direction: column; align-items: center; gap: 12px;">'
            + create_circle_badge(f"{stats_engine.get_reading_percentage()}%", "of Millionaires<br>Read Books")
            + create_circle_badge(f"{stats_engine.get_planning_adoption_stats()['active_percentage']}%", "of Millionaires<br>Do Planning")
            + create_circle_badge(f"{stats_engine.get_charity_givers_percentage()}%", "of Millionaires<br>Give Charity")
            + '</div>', unsafe_allow_html=True
        )

def render_statistics_page():
    st.markdown("<h1 style='text-align: center; color: #D4AF37; margin-bottom: 5px;'>🏆 Millionaire Statistics</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #333333; font-size: 1.05rem; margin-bottom: 20px;'>Empirical behavioral charts and wealth rankings audited from 4,263 Millionaire profiles.</p>", unsafe_allow_html=True)
    st.write("---")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<h4 style='color: #B38728;'>💼 Business Owners: Work Hours by Wealth Tier</h4>", unsafe_allow_html=True)
        tier_hours = stats_engine.get_business_owner_work_by_wealth()
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        bars = ax1.bar(tier_hours.index.astype(str), tier_hours.values, color=['#2C2C2E', '#555555', '#B38728', '#D4AF37'], edgecolor='black', width=0.52)
        ax1.set_xlabel('Business Owner Net Worth Tier', fontweight='bold')
        ax1.set_ylabel('Avg Deep Work (Hours / Day)', fontweight='bold')
        ax1.set_ylim(0, max(tier_hours.values) * 1.28)
        for bar in bars:
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.08, f"{bar.get_height():.2f}h", ha='center', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig1)

    with c2:
        st.markdown("<h4 style='color: #B38728;'>🤝 Annual Charity Donations vs. Net Worth</h4>", unsafe_allow_html=True)
        df = stats_engine.millionaires.copy()
        df['net_worth'] = pd.to_numeric(df['net_worth'], errors='coerce').fillna(0)
        df['annual_charity_donations'] = pd.to_numeric(df['annual_charity_donations'], errors='coerce').fillna(0)
        donors = df[df['annual_charity_donations'] > 0]
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.scatter(donors['net_worth'] / 1e6, donors['annual_charity_donations'] / 1e3, color='#D4AF37', edgecolor='#1A120B', alpha=0.55, s=28)
        ax2.set_xlabel('Net Worth ($ Millions)', fontweight='bold')
        ax2.set_ylabel('Annual Charity ($ Thousands)', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig2)

    st.markdown("<h4 style='color: #B38728;'>⏱️ Time Management Score Tiers vs. Daily Productivity</h4>", unsafe_allow_html=True)
    tm_prod = stats_engine.get_productivity_by_time_management()
    fig3, ax3 = plt.subplots(figsize=(10, 3.6))
    bars3 = ax3.bar(tm_prod.index.astype(str), tm_prod.values, color='#D4AF37', edgecolor='black', width=0.45)
    ax3.set_ylabel('Avg Daily Productivity Score', fontweight='bold')
    ax3.set_ylim(0, 100)
    for bar in bars3:
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, f"{bar.get_height():.1f} / 100", ha='center', fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig3)

    st.write("---")
    st.markdown("<h3 style='color: #D4AF37;'>💎 Millionaire Cohort Leaderboard (Ordered by Net Worth)</h3>", unsafe_allow_html=True)
    st.dataframe(stats_engine.get_wealth_leaderboard(top_n=50), height=400)

def render_roadmap_page():
    st.markdown("<h1 style='text-align: center; color: #D4AF37; margin-bottom: 5px;'>🔮 Success Trajectory Optimizer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #333333; font-size: 1.05rem; margin-bottom: 20px;'>Enter your daily habits below to run our ML Classifier and compare your routine against Millionaire benchmarks.</p>", unsafe_allow_html=True)
    st.write("---")

    with st.form("roadmap_optimizer_form"):
        st.markdown("<h4 style='color: #B38728;'>📚 1. Continuous Learning & Planning</h4>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        books_read = c1.slider("Books Read / Year", 0, 50, 6)
        self_learning = c2.slider("Self-Learning Hrs / Month", 0, 100, 20)
        online_courses = c3.number_input("Online Courses / Year", 0, 20, 2)
        planning_active = c4.selectbox("Active Daily/Weekly Planning?", ["Yes (Active)", "No (None)"])

        st.markdown("<h4 style='color: #B38728; margin-top: 15px;'>⚡ 2. Deep Focus & Execution</h4>", unsafe_allow_html=True)
        c5, c6, c7 = st.columns(3)
        deep_work = c5.slider("Deep Work Hours / Day", 0.0, 10.0, 3.0, step=0.5)
        task_completion = c6.slider("Task Completion Rate (%)", 0, 100, 75)
        social_media = c7.slider("Social Media Hours / Day", 0.0, 12.0, 2.0, step=0.5)

        st.markdown("<h4 style='color: #B38728; margin-top: 15px;'>💪 3. Health, Sleep & Recovery</h4>", unsafe_allow_html=True)
        c8, c9, c10, c11 = st.columns(4)
        sleep_hours = c8.slider("Sleep Duration (Hrs/Night)", 4.0, 11.0, 7.5, step=0.5)
        exercise_days = c9.slider("Exercise Days / Week", 0, 7, 3)
        walking_steps = c10.number_input("Walking Steps / Day", 0, 30000, 6000, step=500)
        water_liters = c11.slider("Water Intake (Liters/Day)", 0.0, 5.0, 2.0, step=0.5)

        st.write("")
        submitted = st.form_submit_button("🏆 Generate My Success Roadmap")

    if submitted:
        user_inputs = {
            'self_learning_hours_per_month': self_learning,
            'books_read_per_year': books_read,
            'online_courses_per_year': online_courses,
            'planningHabit': 1 if "Yes" in planning_active else 0,
            'deep_work_hours_per_day': deep_work,
            'task_completion_rate': task_completion,
            'social_media_hours_per_day': social_media,
            'sleep_duration_hours': sleep_hours,
            'exercise_days_per_week': exercise_days,
            'walking_steps_per_day': walking_steps,
            'water_intake_liters': water_liters
        }
        results = ml_engine.evaluate_user(user_inputs)

        st.write("---")
        st.markdown("<h2 style='text-align: center; color: #D4AF37;'>📊 Your Trajectory Audit Results</h2>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("🎯 Millionaire Habit Alignment", f"{results['alignment_score']}%", "Elite Match" if results['alignment_score'] >= 75 else "Room to Grow")
        m2.metric("🤖 Random Forest ML Probability", f"{results['ml_probability']}%", results['ml_label'])
        m3.metric("⚡ Execution Velocity", f"{task_completion}%", f"{deep_work} hrs/day Deep Work")

        st.write("")
        st.markdown("<h3 style='color: #B38728;'>🧭 Personalized Prescriptive Action Plan</h3>", unsafe_allow_html=True)
        if not results['advice']:
            st.success("🏆 **Outstanding Discipline!** Your daily routine already aligns with the top Millionaire habit benchmarks!")
        else:
            for item in results['advice']:
                st.warning(f"📌 {item}")

# ==========================================
# 4. MAIN APPLICATION ROUTER
# ==========================================
apply_custom_css()
render_sidebar()

page = st.session_state.current_page
if page == "Home":
    render_home_page()
elif page == "Stats":
    render_statistics_page()
elif page == "Roadmap":
    render_roadmap_page()

