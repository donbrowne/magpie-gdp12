# Introduction #

Post Mortem submitted 21/03/2012 for Release 2 iteration 1.


# Details #

Accomplishments
> Completed tasks for feature: #All Continue improvements to installation process
    1. Created a make file for easy Magpie installation - Don.
> Acceptance test(s) passed: #All Continue improvements to installation process

> Completed tasks for feature: #1 Knowledge Representation
    1. Implemented back-chaining into the inference engine - Cyril.
> Acceptance test(s) passed: #1 Knowledge Representation

Obstacles
1. Feature #9 (process "Roadmaps") left unimplemented due to late specification of details necessary for design.  Mitigation: we now have the information we need to progress this feature.
2. It should be noted that the installation process is still not nailed down to customer satisfaction.  We plan to mitigate this with inter-group testing.
3. As this was largely a bug fix/feature refinement week there were no other obstacles of note.

Objectives
> Feature: #All Continue improvements to installation process
  1. Implement changes recommended by John - Don.
> 2. Come to arrangement with Group 2 whereby we test each others installation processes - Sean.

> Feature: #1 'Clickable' PML graphs
> Implement cllickable PML graph images in order to allow users to get additional process information from an image of a PML process specification utilising the image map feature from Graphviz.
  1. Investigate Graphviz interactive graph support - Don.
> 2. Split PML description into discrete stages - Don/Sean.
> 3. Associate graph segments with text - Don.

> Feature: #3 Process "Roadmaps"
> Add the ability to generate a "handbook describing a process that is human-readable" from an XML based "Process Document" (based on the implementation provided).
  1. Integrate XML tools into application - Don.
> 2. Add textual description into recommendation - Don.
> 3. Change PML graphing so that it works from the XML source file - Don.

> Feature: #4 Maintainer specifying rules using "OR"
> Allow the specification of rules by a maintainer using logical 'OR'ing of facts (as well as 'AND') to fire recommendations. e.g. ( A=T & B=T  | C=F ) => [R1](https://code.google.com/p/magpie-gdp12/source/detail?r=1) - Cyril.

> Feature: #9 Allow user to revise answers
> Modify the current implementation in order to allow a user to revisit the set of questions they had previously been served with in order to modify their responses and thus get a revised set of recommendations - Cryil.