# OutsideYT
This program helps YouTubers to upload, download and watch YT videos. 
Program has user-friendly interface, created on library PyQt5. At this moment, it has only dark theme and english language (with some ru comments, but it will be removed).
Functions:
1) You can add some Google Accounts and use the program to automatically download videos and information about them.
2) You can upload videos to added Google Account.
3) You can watch videos by selected users.
4) Standardized type of video information in folders.
6) Save your accounts in cookies and load them when needed.

Technologies used:
- Python 3.11+
- PyQt5 (for interfaces)
- pandas (for working with tables)
- requests, aiohttp, selenium, BeautifulSoup (for parsing)
- asyncio, threads (for asinc queries to the Net, work with main interface without blocking it)
- ffmpeg.exe (for concat video and audio after downloading)
- json (to save accounts info. In the future - change to PostgreSQL)
