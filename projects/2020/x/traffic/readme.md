# Traffic Project - Experiments
As a beginner I decided to start of by replicating the machine learning algorithm from the lecture, with very limited success: The final accuracy was 0.0544, which is very low.
After that initial test I decided to play around with different parameters and describe the results and my thoughts.
## Change activation functions
For the sake of simplicity I will keep both the convolution layer's and the hidden layer's activation function the same.
### No activation function
Accuracy: 0.9379  
Loss: 2.6342  
I am not sure why the accuracy improved so much compared to the original code, Unfortunately, keras does not provide information on this scenario. In our case it works really well.
### Sigmoid activation function
Accuracy: 0.9813  
Loss: 0.0846  
The sigmoid activation works very well. I assume that is because instead of a binary result, such as ReLu provides, it actually calculates a confidence value between 0 and 1.
### Softmax activation function
Accuracy: 0.4111  
Loss: 1.9982  
The results with softmax are significantly better than with the ReLu actication function, most likely because the network learns better with distributed probabilities compared to a binary results (as there are multiple categories available).
## Change output activation function
For evaluation purposes I am going to use the original code from the lexture and only change the output activation function.
### No output actication function
Accuracy:  0.0301  
Loss: 8.2058  
I am not sure why the accuracy improved so much compared to the original code, Unfortunately, keras does not provide information on this scenario. In our case it works really well, similar to when we changed the other actication functions.
### ReLu activation function
Accuracy: 0.0061  
Loss: nan  
The results are horrible, it appears that the neural network got it wrong almost the entire time. I assume it does not help that every single node only provides 0 or 1 results, as learning based on that is very slow according to the 10 iterations.
### Sigmoid activation function
Accuracy: 0.0556  
Loss: 3.4927  
The results are quite similar to the initial setup. Since both sigmoid and softmax show some sort of probability as a result that is plausible. Major changes are not expected as both the hidden and convolution layer remain unchanged and train with binary results.
## Double the number of nodes
Accuracy: 0.4242  
Loss: 1.9518  
Doubling the number of nodes drastically improves the performance. Due to the additional input the results the network trains on most likely increase the precision. Nonetheless other parameters still provide far greater accuracy.
## Change the number of filters
### Doubled
Accuracy: 0.0538  
Loss: 3.5008  
While slightly better a growing number of filters used to evaluate the image does not really influence the final outcome.
### Halfed
Accuracy: 0.0547  
Loss: 3.5019  
Similar to the previous experiment a reduction of the number of filters also does not really influence the outcome.
## Increase the poolsize
Poolsize: (4,4)  
Accuracy: 0.0570  
Loss: 3.4928  
Quadrupling the poolsize slighlty improves the results, but I would not classify the change as significant. Similar to the number of filters it does not seem to influence the outcome as long as other parameters are not changed.
## Change the dropout
### 0.75
Accuracy: 0.0547  
Loss: 3.4985  
Decreasing the dependency on single nodes by increasing the dropout has almost no influence on the final result. That tells us that the algorithm is not overfitting, but as long as other parameters are badly adjusted the results remains bad.
### 0.25
Accuracy: 0.0526  
Loss: 3.4908  
Also, increasing the potential dependency on single nodes barely influences the outcome.
## Add an additional layer
Accuracy: 0.0545  
Loss: 3.5040  
Simply adding an additional hidden layer without changing parameters does not really change the outcome. That is expected as the the training process is not influenced.
# Conclusion
After running several experiments it becomes obvious that the activation functions and additional nodes improve the overall outcome of the model that we are training here. Specifically the sigmoid and softmax activation functions appear to have a positive effect. For an image-recognition AI that makes perfect sense, since they are the only functions, that do not provide binary results. If we were looking for a binary image classification, e.g. if the image a stop sign, the relu activation function might deliver better results.  
It also became apparent that other parameters of the algorithm, such as the dropout, or additional hidden layers only provide additional support as they do not drastically change the actual logic.  
# Final adjustment
Based on the prior experiments I decided to run some additional tests with sigmoid and softmax and increased the number of nodes. The activation function in both the convolution layer and the hidden layer are sigmoid now, while the final output uses softmax. This set-up has resulted in an accuracy of >0.098 with a loss <0.05.