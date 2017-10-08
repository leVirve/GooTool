import json

from gootool.youtube import YoutubeMe


if __name__ == '__main__':
    youtube = YoutubeMe(
        credential='./.credentials/youtube-credential.json',
        client_secret='./client_secret.json',
        )
    results = youtube.get_playlists()
    with open('youtube-lists.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
