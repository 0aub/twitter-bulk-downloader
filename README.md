# twitter-bulk-downloader
download all user media and favorites by user URL page

# prerequisites 
you should check your chrome version if it is compatible with chromedriver.exe
<br>
if your browser version is not compatible with the driver, you should download a new driver that works with you
<br>
chrome driver download page: https://chromedriver.chromium.org/downloads

# usage
to run the script, you need to provide it with your Twitter login info in addition to the target page
```
python twitter_dl.py --url [target url page] --username [your email or username] --password [your password] --media --likes
OR
python twitter_dl.py -url [target url page] -u [your email or username] -p [your password] -m -l
```

# notes
- if you run the script for the first time, it may ask you for the confirmation code that sent to your email
- I think the browser/driver compatibility is the only issue you may face
- please let me know if you had any issues with the script


<br><br><br><br><br><br><br>
*Feel free to write any suggestions you think about.*
