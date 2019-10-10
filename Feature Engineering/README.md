# Feature Engineering 

We developed a wholistic approch to develop features that can help answer some of the key questions. 

<b> **Time:** </b>

Accounting for the temporal characteristics of mouse interactions can improve the predictive power of a model. Similarly, we measure the duration of each gesture in milliseconds.
 
<b> Coverage: </b>

These features include the number of x, y points observed in a gesture and the sum of their intra-distances, which indicates how compact or dispersed a gesture is. An interesting observation about coverage is its medium-size correlation, which suggests that the size of the surface that a mouse gesture traverses on is related to the interestingness of the content the user is interacting with. 
 
<b> Distance:</b>

These features include the total distance that the cursor has traveled, the maximum, minimum, average, and standard deviation of the distances of all consecutive pairs in a gesture. They are computed using the Euclidean distance and the pixel distance travelled on the X and Y axes. As seen from Table 1, this category of features are significantly correlated with news article interestingness. Although we lack knowledge about the directionality of this relation (i.e. positive or negative), it is still evident that the distance traversed by the mouse cursor indicates how much the user interacted with the news article and, to some extent, how interesting the latter was perceived. 

<b>Direction:</b> 

For each consecutive pair in a mouse gesture we determine the direction of the movement and normalise
