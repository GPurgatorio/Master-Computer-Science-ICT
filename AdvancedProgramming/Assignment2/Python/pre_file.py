import urllib.request
import urllib.parse

params = urllib.parse.urlencode({"message": "I <3 Advanced Programming! :)", "format": "text"}).encode("ascii")

with urllib.request.urlopen("http://cowsay.morecode.org/say", params) as f:
    print(f.read().decode("ascii"))

