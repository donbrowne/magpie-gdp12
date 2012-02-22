# Makefile to test pml graphing utitilies.
PML=$(wildcard *.pml)
TESTS=$(PML:.pml=.ps)

test: $(TESTS)

%.ps: %.pml
	../graphit -c $<
	@echo "Press 'q' in graph window to continue."
	gv $@
	rm -f $@
	rm -f $(*).analysis
	rm -f $(*).dot
