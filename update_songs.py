import os
import csv
import hashlib

def generate_song_id(album, title, path):
    unique_string = f"{album}:{title}:{path}"
    return hashlib.md5(unique_string.encode('utf-8')).hexdigest()[:8]

def scan_audio_files(base_path='docs/audio'):
    songs = []
    for album in os.listdir(base_path):
        album_path = os.path.join(base_path, album)
        if os.path.isdir(album_path):
            for file in os.listdir(album_path):
                if file.endswith(('.mp3', '.m4a')):
                    title = os.path.splitext(file)[0]
                    songs.append({
                        'album': album,
                        'title': title,
                        'path': f"audio/{album}/{file}"
                    })
    return songs

def update_songs_mapping(songs, csv_path='songs_mapping.csv'):
    existing_songs = {}
    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_songs[row['path']] = row

    new_songs = []
    for song in songs:
        if song['path'] not in existing_songs:
            song_id = generate_song_id(song['album'], song['title'], song['path'])
            new_songs.append({
                'song_id': song_id,
                'album': song['album'],
                'title': song['title'],
                'artist': 'กาญจน์ลดา มฤคพิทักษ์',
                'path': song['path']
            })

    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['song_id', 'album', 'title', 'artist', 'path'])
        writer.writeheader()
        writer.writerows(existing_songs.values())
        writer.writerows(new_songs)

    print(f"Updated {csv_path} with {len(new_songs)} new songs.")

if __name__ == "__main__":
    songs = scan_audio_files()
    update_songs_mapping(songs)
