import pandas as pd
import matplotlib.pyplot as plt

# Set year
YEAR = 2025

# Load and preprocess data 
df = pd.read_csv("sum_by_time_complete.csv", names=["timestamp", "count"])
df["timestamp"] = pd.to_datetime(df["timestamp"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
df = df.dropna(subset=["timestamp"])

df["year"] = df["timestamp"].dt.year
df["month_num"] = df["timestamp"].dt.month
df["month"] = df["timestamp"].dt.month_name()
df["date"] = df["timestamp"].dt.date
df["hour"] = df["timestamp"].dt.hour + df["timestamp"].dt.minute / 60
df["day_of_week"] = df["timestamp"].dt.day_name()
df["weekday"] = df["timestamp"].dt.day_name()
df["week"] = df["timestamp"].dt.to_period("W").apply(lambda r: r.start_time)
df["is_weekend"] = df["timestamp"].dt.dayofweek >= 5

weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
df_year = df[df["year"] == YEAR].copy()

# --- Plot 1: Line plot by hour and day of week ---
counts_by_hour = df_year.groupby(["hour", "day_of_week"])["count"].sum().unstack(fill_value=0)
counts_by_hour = counts_by_hour.reindex(columns=weekday_order)
plt.figure(figsize=(12, 6))
for day in counts_by_hour.columns:
    plt.plot(counts_by_hour.index, counts_by_hour[day], label=day)
plt.xlabel("Hour of Day")
plt.ylabel("Number of Rides")
plt.title(f"Rides by Hour and Day of Week ({YEAR})")
plt.xticks(range(0, 25))
plt.legend(title="Day of Week")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f"plots/plot01_rides_by_hour_and_day_{YEAR}.png")
plt.close()

# --- Plot 2: Bar plot by weekday ---
total_by_weekday = df_year.groupby("day_of_week")["count"].sum().reindex(weekday_order)
plt.figure(figsize=(10, 6))
plt.bar(total_by_weekday.index, total_by_weekday.values)
plt.title(f"Total Number of Rides per Weekday ({YEAR})")
plt.xlabel("Weekday")
plt.ylabel("Total Rides")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"plots/plot02_rides_per_weekday_bar_{YEAR}.png")
plt.close()

# --- Plot 3: Average Daily Ride Count by Month (All Years) ---
daily_avg = df.groupby(["year", "month_num", "month"]).agg({"count": "sum", "date": "nunique"}).reset_index()
daily_avg["avg_per_day"] = daily_avg["count"] / daily_avg["date"]
monthly_avg = daily_avg.groupby(["month_num", "month"])["avg_per_day"].mean().reset_index()
monthly_avg = monthly_avg.sort_values("month_num")
plt.figure(figsize=(10, 6))
plt.bar(monthly_avg["month"], monthly_avg["avg_per_day"])
plt.title("Average Daily Rides per Month (All Years)")
plt.xlabel("Month")
plt.ylabel("Avg Rides per Day")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("plots/plot03_avg_daily_rides_per_month.png")
plt.close()

# --- Plot 4: Heatmap of Rides by Weekday and Hour (All Years) ---
pivot = df.groupby(["weekday", df["timestamp"].dt.hour])["count"].sum().unstack(fill_value=0)
pivot = pivot.reindex(index=weekday_order)
plt.figure(figsize=(12, 6))
plt.imshow(pivot, aspect="auto", cmap="YlOrRd")
plt.colorbar(label="Total Rides")
plt.xticks(range(24), range(24))
plt.yticks(range(7), pivot.index)
plt.title("Heatmap of Rides by Weekday and Hour (All Years)")
plt.xlabel("Hour of Day")
plt.ylabel("Weekday")
plt.tight_layout()
plt.savefig("plots/plot04_heatmap_weekday_hour.png")
plt.close()

# --- Plot 5: Hourly Ride Patterns by Year ---
hourly_by_year = df.groupby(["year", df["timestamp"].dt.hour])["count"].sum().unstack(fill_value=0)
plt.figure(figsize=(14, 6))
for year in sorted(hourly_by_year.index):
    plt.plot(hourly_by_year.columns, hourly_by_year.loc[year], label=year)
plt.title("Hourly Ride Patterns by Year")
plt.xlabel("Hour of Day")
plt.ylabel("Total Rides")
plt.legend(title="Year", fontsize="small")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("plots/plot05_hourly_patterns_by_year.png")
plt.close()

# --- Plot 6: Weekday vs Weekend Hourly Patterns ---
hourly_split = df.groupby([df["timestamp"].dt.hour, "is_weekend"])["count"].sum().unstack(fill_value=0)
plt.figure(figsize=(12, 6))
plt.plot(hourly_split.index, hourly_split[False], label="Weekday", linewidth=2)
plt.plot(hourly_split.index, hourly_split[True], label="Weekend", linewidth=2)
plt.title("Rides by Hour: Weekday vs Weekend")
plt.xlabel("Hour of Day")
plt.ylabel("Total Rides")
plt.xticks(range(0, 24))
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("plots/plot06_rides_by_hour_weekday_vs_weekend.png")
plt.close()

# --- Plot 7: Top 10 Busiest Days for Rides ---
daily_counts = df.groupby("date")["count"].sum().reset_index()
top_days = daily_counts.sort_values("count", ascending=False).head(10)
plt.figure(figsize=(12, 6))
plt.bar(top_days["date"].astype(str), top_days["count"])
plt.xticks(rotation=45)
plt.title("Top 10 Busiest Days for Rides")
plt.xlabel("Date")
plt.ylabel("Total Rides")
plt.tight_layout()
plt.savefig("plots/plot07_top_10_busiest_days.png")
plt.close()

# --- Plot 8: Weekly Ride Totals Over Time ---
weekly_counts = df.groupby("week")["count"].sum().reset_index()
plt.figure(figsize=(14, 6))
plt.plot(weekly_counts["week"], weekly_counts["count"], linewidth=1.2)
plt.title("Weekly Total Rides Over Time")
plt.xlabel("Week")
plt.ylabel("Total Rides")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("plots/plot08_rides_weekly_trend.png")
plt.close()
