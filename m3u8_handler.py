import os
import m3u8
import random

def create_m3u8(videos_directory):
    # List all video files in the directory with specified extensions
    video_files = [f for f in os.listdir(videos_directory) 
                   if f.endswith(('.mkv', '.mp4', '.webm')) 
                   and os.path.isfile(os.path.join(videos_directory, f))]
    
    # Randomize the order of the video files
    random.shuffle(video_files)
    
    # Create a new m3u8 object
    m3u8_obj = m3u8.M3U8()
    
    # Add each video file to the m3u8 object with #EXTINF tag
    for video in video_files:
        video_path = os.path.join(videos_directory, video)
        segment = m3u8.Segment(
            uri=f'file://{video_path}',  # Using file URI scheme
            title=video,
            duration=-1  # Setting duration as -1 for now
        )
        m3u8_obj.segments.append(segment)
    
    # Create the m3u8 content
    m3u8_content = "#EXTM3U\n"
    for segment in m3u8_obj.segments:
        m3u8_content += f'#EXTINF:-1, {segment.title}\n{segment.uri}\n'
    
    # Save the m3u8 file
    m3u8_path = os.path.join(videos_directory, 'playlist.m3u8')
    with open(m3u8_path, 'w') as f:
        f.write(m3u8_content)
    
    print(f"Created m3u8 playlist at {m3u8_path}")

def trim_m3u8(m3u8_path, entry_path):
    # Load the existing m3u8 file
    m3u8_obj = m3u8.load(m3u8_path)
    
    # Find the index of the segment that matches the entry_path
    current_index = None
    for i, segment in enumerate(m3u8_obj.segments):
        if segment.uri == f"file://{entry_path}":
            current_index = i
            break
    
    # If the entry_path is found and is not the first entry, modify the segments list
    if current_index is not None:
        if current_index == 0:
            print(f"Entry {entry_path} is already the first entry in the m3u8 file. No trimming needed.")
            return
        
        m3u8_obj.segments = m3u8.SegmentList(m3u8_obj.segments[current_index:])

        # Save the updated m3u8 file
        with open(m3u8_path, 'w') as f:
            f.write(m3u8_obj.dumps())
        
        print(f"Trimmed m3u8 playlist at {m3u8_path} so that {entry_path} is the first entry.")
    else:
        print(f"Entry {entry_path} not found in the m3u8 file.")
