# Feature Discovery Guide for MAGPIE #


## INDEX ##

1.0 DEFAULT ACCESS
  * 1.1  Administration Account
  * 1.2  Test Account

2.0 FEATURES WALKTHROUGH (RELEASE 1 FEATURE SET)
  * 2.1 KNOWLEDGE REPRESENTATION, WITH FAN-IN AND FAN-OUT
  * 2.2 USER INTERFACE
    * 2.2.1 User Access
    * 2.2.2 Administration Access
    * 2.2.3 Basic User Interface
    * 2.2.4 Administration Interface
  * 2.3 USER ACCESS MECHANISM (TO RECOMMENDATIONS)
  * 2.4 PRESENTATION OF QUESTIONS IN ORDER OF RELEVANCE, BASED ON USER PROFILE
  * 2.5 KNOWLEDGE BASE "MAINTENANCE"
  * 2.6 MAINTENANCE USER
  * 2.7 "EYE CANDY" THIS IS MAINLY A CONSISTENT CSS-BASED LOOK AND FEEL THAT GIVES THE SITE A "MODERN" IMPRESSION
    * 2.7.1 Logo
    * 2.7.2 Favicon
    * 2.7.3 User interface design
    * 2.7.4 Maintenance interface design
  * 2.8 REDUCTION IN "CONCEPTUAL NOISE" OF MAINTENANCE INTERFACE
  * 2.9 PROCESS "ROADMAPS"
  * 2.10 STEP-WISE REFINEMENT OF "HIGH-LEVEL" MODELS
  * 2.11 GRAPHICAL DISPLAY OF PROCESS SPECIFICATIONS
    * 2.11.1 Getting to see a PML graph
  * 2.12 USER PROFILES
    * 2.12.1 Registration
  * 2.13 SPECIFICATION OF USER PROFILES (BY MAINTAINER)
    * 2.13.1 Create a Profile
  * 2.14 SAVE/RESTORE SESSION STATE ON LOGOUT/LOGIN
  * 2.15 ALLOW VIDEOS, PDF FILES, PML MODELS TO BE ATTACHED OR LINKED TO RECOMMENDATIONS
  * 2.16 SPECIFICATION OF VIDEOS, PDF FILES, PML MODELS TO BE ATTACHED OR LINKED TO RECOMMENDATIONS (BY MAINTAINER)
  * 2.17 ACCESS (TO SUPPORTING ARTIFACTS) BASED ON LOGIN ID
  * 2.18 EVOLVING PROFILES
  * 2.19 ENHANCED DISPLAY OF MEDIA, FOR EXAMPLE IN EMBEDDED VIEWERS
  * 2.20 SEPARATE MAINTENANCE FOLDERS

3.0 FEATURES WALKTHROUGH (RELEASE 2 FEATURE SET)
  * 3.1 'CLICKABLE' PML GRAPHS
  * 3.2 PML 'FLIGHT SIMULATOR'
    * 3.2.1 Link the two via 'up'
    * 3.2.2 Save 'Flight Simulator'
  * 3.3 ASSEMBLE PROCESS SPECIFICATION FROM FRAGMENTS BY MATCHING INPUTS & OUTPUTS
  * 3.4 ALLOW 'OR' OF FACTS (AS WELL AS 'AND') TO FIRE RECOMMENDATIONS
  * 3.5 "IMPROVED" RULE SPECIFICATION
    * 3.5.1 Premises
    * 3.5.2 Conclusions
    * 3.5.3 Recommendations
  * 3.6 RULES ASSERT FACTS AS WELL AS RECOMMENDATIONS
  * 3.7 FACTS DETERMINE WHETHER QUESTIONS ARE ASKED
  * 3.8 FEEDBACK TO USER PROGRESS & REASONING BEHIND RECOMMENDATIONS
  * 3.9 ALLOW USER TO REVISE ANSWERS
  * 3.10 SHOW IMPLICITLY ANSWERED QUESTIONS





---


---

1.0 DEFAULT ACCESS

---


---


This section describes the default access accounts for the hosted test system.


1.1 Administration Account

---

Username:	admin
Password:	admin

Administration account has full root level administration rights.


1.2 Test Account

---

Username:	testuser01
Password:	test

Test accounts represent a default user account.





---


---

2.0 FEATURES WALKTHROUGH (RELEASE 1 FEATURE SET)

---


---


The following sections describe details to give an overview for use of the feature set implemented for the first release of MAGPIE.



