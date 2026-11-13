import pandas as pd
import numpy as np

class MillionaireAnalytics:
    """
    Object-Oriented Data Science Engine for the Orphan Rise Roadmap.
    Encapsulates all descriptive metrics derived from the Millionaire cohort.
    """
    
    def __init__(self, csv_path: str = 'optimized_dataset.csv'):
        # Load the dataset and automatically isolate the Millionaire cohort (Net Worth >= $1M)
        self.df_raw = pd.read_csv(csv_path)
        self.millionaires = self.df_raw[self.df_raw['net_worth'] >= 1000000].copy()
        self.total_millionaires = len(self.millionaires)
        
    def _to_binary(self, series: pd.Series) -> pd.Series:
        """Helper method to safely convert text flags ('Yes', 'Daily', 'No', 'Never') into 1 or 0."""
        return series.apply(
            lambda x: 0 if pd.isna(x) or str(x).lower().strip() in ['no', 'never', '0', '0.0', 'false', 'unknown', 'none'] else 1
        )

    def _float_to_clock(self, val: float) -> str:
        """Helper method to convert decimal hours (e.g., 5.5) into readable clock time (05:30 AM)."""
        if pd.isna(val):
            return "N/A"
        hours = int(val)
        minutes = int(round((val - hours) * 60))
        if minutes == 60:
            hours += 1
            minutes = 0
        period = "AM" if hours < 12 or hours == 24 else "PM"
        display_hour = hours if hours <= 12 else hours - 12
        if display_hour == 0:
            display_hour = 12
        return f"{display_hour:02d}:{minutes:02d} {period}"

    # 1. Percentage of millionaires reading books yearly (> 0 books)
    def get_reading_percentage(self) -> float:
        books = pd.to_numeric(self.millionaires['books_read_per_year'], errors='coerce').fillna(0)
        readers_count = (books > 0).sum()
        return round((readers_count / self.total_millionaires) * 100, 2) if self.total_millionaires > 0 else 0.0

    # 2. Average number of books read per year
    def get_average_books_read(self) -> float:
        books = pd.to_numeric(self.millionaires['books_read_per_year'], errors='coerce').fillna(0)
        return round(books.mean(), 1)

    # 3. Millionaires using at least 1 of the 7 planning/tracking tools (and average tools out of 7)
    def get_planning_adoption_stats(self) -> dict:
        cols_7 = [
            'daily_planning', 'weekly_planning', 'planning_minutes_per_day',
            'monthly_goal_review', 'goal_tracking_frequency',
            'calendar_usage', 'to_do_list_usage'
        ]
        score_matrix = pd.DataFrame(index=self.millionaires.index)
        for col in cols_7:
            if col in self.millionaires.columns:
                if col == 'planning_minutes_per_day':
                    score_matrix[col] = (pd.to_numeric(self.millionaires[col], errors='coerce').fillna(0) > 0).astype(int)
                else:
                    score_matrix[col] = self._to_binary(self.millionaires[col])
        
        total_tools_used = score_matrix.sum(axis=1)
        active_planners = (total_tools_used >= 1).sum()
        pct_active = round((active_planners / self.total_millionaires) * 100, 2) if self.total_millionaires > 0 else 0.0
        avg_tools = round(total_tools_used.mean(), 1)
        
        return {
            "active_count": int(active_planners),
            "active_percentage": pct_active,
            "average_tools_out_of_7": avg_tools
        }

    # 4. Wake-up time range (Earliest to Latest)
    def get_wakeup_range(self) -> dict:
        wake_series = pd.to_numeric(self.millionaires['wake_up_time'], errors='coerce').dropna()
        earliest = wake_series.min()
        latest = wake_series.max()
        return {
            "earliest_clock": self._float_to_clock(earliest),
            "latest_clock": self._float_to_clock(latest),
            "average_clock": self._float_to_clock(wake_series.mean())
        }

    # 5. Sleep duration range (Minimum to Maximum hours)
    def get_sleep_range(self) -> dict:
        sleep_series = pd.to_numeric(self.millionaires['sleep_duration_hours'], errors='coerce').dropna()
        return {
            "min_hours": round(sleep_series.min(), 1),
            "max_hours": round(sleep_series.max(), 1),
            "avg_hours": round(sleep_series.mean(), 1)
        }

    # 6. Percentage of millionaires giving to charity (> $0)
    def get_charity_givers_percentage(self) -> float:
        charity = pd.to_numeric(self.millionaires['annual_charity_donations'], errors='coerce').fillna(0)
        givers_count = (charity > 0).sum()
        return round((givers_count / self.total_millionaires) * 100, 2) if self.total_millionaires > 0 else 0.0

    # 7. Average annual charity money donated (across donors or full cohort)
    def get_average_charity_amount(self, donors_only: bool = True) -> float:
        charity = pd.to_numeric(self.millionaires['annual_charity_donations'], errors='coerce').fillna(0)
        if donors_only:
            donors = charity[charity > 0]
            return round(donors.mean(), 2) if len(donors) > 0 else 0.0
        return round(charity.mean(), 2)

    # 8. Prepare Wealth-Tier Work Hours for Business Owners
    def get_business_owner_work_by_wealth(self) -> pd.Series:
        df = self.millionaires.copy()
        df['net_worth'] = pd.to_numeric(df['net_worth'], errors='coerce').fillna(0)
        df['deep_work_hours_per_day'] = pd.to_numeric(df['deep_work_hours_per_day'], errors='coerce').fillna(0)
        
        owners = df[df['business_owner'].apply(
            lambda x: str(x).lower().strip() not in ['0', '0.0', 'no', 'false', 'none', 'unknown', 'nan']
        )].copy()
        
        owners['Wealth_Tier'] = pd.cut(
            owners['net_worth'],
            bins=[999999, 2000000, 5000000, 10000000, float('inf')],
            labels=['$1M–$2M', '$2M–$5M', '$5M–$10M', '$10M+']
        )
        return owners.groupby('Wealth_Tier')['deep_work_hours_per_day'].mean()

    # 9. Prepare Time Management Tiers vs. Productivity
    def get_productivity_by_time_management(self) -> pd.Series:
        df = self.millionaires.copy()
        df['time_management_score'] = pd.to_numeric(df['time_management_score'], errors='coerce').fillna(0)
        df['daily_productivity_score'] = pd.to_numeric(df['daily_productivity_score'], errors='coerce').fillna(0)
        
        df['TM_Tier'] = pd.cut(
            df['time_management_score'],
            bins=[-1, 40, 60, 80, 100],
            labels=['Low (0–40)', 'Moderate (41–60)', 'High (61–80)', 'Elite (81–100)']
        )
        return df.groupby('TM_Tier')['daily_productivity_score'].mean()

    # 10. Get Formatted Wealth-Ordered Leaderboard Table
    def get_wealth_leaderboard(self, top_n: int = 50) -> pd.DataFrame:
        df = self.millionaires.copy()
        for col in ['net_worth', 'total_annual_income', 'annual_charity_donations', 'deep_work_hours_per_day', 'books_read_per_year', 'time_management_score']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        df['Role_Type'] = df['business_owner'].apply(
            lambda x: 'Business Owners' if str(x).lower().strip() not in ['0', '0.0', 'no', 'false', 'none', 'unknown', 'nan'] else 'Salaried / Executives'
        )
        
        cols = ['synthetic_person_id', 'net_worth', 'total_annual_income', 'annual_charity_donations', 'industry', 'Role_Type', 'deep_work_hours_per_day', 'books_read_per_year', 'time_management_score']
        available = [c for c in cols if c in df.columns]
        sorted_df = df.sort_values(by='net_worth', ascending=False)[available].head(top_n).reset_index(drop=True)
        
        sorted_df.rename(columns={
            'synthetic_person_id': 'Person ID',
            'net_worth': 'Net Worth ($)',
            'total_annual_income': 'Annual Income ($)',
            'annual_charity_donations': 'Charity Given ($)',
            'industry': 'Industry',
            'Role_Type': 'Career Path',
            'deep_work_hours_per_day': 'Deep Work (Hrs/Day)',
            'books_read_per_year': 'Books / Year',
            'time_management_score': 'Time Mgmt Score'
        }, inplace=True)

        for money_col in ['Net Worth ($)', 'Annual Income ($)', 'Charity Given ($)']:
            if money_col in sorted_df.columns:
                sorted_df[money_col] = sorted_df[money_col].apply(lambda x: f"${x:,.2f}")
        return sorted_df
