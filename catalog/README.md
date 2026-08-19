# catalog/

Metti qui la lista dei video.

## File

Sorgente di verità: `../video.txt` (già nel repo, 265 URL).

`video-urls.txt` resta solo come eventuale coda extra.

Righe vuote e righe che iniziano con `#` vengono ignorate.

Formati accettati:

```
https://www.youtube.com/watch?v=xxxxxxxxxxx
https://youtu.be/xxxxxxxxxxx
https://www.youtube.com/shorts/xxxxxxxxxxx
xxxxxxxxxxx
```

Quando il file è su GitHub, Fama lancia `scripts/ingest_urls.py`.
