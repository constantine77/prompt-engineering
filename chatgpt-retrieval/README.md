# chatgpt-retrieval

Simple script to use ChatGPT on your own files.

## Installation

Install [Langchain](https://github.com/hwchase17/langchain) and other required packages.
```
pip install langchain openai chromadb tiktoken beautifulsoup4
```
Modify `constants.py` to use your own [OpenAI API key](https://platform.openai.com/account/api-keys).

Place your own data into `data.txt`.

## Example usage
```
> python chatgpt.py "what is valuebale advice authore shares for young people"
```
