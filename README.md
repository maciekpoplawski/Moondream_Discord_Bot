
# Moonsdream Discord Bot

The Moonsdream Discord Bot is an AI-powered bot that allows users to upload an image and ask questions about it. The bot answers with text responses based on the Moondream model. Users can ask multiple questions, and the bot will answer each one based on the context of the uploaded image.

## Installation

Follow these steps to install and set up the Moonsdream Discord Bot:

### Cloning the Moondream  Repository

1. In the main directory, clone the Moondream repository and switch to the required commit:

    ```bash
    git clone https://github.com/vikhyat/moondream.git
    ```
   ```bash
    cd moondream
    ```
   ```bash
    git checkout 3f4815bd86aabb18724d74ef024adeff6c53914e
    ```

### Installing Dependencies

2. **Install Main Dependencies**: Install the requirements from the main directory:

    ```bash
    pip install -r requirements.txt
    ```

3. **Install Moondream Dependencies**: Navigate to the Moondream directory and install its specific requirements:

    ```bash
    cd moondream
    pip install -r requirements.txt
    ```

### Setting Up for GPU Usage (Optional)

4. **GPU Mode Setup**:
   - If you plan to run Moondream in GPU mode, uninstall the existing torch installation:

     ```bash
     pip uninstall torch
     ```

   - Visit [PyTorch's official site](https://pytorch.org/get-started/locally/) and run the latest PyTorch + CUDA command based on your system's configuration.
   - For example:

     ```bash
     pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
     ```

## Starting the Bot

To start the Moonsdream Discord Bot:

1. **Discord Token**: Provide a valid Discord token in the `.env` file under `DISCORD_BOT_TOKEN`.

2. **Database Logging (Optional)**:
   - If you want to log user interactions to a database, first run the [create_db.py](create_db.py) script.
   - Set `collect_interactions_in_db` in [bot.py](bot.py) to `True`.

3. **Run the Bot**: Start the bot by running the [bot.py](bot.py) file:

   ```bash
   python bot.py
   ```

## Bot Functionality

- Users upload an image and can ask questions about it. The bot responds based on the Moondream model's analysis of the image.
- If a question is not asked during the image upload, the bot will ask a default question: "What's in the image?"
- Users can upload a new image at any time, and subsequent questions will be answered based on the new image.
- The bot supports handling user context based on Discord's `user_id`. If the bot is restarted, the context is maintained.
