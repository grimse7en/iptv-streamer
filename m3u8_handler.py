import os
import m3u8

def create_m3u8(videos_directory):
    # List all video files in the directory
    video_files = [f for f in os.listdir(videos_directory) if os.path.isfile(os.path.join(videos_directory, f))]
    
    # Create a new m3u8 object
    m3u8_obj = m3u8.M3U8()
    
    # Add each video file to the m3u8 object
    for video in video_files:
        m3u8_obj.add_segment(m3u8.Segment(uri=os.path.join(videos_directory, video)))
    
    # Save the m3u8 file
    m3u8_path = os.path.join(videos_directory, 'playlist.m3u8')
    with open(m3u8_path, 'w') as f:
        f.write(m3u8_obj.dumps())
    
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
    
    # If the entry_path is found, modify the segments list
    if current_index is not None:
        m3u8_obj.segments = m3u8.SegmentList(m3u8_obj.segments[current_index:])

        # Save the updated m3u8 file
        with open(m3u8_path, 'w') as f:
            f.write(m3u8_obj.dumps())
        
        print(f"Trimmed m3u8 playlist at {m3u8_path} so that {entry_path} is the first entry.")
    else:
        print(f"Entry {entry_path} not found in the m3u8 file.")

# Example usage
if __name__ == "__main__":
    videos_directory = 'path/to/videos'
    create_m3u8(videos_directory)
    
    m3u8_path = 'path/to/playlist.m3u8'
    entry_path = 'path/to/current/file.ts'
    trim_m3u8(m3u8_path, entry_path)
