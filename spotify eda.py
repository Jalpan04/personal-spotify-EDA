
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import calmap

# --- CONFIGURATION ---
# List of all your streaming history JSON files
FILE_NAMES = [
    'Streaming_History_Audio_2020-2023_0.json',
    'Streaming_History_Audio_2023-2024_1.json',
    'Streaming_History_Audio_2024-2025_2.json',
    'Streaming_History_Audio_2025_3.json'
]

# Set the style and color palette for all plots
sns.set(style="whitegrid")
PALETTE = "viridis"


def load_streaming_data(file_paths):
    """
    Loads and combines multiple Spotify streaming history JSON files.

    Args:
        file_paths (list): A list of strings with the paths to the JSON files.

    Returns:
        pandas.DataFrame: A single DataFrame containing all streaming data,
                          or an empty DataFrame if no files could be loaded.
    """
    list_of_dfs = []
    for file in file_paths:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                list_of_dfs.append(pd.DataFrame(data))
                print(f"Successfully loaded: {file}")
        except FileNotFoundError:
            print(f"Warning: File not found - {file}. Skipping.")
        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON from {file}. Skipping.")

    if not list_of_dfs:
        return pd.DataFrame()

    return pd.concat(list_of_dfs, ignore_index=True)


def preprocess_data(df):
    """
    Cleans and enriches the streaming data DataFrame.

    Args:
        df (pandas.DataFrame): The raw streaming data.

    Returns:
        pandas.DataFrame: The preprocessed DataFrame with new time-based features.
    """
    # Convert timestamp to datetime objects
    df['ts'] = pd.to_datetime(df['ts'])

    # Extract useful time-based features
    df['year'] = df['ts'].dt.year
    df['month'] = df['ts'].dt.month
    df['day_of_week'] = df['ts'].dt.day_name()
    df['hour'] = df['ts'].dt.hour

    # Calculate listening duration in minutes
    df['duration_min'] = df['ms_played'] / 60000

    print("\nData preprocessing complete.")
    return df


def plot_top_charts(df):
    """Generates bar charts for top 10 artists, tracks, and albums by listen time."""
    print("\n--- Generating Top Charts ---")

    # Top 10 Artists by stream count
    top_artists = df['master_metadata_album_artist_name'].value_counts().head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_artists.values, y=top_artists.index, hue=top_artists.index, palette=PALETTE, legend=False)
    plt.title('Top 10 Most Streamed Artists')
    plt.xlabel('Number of Streams')
    plt.ylabel('Artist')
    plt.show()

    # Top 10 Tracks by stream count
    top_tracks = df['master_metadata_track_name'].value_counts().head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_tracks.values, y=top_tracks.index, hue=top_tracks.index, palette=PALETTE, legend=False)
    plt.title('Top 10 Most Streamed Tracks')
    plt.xlabel('Number of Streams')
    plt.ylabel('Track')
    plt.show()

    # Top 10 Albums by total listening time
    album_time = df.groupby('master_metadata_album_album_name')['duration_min'].sum()
    top_albums_time = (album_time / 60).sort_values(ascending=False).head(10)
    plt.figure(figsize=(12, 8))
    sns.barplot(x=top_albums_time.values, y=top_albums_time.index, hue=top_albums_time.index, palette=PALETTE,
                legend=False)
    plt.title('Top 10 Albums by Total Listening Time')
    plt.xlabel('Total Listening Time (Hours)')
    plt.ylabel('Album Name')
    plt.show()


def plot_listening_habits_over_time(df):
    """Generates plots showing listening habits by time (hour, day, heatmap)."""
    print("\n--- Generating Listening Habits Plots ---")

    # Listening by Hour
    plt.figure(figsize=(12, 6))
    sns.countplot(x='hour', data=df, hue='hour', palette=PALETTE, legend=False)
    plt.title('Listening Habits by Hour of the Day')
    plt.xlabel('Hour of the Day (0-23)')
    plt.ylabel('Number of Streams')
    plt.show()

    # Listening by Day
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    plt.figure(figsize=(12, 6))
    sns.countplot(x='day_of_week', data=df, order=day_order, hue='day_of_week', palette=PALETTE, legend=False)
    plt.title('Listening Habits by Day of the Week')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Streams')
    plt.show()

    # Heatmap of Listening Habits
    heatmap_data = df.groupby(['day_of_week', 'hour']).size().unstack(fill_value=0).reindex(day_order)
    plt.figure(figsize=(15, 8))
    sns.heatmap(heatmap_data, cmap=PALETTE, linewidths=.5)
    plt.title('Heatmap of Listening Habits by Day and Hour')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Day of the Week')
    plt.show()


def plot_daily_rhythm(df):
    """Creates a ridge plot showing listening distribution for each day of the week."""
    print("\n--- Generating Daily Rhythm Plot ---")
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    g = sns.FacetGrid(df, row="day_of_week", hue="day_of_week", aspect=6, height=1.2, palette=PALETTE,
                      row_order=day_order)
    g.map(sns.kdeplot, "hour", fill=True, alpha=0.8, lw=2)
    g.map(sns.kdeplot, "hour", color="w", lw=2)

    def label(x, color, label):
        ax = plt.gca()
        ax.text(0, .2, label, fontweight="bold", color=color, ha="left", va="center", transform=ax.transAxes)

    g.map(label, "hour")
    g.fig.subplots_adjust(hspace=-0.5)
    g.set_titles("")
    g.set(yticks=[], ylabel="")
    g.despine(bottom=True, left=True)
    plt.suptitle('Your Daily Listening Rhythm', y=0.98, fontsize=18)
    plt.xlabel('Hour of the Day')
    plt.show()


