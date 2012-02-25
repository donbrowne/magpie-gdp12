if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root"
   exit 1
else
   echo "Setting up Magpie dependencies for Ubuntu 10.04/10.10"
fi
add-apt-repository ppa:fkrull/deadsnakes
apt-get update
apt-get --yes install python2.7 graphviz python-distribute-deadsnakes apache2-threaded-dev python2.7-dev flex bison apache2-mpm-worker libapache2-mod-wsgi
easy_install-2.7 pydot django
wget http://modwsgi.googlecode.com/files/mod_wsgi-3.3.tar.gz
tar -xzvf mod_wsgi-3.3.tar.gz
cd mod_wsgi-3.3
./configure --with-python=/usr/bin/python2.7
make
make install
make clean
wget http://people.apache.org/~pquerna/modules/mod_flvx.c
apxs2 -i -a -c mod_flvx.c
rm mod_flvx.c
/etc/init.d/apache2 reload
cd ..
rm -rf mod_wsgi-3.3*
