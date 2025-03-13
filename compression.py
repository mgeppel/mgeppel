import subprocess
import os
import ffmpeg

def compress_audio(input_file, output_file, target_size_mb=5, bitrate="128k", codec="mp3"):
    """
    Compress an audio file using FFmpeg.
    
    :param input_file: Path to input audio file (e.g., WAV, MP3, FLAC)
    :param output_file: Path to output compressed audio file
    :param target_size_mb: Desired file size in MB (approximate)
    :param bitrate: Audio bitrate (e.g., '128k' for 128 kbps)
    :param codec: Output codec ('mp3', 'aac', 'flac')
    """
    try:
        # Probe the audio to get metadata
        probe = ffmpeg.probe(input_file)
        duration = float(probe['format']['duration'])  # Duration in seconds
        audio_stream = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
        sample_rate = int(audio_stream.get('sample_rate', 44100))  # Default to 44.1 kHz if not found
        
        # Calculate target bitrate if not specified, based on target size
        if bitrate == "auto":
            target_size_bits = target_size_mb * 8 * 1024 * 1024  # Convert MB to bits
            target_bitrate = int(target_size_bits / duration)  # Bits per second
            bitrate = f"{target_bitrate}k"  # Convert to kbps format (e.g., "128k")
        else:
            target_bitrate = int(bitrate.replace("k", "")) * 1000  # Convert "128k" to 128000 bps
        
        # Validate bitrate
        if target_bitrate < 32000:  # Minimum reasonable bitrate (32 kbps)
            raise ValueError("Calculated bitrate too low for decent quality.")
        
        # Codec-specific settings
        if codec == "mp3":
            codec_opt = "libmp3lame"
            format_opt = "mp3"
        elif codec == "aac":
            codec_opt = "aac"
            format_opt = "mp4"  # AAC typically uses MP4 container
        elif codec == "flac":
            codec_opt = "flac"
            format_opt = "flac"
            bitrate = None  # FLAC doesn't use bitrate; it's lossless
        else:
            raise ValueError("Unsupported codec. Use 'mp3', 'aac', or 'flac'.")
        
        # FFmpeg command
        stream = ffmpeg.input(input_file)
        output_args = {
            "c:a": codec_opt,
            "b:a": bitrate if bitrate else None,  # Bitrate for lossy, None for lossless
            "ar": str(sample_rate),  # Preserve sample rate
            "format": format_opt,
            "y": True  # Overwrite output without asking
        }
        stream = ffmpeg.output(stream, output_file, **{k: v for k, v in output_args.items() if v is not None})
        
        # Run the FFmpeg command
        ffmpeg.run(stream, quiet=True)
        
        # Verify output file size
        output_size_mb = os.path.getsize(output_file) / (1024 * 1024)
        print(f"Compressed file size: {output_size_mb:.2f} MB")
        print(f"Output saved as: {output_file}")
        
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode()}")
    except Exception as e:
        print(f"Error: {str(e)}")

# Example usage
if __name__ == "__main__":
    input_audio = "input_audio.wav"  # Replace with your audio file
    output_audio = "output_compressed.mp3"
    
    if not os.path.exists(input_audio):
        print("Input file not found!")
    else:
        # Compress to ~5 MB MP3 with 128 kbps
        compress_audio(input_audio, output_audio, target_size_mb=5, bitrate="128k", codec="mp3")
        
        # Alternative: Compress with automatic bitrate calculation
        # compress_audio(input_audio, "output_auto.mp3", target_size_mb=5, bitrate="auto", codec="mp3")
        
        # Alternative: Lossless FLAC
        # compress_audio(input_audio, "output_lossless.flac", target_size_mb=None, bitrate=None, codec="flac")