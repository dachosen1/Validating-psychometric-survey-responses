## Feature Engineering 

### The features below were created based on the mouse_paths and votes datasets:

These features are created on the user level and hence the values are aggregated 

#### CURRENT FEATURES: 

| Feature Category        | Feature Name | Feature Description |
| -------------           | ------------ | ------------------- |
| Mouse Activity Related  | Click Count  | Number of times a user has answered a question
| Mouse Activity Related  | User Record Count | Number of times user has performed any mouse activity (scroll+moves+clicks)
| Mouse Activity Related  | Validation   | Target Variable for supervised machine learning (boolean); classification modeling
| Mouse Activity Related  | average_click_delay | Average time taken between one click and the next; aggregated by user
| Time Related            | Max time lapsed | Total time taken by the user to complete the survey 
| Distance Related        | Total Distance  | Total distance traveled by the user (Euclidean distance)
| Distance Related        | Measure_width_covered | A feature to give us a measure of screen coverage by user in terms of width (x coordinate)
| Distance Related        | Measure_height_covered | A feature to give us a measure of screen coverage by user in terms of height (y coordinate)
| Direction Related       | Moves left , Perc of left movements | The count and percentage of instances when the user moves from right to left on the screen 
| Direction Related       | Moves right, perc of right movements | The count and percentage of instances when the user moves from left to right on the screen 
| Direction Related       | Moves up, perc of up movements | The count and percentage of instances when the user moves from bottom to top on the screen 
| Direction Related       | Moves down, perc of down movements | The count and percentage of instances when the user moves from top to bottom on the screen 
| Direction Related       | No horizontal movement | Count and percentage of instances when user shows no horizontal movement on the screen
| Direction Related       | No vertical movement   | Count and percentage of instances when user shows no vertical movement on the screen                                                                             |
| Survey Related          | Bf_votes_1,2,3,4,5, Bs_votes_1,2,3,4,5, Miq_votes_1,2,3,4,5, pgi_votes_1,2,3,4,5,6,7                 | Choice of answers for each category for each question
| Survey Related          | Bf_abs_min_max_response, Bs_abs_min_max_response, Miq_abs_min_max_response, pgi_abs_min_max_response | Checks whether the user has selected all 1s (absolute minimum value of question choice selection) or 5s/7s (absolute max value of question choice selection) per question category type (bf_questions, bs_questions, miq_questions, pgi_questions). Boolean          


### ADDITIONAL FEATURES: 

##### Working on some other features which are listed as follows:

###### 1) More detailed information on direction of user movements such as NE, NW, SE, SW, NN, SS along with distance traveled in that direction (will be done on each user movement level) (idea is to use this feature as an input in Hidden Markov Model)

###### 2) Calculate the average read time per survey question, and deduct the read time per user per survey question based on the radio click and time elapsed features to find whether user has spent less or more time than average to read the survey question.

###### 3) Perform word2vec and clustering to group survey questions by semantic similarity and calculate average score per clustered question group for each user. 