def plot_track_behavior_analysis(df):
    """Generates plots analyzing track-specific behavior like skips and titles."""
    print("\n--- Generating Track Behavior Analysis ---")

    # Skipped vs. Not Skipped Pie Chart
    skipped_counts = df['skipped'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(skipped_counts, labels=['Not Skipped', 'Skipped'], autopct='%1.1f%%', startangle=140,
            colors=['#c3b1e1', '#66cdaa'])
    plt.title('Skipped vs. Not Skipped Tracks')
    plt.axis('equal')
    plt.show()

    # Proportional Skip Rate by Hour
    skip_data = df.groupby(['hour', 'skipped']).size().unstack(fill_value=0)
    skip_data_percent = skip_data.apply(lambda x: x * 100 / sum(x), axis=1)
    skip_data_percent.plot(kind='bar', stacked=True, color=['#2ca02c', '#d62728'], figsize=(15, 8))
    plt.title('Proportion of Skipped Songs by Hour')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Percentage (%)')
    plt.legend(title='Status', labels=['Not Skipped', 'Skipped'])
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    # Word Cloud of Track Titles
    text = " ".join(track for track in df['master_metadata_track_name'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap=PALETTE,
                          collocations=False).generate(text)
    plt.figure(figsize=(15, 7))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title('Most Common Words in Track Titles')
    plt.show()


def plot_artist_deep_dive(df, top_n_artists=5):
    """Generates deep-dive plots for top artists."""
    print("\n--- Generating Artist Deep Dive ---")

    top_artists = df['master_metadata_album_artist_name'].value_counts().head(top_n_artists).index.tolist()
    df_top_artists = df[df['master_metadata_album_artist_name'].isin(top_artists)]

    # Violin Plot of Song Duration
    plt.figure(figsize=(15, 8))
    sns.violinplot(
        x='master_metadata_album_artist_name',
        y='duration_min',
        data=df_top_artists,
        palette=PALETTE,
        hue='master_metadata_album_artist_name',
        legend=False,
        order=top_artists
    )
    plt.title(f'Song Duration Distribution for Top {top_n_artists} Artists')
    plt.xlabel('Artist')
    plt.ylabel('Listening Duration (Minutes)')
    plt.xticks(rotation=45)
    plt.show()

    # Smoothed Daily Listening Trends
    artist_daily_data = {}
    for artist in top_artists:
        df_artist = df[df['master_metadata_album_artist_name'] == artist].copy()
        daily_streams = df_artist.set_index('ts').resample('D').size()
        smoothed_streams = daily_streams.rolling(window=30, min_periods=1).mean()
        artist_daily_data[artist] = smoothed_streams

    comparison_df = pd.DataFrame(artist_daily_data).fillna(0)
    plt.figure(figsize=(18, 10))
    sns.lineplot(data=comparison_df, dashes=False, lw=2.5, palette=PALETTE)
    plt.title(f'Daily Listening Trends for Top {top_n_artists} Artists (30-Day Smoothed Average)')
    plt.xlabel('Date')
    plt.ylabel('Average Daily Streams (Smoothed)')
    plt.legend(title='Artist')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()


def plot_calendar_heatmap(df):
    """Generates a calendar heatmap of total daily listening minutes."""
    daily_minutes = df.groupby(df['ts'].dt.date)['duration_min'].sum()
    daily_minutes.index = pd.to_datetime(daily_minutes.index)

    fig, axes = calmap.calendarplot(
        daily_minutes, cmap='viridis', fillcolor='lightgrey',
        linewidth=0.5, fig_kws={'figsize': (20, 10)}
    )

    # Corrected line: Use axes[0].collections[0] to get the correct artist
    mappable = axes[0].collections[0]
    fig.colorbar(mappable, ax=axes.ravel().tolist(), orientation='vertical', label='Minutes Played',
                 pad=0.05)

    fig.suptitle("Daily Spotify Listening Time (Minutes)", fontsize=20, y=1.0)
    plt.show()




def main():
    """Main function to run the Spotify EDA."""
    # 1. Load and preprocess data
    df = load_streaming_data(FILE_NAMES)

    # 2. Proceed only if data was loaded successfully
    if df.empty:
        print("\nNo data was loaded. Exiting analysis.")
        return

    df = preprocess_data(df)

    # 3. Generate all visualizations
    plot_top_charts(df)
    plot_listening_habits_over_time(df)
    plot_daily_rhythm(df)
    plot_track_behavior_analysis(df)
    plot_artist_deep_dive(df, top_n_artists=5)
    plot_calendar_heatmap(df)

    print("\n\nAnalysis complete! ✨")


if __name__ == "__main__":
    main()