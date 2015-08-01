Feature Discovery Guide




---

DEFAULT ACCESS

---


Administration account

Username:	admin
Password:	admin

Testuser

Username:	testuser[number](number.md)
Password:	test

e.g. username: testuser01 has the password: test


---

FEATURES WALKTHROUGH (Release 1)

---



1 Knowledge Representation, with fan-in and fan-out.

---

? What is this exactly???
BACK HERE LATER


2    User interface. 10 pts.

---


User Access

The applications user front end is accessed through a web browser.


Administration Access

The back end administration console is accessed through a web browser.


Basic User Interface

Users are prompted to click a "Start" button to begin a line of questioning with the aim of serving recommendation(s) to them.
Users should click a radio button to indicate their answer and then click on the button for "Next".
Any recommendations served can be expanded by clicking on a button on the right side of the interface, this allows media to be managed more effectively than if the media was listed directly in the interface.
Previously answered question answers are listed under the question section.
Answers can be modified in this list by selecting the appropriate radio button and clickint on the "Change Answers" button.
The section for Reasons on the bottom right of the interface displays the reasoning behind any recommendations.


3 User access mechanism (to recommendations). 25 pts.

---


As mentioned above any recommendations served to users can be expanded by clicking on a button on the right side of the interface.
Recommendations can take various forms: images, video, PML (specification/roadmap/interactive graph), Web hyper-links, internal hyper-links etc.


4 Presentation of questions in order of relevance, based on user profile (this was folded into the user access mechanism).

---


Steps for changing the ordering of rules in a given rule set (e.g. for IngestUser in the test database):

1. From: [Home › Knowledge › Rule sets ](.md), click on the rule set of interest (for this example click IngestUser).

You should now be in [Home › Knowledge › Rule sets › IngestUser ](.md).  For any given rule you should see on the left of its "bar" a numeric ordering.
This indicates the order in which the rules fire.  In order to change this ordering procede as follows.

2. Locate the "Move Item" control on the "bar" for the rule you wish to re-order (it is a diamond shaped icon to the right of the X icon on the right of the "bar").

Note that if you accidentaly click on the X icon for deletion and the bar turns red, simply click the X icon again to deselect it.

3. Click and hold the "Move Item" icon (the bar will turn yellow) and simply drag the bar to the place in the list where you want the rule to fire.

4. Next click on one of the options to save along the bottom of the window - e.g. "Save and continue editing" if you need to change the order of a number of rules in the list.

This is all you need to do to re-order the list of rules within a rule set.



5 Knowledge base "maintenance." 29 pts.

---


BACK HERE LATER!!!!!!!!!!!



6 Maintenance user. 11 pts.

---


Specify a maintanence user:

From the administration site [Home › Auth › Users ](.md) one can create new users with the "+ Add user" button on the upper right hand side of the interface.
In order to specify a maintenance level user do as follows.

1. Click the "+ Add user" button.

2. Input details for the username, password and confirm password fields and click on "Save and continue editing" at the bottom of the window.

3. You may input data into the "Personal info" area as appropriate.

The "Permissions" area of the window is where one can specify the permissions that apply to the account.

4. A maintanence user must have the tick box for Staff status selected (obviously in addition to needing to have the tick box for Active selected).
> Note that you should not tick the box for Superuser status unless you wish to create a full administration account.

5. From the "Available user permissions" section you will need to select the appropriate permissions for the account you require.
> You may use ctrl-click or shift-click selection.  Click on the blue arrows to move permissions to the "Chosen user permissions" and back.

6. Lastly the account can be assigned to groups.  In addition to any permissions manually assigned, this user will also get all permissions granted to each group he/she is assigned to.



7 "Eye candy." 35 pts. This is mainly a consistent css-based look and feel that gives the site a "modern" impression.

---


Logo:

Original artwork specially designed for use of the project.
Helps to strongly distinguish the interface from any similar looking applications the user might use aiding user memory recognition.


Favicon:

