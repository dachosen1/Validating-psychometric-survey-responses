
<b> MODELING APPROACH </b>

For this project, two major approaches to modeling will be pursued:

<b> Classification (Supervised Approach): </b>

For this approach, we have created a baseline logistic regression model with the features as detailed in the Feature Engineering ReadME. 
The most important features as a result of the logistic model are:
- How users answer some questions
- movements right,left, down etc
- no of records(scroll+click+moves) by user
- total time taken by user to complete survey

The baseline model will be rebuilt with additional features through our iterative process.

<b> Unsupervised Approach: </b>

Currently, we plan to study <b> Hidden Markov Models </b> in-depth to create an approach to select some features which might help us 
identify behavioral traits of users while performing surveys. As of now, we are thinking of using displacement and direction of mouse
movement followed by the user as our potential input features. 

<b> Components of a potential HMM: </b>

- states= ('valid', 'non-valid' )
- observations= ('clicks', 'movements', 'scrolls', 'votes_response')
- start_probability= ('valid': avg x%, 'non-valid': avg y% )
- transition_probability= ('valid': change in x%, 'non-valid': change in y% )
- emission_probability=('valid': {'clicks': %, 'movements': %, 'scrolls': %, 'votes_response': %) 

