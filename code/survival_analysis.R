library(survival)
library(survsim)

data <-read.csv('/Users/Yuxia/Desktop/survival/survival_code/data/survival_com_new_data.csv', head = TRUE); 
faim <- factor(data$aim);

fit.tdc <- coxph(Surv(tstart, tstop, endpt)~ faim + scale + intensity + domination, data); fit.tdc
Call:
coxph(formula = Surv(tstart, tstop, endpt) ~ faim + scale + intensity + 
    domination, data = data)

                 coef  exp(coef)   se(coef)      z        p
faim2      -1.460e+00  2.322e-01  3.687e-01 -3.961 7.47e-05
faim3       8.806e-01  2.412e+00  1.691e-01  5.208 1.91e-07
faim4      -4.414e-01  6.431e-01  2.971e-01 -1.485   0.1374
faim5       3.301e-01  1.391e+00  1.894e-01  1.743   0.0813
faim6       5.166e-03  1.005e+00  4.249e-01  0.012   0.9903
faim7       1.966e+00  7.145e+00  2.310e-01  8.513  < 2e-16
scale      -5.227e-01  5.929e-01  5.459e-02 -9.575  < 2e-16
intensity  -3.664e+01  1.227e-16  9.400e+00 -3.897 9.72e-05
domination -3.120e-01  7.320e-01  2.743e-01 -1.138   0.2553

Likelihood ratio test=261.3  on 9 df, p=< 2.2e-16
n= 987, number of events= 260 

summary(fit.tdc)
Call:
coxph(formula = Surv(tstart, tstop, endpt) ~ faim + scale + intensity + 
    domination, data = data)

  n= 987, number of events= 260 

                 coef  exp(coef)   se(coef)      z Pr(>|z|)    
faim2      -1.460e+00  2.322e-01  3.687e-01 -3.961 7.47e-05 ***
faim3       8.806e-01  2.412e+00  1.691e-01  5.208 1.91e-07 ***
faim4      -4.414e-01  6.431e-01  2.971e-01 -1.485   0.1374    
faim5       3.301e-01  1.391e+00  1.894e-01  1.743   0.0813 .  
faim6       5.166e-03  1.005e+00  4.249e-01  0.012   0.9903    
faim7       1.966e+00  7.145e+00  2.310e-01  8.513  < 2e-16 ***
scale      -5.227e-01  5.929e-01  5.459e-02 -9.575  < 2e-16 ***
intensity  -3.664e+01  1.227e-16  9.400e+00 -3.897 9.72e-05 ***
domination -3.120e-01  7.320e-01  2.743e-01 -1.138   0.2553    
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

           exp(coef) exp(-coef) lower .95 upper .95
faim2      2.322e-01  4.306e+00 1.127e-01 4.783e-01
faim3      2.412e+00  4.145e-01 1.732e+00 3.360e+00
faim4      6.431e-01  1.555e+00 3.592e-01 1.151e+00
faim5      1.391e+00  7.188e-01 9.598e-01 2.016e+00
faim6      1.005e+00  9.948e-01 4.371e-01 2.312e+00
faim7      7.145e+00  1.400e-01 4.543e+00 1.124e+01
scale      5.929e-01  1.687e+00 5.328e-01 6.599e-01
intensity  1.227e-16  8.150e+15 1.223e-24 1.231e-08
domination 7.320e-01  1.366e+00 4.276e-01 1.253e+00

Concordance= 0.827  (se = 0.015 )
Likelihood ratio test= 261.3  on 9 df,   p=<2e-16
Wald test            = 218  on 9 df,   p=<2e-16
Score (logrank) test = 290.2  on 9 df,   p=<2e-16
