# Smart QnA Bot with Memory

## Overview

This project is a conversational assistant built using **LangChain**. It can fetch weather information and perform Wikipedia searches, all while remembering previous interactions with users. The bot is powered by the `ChatOpenAI` model and integrates a memory buffer for contextual conversations. The project also includes a simple **GUI** built with **Panel** to allow users to interact with the bot.

---

## Features

- **Weather Information**: Fetches the current weather of a location using Open-Meteo API based on latitude and longitude.
- **Wikipedia Search**: Allows users to search Wikipedia and retrieve page summaries.
- **Memory**: Remembers previous interactions and responses, providing a personalized experience.
- **Sassy Assistant**: The bot is programmed with a playful and engaging tone to create an interactive experience.
- **Interactive GUI**: A graphical interface built with **Panel** for real-time interaction with the assistant.

---

## Installation

To get started with the project, clone this repository to your local machine.

```bash
git clone https://github.com/yourusername/smart-qna-bot-with-memory.git
cd smart-qna-bot-with-memory
```

## Requirements
Make sure to install the required dependencies:


## How to Run
To run the bot locally:

1. Ensure that you have installed all required dependencies (listed in requirements.txt).

2. Run the Python script using the command:

```bash
python main.py
```
3. The bot's user interface will open, allowing you to interact with the assistant and ask questions related to weather or Wikipedia search.

## Usage
Once the bot is running, you can input queries such as:
- "What is the weather in Vellore?"
- "What is LangChain?"
- "Tell me about Python programming"

The bot will respond with the relevant weather information or a Wikipedia summary. It remembers prior conversations, so you can ask follow-up questions like:
- "Where is Vellore?"
- "What did I ask you earlier?"

## Contributing
Contributions are welcome! If you want to contribute to this project, please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
- LangChain: A framework for developing applications powered by LLMs.
- OpenAI: For providing the ChatGPT model used in this project.
- Open-Meteo: For providing weather data via their API.
- Wikipedia API: For accessing Wikipedia page summaries.
- Panel: For building the GUI interface.

## Contact
For any questions or issues, feel free to open an issue or reach out to me at [anandmanikandan652@gmail.com].

