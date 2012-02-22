CC	= gcc
CFLAGS	= -I..  -g -Wall
LIB	= ../pml/libpml.a
OBJS	= traverse.o
SRCS	= traverse.c
INSTALL_DIR = $(HOME)

all:	traverse print_io

traverse:	traverse.o $(LIB)
	$(CC) -o $@ $< $(LIB)
print_io:	print_io.o $(LIB)
	$(CC) -o $@ $< $(LIB)
pmlpic:	pmlpic.o $(LIB)
	$(CC) -o $@ $< $(LIB)


%.ps:	%.dot
	dot -Tps $< > $@

install: traverse print_io
	[ -d "${INSTALL_DIR}" ] || mkdir ${INSTALL_DIR}
	[ -d "${INSTALL_DIR}/bin" ] || mkdir ${INSTALL_DIR}/bin
	[ -d "${INSTALL_DIR}/lib" ] || mkdir ${INSTALL_DIR}/lib
	cp traverse ${INSTALL_DIR}/bin 
	cp graphit  ${INSTALL_DIR}/bin 
	cp color-pml.awk ${INSTALL_DIR}/lib
	cp print_io ${INSTALL_DIR}/bin 
clean:
	rm -f $(OBJS)

test: netbeans_req_release.ps

netbeans_req_release.dot: netbeans_req_release.pml
	traverse -L -c AssignDevelopersToCompleteProjectMilestones \
	-c SolicitModuleMaintainersForInclusionInUpcomingRelease \
	$< > $@

%.ps:	%.dot
	dot -Tps $< > $@

.PHONY: netbeans_req_release.dot
