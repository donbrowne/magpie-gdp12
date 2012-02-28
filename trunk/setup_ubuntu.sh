if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root"
   exit 1
else
   echo "Setting up Magpie dependencies for Ubuntu"
fi
apt-get --yes remove python-django
apt-get update
apt-get --yes install graphviz apache2-threaded-dev flex bison apache2-mpm-worker libapache2-mod-wsgi python-pip
pip install pydot django ordereddict
wget http://people.apache.org/~pquerna/modules/mod_flvx.c
apxs2 -i -a -c mod_flvx.c
rm -r mod_flvx*
rm pip-log.txt
/etc/init.d/apache2 restart
