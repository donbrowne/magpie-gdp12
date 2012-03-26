#Change DESTDIR to the target directory for your installation.
#Alternatively, specify DESTDIR as an argument to the makefile.
DESTDIR=$(PWD)
MAGDIR=$(PWD)
SHELL='/bin/bash'
FILE_MODE=ug+rw,o-rw
DIR_MODE=ug+rwX,o-rwX
INST=install --mode=$(FILE_MODE)
INSTDIR=install --mode=$(DIR_MODE)

all: install

build: sqlite3/magpie.db pml/graph/traverse resources resources/static

sqlite3/magpie.db:
	@echo "Setting up sample database"
	$(INSTDIR) -d sqlite3
	$(INST) $(MAGDIR)/dataload/magpie.db $(MAGDIR)/sqlite3/
	@echo "Done!"
	
pml/graph/traverse:
	@echo "Building PML tools"
	$(MAKE) -C pml
	@echo "Done!"

resources: 
	@echo "Collecting media content"
	$(INSTDIR) -d resources $(MAGDIR)/resources/media
	$(INST) $(MAGDIR)/dataload/media/* $(MAGDIR)/resources/media/
	$(INST) $(MAGDIR)/dataload/media/.htaccess $(MAGDIR)/resources/media/
	@echo "Done!"
	
resources/static:
	@echo "Collecting static content"
	python $(MAGDIR)/django_magpie/manage.py collectstatic --noinput
	@echo "Done!"

clean: 
	$(MAKE) clean -C pml
	find $(MAGDIR)/django_magpie/ -type f -name "*.pyc" -exec rm -f {} \;

install: build
	@if [ -d $(DESTDIR) ]; then echo "Creating symlinks"; cd $(DESTDIR); ln -s $(MAGDIR)/django_magpie/magpie.wsgi magpie.wsgi; ln -s $(MAGDIR)/resources/media media; ln -s $(MAGDIR)/resources/static static; echo "Done!"; else echo "ERROR: DESTDIR does not exist"; fi
	
test: build
	python2 $(MAGDIR)/django_magpie/manage.py test
	
reset: build
	@echo "Resetting database and deleting media files"
	rm -f $(MAGDIR)/resources/media/*
	rm -f $(MAGDIR)/sqlite3/magpie.db
	python $(MAGDIR)/django_magpie/manage.py syncdb
	chmod $(FILE_MODE) $(MAGDIR)/sqlite3/magpie.db 
	@echo "Done!"
	
distclean: clean 
	rm -rf $(MAGDIR)/sqlite3
	rm -rf $(MAGDIR)/resources/
	rm $(MAGDIR)/pml/graph/traverse
	rm $(MAGDIR)/pml/graph/print_io
	if [ -d $(DESTDIR) ]; then echo "Destroying symlinks"; cd $(DESTDIR); rm magpie.wsgi; rm media; rm static; cd $(MAGDIR); echo "Done!"; else echo "ERROR: DESTDIR does not exist"; fi;
