# Cryptopunks
 Crypto Visualization Project
 
 # TODO FRONTEND
  - [x] Create Flask App to Communicate with BackEnd
  - [ ] Tab1: Graph Indicators -> Price
  - [ ] Tab2: Graph Heatmap -> volume/price
  - [ ] Tab3: Allow user to create custom QLearning/DecisionTree -> Graph results overalayed on Price
  - [ ] Tab4: Aesthetic Feature for Points -> Graph candlestick/indicator iteratively as an animation, instead of loading/displaying all candlesticks as imgage
  - [ ] Tab5: Aesthetic Feature -> Graph BTC MarketCap over Time by increasing area of circle (Each year has circle/size of circle is market cap)
  - [ ] Tab6: Aesthetic Feature -> Allow User to draw lines on price graph (User can manually draw Long term Support/Ceilings)
 
 # TODO DATAFRAME/DATA ENGINEERING
  - [x] Get Final List of Indicators
  - [x] Create Spark Functions to calculate all Indicators
   - [x] Input -> Allow user to give custom Day range as Parameter
   - [x] Output -> Convert Spark Dataframe and return Pandas Dataframe for consumption by downstream models
 
 # TODO QLEARNING/DECISION TREE
  - [ ] Making Decision Tree
  - [ ] Create QLearning/DecisionTree Wrapper 
   - [ ] Input -> Allow user to input parameters for Models and run new model on Data
   - [ ] Output -> Return Dataframe with custom input from user to FrontEnd
  - [ ] Integrate Optimal QLearning/DecisionTree results with Indicator Dataframe to be used by frontend 

# How To Run
1. Install Docker if it isn't already installed on your machine. Installation instructions can be found [here from the CSE6242 HW3 resources](https://poloclub.github.io/cse6242-2022spring-online/hw3/Docker_Getting_Started_Guide_Spring_2022.pdf).



2. On the command line, change directories to the root of this repository/folder.

`cd ~/Downloads/Cryptopunks/`


3. Build a Docker image named cryptopunks-app using the following command on the command line. Please note this image is about ~2GB large but it can be deleted later as described on step 4. In the event of an error, ensure that buildKit is set to True on your Docker installation. [This link](https://stackoverflow.com/questions/64221861/an-error-failed-to-solve-with-frontend-dockerfile-v0) may be helpful.

`docker build --tag cryptopunks-app .`


4. Confirm the image is created:

`docker images`

Alternatively, if you need to delete the image run the following command:

`docker image rm -f <IMAGE ID here>`


5. Using the newly created cryptopunks-app Docker image, create and run a Docker container. By default Flask applications run on port 5000 so we expose that port.

`docker run -d -p 5000:5000 cryptopunks-app`


6. Confirm the container is up and running:

`docker ps`


7. Open your browser and navigate to the following URL to confirm Flask is running successfully:

http://127.0.0.1:5000/ 
