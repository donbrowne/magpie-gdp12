INSTALLATION INSTRUCTIONS:

---Installing Dependencies---

From the magpie directory (or trunk, if pulled from svn) run -

  chmod +x *.sh

Due to the age of the Ubuntu 10.04/10.10 package set, it is necessary to 
use a third party repository to supply an updated version of Python. To 
automatically handle the Python and the other dependencies under these
platforms, run the following -

  sudo ./setup_tenfour.sh
   
For users not running Ubuntu 10.04 or 10.10, the dependencies need to be
manually installed, and the setup_tenfour script should not be run.
Skip to the "Preparing Django" section. A list of dependencies will be 
specified in accompanying documentation. 
  
Once the script is run, the following command should be used instead of 
'python' for starting initializing the Django application -

  python2.7

and all additional Python modules should be installed with -

  sudo easy_install-2.7 <module name>

'python2.7' is used in the rest of this documentation. If you are 
running a distribution of Linux where Python 2.7 is the default, use
'python' instead. In theory, a symlink could be set up between python2.7
and python, but this can cause other applications to break, and is not
recommended.

---Preparing Django---

All users must then run -

  ./setup.sh

On the first run of the application, it is necessary to cd to the 
django_magpie directory, and run -

  python2.7 manage.py syncdb
  cd .. 
  sudo chown -R www-data resources/ sqlite3/

www-data is the Apache user for Ubuntu. This username varies from 
distribution to distribution, consult the OS documentation if in doubt. 

CONFIGURING APACHE

NOTE:
The exact method of configuring Apache varies from one Linux 
distribution to another. The following method is used to configure 
Ubuntu 10.04 and 10.10 For other distributions, the OS documentation 
should be consulted.

The following shorthand will be used in this section, and the
accompanying features.txt, any time you see these mentioned, substitute 
for the appropriate value -

PATH - The path to the magpie-gdp12 folder in the installation tarball
        or the magpie-gdp12-read-only folder if pulling from svn.
HOST - The hostname of your computer
NAME - The subdomain where you want the site to run. If have no
        preference, you can choose whatever you want for this name.

---Hosts---

First off, the hostname for the site must be configured. With your text
editor of choice, open /etc/hosts as root. Insert -

127.0.1.1  NAME.HOST

Some distributions require a fully qualified hostname, in which case -

127.0.1.1 NAME.HOST.localdomain NAME.HOST

This assumes that the Apache installation is set up purely for testing.
If your computer has been configured as a production web server, you 
will need to change the IP and 'localdomain' to match the rest of your
configuration.

---Configuring Apache---

In the folder with this documentation, you will find a template config
file for Apache named apacheConfig. Assuming that the docs folder is the 
current directory, run -

  sudo cp apacheConfig /etc/apache2/sites-available/NAME

Open /etc/apache2/sites-enabled/NAME file with your text editor of 
choice as root. For all occurences of PATH, HOST and NAME, substitute 
them for the appropriate values.

---WSGI Scripts---

Next, in your django_magpie folder, you will find a script named 
'magpie.wsgi', and another named 'auth.wsgi'. Open these files and 
substitute PATH for the value of PATH as described above.

Now run (can be run from any directory) -

  sudo a2ensite NAME
  sudo /etc/init.d/apache2 reload
  
---Viewing the Website---

The site can now be accessed at http://NAME.HOST

If you wish to use Django's manage.py runserver for hosting the site,
note that you will need to take care of hosting the media and static 
files, and configuring settings.py as appropriate.
