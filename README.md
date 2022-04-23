# Cryptopunks
 Crypto Visualization Project

# Description

The Cryptopunks application allows users to train and test a Q-learning or Grid Search model for recommending buying, selling, or holding Bitcoin cryptocurrency. The user inputs for the model (such as the lookback windows for moving averages) include parameters that calculate the following variables that are then used to train and test the model:
- Average Twitter Sentiment (obtained using the pre-trained [NLTK Vader Sentiment Analyzer](https://www.nltk.org/api/nltk.sentiment.html) on 4 GB of tweets about Bitcoin from 2014 to 2019)
- Simple Moving Average (SMA)
- Bollinger Bands
- Moving Average Convergence Divergence (MACD)
- Stochastic Oscillator
- On Balance Volume (OBV)
- Momentum

Additionally the following hyperparameters are selected by the user as well:
- Alpha
- Gamma
- Random Action Rate (RAR)
- Random Action Decay Rate (RADR)
- Simple Moving Average (SMA) Threshold
- Stochastic Oscillator Upper and Lower Limit
- Momentum Threshold
- Sentiment Threshold

FrontEnd: The front end HTML/CSS/Javascript files can be found in our [visualization folder](https://github.com/vikkumar2021/Cryptopunks/tree/main/visualization). The front end was created using Observable and D3. The front end is interactive and allows the user to input parameters for the data pipeline and model algorithm (Q-learning or Grid Search) via sliders, dropdowns, and checkboxes. The frontend queries the backend to obtain the Q-learner or Grid Search model results and renders the visualizations using the returned JSON data.

Backend: Our backend consists of a REST API that runs in a Docker Container. This API is responsible for serving the data the frontend needs based on input parameters the user selects on the interactive visualization. The API was built using the Flask web framework. The front end submits a HTTP GET request to the `run_qlearner` or `run_gridsearch` Flask API end point. The parameters in the URL are parsed and passed to the Pyspark pipeline which in turn processes the Bitcoin price data and the Twitter sentiment data. The resulting Spark dataframe is then converted to a Pandas dataframe and passed to the model (either Q-learner or Grid Search). The model is run on the Pandas dataframe and the training and testing results are returned to the front end as a JSON.

![CryptopunksApplicationFlow](https://github.com/vikkumar2021/Cryptopunks/blob/main/CryptopunksApplicationFlow.png)


# Installation & Execution
1. Download the Cryptopunks application from the [Crypopunks GitHub](https://github.com/vikkumar2021/Cryptopunks/). If you are peer reviewing this for CSE-6242 then you may skip this step as you have already downloaded the file.


2. Install Docker if it isn't already installed on your machine. Installation instructions can be found [here from the CSE6242 HW3 resources](https://poloclub.github.io/cse6242-2022spring-online/hw3/Docker_Getting_Started_Guide_Spring_2022.pdf).

3. On the command line unzip the download and change directories to the "CODE" folder in the root of the repository/folder. The below steps are intended to be completed on the command line interface.

 `cd ~/Downloads/Cryptopunks/CODE/`

To ensure you're in the correct directory, when you run the `ls` command you should see the Dockerfile as well as this current README.md file listed.


4. Build a Docker image named cryptopunks-app using the following command on the command line. Please note this image is about ~2GB large but it can be deleted later as described on step 4. In the event of an error, ensure that buildKit is set to True on your Docker installation. [This link](https://stackoverflow.com/questions/64221861/an-error-failed-to-solve-with-frontend-dockerfile-v0) may be helpful.

  `docker build --tag cryptopunks-app .`


5. Confirm the image is created:

  `docker images`

Alternatively, if you need to delete the image run the following command:
  `docker image rm -f <IMAGE ID here>`


6. Using the newly created cryptopunks-app Docker image, create and run a Docker container. By default Flask applications run on port 5000 so we expose that port.

  `docker run -d -p 5000:5000 cryptopunks-app`

For Mac users, AirPlay may already be using port 5000 on your computer. If this is the case, use port 5001 instead with this modified command:

  `docker run -d -p 5001:5000 cryptopunks-app`


7. Confirm the container is up and running:
  `docker ps`


8. Open your browser and navigate to the following URL to confirm Flask is running successfully: http://localhost:5000/


9. Next run a local python HTTP server on port 8000:

  `python -m http.server 8000`

On your browser navigate to the following URL: http://localhost:8000/CODE/visualization/


10. You should see the `visualization` folder on your browser. Click into it and this should launch the Cryptopunks application.
