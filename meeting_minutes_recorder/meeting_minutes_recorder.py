"""
Meeting Minutes Recorder
Transcribes audio files and generates meeting minutes using AI.

Requirements:
    pip install bitsandbytes
    pip install --upgrade accelerate
    pip install transformers openai huggingface_hub torch python-dotenv

Environment Variables:
    HF_TOKEN: HuggingFace API token (required)
    OPENAI_API_KEY: OpenAI API key (optional, only if using OpenAI transcription)

Usage:
    python meeting_minutes_recorder.py --audio /path/to/audio.mp3
    python meeting_minutes_recorder.py --audio /path/to/audio.mp3 --use-openai
"""

# ============================================================================
# IMPORTS
# ============================================================================

import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer, BitsAndBytesConfig
from transformers import pipeline
import torch


# ============================================================================
# CONSTANTS
# ============================================================================

LLAMA = "meta-llama/Llama-3.2-1B-Instruct"
AUDIO_MODEL = "gpt-4o-mini-transcribe"


# ============================================================================
# SETUP
# ============================================================================

# Load environment variables from .env file
load_dotenv()

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Generate meeting minutes from audio files')
parser.add_argument('--audio', type=str, help='Path to the audio file (default: denver_extract.mp3 in current directory)')
parser.add_argument('--use-openai', action='store_true', help='Use OpenAI for transcription instead of Whisper')
parser.add_argument('--output', type=str, help='Output file path for the meeting minutes')
args = parser.parse_args()

# Use provided audio file or default to denver_extract.mp3
if args.audio:
    audio_filename = args.audio
else:
    # Default to denver_extract.mp3 in the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    audio_filename = os.path.join(script_dir, 'denver_extract.mp3')
    print(f"No audio file specified, using default: {audio_filename}")

# Verify audio file exists
if not os.path.exists(audio_filename):
    raise FileNotFoundError(f"Audio file not found: {audio_filename}")

# Sign in to HuggingFace Hub
hf_token = os.getenv('HF_TOKEN')
if not hf_token:
    raise ValueError("HF_TOKEN environment variable not set. Please set it in your .env file or environment.")
login(hf_token, add_to_git_credential=True)


# ============================================================================
# STEP 1: TRANSCRIBE AUDIO
# ============================================================================

print("Starting transcription...")

if args.use_openai:
    # Option 1: Use OpenAI for Transcription
    print("Using OpenAI for transcription...")
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set. Please set it in your .env file or environment.")
    
    openai_client = OpenAI(api_key=openai_api_key)
    with open(audio_filename, "rb") as audio_file:
        transcription = openai_client.audio.transcriptions.create(
            model=AUDIO_MODEL, 
            file=audio_file, 
            response_format="text"
        )
else:
    # Option 2: Use Open Source Whisper - Hugging Face Pipelines
    print("Using Whisper for transcription...")
    
    # Detect device (CUDA if available, otherwise CPU)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    torch_dtype = torch.float16 if device == 'cuda' else torch.float32
    
    print(f"Running on device: {device}")
    
    pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-small.en",
        torch_dtype=torch_dtype,
        device=device,
        return_timestamps=True
    )
    
    result = pipe(audio_filename)
    transcription = result["text"]

print("\nTranscription completed!")
print("="*80)
print(transcription)
print("="*80 + "\n")


# ============================================================================
# STEP 2: ANALYZE & REPORT
# ============================================================================

print("Generating meeting minutes...")

# Prepare prompts for meeting minutes generation
system_message = """
You produce minutes of meetings from transcripts, with summary, key discussion points,
takeaways and action items with owners, in markdown format without code blocks.
"""

user_prompt = f"""
Below is an extract transcript of a meeting.
Please write minutes in markdown without code blocks, including:
- a summary with attendees, location and date
- discussion points
- takeaways
- action items with owners

Transcription:
{transcription}
"""

messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_prompt}
]

# Load model and generate meeting minutes
print("Loading Llama model (this may take a while on first run)...")
tokenizer = AutoTokenizer.from_pretrained(LLAMA)
tokenizer.pad_token = tokenizer.eos_token

# Detect device and move inputs accordingly
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Loading model on device: {device}")

# Load model without device_map to avoid accelerate dependency
model = AutoModelForCausalLM.from_pretrained(LLAMA, torch_dtype=torch.float32 if device == 'cpu' else torch.float16)
model = model.to(device)

inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to(device)

streamer = TextStreamer(tokenizer)
outputs = model.generate(inputs, max_new_tokens=700, streamer=streamer)

# Decode response
response = tokenizer.decode(outputs[0])

# Extract the actual meeting minutes (remove the prompt part)
# The response often contains the full conversation, so we try to extract just the assistant's response
if "<|start_header_id|>assistant<|end_header_id|>" in response:
    response = response.split("<|start_header_id|>assistant<|end_header_id|>")[-1]
    response = response.replace("<|eot_id|>", "").strip()

print("\n" + "="*80)
print("MEETING MINUTES")
print("="*80 + "\n")
print(response)

# Save to file if output path is specified
if args.output:
    with open(args.output, 'w') as f:
        f.write(response)
    print(f"\n\nMeeting minutes saved to: {args.output}")

