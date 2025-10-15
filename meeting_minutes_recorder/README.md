# Meeting Minutes Recorder

Automatically transcribe audio files from meetings and generate well-formatted meeting minutes using AI.

## Features

- 🎙️ **Audio Transcription**: Choose between open-source Whisper or OpenAI's transcription API
- 📝 **AI-Powered Minutes**: Automatically generates structured meeting minutes including:
  - Summary with attendees, location, and date
  - Key discussion points
  - Takeaways
  - Action items with owners
- 💾 **Flexible Output**: Print to console or save to file
- 🚀 **Portable**: Runs on CPU or GPU (CUDA)

## Prerequisites

- Python 3.8 or higher
- CUDA-capable GPU (optional, for faster processing)
- HuggingFace account and API token
- OpenAI API key (optional, only if using OpenAI transcription)

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd meeting_minutes_recorder
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp env.example .env
```

4. Edit `.env` and add your API tokens:
   - `HF_TOKEN`: Get from [HuggingFace Settings](https://huggingface.co/settings/tokens)
   - `OPENAI_API_KEY`: Get from [OpenAI Platform](https://platform.openai.com/api-keys) (optional)

## Usage

### Basic Usage (Default Audio File)

If you have `denver_extract.mp3` in the same directory:

```bash
python meeting_minutes_recorder.py
```

### Basic Usage (Custom Audio File)

```bash
python meeting_minutes_recorder.py --audio /path/to/your/audio.mp3
```

### Using OpenAI for Transcription

```bash
python meeting_minutes_recorder.py --audio /path/to/your/audio.mp3 --use-openai
```

### Save Output to File

```bash
python meeting_minutes_recorder.py --audio /path/to/your/audio.mp3 --output minutes.txt
```

## Command-Line Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--audio` | No | Path to the audio file to transcribe (default: `denver_extract.mp3` in script directory) |
| `--use-openai` | No | Use OpenAI for transcription instead of Whisper |
| `--output` | No | Output file path for the meeting minutes |

## Supported Audio Formats

- MP3
- WAV
- M4A
- OGG
- FLAC
- AAC

## How It Works

1. **Transcription**: The audio file is transcribed using either:
   - **Whisper** (open-source): Runs locally using HuggingFace's transformer pipeline (default: `openai/whisper-small.en` for speed)
   - **OpenAI**: Uses OpenAI's transcription API

2. **Minutes Generation**: The transcription is processed by Meta's Llama 3.2 model to generate structured meeting minutes (default: `meta-llama/Llama-3.2-1B-Instruct`)

## Performance Notes

- **GPU Processing**: If you have a CUDA-capable GPU, the script will automatically use it for faster processing
- **CPU Processing**: The script will fall back to CPU if no GPU is available (slower but functional)
- **Model Size**: The default smaller models are faster and lighter:
- Whisper small: ~0.5GB
- Llama 3.2 1B: ~2GB

### Runtime expectations

- First run can take a while because models are downloaded to your machine and then loaded into memory before any work starts.
- Without a GPU, both transcription and minutes generation execute on the CPU, which is significantly slower. Subsequent runs are faster since models are cached locally.

## Troubleshooting

### "CUDA out of memory" error
- Try using OpenAI transcription: `--use-openai`
- Or reduce your audio file length

### Slow processing on CPU
- Consider using OpenAI transcription for faster results
- Or use a smaller Whisper model (modify `openai/whisper-medium.en` to `openai/whisper-small.en` in the code)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- OpenAI Whisper for speech recognition
- Meta Llama for text generation
- HuggingFace for the transformers library

