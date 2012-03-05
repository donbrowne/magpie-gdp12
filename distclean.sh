rm -rf sqlite3
rm -rf ./resources/static/*
rm -rf ./resources/media/*
echo "Please enter the path to the folder from which Apache serves files"
echo "e.g. /home/magpie/public_html/"
echo "If left blank, symlinks to the wsgi script and static/media folders won't be deleted"
read $public_path
rm $public_path/magpie.wsgi
rm $public_path/media
rm $public_path/static
if [ ! -z $fsPath ]; 
then
    echo "Destroying symlinks"
    rm $public_path/magpie.wsgi
    rm $public_path/media
    rm $public_path/static
fi
