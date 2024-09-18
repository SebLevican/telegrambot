# Telegram Bot for Skate Trick Evaluation

This project implements a Telegram bot that allows users to upload videos of skate tricks for analysis. The bot uses pose detection and movement comparison techniques to provide feedback on trick execution.

## Project Files

### 1. `bot.py`

This is the main file that initializes and runs the Telegram bot.

- **Imports**:
  - `os`: For handling environment variables and system operations.
  - `dotenv`: For loading environment variables from a `.env` file.
  - `TelegramBot`: The class that manages the bot's logic.

- **Main Code**:
  - Loads the Telegram token from environment variables.
  - Initializes an instance of `TelegramBot` with the token.
  - Runs the bot.

### 2. `telegram_bot.py`

Contains the implementation of the `TelegramBot` class, which handles the Telegram bot logic.

- **Key Methods**:
  - `__init__(self, token)`: Configures the Telegram bot with the token and an instance of `FeedbackGenerator`.
  - `folder_selected(self, update, context)`: Handles folder selection and displays available `.json` files.
  - `start(self, update, context)`: Displays available folders for selection.
  - `json_selected(self, update, context)`: Handles `.json` file selection and prompts the user to upload a video.
  - `video_handler(self, update, context)`: Handles video uploads and calls `process_trick` to analyze the trick.
  - `process_trick(self, trick_name, video_path, base_folder, update, context)`: Processes the uploaded video, compares the trick with base landmarks, and generates feedback.
  - `welcome_handler(self, update, context)`: Sends a welcome message with information about available commands.
  - `button_handler(self, update, context)`: Handles folder and file selection buttons.

- **`run` Method**:
  - Configures command and message handlers.
  - Starts the bot.

### 3. `feedback_generator.py`

Implements the `FeedbackGenerator` class, which generates feedback on the alignment of key body points in the video.

- **Key Methods**:
  - `__init__(self)`: Defines the names of key body points.
  - `generate_feedback(self, differences)`: Generates comments on misalignments in key points.

### 4. `movement_comparator.py`

Contains the `MovementComparator` class, which compares body key points between the uploaded video and reference landmarks.

- **Key Methods**:
  - `__init__(self, base_landmarks, comparison_landmarks)`: Initializes with base and comparison landmarks.
  - `calculate_differences(self, frame_num, threshold=0.05)`: Calculates differences between base and comparison landmarks for a given frame.
  - `_euclidean_distance(self, point1, point2)`: Computes the Euclidean distance between two points.

### 5. `pose_detector.py`

Implements the `PoseDetector` class, which uses MediaPipe to detect poses in video frames.

- **Key Methods**:
  - `__init__(self)`: Initializes the pose detector.
  - `process_video(self, video_path)`: Processes the video and stores pose landmarks for each frame.
  - `_store_landmarks(self, landmarks)`: Stores pose landmarks as a dictionary.
  - `save_landmarks_to_json(self, output_path)`: Saves detected landmarks to a JSON file.
  - `load_landmarks_from_json(self, input_path)`: Loads landmarks from a JSON file.
