#Change DESTDIR to the target directory for your installation.
#Alternatively, specify DESTDIR as an argument to the makefile.
DESTDIR=$(PWD)
SHELL='/bin/bash'
MAGDIR=$(PWD)
FILE_MODE=ug+rw,o-rw
DIR_MODE=ug+rwX,o-rwX
INST=install --mode=$(DIR_MODE)

all: install

build: sqlite3/magpie.db pml/graph/traverse resources resources/static

sqlite3/magpie.db:
	@echo "Setting up sample database"
	$(INST) -d sqlite3
	cp -n ./dataload/magpie.db ./sqlite3/
	chmod $(FILE_MODE) ./sqlite3/magpie.db
	@echo "Done!"
	
pml/graph/traverse:
	@echo "Building PML tools"
	$(MAKE) -C pml
	@echo "Done!"

resources: 
	@echo "Collecting media content"
	$(INST) -d resources
	cp -r ./dataload/media/ ./resources/
	chmod $(FILE_MODE) ./resources/*
	@echo "Done!"
	
resources/static:
	@echo "Collecting static content"
	python ./django_magpie/manage.py collectstatic --noinput
	@echo "Done!"

clean: 
	$(MAKE) clean -C pml
	find ./django_magpie/ -type f -name "*.pyc" -exec rm -f {} \;

install: build
	@if [ ! -z $(DESTDIR) ]; then echo "Creating symlinks"; cd $(DESTDIR); ln -s $(MAGDIR)/django_magpie/magpie.wsgi magpie.wsgi; ln -s $(MAGDIR)/resources/media media; ln -s $(MAGDIR)/resources/static static; fi
	@echo "Done!"
	
test: build
	python2 ./django_magpie/manage.py test
	
distclean: clean 
	rm -rf ./sqlite3
	rm -rf ./resources/static/*
	rm -rf ./resources/media/*
	rm ./pml/graph/traverse
	rm ./pml/graph/print_io
	if [ ! -z $(DESTDIR) ]; then echo "Destroying symlinks"; cd $(DESTDIR); rm magpie.wsgi; rm media; rm static; cd $(MAGDIR); fi;