Important for users who use multiple tabs when using browsers to aid in distinguishing tabs.


User interface design:

We have strived for a consistent style for the user front end.


Maintenence interface design:

The maintenence interface has a markedly different style to the front end and are thus easy to differentiate.


8 Reduction in "conceptual noise" of maintenance interface. 30 pts.

---

"The maintenance interface is currently based on automatically generated forms that require significant interpretation on the part of the user.
This feature would tailor the appearance of forms to the maintenance task".

What do the various fields mean?
What is the sequence of steps for adding rules?
Explanatory text on each screen would be helpful.
Its not apparant that logging in to the admin UI changes the user ID as well.
Its not possible to test new rule sets with a user different from the admin user without loggint
No docco for this!

Finally, is it possible to expand the descriptions of the various priv-
> ileges  to grant for new maintenance users?  Some are clear after using
> the maintenance interface, others seem to be about Django admin.

BACK TO THIS!!!!!!!!!!!!!!!


9.0 Process "roadmaps." 20 pts.

---

"A roadmap in this context is a narrative description of the sequence of steps required to achieve some goal.
One approach is to automatically generate them from a PML specification that is suitably elaborated with textual annotations."

Note: This was left unimplemented for release 1.

The example of a PML roadmap description is triggered when a user answers "Yes" to the following questions:

Are you hungry?				Yes
Do you have a kitchen?		Yes
Do you like cooking?		Yes

Note you can just next past any of the other questions without the need to specify an answer to get to the roadmap.

1. These answers will produce a recommendation button "Make these foods in yoiur own kitchen".

2. Click on this button to expand the details of the recommendation.

3. Click on the link entitled "Click here to view the PML roadmap." in order to be browse to the roadmap description.



10.0 Step-wise refinement of "high-level" models. 20 pts.

---


What is this????????????
Unimplemented for release 1 whatever it is.



11 Graphical display of process specifications.

---

"PML models would be an example of a process specification."

The example of a graphical display of a PML process specification is triggered when a user answers "Yes" to the following questions:

Are you hungry?				Yes
Do you have a kitchen?		Yes
Do you like cooking?		Yes


As in the previous feature example, you can just next past any of the other questions without the need to specify an answer to get to the graphical PML.

1. The answers will produce a recommendation button "Make these foods in yoiur own kitchen".

2. Click on this button to expand the details of the recommendation.

3. Click on the link entitled "Click here to view the interactive PML Graph." to browse to a Web page displaying the graphical PML specification.

4. If the graph appears to be too large or small you may find it helpful to zoom your browser in or out as appropriate (e.g. "ctrl" and "+").

5. In the graph itself additional information is provided to the user when they click on any of the nodes.
> This information is in the form of a pop-up and can be dismissed by clicking on the "OK" button in the pop-up.



12  User profiles. 10 pts.

---


Registration

By default users have a guest level of access to the site and can explore functionality.
Additionally users can register a profile by clicking on the link "Register" found at the top right of the user site.
Users must provide a unique username and fill out the password field (and confirm password field).
If a user supplies an existing username they will get an error message.
If a user fails to provide password data they get an error message.
Users are not explicitly required to provide an email address.
A newly registered user is logged in to the system by default.

Once logged into the system a user has the option links in the banner changed from:

[Log in | Register ](.md)

to

[Account | Reset | Log out ](.md)

The account link allows a user to select a "user profile" from a drop down list box to associate with their account.
Additionally they can input a first name, last name and email address to associate with the account.



13   Specification of user profiles (by maintainer). 20 pts.

---


User profiles are specified in the administration interface from:

[Home › Register › Profiles ](.md)

Profiles lists all the profiles set up on the system. New profiles can be created in this section.
Profiles are created with a profile name.
Profiles are associated with a ruleset - a ruleset is a list of facts automatically asserted when a user starts a line of questions e.g. likes cake = No, is hungry = Yes etc.
Thus the profiles may have a list of variables set to specific default values from this ruleset.


