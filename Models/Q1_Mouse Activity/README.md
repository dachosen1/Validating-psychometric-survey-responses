## <b> Hidden Markov Models for Mouse Movements </b>


### Goal: 
- The ultimate goal for this analysis is to analyze all the user's mousement and determine the key outliers 

### Assumption: 
- The majority of the users complete the survey in good faith
- Future state is indepent of the past given that we know the present 

### Approach: 
- Converted x and y direction into cardinal coordinates, We ignore the first coordinate and measure the direction thereafter
- Calculated the transition probabilities, and identy the current state probability
- Implemented the verbeti algority to identy the most likey state and calculate the likely movement proability for user 365, which is a user that the team had suspicion on. 

### Preliminaty finding 
- There are some user who have patterns that statistically different from the majority
- Only about 64 users went on each page .

### Next Steps
- Sequence to sequence models are based on the assumption of a consitant time interval, and we need to adjusted the modify sequene using a golay filter 
- We discovered that the mouse patterns vary by pages, we introduced a lot noise by capturing all 15 pages. In the next iteration we will model each page seperately
- User on mobile devices have different patterns then users on laptop computers, and the model woulnd't be able to generalize between those user segments. We need to model mobile devices and window pc seperatly 
- Implement a RNN to further test the idea

### Key Questions: 
- Should we include only users that completed the entire page or the just a page in the survey 
- Should we analyize a window of mouse movements rather than the entire movement
- What threshold determines if a person is fraud 
