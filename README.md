# Google Hawk: Automated Search and Data Analysis Tool Powered by AI

**Google Hawk** is an advanced tool for ethical hacking and data analysis, developed to streamline the process of conducting Google searches with Google Dorks, enhanced by AI-powered dork generation. This tool is ideal for cybersecurity professionals and data analysts looking to extract critical information efficiently and effectively.


## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Search](#basic-search)
  - [AI-Powered Dork Generation](#ai-powered-dork-generation)
  - [Automated Browser Search](#automated-browser-search)
  - [Local File Search with SmartSearch](#local-file-search-with-smartsearch)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Automated Google Dorks**: Perform advanced Google searches using predefined or AI-generated Google Dorks.
- **AI-Powered Dork Generation**: Generate Google Dorks based on natural language descriptions using models like OpenAI's GPT.
- **Intuitive GUI**: User-friendly graphical interface built with `tkinter` for easy operation without command-line usage.
- **Automated Browser Search**: Utilize Selenium to perform automated searches directly within a browser, bypassing API limitations.
- **SmartSearch**: Advanced search within local files using regex or AI prompts, enabling detailed analysis of large datasets.

## Installation

### Step 1: Clone the Repository

Clone this repository to your local machine using:

\```bash
git clone https://github.com/your-username/google-hawk.git
cd google-hawk
\```

### Step 2: Install Dependencies

Install the required Python packages using `pip`:

\```bash
pip install -r requirements.txt
\```

### Step 3: Set Up Environment Variables

You need to configure your environment variables for Google and OpenAI API keys. Create a `.env` file in the project root and add your credentials:

\```makefile
API_KEY_GOOGLE=your_google_api_key
SEARCH_ENGINE_ID=your_custom_search_engine_id
OPENAI_API_KEY=your_openai_api_key
\```

## Usage

### Basic Search

You can perform a basic Google Dork search by running:

\```bash
python main.py -q "site:example.com filetype:pdf"
\```

### AI-Powered Dork Generation

Generate a Google Dork automatically using a natural language description:

\```bash
python main.py -gd "Find PDF files on cybersecurity published in 2023"
\```

You will be prompted to choose between OpenAI or a local AI model for generating the Dork.

### Automated Browser Search

To perform a search using Selenium (for example, if the API has usage limits):

\```bash
python main.py -q "site:example.com filetype:pdf" --selenium
\```

This will open a browser window, conduct the search, and extract the results automatically.

### Local File Search with SmartSearch

Search within local files using regex or AI:

#### Regex Search

\```bash
python main.py --smartsearch-file "path/to/your/files" --smartsearch-regex "\\bcybersecurity\\b"
\```

#### AI-Prompt Search

\```bash
python main.py --smartsearch-file "path/to/your/files" --smartsearch-prompt "Search for cybersecurity incidents in these documents"
\```

### GUI Operation

For users who prefer a graphical interface, simply run:

\```bash
python search_gui.py
\```

This will launch the `tkinter`-based GUI, where you can easily navigate and configure your searches.

## Requirements

- **Python 3.8+**
- **API Keys**: 
  - [Google API Key](https://developers.google.com/custom-search/v1/overview)
  - [OpenAI API Key](https://beta.openai.com/signup/)
- **Packages**:
  - `selenium`, `tkinter`, `openai`, `gpt4all`, among others (see `requirements.txt` for full list).

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
"""
