# Video-Editor-CLI

Video Editor CLI is a powerful command-line tool for video editing.

## Features

- **Add Videos**: Add video files to your project.
- **Define Segments**: Specify segments of each video to include in the final render.
- **List Videos**: Display all added videos with their index and filename.
- **List Segments**: Display all defined segments with video indices and filenames.
- **Set Segment Order**: Arrange segments in the desired order for the final edit.
- **Randomize Segment Order**: Arrange segments in a random order for the final edit.
- **Auto Montage**: Automatically create segments for each video by removing 2 seconds from the beginning and end, and arrange them in the order of the videos.
- **Merge Videos**: Concatenate the defined segments and apply a fade-out transition at the end of the film.
- **Show Statistics**: View the number of segments, the duration of each segment, and the total duration of the film.

## Installation

### Prerequisites

Ensure that Python is installed on your machine. You can download Python from [Python.org](https://www.python.org/downloads/).

### Installing Dependencies

Open your terminal and run the following commands to install the necessary libraries:

pip install click moviepy PyQt5


### Available Commands

1.  **Add Videos**
    
    *   Select videos to add to your project (supported formats: **.mp4**, **.avi**, **.mov**, **.mkv**).
        
2.  **Add a Segment**
    
    *   Enter the index of the video (starting from 1).
        
    *   Enter the start and end time of the segment in seconds or minutes(e.g., **1.30** for 1 minute and 30 seconds).
        
3.  **List Videos**
    
    *   Display all loaded videos with their index and filename.
        
4.  **List Segments**
    
    *   Display all defined segments for each video with video indices and filenames.
        
5.  **Set Segment Order**
    
    *   Enter the order of segments as pairs **video\_index:segment\_index**, separated by commas (e.g., **1:1,2:1,1:2**).
        
6.  **Randomize Segment Order**
    
    *   Arrange segments in a random order for the final edit.
        
7.  **Auto Montage**
    
    *   Automatically create segments for each video by removing 2 seconds from the beginning and end, and arrange them in the order of the videos.
        
8.  **Merge Videos**
    
    *   Concatenate the defined segments in the specified order and create the final video with a 4-second fade-out transition at the end.
        
9.  **Show Statistics**
    
    *   Display the total number of segments, the duration of each segment, and the total duration of the final video.
        
10.  **Quit**
    
    *   Close the interactive menu.
        

### Example Usage

1.  **Add two videos**:
    
    *   Video 1: **video1.mp4**
        
    *   Video 2: **video2.mp4**
        
2.  **Add segments**:
    
    *   Segment 1 of Video 1: start at **0s**, end at **10s**
        
    *   Segment 1 of Video 2: start at **1m30s**, end at **2m**
        
3.  **Set the segment order**:
    
    *   Order: **1:1,2:1**
        
4.  **List videos and segments for verification**
    
5.  **Show statistics**
    
6.  **Merge videos**:
    
    *   Output filename: **output.mp4**
        

Contributing
------------

Contributions are welcome! Please submit a pull request or open an issue to discuss the changes you would like to make.

License
-------

This project is licensed under the MIT License
