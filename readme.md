# MediaFire Free Folder Downloader

**Disclaimer**  
I take no responsibility for the use of this script.

**Note**  
This is a project made quickly, so don't pay too much attention to the code quality.

I hope this can be useful to someone.

## Usage

1. Clone the repository and run the script with Python 3.
```bash
git clone https://github.com/Hider-alt/MediaFireDownload
cd MediaFireDownload
```

2. Edit the url variable in main.py with the MediaFire folder URL you want to download.
3. Run main.py
```bash
python main.py
```
4. You will find the downloaded files in the folder "output" in the same directory as main.py.

---

By default the script waits 2 seconds between each download. You can change this by editing the sleep_per_download 
parameter in ```MediaFireAPI(sleep_per_download=2)``` in main.py. <br>
Decreasing this value will make the script faster, but it will be more likely to get blocked by MediaFire. 
(I don't know the exact value to set to not get blocked, but I recommend not going below 1 second.)