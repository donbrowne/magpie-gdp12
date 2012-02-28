#!/bin/bash
if [ "$(id -u)" -ne "0" ]; then
   echo "This script must be run as root"
   exit 1
fi

if [ ! -e sqlite3 ]; then
   echo "Database folder not found"
   echo "You have either run this from the wrong folder, or your"
   echo "Database does not exist"
   exit 1
else
   echo "Setting up Magpie application instance with Apache"
fi

path="$(pwd)"
escaped=${path//\//\\\/}
echo "Using the current working directory as the path to this folder"
echo $path
echo "Using the following hostname as the hostname:"
hostname="$(hostname)"
echo $hostname
echo "Please specify the subdomain of the host where you would like"
echo "the application to be served (ie. the 'foo' in http://foo.myhost)"
echo "Will default to 'magpie' if left blank"
read appname
echo "Enter the IP address for this computer. If you do not have any" 
echo "specific IP address requirements, leave this field blank so that"
echo "it defaults to 127.0.1.1"
read ipaddr

if [ -z $appname ]; 
then
     echo "Defaulting to magpie"
     appname="magpie"
fi

#!/bin/bash
if [ -e /etc/apache2/sites-available/$appname ]; then
   echo "ERROR! A site with this name already exists"
   echo "Re-run this script and use another subdomain name!"
   exit 1
else
   echo "Configuring /etc/hosts"
fi

if [ -z $ipaddr ]; 
then
     echo "Defaulting to 127.0.1.1"
     ipaddr="127.0.1.1"
fi

echo "$ipaddr    $appname.$hostname" >> /etc/hosts
echo "Configuring" /etc/apache2/sites-available/$appname
cp ./docs/apacheConfig /etc/apache2/sites-available/$appname
sed -i "s/PATH/$escaped/g" /etc/apache2/sites-available/$appname
sed -i "s/NAME/$appname/g" /etc/apache2/sites-available/$appname
sed -i "s/HOST/$hostname/g" /etc/apache2/sites-available/$appname
echo "Configuring wsgi scripts"
sed -i "s/PATH/$escaped/g" ./django_magpie/auth.wsgi
sed -i "s/PATH/$escaped/g" ./django_magpie/magpie.wsgi
echo "chown'ing the database and media folders"
chown -R www-data sqlite3/ resources/

echo "Restarting Apache"
a2ensite magpie
/etc/init.d/apache2 restart

echo "Building PML tools"
cd ./pml
make
make clean
cd ..

echo "Done!"
echo "Site can be accessed from " "http://"$appname"."$hostname