In order to create a profile:

1. Click on the button "Add profile"

This will bring you to [Home › Register › Profiles › Add profile ](.md)

2. Next input a name for the profile.

3. Click on the dropdown list box beside "Ruleset:" to choose a ruleset to associate with the profile (you can also define a new ruleset from here using the "+" icon).

4. Once you are happy with the details choose one of the save options at the bottom of the screen.



14    Save/restore session state on logout/login. 10 pts.

---


The system is designed to save the state of a line of questioning for registered users.
This feature is unavailable for guest users.

Once a user is logged in the user may reset their saved data with the "Reset" link from the banner links along the top of the window: [Account | Reset | Log out ](.md)

When a user clicks on the "Start" button the system will display, in the Previously Answered section under the Questions "Nothing so far!".
This is to indicate that there is no history of questions answered stored on the system.

As soon as a user selects an answer to a question and clicks "Next" this answer is saved by the system into a database and associated with the account.
The system will store up any answers specified by the user in this fashion.
As soon as "Next" is clicked the database is updated and the answers are saved allowing the user to come back and continue from where they were previously.

If a user decides not to give an answer to any particular question and then logs out they will be re-asked any quesitons they did not specify answers for previously.

Users have the option to change their previously answered questions with the "Change Answers" button which appears beneath the Previously Answered section.

In addition to the question state, the associated Recommendations and Reasons are also saved.




15	Allow videos, PDF files, PML models to be attached or linked to recommendations. 10 pts.

---


Resource files can be linked to recommendatons as follows:

1. From the administration interface section [Home › Knowledge › Recommends ](.md) select a Recommend by clicking on it.

2. Select the resource from one of the 3 link fields as appropriate for your need.

3. You may attach multiple resource links in the "OtherLinks: " section.

4. Additionally external Web hyper-links may be added to a recommendation along with some descriptive text.




16    Specification of videos, PDF files, PML models to be attached or linked to recommendations (by maintainer).

---

"Such artifacts should be stored on the server hosting the DSS, or optionally linked to on YouTube or other external web sites" - see 15 (step 4) listed above.

Resource files can be added (stored) to the server using administration interface at:

[Home › Knowledge › Resource files ](.md)

In order to add a resource file:

1. Click on the button for "+ Add resource file".

2. You must input a description of the file in the "Description:" field.

3. Click on the "Browse..." button to browse to the resource you wish to add to the system.

4. Files can be restricted by user by ticking the box for "Restricted" and highlighting the users who can access the file in the "Restricted to:" section.




17    Access (to supporting artifacts) based on login ID. 20 pts.

---


Seems to work flawlessly.


18    Evolving profiles (new feature). 20 pts. When a profile specification is modified, existing user profiles following the old specification need to be updated to match the new specification.

---


Changes not evident until the interview process starts over??


19  Enhanced display of media, for example in embedded viewers. 20 pts.

---


Describe the display of media.


20    Separate maintenance folders. 30 pts. Each maintenance user gets to "own" his or her uploaded artifacts, meaning only he or she can modify or delete them, but any maintenance user can attach them to a recommendation.

---


Any non-admin maintainer can only modify those files which they have uploaded.



---

FEATURES WALKTHROUGH (Release 2)

---


1     'Clickable' PML graphs

2     PML 'Flight Simulator - next/prev/up

2.5   Lint the two via 'up'

3.    Assemble process spec. from fragments
> by matching inputs & outputs

> g: product.state = installed

4.    Allow 'OR' of facts (as well as 'AND')
> to fire rec.    A=T & B=T  | C=F

5.    "improved" rule specification

> cond: [.md](.md)     (outsourcing & mult\_culture) | gsd => kick-off
> rec:  [.md](.md)

6.    Rules assert facts as well as rec.

7.    Facts determine whether questions are asked

8.    Feedback to user progress & reasoning behind recs.

9.    Allow user to revise answers.

10.   Show implicitly answered Qs





---
