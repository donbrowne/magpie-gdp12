-MAGPIE README-

DESCRIPTION -

Magpie -  Model Advice Guidance Process Intergration Explorer
A software system specifically designed for knowledge management of 
information relating to software processes. Magpie is hosted on a server 
and can be accessed and administered from a web browser. When 
configured, Magpie will ask users a series of yes/no questions and based 
on this can infer a list of recommendations for the user.
Recommendations that provide the process modeling information can 
contain a mix of various multimedia formats such as images, video, 
rendered PML models, hyperlinks etc.

DEPENDENCIES -

The following packages need to be installed for this application to work

For the installation of Python modules, it is recommended that the user
uses a Python module installer such as python-pip to install the Python
modules. This ensures that the modules are up to date.

---Main Application---

Python 2.7 (or Python 2.6 with the ordereddicts module)
Django 1.3 (a Python module)
mod_wsgi

---Graphing---

Graphviz
Pydot (a Python module)
flex
bison
libxml2 (a Python module)
libxslt (a Python module)

---Video---

A module named mod_flvx is used to stream videos from Apache. To install
this module, first run -

  wget http://people.apache.org/~pquerna/modules/mod_flvx.c
  
The Ubuntu packages apache2-threaded-dev and apache2-mpm-worker are 
needed for the next step. For other distributions, you should find the 
suitable equivalents.

Run as root -

  apxs2 -i -a -c mod_flvx.c

(apxs2 may be named differently under different distributions)
And then restart Apache.

INSTALLATION -

The folder in which this readme is contained should not be located in 
the document root of Apache, but can otherwise be located where the user
wishes.

Make sure the directory containing this README is your current working
directory. Run the following (where the path following DESTDIR should be 
the file system path to the folder that serves as the Apache document 
root, or a subdirectory of that folder. DESTDIR must exist, the makefile 
will check if the folder exists, and terminate if it does not) -

  make install DESTDIR=/home/magpie/public_html/
  
Alternatively, the user can edit the Makefile, and set the DESTDIR
variable as desired. It defaults to the current working directory.
  
This will copy the default database and puts it in the application 
database folder, builds the PML tools, and create the symlinks to  
django_magpie/magpie.wsgi and the resources/static and resources/media 
folders to the folder specified by DESTDIR. If the user wants to start
with a blank database, or they wish to reset the database at any time, 
and get rid of all the uploaded media files, they should run -

  make reset

The installation process will set permissions so that the user and group
of the file have full access, but they are otherwise inaccessible by
other users. The user must make sure that the Apache user (called 
'www-data' in Ubuntu) is either the owner or in the group of the file.
One posible solution is to run -

  sudo chgrp -R www-data resources/
  sudo chgrp -R www-data static/
  
The install stage of the script will symlink the wsgi script, as well
as the media and static files folders to the DESTDIR folder. The page 
can be accessed by navigating to the URL where that folder is served, 
and launching the wsgi script. It also copies a htaccess file to that
directory, containing -

  Options +ExecCGI 
  AddHandler wsgi-script .wsgi
  
After the install, the resources/media/ folder contains a .htaccess
file to serve FLV videos.
  
Details of features can be found at -

http://code.google.com/p/magpie-gdp12/wiki/Features

When using either the sample database, or the when the database has been
reset using make reset, the admin user is -
  
  Username: admin
  Password: admin
  
When logged in as an admin or maintainer user, a link to the admin 
interface is presented on the top right hand corner of the screen.
 
---Note about alternative configurations---

If you wish to run with the local Django runserver, or you are setting
up an Apache virtual hosts, run -
  
  make build
  
'make install' is not necessary as it only creates symlinks so that
the scripts can appear in a document root.

If you wish to unit test the program, you can run 'make test', if you 
need to unit test using manage.py, make sure you run 'make build' first,
as the unit tests depend on certain files being in place.

Functionality relating to media upload will not function in the 
runserver as Django requires an external web server to serve files. 
You can simulate this behavior by using python's SimpleHTTPServer, and 
configuring settings.py appropriately, but some functionality, such as 
video streaming, will be lost.

UNINSTALLATION

If you set the DESTDIR variable in the makefile during installation, run 
the following -

  make distclean
  
If you specified the DESTDIR as a command line argument, run the 
following (where DESTDIR should be the same path that was specified 
during installation) -

  make distclean DESTDIR=/home/magpie/public_html/

This deletes the symlinks in DESTDIR, as well as cleaning up the static
and media folders. As with the installation process, if the DESTDIR does
not exist, an error will be thrown.

If the user wishes to serve the application from a different folder, 
they should cd to the DESTDIR directory specified during installation 
and run the following -

  cp -P magpie.wsgi media static /path/to/new/folder/
  rm magpie.wsgi media static
  
The site should be served from the new directory. Alternatively, they
can uninstall from the old location, and reinstall to the new location.
