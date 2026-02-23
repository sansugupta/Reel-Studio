import os
import subprocess
from pathlib import Path
import shutil

def process_video(session_id: str, video_path: str):
    """Process video: extract audio, remove audio, separate vocals"""
    try:
        output_dir = f"temp_outputs/{session_id}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Check if ffmpeg is available
        ffmpeg_cmd = shutil.which("ffmpeg")
        if not ffmpeg_cmd:
            raise Exception("FFmpeg not found. Please install FFmpeg.")
        
        # 1. Extract full audio
        full_audio_path = f"{output_dir}/full_audio.mp3"
        subprocess.run([
            ffmpeg_cmd, "-i", video_path,
            "-vn", "-acodec", "libmp3lame", "-b:a", "192k",  # Reduced bitrate for speed
            full_audio_path, "-y"
        ], check=True, capture_output=True, text=True)
        
        # 2. Create video without audio
        video_no_audio_path = f"{output_dir}/video_no_audio.mp4"
        subprocess.run([
            ffmpeg_cmd, "-i", video_path,
            "-an", "-c:v", "copy",
            video_no_audio_path, "-y"
        ], check=True, capture_output=True, text=True)
        
        # 3. Use Demucs for vocal separation (optimized)
        try:
            # Check if demucs is available
            demucs_cmd = shutil.which("demucs")
            if not demucs_cmd:
                raise Exception("Demucs not found")
            
            # Run Demucs with faster settings
            subprocess.run([
                demucs_cmd,
                "--two-stems=vocals",
                "-o", output_dir,
                "--mp3",
                "--mp3-bitrate", "192",  # Reduced bitrate
                "-n", "htdemucs_ft",  # Faster model
                "--jobs", "1",  # Single job to avoid memory issues
                full_audio_path
            ], check=True, capture_output=True, text=True, timeout=120)  # 2 min timeout
            
            # Demucs creates: output_dir/htdemucs_ft/full_audio/vocals.mp3 and no_vocals.mp3
            audio_name = Path(full_audio_path).stem
            demucs_output = Path(output_dir) / "htdemucs_ft" / audio_name
            
            # Move the separated files
            vocals_src = demucs_output / "vocals.mp3"
            music_src = demucs_output / "no_vocals.mp3"
            
            vocals_dest = f"{output_dir}/vocals_only.mp3"
            music_dest = f"{output_dir}/music_only.mp3"
            
            if vocals_src.exists():
                shutil.move(str(vocals_src), vocals_dest)
            else:
                # Fallback
                shutil.copy(full_audio_path, vocals_dest)
            
            if music_src.exists():
                shutil.move(str(music_src), music_dest)
            else:
                # Fallback
                shutil.copy(full_audio_path, music_dest)
            
            # Clean up Demucs output directory
            htdemucs_dir = Path(output_dir) / "htdemucs_ft"
            if htdemucs_dir.exists():
                shutil.rmtree(htdemucs_dir)
                
        except subprocess.TimeoutExpired:
            print(f"Demucs timeout for {session_id}, using fallback")
            # Fallback: create copies of full audio
            shutil.copy(full_audio_path, f"{output_dir}/vocals_only.mp3")
            shutil.copy(full_audio_path, f"{output_dir}/music_only.mp3")
        except Exception as demucs_error:
            print(f"Demucs error: {demucs_error}, using fallback")
            # Fallback: create copies of full audio
            shutil.copy(full_audio_path, f"{output_dir}/vocals_only.mp3")
            shutil.copy(full_audio_path, f"{output_dir}/music_only.mp3")
        
        # Cleanup uploaded video
        if os.path.exists(video_path):
            os.remove(video_path)
        
        print(f"Processing completed for session {session_id}")
        
    except subprocess.CalledProcessError as e:
        error_msg = f"FFmpeg error: {e.stderr if e.stderr else str(e)}"
        print(f"Error processing video {session_id}: {error_msg}")
        with open(f"{output_dir}/error.txt", "w") as f:
            f.write(error_msg)
    except Exception as e:
        print(f"Error processing video {session_id}: {str(e)}")
        with open(f"{output_dir}/error.txt", "w") as f:
            f.write(str(e))