2.1 KNOWLEDGE REPRESENTATION, WITH FAN-IN AND FAN-OUT

---


Forward chaining and backward chaining is implemented within the inference engine.



2.2 USER INTERFACE

---


2.2.1 User Access

The applications user front end is accessed via web browser.
When a user visits the site they are provided by default with guest level access to features.
Users can register with the site in order to utilise some additional features for saving recommendations and user profile specific lines of questioning.
Users may register accounts by clicking on the link along the top menu banner and then supplying username, password and email address. Users may modify their account, from the link along the top menu banner, to modify the account details. Users may select a profile type to help tailor recomendations. Registered users question answers and recommendations are saved by the system as they progress through answering questions and getting recommendations.

For more detail on registration see 2.12.1 Registration.

For more detail on saving recommendation data see 2.14 SAVE/RESTORE SESSION STATE ON LOGOUT/LOGIN.


2.2.2 Administration Access

The back end administration console is accessed via web browser.

For more detail on the operation of this console see section: 2.2.4 Administration Interface.


2.2.3 Basic User Interface

Users are prompted to click a "Start" button to begin a line of questioning with the aim of serving recommendation(s) to them.
Users may click a radio button to indicate answers and then click on the button for "Next".

Any recommendations served can be expanded by clicking on a button on the right side of the interface, this allows media to be managed more effectively than if the media was listed directly in the interface.
Previously answered question answers are listed under the question section.
Answers can be modified in this list by selecting the appropriate radio button and clicking on the "Change Answers" button.
The section for Reasons on the bottom right of the interface displays the reasoning behind any recommendations.


2.2.4 Administration Interface

The following section seeks to give a brief overview of the administration interface.  More detail on specific features can be found in the rest of the document as indicated.

When an admin account is used to log in to the Magpie administration interface the Magpie site admin Home screen is displayed presenting the system overview.
The overview is broken down into four sections:

  * AUTH (AUTHORISATION)
  * KNOWLEDGE
  * REGISTER
  * SITES


### AUTH (AUTHORISATION) ###

Auth(authorisation) is utilised to manage Magpie administration rights at group and account level.
Contains two subsections: Groups and Users.
Various permissions can be specified relating to how a unique account or accounts belonging to a particular group can interact with the system.


### KNOWLEDGE ###

Knowledge is where you can create recommendations, upload multimedia content and specify rules of inferrence to tailor recommendations to users.
Contains four subsections: Recommends, Resource files, Rule sets, and Variables.


#### Recommends ####
This section contains the list of the set of recommendations that have been input. The process of having the user answer questions allows a subset of recommendations to be generated from this list and displayed to the user. Clicking on the button "Add recommend" opens a window to allow you to input details for a given recommend.

Recommends must consist of an identifying name, some descriptive text.
Optionally they can have one or more of: PML model, Video file or other multimedia link attached from resources stored on the Magpie server.
Optionally they can also have external links attached (along with some required descriptive text for the link) e.g. linking to an internet site.

Once satisfied with all the details you will need to choose one of the save options along the bottom menu banner to complete the "Add recommend" process. In this manner you can build up a list of all the various different recommendations which are served based on the inference rules, as specified in "Rule sets"(see details below).

For additional information see section:

3.5.3 Recommendations


#### Resource files ####
This section allows you to upload resource files to the Magpie server for attaching to the recommendations.

You must specify a description of the resource for ease of administration.
You must specify a local path to the file (or simply click the button "Browse..." and select the file).
Restricted files - tick the box, and the file can only be accessed by an admin, maintainer, or user who has the view restricted files permission. You can also select users from the list to be allowed.

Once satisfied with all the details you will need to choose one of the save options along the bottom menu banner to complete the "Add resource file" process.

Additionally you can edit any exsiting resource files as well as view any historical edits to them.

For additional information see sections:

2.15 ALLOW VIDEOS, PDF FILES, PML MODELS TO BE ATTACHED OR LINKED TO RECOMMENDATIONS
2.16 SPECIFICATION OF VIDEOS, PDF FILES, PML MODELS TO BE ATTACHED OR LINKED TO RECOMMENDATIONS (BY MAINTAINER)
2.17 ACCESS (TO SUPPORTING ARTIFACTS) BASED ON LOGIN ID


