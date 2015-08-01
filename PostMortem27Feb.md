# Introduction #

Our second post mortem report.


# Details #
From: osull_@tcd.ie
Subject: Iteration 3 Post Mortem_

Accomplishments
> Completed tasks for feature : #19 Enhanced Display of Media (Embedded Video)
  1. Embed video from resource Files onto page - Don
> 2. Modifications to Model/View to pass video link to web page - Don
> Acceptance test(s) passed: #19 Enhanced Display of Media (Embedded Video)

> Completed tasks for feature: #20 Separate Maintenance Folders
  1. Modified view/model so that files can be uploaded to a
maintainer's folder - Don
> 2. Modified resource file handling to enable the administration of
file access to users - Don
> Acceptance test(s) passed: #20 Separate Maintenance Folders

> Completed tasks for feature: #16 Specification of Resources for
Recommendations(by maintainer)
  1. Created WSGI scripts to allow Django to run on top of Apache - Don
> 2. Created make scripts for turning SVN snapshot into a sensible
installation - Don
> Acceptance test(s) passed: #16 Specification of Resources for
Recommendations(by maintainer)

> Completed tasks for feature: #17 Access (to Supporting Artifacts)
Based on Login ID
  1. Implemented serving the uploaded files to users - Don
> 2. Implemented methods to facilitate controlling file access by
authorised users - Don
> Acceptance test(s) passed: #17 Access (to Supporting Artifacts) Based
on Login ID

Completed tasks for feature: #18 Evolving profiles
  1. Designed and unit tested new inference engine - Cyril
Acceptance test(s) passed: #18 Evolving profiles

Obstacles
1. Ensuring all dependencies have been satisfied for the application
> has led to a technically complex installation procedure.
> Mitigation: Streamline the process using scripting and by improving
> the quality of the install document.
2. Our knowledge model no longer works and needs to replaced ASAP by a
> proper rules based inference engine.
> Mitigation: The new rewritten engine is currently being integrated
> into the next release.
3. Lack of documentation surrounding features of the application and
> some unintuitive layout has made it difficult for both testers and
> clients to find and assess the features.
> Mitigation: Improve the quality of the documentation surrounding
> features.  Improve the design layout in places where confusion is
> judged to arise.

Objectives
> Feature: #19 Enhanced Display of Media (Embedded Video)  - Don

> Feature: #20 Separate Maintenance Folders  - Don

> Feature: #16 Specification of Resources for Recommendations(by
maintainer) - Don

> Feature: #17 Access (to Supporting Artifacts) Based on Login ID - Don

> Feature: #8 Reduction in "conceptual noise"/Feature #18 Evolving
profiles - Cyril