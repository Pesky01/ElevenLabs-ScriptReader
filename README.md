# ScriptReader

A quick & dirty tool to convert an annotated dialogue text file into an MP3 using the ElevenLabs API.

## Requirements

- **ffmpeg**
- **Python 3.9+**
- **uv** – A fast Python project manager  
  - **macOS/Linux:**  
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```  
  - **Windows:**  
    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

## Setup

1. **Clone the repo:**
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Set your API key:**  
   Create a `.env` file in the repo root with:
   ```
   ELEVENLABS_API_KEY=your_api_key_here
   ```

3. **Update voice IDs:**  
   Edit `main.py` if needed to update the `SPEAKER_VOICE_MAP` with your voice IDs.

## Usage

Prepare an input file (e.g., `input.txt`) with lines like:
```
[Roger] It looks like it's going to rain.
[Aria] No, I don't think so.
```

Then run:
```bash
uv run main.py input.txt output.mp3
```

Your output audio will be saved as `output.mp3`.
