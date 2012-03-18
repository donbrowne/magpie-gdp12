case "$1" in
        build)
mkdir sqlite3
cp ./dataload/magpie.db ./sqlite3/
cd pml
make
cd ..
cd django_magpie
python manage.py collectstatic
cd ..
            ;;
        install)
echo "Setting up Magpie application instance"
path="$(pwd)"
escaped=${path//\//\\\/}
echo "Using the current working directory as the path to this folder"
echo $path
echo "Please enter the path to the folder from which Apache serves files"
echo "e.g. /home/magpie/public_html"
echo "If left blank, symlinks to the wsgi script and static/media folders won't be made"
read fsPath
echo "Configuring wsgi script and settings.py"

if [ ! -z $fsPath ]; 
then
    echo "Creating symlinks"
    cd $fsPath
    ln -s $path/django_magpie/magpie.wsgi magpie.wsgi
    ln -s $path/resources/media media
    ln -s $path/resources/static static
fi
echo "Done!"
            ;;
        clean)
cd pml
make clean
cd ..
            ;;
        distclean)
rm -rf sqlite3
rm -rf ./resources/static/*
echo "Please enter the path to the folder from which Apache serves files"
echo "e.g. /home/magpie/public_html/"
echo "If left blank, symlinks to the wsgi script and static/media folders won't be deleted"
read public_path

if [ ! -z $fsPath ]; 
then
    echo "Destroying symlinks"
    rm $public_path/magpie.wsgi
    rm $public_path/media
    rm $public_path/static
fi

            ;;
        test)
cd django_magpie
python manage.py test
cd ..
            ;;
         
        *)
            echo $"Usage: $0 {build|clean|install|test|distclean}"
            exit 1
esac
