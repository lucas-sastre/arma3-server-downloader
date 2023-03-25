# arma3-server-downloader
This is a docker container with a python script that download steamcmd, arma 3 server and a list of mods (from a file). The python script has a 10 retry for each mod with a cold down timer. 
This container it's ment to be used with https://github.com/Dahlgren/arma-server-web-admin
This container does not run the arma 3 server. It only downloads it.


usage:

docker build -t arma3-server-download
docker run -v [host/dir]:/arma3 -v [host/dir]:/steamcmd arma3-server-download
