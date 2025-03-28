# informatikans-bot

# How to run the bot

1. Fork and clone the repository

    ```bash
    git clone <your-fork-url>
    ```

2. Create a virtual environment and activate it

    ```bash
    cd informatikans-bot
    python -m venv venv
    ```

    or if you are using `uv`:

    ```bash
    uv venv
    ```

    Then activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

3. Install the requirements: `pip install -r requirements.txt` or `uv pip install -r requirements.txt`
4. Create a `.env` file in the root directory and add your bot token and other environment variables. You can use the `.env.example` file as a template.
5. Run the bot: `python main.py`
