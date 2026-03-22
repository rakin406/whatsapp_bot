# WhatsApp Bot

This is a Python-based WhatsApp chatbot that uses Selenium for browser automation and Ollama to 
connect with a local Large Language Model (LLM). The bot can join a specified WhatsApp group, 
read incoming messages, generate responses using the LLM, and post them back to the group.

> [!CAUTION]
> You might get banned from WhatsApp.

**[Demo](https://vimeo.com/1175979112?fl=tl&fe=ec)**

## How It Works

The bot operates by automating a headless Chromium browser instance to interact with WhatsApp Web.

1.  **Browser Automation**: It uses Selenium to launch a headless Chromium browser, utilizes your 
existing user profile to handle authentication automatically.
2.  **Group Chat Entry**: The bot joins a target WhatsApp group using the provided invitation link.
3.  **Message Processing**: It continuously monitors the chat for new incoming messages.
4.  **LLM Integration**: When a new message is detected, it is sent as a prompt to a locally running LLM via the Ollama API. 
The `Modelfile` in this repository defines the bot's personality.
5.  **Response Generation**: The LLM generates a response based on the message content and the predefined personality.
6.  **Sending Messages**: The generated response is then typed and sent back to the WhatsApp group.

## Features

*   **Local LLM Integration**: Connects to any LLM supported by Ollama.
*   **Customizable Personality**: Easily define the bot's behavior, tone, and style using the `Modelfile`.
*   **Automated Interaction**: Runs autonomously in a specified WhatsApp group chat.
*   **Headless Operation**: Operates in the background without a visible browser window.
*   **Persistent Session**: Uses your existing Chromium user data to stay logged into WhatsApp.

> [!CAUTION]
> If your main browser is Chromium, you will be logged out of all accounts (except WhatsApp) 
after running this program.

## Prerequisites

Before you begin, ensure you have the following installed and configured:

*   **Python**
*   **Chromium browser**
*   **Logged into WhatsApp Web**: You must be logged into WhatsApp Web on the `Default` profile 
of your Chromium browser. The script will use this session to authenticate.
*   **[Ollama](https://ollama.com/)**: Ollama must be installed and running on your system.
*   **An Ollama Model**: You need to have pulled a model. This bot is configured for `llama3.2`.
    ```bash
    ollama pull llama3.2
    ```

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/rakin406/whatsapp_bot.git
    cd whatsapp_bot
    ```

2.  Install the `uv` package manager if you don't have it:
    ```bash
    pip install uv
    ```

3.  Install project dependencies using `uv`:
    ```bash
    uv sync
    ```

## Configuration

The bot's personality is defined in the `Modelfile`. You need to create a custom Ollama model from this file 
to apply the system prompt and parameters.

Run the following command in your terminal to create a model named `rakinbot`:

```bash
ollama create rakinbot -f Modelfile
```

This command packages the `llama3.2` model with the specific personality instructions into a new, reusable model.

## Usage

To run the bot, execute the `main.py` script with the Ollama model name and the WhatsApp group invitation link as arguments.

**Syntax:**
```bash
python main.py <model-name> <group-invite-link>
```

**Example:**
```bash
python main.py rakinbot "https://chat.whatsapp.com/Gjxxxxxxxxxxxxxxxxxx"
```

The bot will then launch, join the group, send a greeting message, and begin responding to new messages.

## Acknowledgments

* [Ollama's documentation](https://docs.ollama.com/)
* [GitRead](https://www.gitread.dev/)
* [Choose an Open Source License](https://choosealicense.com)

## Contact

Rakin Rahman - rakinrahman406@gmail.com

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](./LICENSE) file for details.
