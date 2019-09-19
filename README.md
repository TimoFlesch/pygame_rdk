# Random Dot Kinematogram
a random dot kinematogram implemented in pygame
The RDK is fully customisable, i.e. you can change its colour, size, dot coherence, duration of display etc.
Each frame is written to a numpy array and returned by the RDK object, which makes this implementation
suitable for simulations etc.  

### Examples
The easiest way to get started is to call the rdk script and play around with different parameters

#### Trials with Fixation
I've also implemented a fixation cross and aperture, as well as a separate class to define trial sequences.
Below is an example:  
![trialseq](gifs/example_trial.gif)

#### Dot coherence
The coherence of random dot motion, i.e. the percentage of dots moving in the
requested direction, can be varied parametrically.  

**1. Example with coherence of 100%**  
![coher100](gifs/coherence100pcnt.gif)  

**2. Example with coherence of 50%**     
![coher100](gifs/coherence50pcnt.gif)  

**3. Example with 0% coherence**  
![coher100](gifs/coherence0pcnt.gif)


#### Dot size and density
Both the number of dots and their size can be adjusted.

**1. Example with small and many dots**   
![smallandmany](gifs/smallandmany.gif)

**2. Example with few and large dots**    
![fewandlarge](gifs/largeandfew.gif)  

#### Dot speed
You can also change the speed with which dots move over the screen (in terms of pixels per frame)  

**1. Slow dots**  
![fewandlarge](gifs/largeandfew.gif)  

**2. Fast dots**   
![fewandlargefast](gifs/largeandfew_fast.gif)  
