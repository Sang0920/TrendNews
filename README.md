
# TrendNews - News Keyword Extractor API

TrendNews is a Django-based API that extracts keywords from news articles using various algorithms like TF-IDF and LDA. This project provides a simple and efficient way to analyze and extract key terms from news titles in multiple languages.

## Features

- Extract keywords from news titles using TF-IDF or LDA algorithms.
- Supports multiple languages, including English (`en`) and Vietnamese (`vi`).
- Configurable parameters for keyword extraction, such as n-gram range and time period.
- Integration with Google News to fetch the latest articles based on a specified topic and region.

## Installation

### Prerequisites

- Python 3.10+
- Django 5.1
- Other dependencies as listed in `requirements.txt`

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Sang0920/TrendNews.git
   cd TrendNews
   ```

2. Set up a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Django development server:

   ```bash
   python manage.py runserver
   ```

5. Visit `http://127.0.0.1:8000/` in your browser to access the API documentation.

## Usage

### API Endpoints

#### 1. Get Keywords

- **Endpoint:** `/api/keywords`
- **Method:** `GET` or `POST`
- **Description:** Extracts keywords from news titles based on the specified parameters.

**Parameters:**

- `algo` (optional): The algorithm to use for keyword extraction (`TF-IDF` or `LDA`). Default is `TF-IDF`.
- `lang` (optional): The language of the news (`en` for English or `vi` for Vietnamese). Default is `en`.
- `region` (optional): The region to get news from. Default is `US`.
- `topic` (optional): The topic for news extraction. Default is a World topic. Example topics:
  - `CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB`: World
  - `CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB`: Business
  - `CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB`: Technology
- `period` (optional): Number of days to fetch news from. Default is `1`.
- `min_ngram` (optional): Minimum n-gram size for keyword extraction. Default is `5`.
- `max_ngram` (optional): Maximum n-gram size for keyword extraction. Default is `5`.

**Example Request:**

```bash
GET /api/keywords?algo=TF-IDF&lang=en&period=7
```

### Support

For any issues or questions, please contact [dothesang20@gmail.com](mailto:dothesang20@gmail.com).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on [GitHub](https://github.com/Sang0920/TrendNews).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Live deployment
https://trendnews.onrender.com/
