📖 Description
AudioSwap is a Python script that allows you to replace the audio track of a video file with the audio track from another video file.

Use case example: You have a Japanese anime episode with French hardcoded subtitles, but you prefer the English audio track. You also have the same episode in English. AudioSwap will take the video (with subtitles) from the Japanese version and the audio from the English version, and combine them into a single file.

🎯 Purpose
This tool is designed for language learners who want to watch content with:

Audio in their target language (e.g., English)

Subtitles in their native language (e.g., French)

By combining the best of both versions, you get an optimal learning experience.

✨ Features
✅ Batch processing – Process multiple files at once

✅ Strict validation – Everything is checked before any processing begins

✅ Duration verification – Ensures audio and video durations match exactly (0 tolerance)

✅ Extension flexibility – Supports mixed video formats (.mp4, .mkv, .avi, .mov, .webm)

✅ Automatic output – Creates a produits_finaux/ directory with numbered files

✅ Conflict handling – Automatically adds suffixes if output files already exist

✅ Clear error reporting – Detailed messages for every issue encountered

✅ Bilingual README – Documentation available in English and French

🧰 Requirements
Python 3.6+

FFmpeg (with ffprobe) – installed and accessible in your PATH

Installing FFmpeg
OS	Command / Instructions
Ubuntu/Debian	sudo apt install ffmpeg
macOS (Homebrew)	brew install ffmpeg
Windows	Download from ffmpeg.org and add to PATH
Verify installation:

bash
ffmpeg -version
ffprobe -version
📁 Project Structure
text
AudioSwap/
├── video/              ← Source videos with subtitles (keep video track)
├── audio/              ← Source videos with desired audio (keep audio track)
├── produits_finaux/    ← Output directory (created automatically)
└── audioswap.py        ← Main script
🚀 Usage
1. Prepare your files
Place your video files in the appropriate directories:

Directory	Content	What is kept
video/	Videos with the subtitles you want (e.g., Japanese version)	Video track only
audio/	Videos with the audio you want (e.g., English version)	Audio track only
Important: Both directories must contain the same number of files, and files are paired in alphabetical order.

2. Run the script
bash
python audioswap.py
3. Follow the prompts
text
Enter the base name for output files: MyAnime
4. Validation
The script performs a complete pre-check before any processing:

FFmpeg/ffprobe are installed

Both directories exist

Each directory contains at least one valid video file

The number of files in both directories is equal

All video durations match exactly (pair by pair)

Output directory can be created/written

If any check fails, the script stops immediately with a clear error message.

5. Output
Files are generated as:

text
produits_finaux/[base_name]_01.mp4
produits_finaux/[base_name]_02.mp4
...
If a file already exists, a suffix is added automatically:

text
produits_finaux/[base_name]_01_1.mp4
🔧 Technical Details
How It Works
Validation phase: All prerequisites and file pairs are verified

Processing phase: For each valid pair:

Extract video stream from video/ file

Extract audio stream from audio/ file

Combine them into a single .mp4 file using FFmpeg

Core FFmpeg Command
The script uses this FFmpeg command (conceptually):

bash
ffmpeg -i video_source.mp4 -i audio_source.mp4 \
       -c:v copy -map 0:v:0 -map 1:a:0 -shortest output.mp4
-c:v copy – Copy video stream without re-encoding (fast)

-map 0:v:0 – Take the first video stream from the first input

-map 1:a:0 – Take the first audio stream from the second input

-shortest – Cut to the shortest duration (safety measure)

Supported Video Extensions
.mp4

.mkv

.avi

.mov

.webm

(You can modify the list in the script if needed)

⚠️ Error Handling
The script performs strict pre-validation. If any of these issues are detected, it stops immediately:

Issue	Message
FFmpeg not installed	❌ ERROR: FFmpeg is not installed or accessible.
Directory missing	❌ ERROR: Directory "video/" not found.
Directory empty	❌ ERROR: Directory "video/" is empty.
Unsupported file	❌ ERROR: "video/image.jpg" is not a supported video file.
File count mismatch	❌ ERROR: video/ has 5 files, audio/ has 3 files.
Duration mismatch	❌ ERROR: Duration mismatch: ep03.mp4 (23.456s) ≠ ep03_EN.mp4 (24.123s).
Write permission	❌ ERROR: Cannot create/write in "produits_finaux/".
📄 License
This project is licensed under the GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later).

This license ensures that:

The source code remains open

Modifications must be shared

Network use is considered distribution

See the LICENSE file for details.

🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request.

Guidelines
Fork the repository

Create a feature branch

Make your changes

Submit a pull request with a clear description

📧 Contact
For questions, suggestions, or issues, please open a GitHub issue.

🌟 Acknowledgments
FFmpeg – The multimedia framework that makes this possible
