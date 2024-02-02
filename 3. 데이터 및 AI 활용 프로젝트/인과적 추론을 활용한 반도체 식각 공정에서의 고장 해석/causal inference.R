library(dplyr)
library(ggplot2)
library(mediation)
library(lavaan)
# 실험 1
milling = read.csv("C:/Users/sjkan/Desktop/연세/23-1/인과적추론/프로젝트/data.csv")
milling = na.omit(milling)
milling
A = milling$ETCHBEAMVOLTAGE #IONGAUGEPRESSURE # exposure
M = milling$ETCHSUPPRESSORVOLTAGE #ETCHBEAMVOLTAGE    # mediator
Y = milling$FLOWCOOLPRESSURE #fault_name   # outcome FLOWCOOLPRESSURE

# Set up the model (no interaction between exposure and mediator)
med.fit = lm(M ~ A, data=milling)
out.fit = lm(Y ~ A + M, data=milling)
med.out = mediate(med.fit, out.fit, treat="A", mediator='M', sims=100)
summary(med.out)
plot(med.out)

#implement of sensitivity analysis.
sens.out = medsens(med.out, rho.by=0.1, effect.type = 'both', sims=100)
summary(sens.out)
plot(sens.out) 

###

# Set up the model (interaction between exposure and mediator)
med2.fit = lm(M ~ A, data=milling)
out2.fit = lm(Y ~ A + M + A*M, data=milling)
med2.out = mediate(med2.fit, out2.fit, treat="A", mediator='M', sims=100)
summary(med2.out)
plot(med2.out)

#implement of sensitivity analysis.
sens2.out = medsens(med2.out, rho.by=0.1, effect.type = 'both', sims=100)
summary(sens2.out)
plot(sens2.out)

# 실험 2
milling = read.csv("C:/Users/sjkan/Desktop/연세/23-1/인과적추론/프로젝트/data.csv")
milling = na.omit(milling)
milling
A = milling$ETCHBEAMVOLTAGE #IONGAUGEPRESSURE # exposure
M = milling$ETCHSUPPRESSORCURRENT #ETCHBEAMVOLTAGE    # mediator
Y = milling$FLOWCOOLPRESSURE #fault_name   # outcome FLOWCOOLPRESSURE

# Set up the model (no interaction between exposure and mediator)
med.fit = lm(M ~ A, data=milling)
out.fit = lm(Y ~ A + M, data=milling)
med.out = mediate(med.fit, out.fit, treat="A", mediator='M', sims=100)
summary(med.out)
plot(med.out)

#implement of sensitivity analysis.
sens.out = medsens(med.out, rho.by=0.1, effect.type = 'both', sims=100)
summary(sens.out)
plot(sens.out) 

###

# Set up the model (interaction between exposure and mediator)
med2.fit = lm(M ~ A, data=milling)
out2.fit = lm(Y ~ A + M + A*M, data=milling)
med2.out = mediate(med2.fit, out2.fit, treat="A", mediator='M', sims=100)
summary(med2.out)
plot(med2.out)

#implement of sensitivity analysis.
sens2.out = medsens(med2.out, rho.by=0.1, effect.type = 'both', sims=100)
summary(sens2.out)
plot(sens2.out)

# 실험 3
milling = read.csv("C:/Users/sjkan/Desktop/연세/23-1/인과적추론/프로젝트/data.csv")
milling = na.omit(milling)
milling
A = milling$ETCHBEAMVOLTAGE #IONGAUGEPRESSURE # exposure
M = milling$ETCHPBNGASREADBACK #ETCHBEAMVOLTAGE    # mediator
Y = milling$FLOWCOOLPRESSURE #fault_name   # outcome FLOWCOOLPRESSURE

# Set up the model (no interaction between exposure and mediator)
med.fit = lm(M ~ A, data=milling)
out.fit = lm(Y ~ A + M, data=milling)
med.out = mediate(med.fit, out.fit, treat="A", mediator='M', sims=100)
summary(med.out)
plot(med.out)

#implement of sensitivity analysis.
sens.out = medsens(med.out, rho.by=0.1, effect.type = 'both', sims=100)
summary(sens.out)
plot(sens.out) 

###

# Set up the model (interaction between exposure and mediator)
med2.fit = lm(M ~ A, data=milling)
out2.fit = lm(Y ~ A + M + A*M, data=milling)
med2.out = mediate(med2.fit, out2.fit, treat="A", mediator='M', sims=100)
summary(med2.out)
plot(med2.out)

#implement of sensitivity analysis.
sens2.out = medsens(med2.out, rho.by=0.1, effect.type = 'both', sims=100)
summary(sens2.out)
plot(sens2.out)

# 실험 4
milling = read.csv("C:/Users/sjkan/Desktop/연세/23-1/인과적추론/프로젝트/data.csv")
milling = na.omit(milling)
milling
A = milling$ETCHSUPPRESSORVOLTAGE #IONGAUGEPRESSURE # exposure
M = milling$ETCHPBNGASREADBACK #ETCHBEAMVOLTAGE    # mediator
Y = milling$FLOWCOOLPRESSURE #fault_name   # outcome FLOWCOOLPRESSURE

# Set up the model (no interaction between exposure and mediator)
med.fit = lm(M ~ A, data=milling)
out.fit = lm(Y ~ A + M, data=milling)
med.out = mediate(med.fit, out.fit, treat="A", mediator='M', sims=100)
summary(med.out)
plot(med.out)

#implement of sensitivity analysis.
sens.out = medsens(med.out, rho.by=0.1, effect.type = 'both', sims=100)
summary(sens.out)
plot(sens.out) 

###

# Set up the model (interaction between exposure and mediator)
med2.fit = lm(M ~ A, data=milling)
out2.fit = lm(Y ~ A + M + A*M, data=milling)
med2.out = mediate(med2.fit, out2.fit, treat="A", mediator='M', sims=100)
summary(med2.out)
plot(med2.out)

#implement of sensitivity analysis.
sens2.out = medsens(med2.out, rho.by=0.1, effect.type = 'both', sims=100)
summary(sens2.out)
plot(sens2.out)

# 실험 5
milling = read.csv("C:/Users/sjkan/Desktop/연세/23-1/인과적추론/프로젝트/data.csv")
milling = na.omit(milling)
milling
A = milling$ETCHSUPPRESSORCURRENT #IONGAUGEPRESSURE # exposure
M = milling$ETCHPBNGASREADBACK #ETCHBEAMVOLTAGE    # mediator
Y = milling$FLOWCOOLPRESSURE #fault_name   # outcome FLOWCOOLPRESSURE

# Set up the model (no interaction between exposure and mediator)
med.fit = lm(M ~ A, data=milling)
out.fit = lm(Y ~ A + M, data=milling)
med.out = mediate(med.fit, out.fit, treat="A", mediator='M', sims=100)
summary(med.out)
plot(med.out)

#implement of sensitivity analysis.
sens.out = medsens(med.out, rho.by=0.1, effect.type = 'both', sims=100)
summary(sens.out)
plot(sens.out) 

###

# Set up the model (interaction between exposure and mediator)
med2.fit = lm(M ~ A, data=milling)
out2.fit = lm(Y ~ A + M + A*M, data=milling)
med2.out = mediate(med2.fit, out2.fit, treat="A", mediator='M', sims=100)
summary(med2.out)
plot(med2.out)

#implement of sensitivity analysis.
sens2.out = medsens(med2.out, rho.by=0.1, effect.type = 'both', sims=100)
summary(sens2.out)
plot(sens2.out)