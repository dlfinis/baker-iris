# Baker Iris

Baker Iris is a project designed to process audio, generate transcriptions, and provide responses using language models. It is optimized for technical interviews and leverages tools like SpaCy, Ollama, `python-dotenv`, and more.

## Features

- Real-time audio processing.
- Transcription and response generation using language models.
- Support for SpaCy models and environment variable configuration.
- Support Ollama for the connection with local LLMs.

---

## Prerequisites

Before starting, ensure you have the following installed:

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/)
- Python 3.9 or higher

---

## Installation

1. **Clone this repository**:
   ```bash
   git clone <REPOSITORY_URL>
   cd baker-iris
   ```

2. **Create a Conda environment**:
   ```bash
   conda create -n baker-iris python=3.9 -y
   conda activate baker-iris
   ```

3. **Install dependencies**:
   Use the `requirements.txt` file to install dependencies with `pip` inside the Conda environment:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root and define the following variables:
   ```env
   GROQ_API_KEY=<your_api_key>
   WHISPER_MODEL_NAME=<whisper_model_name>
   MODEL_NAME=<llm_model_name>
   ```

5. **Download SpaCy models**:
   ```bash
   python setup_spacy.py
   ```

---

## Usage

1. **Activate the Conda environment**:
   ```bash
   conda activate baker-iris
   ```

2. **Run the initial setup**:
   ```bash
   python setup_start.py
   ```

3. **Start the application**:
   If you have a main script to start the application, run it:
   ```bash
   python main.py
   ```

---

## Project Structure

```plaintext
baker-iris/
├── iris_base.py         # Main logic for audio processing and response generation
├── setup_spacy.py       # Setup and installation of SpaCy models
├── setup_start.py       # Initial project setup
├── requirements.txt     # Project dependencies
├── .env                 # Environment variables (not included in the repository)
└── README.md            # Project documentation
```

---

## Key Dependencies

The project uses the following dependencies:

- **groq**: For processing language models.
- **keyboard**: For handling keyboard input.
- **numpy**: For mathematical operations and data handling.
- **python-dotenv**: For managing environment variables.
- **sounddevice**: For audio processing.
- **spacy**: For natural language processing.
- **webrtcvad**: For voice activity detection in audio.
- **ollama**: For local access of llms.

---

## Contributing

If you want to contribute to the project:

1. Fork the repository.
2. Create a branch for your feature (`git checkout -b feature/new-feature`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Submit a pull request.

---

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the `LICENSE` file for details.

### Adjustments for Conda:
1. **Environment Creation**:
   - Added instructions to create and activate a Conda environment using `conda create` and `conda activate`.

2. **Dependency Installation**:
   - Dependencies are installed using `pip install -r requirements.txt` inside the Conda environment.

3. **Environment Activation**:
   - Reminded users to activate the Conda environment before running any scripts.
