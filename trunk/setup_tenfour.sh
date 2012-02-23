if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root"
   exit 1
else
   echo "Setting up Python environment for Ubuntu 10.04"
fi
add-apt-repository ppa:fkrull/deadsnakes
apt-get update
apt-get --yes install python2.7 graphviz python-distribute-deadsnakes apache2-threaded-dev python2.7-dev
easy_install-2.7 pydot django
wget http://modwsgi.googlecode.com/files/mod_wsgi-3.3.tar.gz
tar -xzvf mod_wsgi-3.3.tar.gz
cd mod_wsgi-3.3
./configure --with-python=/usr/bin/python2.7
make
make install
make clean
/etc/init.d/apache2 reload
cd ..
rm -rf mod_wsgi-3.3*
