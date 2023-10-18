
# OutsideYT
This program helps YouTubers to upload, download and watch YT videos. 
Program has user-friendly interface, created on library PyQt5. At this moment, it has only dark theme and english language (with some ru comments, but it will be removed).
Functions:
1) You can add some Google Accounts and use the program to automatically download videos and information about them.
2) You can upload videos to added Google Account.
3) You can watch videos by selected users.
4) Standardized type of video information in folders.
6) Save your accounts in cookies and load them when needed.

**Technologies used**:
- Python 3.11+
- PyQt5 (for interfaces)
- pandas (for working with tables)
- requests, aiohttp, playwright, selenium, BeautifulSoup (for parsing)
- asyncio, threads (for asinc queries to the Net, work with main interface without blocking it)
- ffmpeg.exe (for concat video and audio after downloading)
- json (to save accounts info. In the future - change to PostgreSQL)

**Installation:**
You need to download the package and install all libs from requirements.txt.
After that you need to start *download_driver.bat* to download Chrome browser  for working program.
To start OutsideYT run *OutsideYT.py*.
**Default Settings**
Project folder contains:

 - /videos - the folder in which the program will search for videos for your accounts. When you add a new account, a folder with your account's name is created in the videos/ folder. These folders will store videos in Universal format. Additionally, you can store your videos everywhere and add videos to the program using File Explorer, but if you store them in standard folder,  adding videos can be faster and easier.
 - outside - main folder of module. There are common modules for work OutsideYT and:
 - outside/bin - folder with necessary programs for OutsideYT to work.
 - outiside/oyt_info - folder with information about YouTube accounts and OutsideYT settings. 
 - outside/views_py and outside/views_ui - folders with the design of the main windows (in Python code and Qt Designer ui format)
 - outside/YT - folder with modules for working with YouTube and the network.
 - outside/Upload, outside/Download and outside/Watch - modules for the 3 main functions of OutsideYT: uploading, downloading and watching.
 
 **Feedback**
 If you want to use OutsideYT and have any questions, or find errors (or you want to offer me a job)) you can write me on outside.fedkov@gmail.com.
 
**Screenshots of OutsideYT**
Upload Page
![image](https://github.com/Outsider-corp/OutsideYT/assets/75440954/0ceacfa9-d2d8-4903-8abe-bec5e2dac5ab)

Watch Page
![image](https://github.com/Outsider-corp/OutsideYT/assets/75440954/0e03693a-e7ca-4876-910d-94152d79449e)

Download Page
![image](https://github.com/Outsider-corp/OutsideYT/assets/75440954/6647b393-fd8f-44cc-bfe2-1cfb594b7734)

