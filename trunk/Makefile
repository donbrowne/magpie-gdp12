SHELL='/bin/bash'
MAGDIR=$(PWD)
FILE_MODE=660
DIR_MODE=770
INSTALL=install --mode=$(FILE_MODE)
MKDIR=mkdir -m $(DIR_MODE) -p

all: install

build:
	@echo "Building Magpie environment"
	$(MAKE) -C pml
	$(MKDIR) sqlite3
	$(MKDIR) resources
	$(MKDIR) ./resources/media
	$(MKDIR) ./resources/static
	cp -n ./dataload/magpie.db ./sqlite3/
	chmod $(FILE_MODE) ./sqlite3/magpie.db
	$(INSTALL) ./dataload/media/* ./resources/media/
	python ./django_magpie/manage.py collectstatic --noinput
	touch build
	@echo "Done!"

clean: 
	$(MAKE) clean -C pml
	rm build
	find ./django_magpie/ -type f -name "*.pyc" -exec rm -f {} \;

install: build
	@if [ ! -z $(DESTDIR) ]; then echo "Creating symlinks"; cd $(DESTDIR); ln -s $(MAGDIR)/django_magpie/magpie.wsgi magpie.wsgi; ln -s $(MAGDIR)/resources/media media; ln -s $(MAGDIR)/resources/static static; fi
	@echo "Done!"
	
test: build
	python ./django_magpie/manage.py test
	
distclean: clean 
	rm -rf ./sqlite3
	rm -rf ./resources/static/*
	rm -rf ./resources/media/*
	rm ./pml/graph/traverse
	rm ./pml/graph/print_io
	if [ ! -z $(DESTDIR) ]; then echo "Destroying symlinks"; cd $(DESTDIR); rm magpie.wsgi; rm media; rm static; cd $(MAGDIR); fi;