#### Rule sets ####
This is where you may create multiple rule sets to govern which information is asked of users and which recommendations are presented to them.
A users profile is associated a rule set to determine which questions are posed to the user. Thus different user profiles may be posed different sets of questions to get different recommendations from the same knowledge base.
The button "Add rule set" allows you to specify a list of rules which are run in order starting at Rule 1. Rule sets need a name to identify them for administration.
The button "Add Rule" will launch a UI form that allows you to add an inference rule(s) to the rule set.
Rules take the form of premises setting conclusions and yielding recomendations:

Premise(s) -> Conclusion(s) => Recommendation(s)

You can add multiple premises that effectively ask the user a question(s) in order to set the values for the premise variable(s).
Conclusions may then be fired in order to set values for additional variables thereby triggering other rules from the rule set.
Any associated recommendations are presented to the user.

THERE MUST BE AT LEAST ONE RECOMMENDATION ASSOCIATED WITH A RULE OR THE SYSTEM WILL NOT POSE THE PREMISE(S) ASSOCIATED QUESTIONS.

The order in which the rules are fired can be changed from the GUI by dragging and dropping with the <|> arrows icon on the left of the X icon (see section 2.4 below).
Once rules are added to the rule set is it necessary to choose one of the options to save along the bottom banner menu.

For more details please see sections:

2.4 PRESENTATION OF QUESTIONS IN ORDER OF RELEVANCE, BASED ON USER PROFILE
3.5 "IMPROVED" RULE SPECIFICATION
3.6 RULES ASSERT FACTS AS WELL AS RECOMMENDATIONS


#### Variables ####
Variable values are also called "Facts" in the context of this application domain.
The variable values or "Facts" that we are interested in are both Yes/No answers to questions posed to users as well as values from any conclusions (inferred) from the user answered questions.
Variables can be added with the button "Add variable" **Home > Knowledge > Variables**.
Variables require a "Name:" to identify them to the Admin system and a "Prompt:" which is typically the text of a question that we wish to pose to a user.
There is a tick box labeled "Ask" which determines whether or not the variable is asked of a user.
We may not want to ask a user about a variable if we intended on inferring the variables value with a conclusion. In this case it may help to set the "Prompt:" to something sensibly descriptive.


### REGISTER ###

Register administration consists of sections: Profiles and Accounts.

#### Profiles ####
Profiles lists all the profiles set up on the system.
New profiles can be created in this section.
Profiles are created with a profile name.
Profiles are associated with a rule set.
Profiles may have particular variables (or answers to questions you may pose) set to specific values by adding Profile answers.

#### Accounts ####
Accounts lists all of the user accounts registered on the system.
Accounts can be created by guest users registering to get a user account on the system.
Clicking on an account in the list allows you to edit its associated parameters.
Accounts are associated with the login name of a user.
An account should be associated with a profile and thus may inherit Profile answers.
An account may have variables set to specific default values by adding Account answers similar to Profile answers above.


### SITES ###

Sites is not currently used in the application but technically we should be settting the domain name in there as well as the FQDN of the website.



2.3 USER ACCESS MECHANISM (TO RECOMMENDATIONS)

---


As mentioned above any recommendations served to users can be expanded by clicking on a button on the right side of the interface.
Recommendations can take various forms: images, video, PML (specification/roadmap/interactive graph), Web hyper-links, internal hyper-links etc.



2.4 PRESENTATION OF QUESTIONS IN ORDER OF RELEVANCE, BASED ON USER PROFILE (THIS WAS FOLDED INTO THE USER ACCESS MECHANISM)

---


Changing the ordering of rules in a given rule set (e.g. for IngestUser in the test database):

1. From: **Home › Knowledge › Rule sets**, click on the rule set of interest (for this example click IngestUser).

You should now be in **Home › Knowledge › Rule sets › IngestUser**.  For any given rule you should see on the left of its "bar" a numeric ordering.
This indicates the order in which the rules fire.  In order to change this ordering proceed as follows.

2. Locate the "Move Item" control on the "bar" for the rule you wish to re-order (it is a diamond shaped icon to the right of the X icon on the right of the "bar").

Note that if you accidentally click on the X icon for deletion and the bar turns red, simply click the X icon again to deselect it.

3. Click and hold the "Move Item" icon (the bar will turn yellow) and simply drag the bar to the place in the list where you want the rule to fire.

4. Next click on one of the options to save along the bottom of the window - e.g. "Save and continue editing" if you need to change the order of a number of rules in the list.

This is all you need to do to re-order the list of rules within a rule set.



