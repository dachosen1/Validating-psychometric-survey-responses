## <b> Hidden Markov Models for Mouse Movements </b>


### Goal: 
- The ultimate goal for this analysis is to analyze all the user's mousement and determine the key outliers 

### Assumption: 
- Since we are analytize the all the users mouse patterns to identity outliers, we are assuming that the majority of the users have completed the survey in good faith. Violaton of this principle could wrongly identity users who completed survey in good faith as fraud
- Future state is indepent of the past given that we know the present 

### Approach: 
- Converted x and y direction into cardinal coordinates, We ignore the first coordinate and measure the direction thereafter
- Calculated the transition probabilities, and identy the current state probability
- Implemented the verbeti algority to identy the most likey state and calculate the likely movement proability for user 365, which is a user that the team had suspicion on. 

### Next Steps
- Sequence to sequence models are based on the assumption of a consitant time interval. The current time internval vary by user, and by mousement. We have researched different methodologies to smoothen the time sequence, and the best option is to use a golay filter to increase the signal-to-noise ratio without greatly distorting the signal
- We discovered that the mouse patterns vary by pages, we introduced a lot noise by capturing all 15 pages.The average user has about 5000 sequences and which can difficult to manage,  In the next iteration we will model each page seperately. This approach reduce the moeling sequences from 5000 to 300
- User on mobile devices have different patterns then users on laptop computers, and we discovred that the  model capture the relationship between the different types of devices. We need to model mobile devices and window pc seperatly 


### Key Questions: 
1) We noticed that many observations do not record all the user’s journey. Some records do not include all the clicks for radio buttons. We identified only 54 users click through each question. How would you tackle the problem? 

2) We would like to hear your opinion about working towards a research paper. Do you think we should avoid this, publish a whitepaper or an official journal paper? What would be the benefit of each option? 

3) If we really want a better validation model than the one that Dotin is using now, we need to avoid the validation questions and think outside of the box. A method we discussed internally is to use HMM with direction movement to find a “Best directional pattern” that resembles the optimal response. We then plan to calculate the difference between our “best fit” and each individual user mouse journey. The journeys that have the highest variance would then be classified as a falsely filled survey. Do you think we are going in the right direction? 

4) In trying to get the read time for our users, we might also need to account for how much time it takes people on avg in our dataset to read through a question. However, we don't think that's a very useful metric because it gets influenced by outliers (the one taking the survey too fast and the ones that are too slow). We are currently using the median instead. Can you recommend something else too?

5) The end goal would be to produce a probability index for each page for user. Our intital approach to identity the fraud user is to conduct a K-Means, and cluster the outliers. An alternaive could be to establish some kind of threshold. Do you have any thoughts on these approaches, and is there a more effective way to identify the outliers? 
