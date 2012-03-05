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
user a Python module installer such as python-pip to install the Python
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

First of all, run

  chmod +x installer.sh
  
Then run

  ./installer.sh build
  ./installer.sh clean
  ./installer.sh install
  ./installer.sh test
  
After doing this, the user will need to ensure that the following 
subdirectories of the folder containing this file, and their contents, 
are readable and writable by the Apache user (www-data in Ubuntu) 

When running 'build', you will be asked if you want to copy, noting that
it will overwrite files. Answer 'yes'.

  resources
  sqlite3 (created by 'build' stage)

One solution is to run 
  
  chown -R www-data <name of folder>
  
The install stage of the script will symlink the wsgi script, as well
as the media and static files folders to a folder served by Apache (or
not if the user leaves the appropriate field blank when prompted by the
script.) The page can be accessed by navigating to the URL where that
folder is served, and launching the wsgi script. This assumes that the
folder from which Apache servers has a suitable htaccess file for 
serving wsgi files, and that Apache has been suitably configured. The
htaccess file will look like -

  Options +ExecCGI 
  AddHandler wsgi-script .wsgi
  
Details of features can be found at -

http://code.google.com/p/magpie-gdp12/wiki/Features

The admin interface can be found at -

 THE_URL_TO_SERVE_FOLDER/magpie.wsgi/admin
 
---Note about Django runserver---

If you wish to run with the local Django runserver, run process as above
making sure that when you run the './installer.sh install' step that you
leave the fields blank when the script asks you for the path and the URL

Functionality relating to media upload will not function as Django 
requires an external web server to serve files. You can simulate this
behavior by using python's SimpleHTTPServer, and configuring settings.py
appropriately, but some functionality, such as video streaming, will be
lost.