2.5 KNOWLEDGE BASE "MAINTENANCE"

---


See 3.5 "IMPROVED" RULE SPECIFICATION



2.6 MAINTENANCE USER

---


Specify a maintenance user:

From the administration site **Home › Auth › Users** one can create new users with the "+ Add user" button on the upper right hand side of the interface.
In order to specify a maintenance level user do as follows.

1. Click the "+ Add user" button.

2. Input details for the username, password and confirm password fields and click on "Save and continue editing" at the bottom of the window.

3. You may input data into the "Personal info" area as appropriate.

The "Permissions" area of the window is where one can specify the permissions that apply to the account.

4. A maintenance user must have the tick box for Staff status selected (obviously in addition to needing to have the tick box for Active selected).
> Note that you should not tick the box for Superuser status unless you wish to create a full administration account.

5. From the "Available user permissions" section you will need to select the appropriate permissions for the account you require.
> You may use ctrl-click or shift-click selection.  Click on the blue arrows to move permissions to the "Chosen user permissions" and back.

6. Lastly the account can be assigned to groups.  In addition to any permissions manually assigned, this user will also get all permissions granted to each group he/she is assigned to.




2.7 "EYE CANDY" THIS IS MAINLY A CONSISTENT CSS-BASED LOOK AND FEEL THAT GIVES THE SITE A "MODERN" IMPRESSION

---


2.7.1 Logo


Original artwork specially designed for use of the project.
Helps to strongly distinguish the interface from any similar looking applications the user might use aiding user memory recognition.


2.7.2 Favicon


Important for users who use multiple tabs when using browsers to aid in distinguishing tabs.


2.7.3 User interface design


We have strived for a consistent style for the user front end.


2.7.4 Maintenance interface design


The maintenance interface has a markedly different style to the front end and are thus easy to differentiate.



2.8 REDUCTION IN "CONCEPTUAL NOISE" OF MAINTENANCE INTERFACE

---


Improvements implemented.

See 3.5 "IMPROVED" RULE SPECIFICATION for details.



2.9 PROCESS "ROADMAPS"

---


Note: This was left unimplemented for release 1.

Getting to see a PML roadmap:

The example of a PML roadmap description is triggered when a user answers "Yes" to the following questions:

Are you hungry?				Yes
Do you have a kitchen?		Yes
Do you like cooking?		Yes

Note you can just next past any of the other questions without the need to specify an answer to get to the roadmap.

1. These answers will produce a recommendation button "Make these foods in your own kitchen".

2. Click on this button to expand the details of the recommendation.

3. Click on the link entitled "Click here to view the PML roadmap." in order to be browse to the roadmap description.



2.10 STEP-WISE REFINEMENT OF "HIGH-LEVEL" MODELS

---


It is not clearly understood in the team what this exactly entails.

Unimplemented.



2.11 GRAPHICAL DISPLAY OF PROCESS SPECIFICATIONS

---


2.11.1 Getting to see a PML graph:

The example of a graphical display of a PML process specification is triggered when a user answers "Yes" to the following questions:

Are you hungry?				Yes
Do you have a kitchen?		Yes
Do you like cooking?		Yes


As in the previous feature example, you can just next past any of the other questions without the need to specify an answer to get to the graphical PML.

1. The answers will produce a recommendation button "Make these foods in your own kitchen".

2. Click on this button to expand the details of the recommendation.

3. Click on the link entitled "Click here to view the interactive PML Graph." to browse to a Web page displaying the graphical PML specification.

4. If the graph appears to be too large or small you may find it helpful to zoom your browser in or out as appropriate (e.g. "ctrl" and "+").

5. In the graph itself additional information is provided to the user when they click on any of the nodes.
> This information is in the form of a pop-up and can be dismissed by clicking on the "OK" button in the pop-up.

2.11.2 Display of PML specification -

Along side with the link for the graph viewer, a link to see the PML specification is available. This brings the user to a plain text display of the PML specification. This specification is useful for tools that can read PML.

2.12  USER PROFILES

---


2.12.1 Registration

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

The Log out link will log a user out of the site bringing them back to guest level access.

The Reset link will reset any saved question data.
For more detail see section 2.14 SAVE/RESTORE SESSION STATE ON LOGOUT/LOGIN.



2.13 SPECIFICATION OF USER PROFILES (BY MAINTAINER)

---


User profiles are specified in the administration interface from: **Home › Register › Profiles › Profiles**

