import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set professional style for charts
sns.set_theme(style="whitegrid")

def load_cleaned_data(path):
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_cleaned_data('cleaned_expenses.csv')

def get_category_totals(dataframe):
    return dataframe.groupby('Category')['Amount'].sum().sort_values(ascending=False)

category_data = get_category_totals(df)

def plot_spending_pie(data):
    plt.figure(figsize=(10, 6))
    data.plot.pie(autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    plt.title('Spending Distribution by Category')
    plt.ylabel('') # Hide the y-label
    plt.tight_layout()
    plt.savefig('spending_pie.png')
    print("Saved spending_pie.png")

plot_spending_pie(category_data)

# Quick check of top expenses
print(category_data.head())
def get_monthly_trend(dataframe):
    monthly = dataframe.resample('M', on='Date')['Amount'].sum()
    return monthly

monthly_trend = get_monthly_trend(df)
def plot_monthly_trend(data):
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=data.index, y=data.values, marker='o', linewidth=2.5)
    plt.title('Spending Trends Over Time')
    plt.xlabel('Month')
    plt.ylabel('Total Spent ($)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('spending_trend.png')

plot_monthly_trend(monthly_trend)
def print_spending_report(dataframe):
    summary = dataframe.groupby('Category').agg({'Amount': ['sum', 'mean', 'count']})
    print("\n--- Final Spending Report ---")
    print(summary)

print_spending_report(df)
plt.rcParams.update({'font.size': 12, 'figure.facecolor': 'white'})
if __name__ == '__main__':
    print("Visualization processing complete. Images saved.")
