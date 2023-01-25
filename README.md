# What is CLTV?

Probabilistic lifetime value estimation with time projection will be performed.
CLTV base transaction : average earnings per purchase * number of purchases

The transactions here will go according to the above transaction.

For simplicity, the formulation has been modified as follows.

CLTV base transaction: number of purchases * average earnings per purchase.

The formulation that we will discuss in this chapter will be based on probabilistic estimation.
So our formula is;
CLTV = Expected Number of Transaction * Expected Average Profit. The Expected Number of Transaction part of this formula, which is about probability, will be modeled with a probability formula, and then the expected number of purchases and expected number of transactions will be estimated for each person by using the behavior patterns we modeled with this probability distribution in a conditional way, that is, for each person. If the Expected Average Profit part is
We will model the average profit value of all customers as probabilistic, then when we enter the person characteristics using this model, the probabilistic average profit value for each person will be calculated by feeding the conditional expeceted average profit values on the main mass.

Two models will be used here.
CLTV = BG/NBD MODEL * GAMMA GAMMA SUBMODEL
and the CLTV value will be calculated.

Expected purchase status (Expected Number of Transaction) will be estimated with BG/NBD MODEL.

The Expected Average Profit value will be estimated with the GAMMA GAMMA SUBMODEL.

Expected Number of Transaction with BG/NBD

What is Expected?
Expected = Used to express the expected value of a random variable.

The expected value of a random variable is the mean of that random variable. A random variable is a variable that gets its values from the result of an experiment.
 
The BG/NBD model allows the Expected Sale Forecasting value to be calculated.

(The BG/NBD model is a stand-alone model used as a sales forecasting model.). Also referred to as BG/NBD Buy Till You Die. That means buy until you die.

The BG/NBD model probabilistically models the two processes for the Expected Number of Transaction as follows.
Transaction Process(Buy,Purchase process) + Dropout Process(Till you die,Abandonment process)

Transaction Process(Buy,Purchase Process): As long as it is alive, the number of transactions to be performed by a customer in a certain time period is distributed with the transaction rate parameter.

As long as a customer is alive, he will continue to make random purchases around his own transaction rate.

Transaction rates vary for each client and are for the entire audience.
gamma distributed (r,a) (i.e. probabilistic distributed)

Dropout Process: Each customer has a dropout rate with probability p. That is, the state of being inactive.

A customer drops with a certain probability after making a purchase. Dropout Rates vary for each client and beta is spread out for the entire audience.

Gamma Gamma Submodel
It is used to estimate how much profit a customer can generate on average per trade. The monetary value of a customer's transactions is randomly distributed around the average of their transaction values.
The average transaction value may change between users over time, but not for a single user. The average transaction value is gamma distributed among all customers.
