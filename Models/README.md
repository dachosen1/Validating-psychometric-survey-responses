
<b> MODELING APPROACH </b>

We have developed an overview of the modeling techniques that will be used throught this semester, and each model presents a different perspective, and will be collecitively provide a holictic answer to the research questions.  

1. **Mouse Activity:** How do we use user mouse activity to validate survey answers to psychometric questions? 

Currently, we plan to study <b> Hidden Markov Models </b> in-depth to create an approach to select some features which might help us 
identify behavioral traits of users while performing surveys. As of now, we are thinking of using displacement and direction of mouse
movement followed by the user as our potential input features. 

<b> Components of a potential HMM: </b>

- states = ('mouse movement direction' )
- observations = ('clicks', 'movements', 'scrolls', 'votes_response')
- transition_probability= (represents the probability of moving from one state to another )
- emission_probability=('valid': {'clicks': %, 'movements': %, 'scrolls': %, 'votes_response': %}
                        'non-valid': {'clicks': %, 'movements': %, 'scrolls': %, 'votes_response': %) 
   
 HMM would allows us to determine the users with mouse movements that have a low sequence probabilty. 

2. **Response Time:** Does the variability in survey response time indicate suspicious behavior?

For this approach, we have created a baseline logistic regression model with the features as detailed in the Feature Engineering ReadME. 
The most important features as a result of the logistic model are:
- How users answer some questions
- movements right,left, down etc
- no of records(scroll+click+moves) by user
- total time taken by user to complete survey


Ther are a number of variation in HMM and we plan on exploring the ones that makes sense for this project. 

The baseline model will be rebuilt with additional features through our iterative process.

3. **Survey Question:** Does the level of suspicious behavior vary across different types of survey questions?

Factor analysis is a statistical method used to describe variability among observed, and it will allow us to formulate a question similarity index using the user responses. Based on that index we can identify the types of questions that are a higher risk of receiving fraudulent responses. 