Profiles lists all the profiles set up on the system. New profiles can be created in this section.
Profiles are created with a profile name.
Profiles are associated with a rule set - a rule set is a list of facts automatically asserted when a user starts a line of questions e.g. likes cake = No, is hungry = Yes etc.
Thus the profiles may have a list of variables set to specific default values from this rule set.


2.13.1 Create a Profile:

1. Click on the button "Add profile"

This will bring you to **Home › Register › Profiles › Add profile**

2. Next input a name for the profile.

3. Click on the dropdown list box beside "rule set:" to choose a rule set to associate with the profile (you can also define a new rule set from here using the "+" icon).

4. Once you are happy with the details choose one of the save options at the bottom of the screen.



2.14 SAVE/RESTORE SESSION STATE ON LOGOUT/LOGIN

---


The system is designed to save the state of a line of questioning for registered users.
This feature is unavailable for guest users.

Once a user is logged in the user may reset their saved data with the "Reset" link from the banner links along the top of the window: [Account | Reset | Log out ](.md)

When a user clicks on the "Start" button the system will display, in the Previously Answered section under the Questions "Nothing so far!".
This is to indicate that there is no history of questions answered stored on the system.

As soon as a user selects an answer to a question and clicks "Next" this answer is saved by the system into a database and associated with the account.
The system will store up any answers specified by the user in this fashion.
As soon as "Next" is clicked the database is updated and the answers are saved allowing the user to come back and continue from where they were previously.

If a user decides not to give an answer to any particular question and then logs out they will be re-asked any questions they did not specify answers for previously.

Users have the option to change their previously answered questions with the "Change Answers" button which appears beneath the Previously Answered section.

In addition to the question state, the associated Recommendations and Reasons are also saved.



2.15 ALLOW VIDEOS, PDF FILES, PML MODELS TO BE ATTACHED OR LINKED TO RECOMMENDATIONS

---


Resource files can be linked to recommendations as follows:

1. From the administration interface section **Home › Knowledge › Recommends** select a Recommend by clicking on it.

2. Select the resource from one of the 3 link fields as appropriate for your need.

3. You may attach multiple resource links in the "OtherLinks: " section.

4. Additionally external Web hyper-links may be added to a recommendation along with some descriptive text.



2.16 SPECIFICATION OF VIDEOS, PDF FILES, PML MODELS TO BE ATTACHED OR LINKED TO RECOMMENDATIONS (BY MAINTAINER)

---


Artifacts (resources) should be stored on the server hosting the DSS, or optionally linked to on YouTube or other external web sites - see 2.15 (step 4) listed above.
Resource files can be added (stored) to the server using administration interface at **Home › Knowledge › Resource files**.

In order to add a resource file:

1. Click on the button for "+ Add resource file".

2. You must input a description of the file in the "Description:" field.

3. Click on the "Browse..." button to browse to the resource you wish to add to the system.

4. Files can be restricted by user by ticking the box for "Restricted" and highlighting the users who can access the file in the "Restricted to:" section.



2.17 ACCESS (TO SUPPORTING ARTIFACTS) BASED ON LOGIN ID

---


Resources can be restricted by user login ID following the steps listed in 16 above when adding a resource.  An existing resource can be modified from **Home › Knowledge › Resource files**.

To modify an existing resource:

1. Click on the description of the resource file link.

2. From this screen you can change the "Owner:" field, as well as set the restriction tick box, "Restricted".

3. By highlighting any number of login ID in the "Restricted to:" section you set which login IDs have access to the resource.



2.18 EVOLVING PROFILES

---


The rule set associated with a user profile may be updated.
The system will automatically ask the new question set the next time the user resets their saved state (starts over).



2.19 ENHANCED DISPLAY OF MEDIA, FOR EXAMPLE IN EMBEDDED VIEWERS

---


Instead of displaying all media in recommendations at the same time on the Web page users must click on buttons to expand recommendation content.
Media content is displayed embedded ensuring that it is not easily missed by users.
Additionally each of the embedded resources is listed numerically with the hyper-link (internal or external as appropriate) to the original resource.



2.20 SEPARATE MAINTENANCE FOLDERS

---


A non-admin maintainer login ID can only modify those resource files which they have uploaded under that login ID.
Any maintenance user can attach them to a recommendation (so long as the resource is not restricted from them).
The idea here is that each maintenance user gets to "own" his/her uploaded resources and they are the only non admins who can modify or delete the resource.





