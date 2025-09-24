# Spotify Streaming History Analysis

## Project Description

This project provides an in-depth exploratory data analysis (EDA) of personal Spotify streaming history data. The analysis is conducted using Python with data manipulation and visualization libraries such as Pandas, Matplotlib, and Seaborn. The primary goal is to uncover listening patterns, identify favorite artists and tracks, and visualize trends over time.

## Features

The analysis covers several aspects of streaming history, including:
* **Top Charts:** Identification of the most-streamed tracks, artists, and albums.
* **Listening Habits:** Analysis of listening activity by time of day, day of the week, and month.
* **Trend Analysis:** Visualization of streaming duration and frequency over multiple years.
* **Calendar Heatmap:** A daily overview of total listening minutes throughout the year.
* **Artist Deep Dive:** A look into streaming trends for top artists over time.

## Dataset

The data required for this analysis is your personal Spotify data package, which can be requested from Spotify's official website under "Privacy Settings" -> "Download your data".

**Note:** The `.json` data files containing personal streaming history are not included in this repository. They are intentionally excluded via the `.gitignore` file to protect user privacy. You must use your own data files to run this analysis.

## Prerequisites

To run this analysis, you will need Python 3 and the following libraries:

* pandas
* numpy
* matplotlib
* seaborn
* wordcloud
* calmap

You can install all the required libraries with the following command:
```bash
pip install pandas numpy matplotlib seaborn wordcloud calmap
```

## How to Use

To replicate this analysis with your own data, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourUsername/YourRepositoryName.git](https://github.com/YourUsername/YourRepositoryName.git)
    cd YourRepositoryName
    ```

2.  **Obtain your data:** Request and download your data package from Spotify. You will receive several files; locate the ones named `Streaming_History_Audio_....json`.

3.  **Add data to the project:** Place your `Streaming_History_Audio_....json` files into the root directory of this project.

4.  **Update the script:** Open either `spotify eda.py` or `spotify eda.ipynb` and update the list of file names to match the files you just added.
    ```python
    # In the script, find and update this list:
    FILE_NAMES = [
        'Your_File_1.json',
        'Your_File_2.json',
        # ... and so on
    ]
    ```

5.  **Run the analysis:**
    * **For the Python script:**
        ```bash
        python "spotify eda.py"
        ```
    * **For the Jupyter Notebook:**
        Launch Jupyter Lab or Jupyter Notebook and open the `spotify eda.ipynb` file. Run the cells to see the analysis.

## File Structure

* `spotify eda.py`: A Python script containing the full data loading, processing, and visualization pipeline.
* `spotify eda.ipynb`: A Jupyter Notebook with the same analysis, presented in a cell-by-cell format for interactive exploration.
* `.gitignore`: Specifies which files and directories to exclude from version control, such as data files and Python cache.
* `README.md`: This file, providing an overview and instructions for the project.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
