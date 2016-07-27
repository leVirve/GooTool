# GooTool
A wrapper for auth and make services with newest Google API.

###開發環境
- Python 3.4+

###Dependencies
- Install Google official client
- setup install/develop this project

```
$> pip install --upgrade google-api-python-client

$> python setup.py install
```

### Example
- This is a code to fetch information of videos in each of your playlists.

```python
import json

from gootool.youtube import YoutubeMe


if __name__ == '__main__':
    youtube = YoutubeMe()
    results = youtube.get_playlists()
    with open('youtube-lists.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

```

- This is an example to make use of `DriveMan` to fetch metadata and download file.

```python
from gootool.drive import DriveMan


if __name__ == '__main__':
    drive = DriveMan()
    metadata = drive.get_metadata('{File Hash ID here}')
    
    drive.dowload('{File Hash ID here}')

```

---

###必要檔案：
OAuth Client 需要提供可供 Resource server (Google) 辨識資料，詳細請查 Wikipedia  [OAuth](https://zh.wikipedia.org/wiki/OAuth)

`client_secret.json`：請至 [Google 開發者中心](https://console.developers.google.com/project)申請。[詳細說明](https://developers.google.com/drive/web/about-auth)