---


---

3.0 FEATURES WALKTHROUGH (RELEASE 2 FEATURES)

---


---


The following sections describe details to give an overview for use of the feature set implemented for the second (and final) release of MAGPIE.


3.1 'CLICKABLE' PML GRAPHS

---


Implemented.  For instructions on inspecting this feature, see above: 2.11 GRAPHICAL DISPLAY OF PROCESS SPECIFICATIONS.



3.2 PML 'FLIGHT SIMULATOR'

---

3.2.1 Link the two via 'up'

---

3.2.2 Save 'Flight Simulator'

---


As agreed with the client we did not implement these features.



3.3 ASSEMBLE PROCESS SPECIFICATION FROM FRAGMENTS BY MATCHING INPUTS & OUTPUTS

---


Not implemented.



3.4 ALLOW 'OR' OF FACTS (AS WELL AS 'AND') TO FIRE RECOMMENDATIONS

---



To see a logical 'OR' in action in the test database one merely needs to answer yes to either of the two questions:

  * Have you just been in the rain?

  * Were you just exercising vigorously?

The recommendation "You should dry off with a towel" is presented along with a link to a magpie stealing a towel.



See section 3.5 "IMPROVED" RULE SPECIFICATION below.



3.5 "IMPROVED" RULE SPECIFICATION

---


Rules are specified in the form of rule sets.
A profile type is associated with a rule set (in the Profiles section of the administration console).
From **Home › Knowledge › Rule sets** click the "+ Add rule set" button to create a new rule set.
Rule sets are made up of one or more rules.
Rules are added to a rule set by using the "Add Rule" button available when editing a rule set.
When specifying a rule there are three main sections:  Premises, Conclusions and Recommendations.


3.5.1 Premises

Allows you to specify variables with an associated value for Yes or No (representing the users answers to specific questions).
Premises are what fires the questions to the users of the system.  Rules must have premises.
You may specify multiple Premises and may avail of logical operators and parenthesis to build up a complex premise as follows:

Lchoice - You can specify characters from the set: { '(', ')', '&', '|' }

Variable - A variable specified in the Variables section of the administration interface (or click the blue '+' icon to add a new one)

Value - Yes or No from the drop down list box

Rchoice - You can specify characters from the set: { '(', ')', '&', '|' }


3.5.2 Conclusions

Premises in a rule, when triggered appropriately, assert question facts in the form of conclusions - see 3.6 below for more detail.
You may specify multiple conclusions in a given rule.
Conclusions may be used in effect to fire additional rules from the rule set.
The form of a conclusion is:

Variable - Choice from the drop down list box (or click the blue '+' icon to add a new one)

Value - Yes or No from the drop down list box


3.5.3 Recommendations

Recommendations are what the system is designed to serve to users based on the inference engine.
There can be multiple recommendations associated with a given rule.

THERE MUST BE AT LEAST ONE RECOMMENDATION ASSOCIATED WITH A RULE AS THESE RECOMMENDATIONS ARE USED AS GOALS DURING THE INFERENCE STEPS.
THE GOAL OF THE SYSTEM IS TO FIND RECOMMENDATIONS SO IT IS POINTLESS TO HAVE RULES WITHOUT A RECOMMENDATION AT THE END.

The form for Recommendations is:

Recommend - Drop down list box of recommendations previously defined in the Recommendation section of the admin interface (or click the blue '+' icon to add a new one).

Rank - A feature for assigning a priority ranking to recommendations.



3.6 RULES ASSERT FACTS AS WELL AS RECOMMENDATIONS

---


Rules may assert facts in the form of conclusions.

From **Home › Knowledge › Rule sets** one can add or edit an existing rule set.

When specifying a rule you may list premises which when evaluated collectively will result in conclusions (asserted facts) being set.
This is in addition to any recommendations fired by the list of premises being evaluated.
These conclusions as asserted facts may in turn fire other conclusions or recommendations depending on how the rule base is configured.



3.7 FACTS DETERMINE WHETHER QUESTIONS ARE ASKED

---

3.8 FEEDBACK TO USER PROGRESS & REASONING BEHIND RECOMMENDATIONS

---

3.9 ALLOW USER TO REVISE ANSWERS

---

3.10 SHOW IMPLICITLY ANSWERED QUESTIONS

---


For 3.7 - 3.10 - Implemented in user interface - Please see 2.2 USER INTERFACE for details.