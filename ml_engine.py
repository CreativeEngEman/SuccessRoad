import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

class SuccessRoadmapEngine:
    """
    Encapsulates Machine Learning training, trajectory probability prediction,
    Habit Alignment scoring, and personalized action plan generation.
    """
    def __init__(self, csv_path: str = 'ML_dataset.csv'):
        self.csv_path = csv_path
        self.pipeline = None
        self.feature_columns = []
        self._train_model()

    def _train_model(self):
        df = pd.read_csv(self.csv_path)
        y = (df['net_worth'] >= 1000000).astype(int)

        drop_cols = [
            'synthetic_person_id', 'age', 'age_group', 'education_level', 'field_of_study', 'industry',
            'habit_tracking', 'habit_tracking_frequency', 'annual_charity_donations',
            'time_management_score', 'priority_setting_score', 'business_owner',
            'business_age_years', 'daily_productivity_score', 'wealth_category',
            'net_worth', 'total_annual_income', 'millionaire_status'
        ]
        X = df.drop(columns=drop_cols, errors='ignore').copy()

        for col in ['work_start_time', 'work_end_time', 'wake_up_time', 'sleep_time']:
            if col in X.columns and X[col].dtype == 'object':
                parsed = pd.to_datetime(X[col], format='%H:%M', errors='coerce')
                X[col] = parsed.dt.hour + (parsed.dt.minute / 60.0)

        num_cols = X.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns.tolist()
        cat_cols = X.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

        try:
            ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        except TypeError:
            ohe = OneHotEncoder(handle_unknown='ignore', sparse=False)

        preprocessor = ColumnTransformer([
            ('num', Pipeline([('imp', SimpleImputer(strategy='median')), ('sc', StandardScaler())]), num_cols),
            ('cat', Pipeline([('imp', SimpleImputer(strategy='most_frequent')), ('enc', ohe)]), cat_cols)
        ])

        self.pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(
                n_estimators=200, max_depth=10, min_samples_leaf=5,
                class_weight='balanced', random_state=42
            ))
        ])
        self.pipeline.fit(X, y)
        self.feature_columns = X.columns.tolist()

    def evaluate_user(self, user_inputs: dict) -> dict:
        """Runs ML probability, Habit Alignment score, and generates personalized advice."""
        input_df = pd.DataFrame([{col: user_inputs.get(col, None) for col in self.feature_columns}])
        ml_prob = round(float(self.pipeline.predict_proba(input_df)[0][1]) * 100, 1)
        ml_label = "Millionaire Habit Cluster" if ml_prob >= 50 else "Developing Routine"

        # Calculate 0-100% Habit Alignment Score
        books = user_inputs['books_read_per_year']
        learn = user_inputs['self_learning_hours_per_month']
        plan  = user_inputs['planningHabit']
        deep  = user_inputs['deep_work_hours_per_day']
        soc   = user_inputs['social_media_hours_per_day']
        exer  = user_inputs['exercise_days_per_week']
        sleep = user_inputs['sleep_duration_hours']

        score = (
            min(books / 12.0, 1.0) * 18 +
            min(learn / 30.0, 1.0) * 18 +
            (16.0 if plan == 1 else 0.0) +
            min(deep / 3.5, 1.0) * 18 +
            max(0.0, (4.0 - soc) / 4.0) * 15 +
            (min(exer / 3.0, 1.0) * 7.5) +
            (1.0 - min(abs(sleep - 7.5) / 3.5, 1.0)) * 7.5
        )

        # Generate Prescriptive Action Plan
        advice = []
        if plan == 0:
            advice.append("**Start One Daily Planning Routine:** Spend 15 focused minutes planning tomorrow tonight to boost daily execution.")
        if books < 10:
            advice.append(f"**Increase Reading Volume:** You logged **{books} books/year**. Aim for **12 books/year** (1 per month) to match millionaire benchmarks.")
        if learn < 25:
            advice.append(f"**Boost Skill Acquisition:** You logged **{learn} hrs/month** of self-learning. Add 30 minutes a day (+15 hrs/month) to accelerate skill mastery.")
        if deep < 3.0:
            advice.append(f"**Protect Deep Work Blocks:** Increase distraction-free deep work from **{deep} hrs** to **3.0–3.5 hrs/day**.")
        if soc > 2.0:
            advice.append(f"**Cut Digital Distractions:** Reduce social media from **{soc} hrs/day** to under **1.5 hrs/day** to reclaim 15+ hours every month.")
        if exer < 3 or sleep < 6.5:
            advice.append("**Stabilize Biological Energy:** Aim for **7–8 hours of sleep** and at least **3 days of exercise** per week.")

        return {
            "ml_probability": ml_prob,
            "ml_label": ml_label,
            "alignment_score": round(score, 1),
            "advice": advice
        }
