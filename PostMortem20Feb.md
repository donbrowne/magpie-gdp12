# Introduction #

This is our first PM report from 20th Feb.


# Details #

From: osull_@tcd.ie
Subject: Iteration 2 Post Mortem_

## Accomplishments ##
> Completed tasks for feature : #11 Display of Process Specifications in Graphical Form
    1. Build PML tools, test their operation - Don
> > 2. Find suitable Python tool for graphing, test with PML tools - Don
> > 3. Implement a Python function that reads a file and generates Graph - Don
> > 4. Display a graph on the page from a hardcoded PML file - Don
> > 5. Modify function to take a PML file path from a GET request - Don
> > 6. Modify Recommendation view code so that it passes a PML file path to the web page - Don
> > 7. Modify template so that it generates a graph for each PML file specified - Don
> > Acceptance test(s) passed: #11 Display of Process Specifications


> Completed tasks for feature: #12 User Profiles
    1. Create User Registration, test the operation - Cyril
> > 2. Create User Profiles, test building profiles - Cyril
> > 3. Implement and test User Profile Editing - Cyril
> > 4. Associate User Profile Information with Recommendations and test - Cyril

> Acceptance test(s) passed: #12 User Profiles

> Completed tasks for feature: #13 Specification of User Profiles (by Maintainer)
    1. New User Profile Creation (by admin user) - Cyril
> > 2. Associate Facts with User Profiles (by admin user) - Cyril
> > 3. Implement and test User Profile Editing (by admin user) - Cyril
> > 4. View User Profile Information (by admin user) - Cyril

> Acceptance test(s) passed: #13 Specification of User Profiles (by Maintainer)

> Completed tasks for feature: #14 Save/Restore Session State on Logout/Login
    1. Create (by logged in user) function to enable saving (or storing) their answers to questions to their user profile - Cyril
> > 2. Create (by logged in user) function to enable viewing (or restoring) saved answers to quesitons - Cyril
> > 3. Create (by maintainer) function to see the view/change the list of user answers - Cyril

> Acceptance test(s) passed: #14 Save/Restore Session State on Logout/Login

> Completed tasks for feature: #15 Linking to Recommendations Resources - Video, PDF, PML Models etc. (by maintainer)
    1. Modify Recommends model to allow three link charFields (PDF, PML, Video) to be attached. - Don
> > 2. Modify templates to display links if they are present - Don
> > 3. Created External Link model to allow maintainer to specify links to external resources, and associate them with a recommendation - Don
> > 4. Modify Recommendations admin screen so that External Links can be created and associated with the recommndations - Don
> > 5. Introduce new code to simplify passing the list of links to the web page - Don
> > 6. Modify template so that links are displayed alongside recommendations - Don

> Acceptance test(s) passed: #15 Linking to Recommendations Resources - Video, PDF, PML Models etc. (by maintainer)

> Completed tasks for feature: #16 Specification of Resources for Recommendations(by maintainer)
    1. Created Resource File model to allow uploading a file - Don
> > 2. Made appropriate changes to configuration to handle file uploads - Don
> > 3. Modified Recommendation model to allow maintainer to associate links to internal content to them - Don
> > 4. Modified templates and view code to ensure internal links are displayed alongside external ones - Don
> > 5. Changed PML, Video links from External Links to Resource Files for use with graphing tools and embedded video - Don

> Acceptance test(s) passed: #16 Specification of Resources for Recommendations(by maintainer)

> Completed tasks for feature: #17 Access (to Supporting Artifacts) Based on Login ID
    1. Modified Resource File model to allow maintainer to associate user groups with files - Don
> > 2. Implemented a function to check if a user can access a file based on their user group - Don
> > 3. Modified recommendation link code so that it only displays links to internal content that that user is allowed to see - Don

> Acceptance test(s) passed: #17 Access (to Supporting Artifacts) Based on Login ID

## Obstacles ##
1. Django framework found to have good back end support but the front end is difficult to work with for complicted User Interfaces.
> A lot of time has been spent trying to figure out how to get a particular UI feature working.
> It may have been a whole lot faster to do the whole thing in pure python server up the results
> to either a java applet or some kind of pure javascript framework such as sencha's extjs that lets dev worry about code rather than html/css.
> Mitigation: Too late to change front end at this stage, mitigation will have to come through increasing familiarity with Django.
2. File serving more complicated than anticipated, requires Apache to serve files.  Security needs to be applied to files to ensure unauthorized parties cannot hotlink to them.
> Mitigation: Devote time during next iteration to read documentation and implement and test a workable solution in VM-based production environment.
3. Our knowledge model no longer works and needs to replaced ASAP by a proper rules based inference engine.
> Mitigation: As a result of rewrite feature 8 will be completed.

## Objectives ##
> Feature: #19 Enhanced Display of Media (Embedded Video)
    1. Investigate methods of embedding video into Django pages - Don
> > 2. Proof of concept: embed hard coded video from Resource Files onto page - Don
> > 3. Make appropriate modifications to Model/View to pass video link to web page - Don
> > 4. Modify templates to display appropriate videos on page - Don


> Feature: #20 Seperate Maintenance Folders
    1. Modify view/model so that the active maintainer's name is passed to the Resource File fileField, so that files are uploaded to that maintainer's folder - Don
> > 2. Modify admin screen for Resource File so that non-admin users can only modify their own files - Don


> Feature: #16 Specification of Resources for Recommendations(by maintainer)
> also Feature: #17 Access (to Supporting Artifacts) Based on Login ID
    1. Set up Ubuntu 10.04 32-bit VM with Apache - Don
> > 2. Create production test environment VM (Ubuntu 10.04 32-bit) - Sean
> > 3. Set up appropriate WSGI scripts to allow Django to run on top of Apache - Don
> > 4. Ceate make scripts for turning SVN snapshot into a sensible installation - Don
> > 5. Investigate and implement methods to serve uploaded files to users - Don
> > 6. Ensure that files can only be served to authorized users - Don
> > 7. Populate a sample test database - Sean
> > 8. Carry out any necessary manual acceptance testing within production VM/actual server - Sean
> > 9. tar up folder and upload to site for user testing - Sean


> Feature #8 Reduction in "conceputal noise"
> also Feature #18 Evolving profiles
    1. Replace knowldege base with rules based inference engine - Cyril
> > 2. Implement backward chaining (as well as the more usual forwards) - Cyril