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

## Installation 💻

### Step 1: Clone the Repository

Clone this repository to your local machine using:


```bash
git clone https://github.com/EmilianoMojica08/Google-Hawk.git
```

THEN

```bash
cd google-hawk
```



### Step 2: Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables

You need to configure your environment variables for Google and OpenAI API keys. Create a `.env` file in the project root and add your credentials:

```makefile
API_KEY_GOOGLE=your_google_api_key
SEARCH_ENGINE_ID=your_custom_search_engine_id
OPENAI_API_KEY=your_openai_api_key
```

## Usage

### Basic Search

You can perform a basic Google Dork search by running:

```bash
python main.py -q "site:example.com filetype:pdf"
```

### AI-Powered Dork Generation

Generate a Google Dork automatically using a natural language description:

```bash
python main.py -gd "Find PDF files on cybersecurity published in 2023"
```

You will be prompted to choose between OpenAI or a local AI model for generating the Dork.

### Automated Browser Search

To perform a search using Selenium (for example, if the API has usage limits):

```bash
python main.py -q "site:example.com filetype:pdf" --selenium
```

This will open a browser window, conduct the search, and extract the results automatically.

### Local File Search with SmartSearch

The SmartSearch feature in Google Hawk allows you to search within local files for specific patterns or information using either regular expressions (regex) or AI-generated responses based on prompts. This is particularly useful when you need to analyze large datasets or documents for specific terms, patterns, or content that may not be easily searchable using simple text search.

#### Regex Search
Regular Expression (Regex) Search allows you to search for patterns within the contents of files. Regular expressions are powerful tools that enable complex pattern matching within text. Here's how you can use this feature:

```bash
python main.py --smartsearch-file "path/to/your/files" --smartsearch-regex "\\bcybersecurity\\b"
```
##### Explanation


--**smartsearch-file **"path/to/your/files": This argument specifies the directory or file where the search will be conducted. Replace "path/to/your/files" with the actual path to the directory or file you want to search within.

--**smartsearch-regex **"\\bcybersecurity\\b": This argument uses a regular expression to search for occurrences of the word "cybersecurity". The \\b in the regex is a word boundary anchor, which ensures that the search matches the whole word "cybersecurity" rather than part of a longer word.



**Example Use Case**: If you have a directory filled with log files or documents and you want to find every instance where the word "cybersecurity" is mentioned, you would use the command above. The tool will scan through each file in the specified directory, look for matches to the regex, and return the results.

#### AI-Prompt Search
AI-Prompt Search allows you to leverage AI to interpret and search through the contents of your files based on a natural language prompt. This is particularly useful when you're looking for more complex patterns or information that would be difficult to capture with a regex.

```bash
python main.py --smartsearch-file "path/to/your/files" --smartsearch-prompt "Search for cybersecurity incidents in these documents"
```
##### Explanation

--**smartsearch-file** "path/to/your/files": This argument, just like in the regex search, specifies the directory or file where the AI will perform its analysis. Replace "path/to/your/files" with the actual path to the directory or file.

--**smartsearch-prompt** "Search for cybersecurity incidents in these documents": This argument provides a natural language prompt that the AI will use to search through the files. In this case, you're asking the AI to identify and report any references to cybersecurity incidents within the documents.

**Example Use Case**: Suppose you have a collection of internal reports or emails and you want to identify discussions or reports related to cybersecurity incidents. By providing this prompt, the AI will analyze the content of each file, understand the context, and return relevant sections or summaries that match the intent of your query.

**Output**
For both search methods, the results are typically printed to the console. Depending on how you've set up the tool, the results could also be saved to a file for further analysis. If matches are found, they will be displayed along with the file names where they were located, making it easy for you to pinpoint exactly where in your documents the relevant information is found.

These tools empower you to conduct both precise and broad searches across your local files, making it a powerful feature in your cybersecurity toolkit.


### GUI Operation

For users who prefer a graphical interface, simply run:

```bash
python search_gui.py
```

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
