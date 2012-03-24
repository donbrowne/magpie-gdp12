SHELL='/bin/bash'
MAGDIR=$(PWD)
FILE_MODE=ug+rw,o-rw
DIR_MODE=ug+rwX,o-rwX
MKDIR=install --mode=$(DIR_MODE) -d

all: install

build:
	@echo "Building Magpie environment"
	$(MAKE) -C pml
	$(MKDIR) sqlite3
	$(MKDIR) resources
	cp -n ./dataload/magpie.db ./sqlite3/
	cp -r ./dataload/media/ ./resources/
	chmod $(DIR_MODE) ./resources/media
	chmod $(FILE_MODE) ./sqlite3/magpie.db ./resources/*
	python2 ./django_magpie/manage.py collectstatic --noinput
	touch build
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
	rm build
