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
  - [ ] Create Spark Functions to calculate all Indicators
   - [ ] Input -> Allow user to give custom Day range as Parameter
   - [ ] Output -> Return Dataframe to frontend for visualization
 
 # TODO QLEARNING/DECISION TREE
  - [ ] Making Decision Tree
  - [ ] Create QLearning/DecisionTree Wrapper 
   - [ ] Input -> Allow user to input parameters for Models and run new model on Data
   - [ ] Output -> Return Dataframe with custom input from user to FrontEnd
  - [ ] Integrate Optimal QLearning/DecisionTree results with Indicator Dataframe to be used by frontend 
