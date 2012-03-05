echo "Setting up Magpie application instance"
path="$(pwd)"
escaped=${path//\//\\\/}
echo "Using the current working directory as the path to this folder"
echo $path
echo "Please enter the path to the folder from which Apache serves files"
echo "e.g. /home/magpie/public_html/"
echo "If left blank, symlinks to the wsgi script and static/media folders won't be made"
read $fsPath
echo "Please enter the URL that Apache serves this folder as"
echo "e.g. http://proisis.lero.ie/~magpie"
echo "If setting up with the Django test server, you should leave this blank"
echo "DO NOT PLACE A FORWARD SLASH (/) AT THE END OF THE URL"
read $urlPath
cd django_magpie
echo "Configuring wsgi script and settings.py"
sed -i "s/PATH/$escaped/g" ./django_magpie/magpie.wsgi
sed -i "s/INSERT-URL-ROOT/$urlPath/g" ./django_magpie/magpie.wsgi
if [ ! -z $fsPath ]; 
then
    echo "Creating symlinks"
    ln -s ./django_magpie/magpie.wsgi $fsPath/magpie.wsgi
    ln -s ./resources/media $fsPath/media
    ln -s ./resources/static $fsPath/static
fi
echo "Done!"
