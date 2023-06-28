import math
import matplotlib.pyplot as plt
import numpy as np
import pymc3 as pm
import theano.tensor as tt   

    
class formels:
    def __init__(self) -> None:
        pass

    # Define the utility function u
    def u(self,alpha, R):
        return R - alpha * ((10-R) - R)

    # Define the acceptance probability
    def propabelety(self,c, alpha,R):
        u=self.u(alpha,R)
        return np.exp(u * c) / (1 + np.exp(u * c))
        
    # Compute the acceptance probability for a given choice (d)
    def acceptance_prob(self,alpha,R ,c, Choice, a=None,propabelety_func="log"):
        
        if propabelety_func == "log":
            p_accept=self.propabelety(alpha,R,c)
            return (Choice * p_accept + (1 - Choice) * (1 - p_accept)).astype('float')
        elif propabelety_func == "g_log":
            p_accept = self.g_propabelety(a,c,alpha,R)
            return (Choice * p_accept + (1 - Choice) * (1 - p_accept)).astype('float')
        raise ValueError("Wrong model name")
    

    # Define the log-likelihood function for a set of decisions
    def log_likelihood(self,alpha,R,c, d):
        return np.sum(np.log(self.acceptance_prob(alpha,R ,c, d)))

    # Find the maximum log-likelihood for a set of log-likelihoods
    def max_log_likelihood(self,log_likelihoods):
        return max(log_likelihoods)

    # Define a generalized acceptance probability function using the logistic function and a parameter a
    def g_propabelety(self,a,c,alpha,R):
        k=1
        u=self.u(alpha,R)
        p_accept=a+((k-a)/(1+np.exp(-u*c)))
        return p_accept
    

class Log_Likelihood(formels): 
    def __init__(self, data, number_of_alphas = 100, min_alpha = 0, max_alpha = 3, min_c = 1 , max_c = 1 , number_of_c = 1):
        self.subject=data.head(1)["Subject"]
        print(self.subject)

        self.data = data

        self.number_of_alphas = number_of_alphas
        self.min_alpha = min_alpha
        self.max_alpha = max_alpha
        self.alpha_range = np.linspace(self.min_alpha,self.max_alpha,self.number_of_alphas)
        
        self.number_of_c=number_of_c
        self.min_c = min_c
        self.max_c = max_c
        self.c_range = np.linspace(self.min_c,self.max_c,self.number_of_c)

        self.probability_space = {}
        self.dict_probabilities()
        self.best_alpha,self.best_c = self.likelihood()
    
    
    def dict_probabilities(self):
        self.probability_space = {}
        for alpha in self.alpha_range:
            for c1 in self.c_range:
                probabilities = []
                for test in self.subject:
                    p_1 = self.acceptance_prob(alpha,test["resiver"],c1,test["choice"],)
                    probabilities.append(p_1)
                self.probability_space[(alpha,c1)] = probabilities

    def finde_fit(self):
        for alpha in self.alpha_range:
            for c1 in self.c_range:
                probabilities = np.zeros(len(self.subject))
                for i,test in enumerate(self.subject):
                    probabilities[i] = self.acceptance_prob(alpha,test["resiver"],c1,test["choice"])

    def plot(self):
        plt.title(f'Best alpha {self.best_alpha} Best c {self.best_c} subject {self.subject}')   
        #print(self.probability_space)
        plt.plot(self.probability_space[(self.best_alpha,self.best_c)])
        plt.show()

    def plot_x2(self):
        listt=[0]*5
        for i, test in self.data.iterrows(): 
            if test['choose'] == 1:
                Rece=test['receivor']
                listt[int(Rece)-1]+=1/8
        plt.plot(listt,'o')
        self.plot()
    
    def alpha_map(self):
        number_of_plots = 5
        for k in range(int(self.number_of_alphas/number_of_plots)):
            # Create figure and subplots
            fig, axs = plt.subplots(number_of_plots, number_of_plots, sharex=True, sharey=True, figsize = (20,20))

            # Loop over subplots and plot data
            for i in range(number_of_plots):
                for j in range(number_of_plots):
                    alpha = self.alpha_range[j+(k*number_of_plots)]
                    c1 = self.c_range[i]
                    axs[i,j].plot(self.probability_space[(alpha,c1)])
                    axs[i,j].set_title(f'a={round(alpha,2)}, c={round(c1,2)}')

            # Set common x and y labels
            fig.text(0.5, 0.04, 'x', ha='center')
            fig.text(0.04, 0.5, 'y', va='center', rotation='vertical')

            # Adjust layout
            fig.tight_layout()

            # Show plot
            plt.show()
    
    def alpha_map_joint(self):
        number_of_plots = 5
        for k in range(int(self.number_of_alphas/number_of_plots**2)):
            # Create figure and subplots
            fig, axs = plt.subplots(number_of_plots, number_of_plots, sharex=True, sharey=True, figsize = (20,20))

            # Loop over subplots and plot data
            for i in range(number_of_plots):
                for j in range(number_of_plots):
                    alpha = self.alpha_range[j+(i*number_of_plots)+(k*number_of_plots**2)]
                    c1 = self.c_range[int(len(self.c_range)/2)]
                    axs[i,j].plot(self.probability_space[(alpha,c1)])
                    axs[i,j].set_title(f'a={round(alpha,3)}, c={round(c1,3)}')

            # Set common x and y labels
            fig.text(0.5, 0.04, 'x', ha='center')
            fig.text(0.04, 0.5, 'y', va='center', rotation='vertical')

            # Adjust layout
            fig.tight_layout()

            # Show plot
            plt.show()





'''
class formels:
    def __init__(self) -> None:
        pass

    # Define the utility function u
    def u(self,alpha, R):
        return R - alpha * ((10-R) - R)

    # Define the acceptance probability
    def propabelety(self,c, u):
        if isinstance(c, np.ndarray) and isinstance(u, np.ndarray):
            print(type(c))
            l=[None]* len(c)
            for i,cc in enumerate(c):
                l[i]= np.exp(u * cc) / (1 + np.exp(u * cc))
            p_accept=np.array(l).reshape(len(c), len(u))
            #p_accept shape (c,alfa)
            return p_accept
        else:
            p_accept = np.exp(u * c) / (1 + np.exp(u * c))
            #p_accept shape (alfa)
            return p_accept
        

    # Compute the acceptance probability for a given choice (d)
    def acceptance_prob(self,u ,c, Choice, a=None,propabelety_func="log"):
        if propabelety_func == "log":
            p_accept=self.propabelety(u,c)

            if isinstance(u, np.ndarray) or isinstance(c, np.ndarray):

                if len(p_accept.shape)==2:
                    #return shape (alfa,c,choise)
                    return p_accept[..., np.newaxis] * Choice + (np.ones(len(Choice))-Choice)*p_accept[..., np.newaxis]
                
                else:
                    if isinstance(Choice, np.ndarray):
                        acceptance=[None]*len(Choice)
                        for i,choicee in enumerate(Choice):
                            acceptance[i]=(choicee * p_accept + (1 - choicee) * (1 - p_accept)).astype('float')
                        return np.array(acceptance).reshape(len(Choice), len(p_accept))
                    else:
                        return (Choice * p_accept + (1 - Choice) * (1 - p_accept)).astype('float')

                
            else:
                print(p_accept)
                if isinstance(Choice, np.ndarray):
                    acceptance=[None]*len(Choice)
                    for i,choicee in enumerate(Choice):
                        acceptance[i]=(choicee * p_accept + (1 - choicee) * (1 - p_accept)).astype('float')
                    return acceptance
                else:
                    return (Choice * p_accept + (1 - Choice) * (1 - p_accept)).astype('float')
            

        elif propabelety_func == "g_log":
            p_accept = self.g_propabelety(a,c,u)
            return (Choice * p_accept + (1 - Choice) * (1 - p_accept)).astype('float')
        raise ValueError("Wrong model name")
    

    # Define the log-likelihood function for a set of decisions
    def log_likelihood(self,u,c, d):
        return np.sum(np.log(self.acceptance_prob(u ,c, d)))

    # Find the maximum log-likelihood for a set of log-likelihoods
    def max_log_likelihood(self,log_likelihoods):
        return max(log_likelihoods)

    # Define a generalized acceptance probability function using the logistic function and a parameter a
    def g_propabelety(self,a,c,u):
        k=1
        p_accept=a+((k-a)/(1+np.exp(-u*c)))
        return p_accept
''' 


class Log_Likelihood2: 
    def __init__(self, data, number_of_alphas = 100, min_alpha = 0, max_alpha = 3, min_c = 1 , max_c = 1 , number_of_c = 1):
        self.subject=data.head(1)["Subject"]
        print(self.subject)
        self.data = data

        self.number_of_alphas = number_of_alphas
        self.min_alpha = min_alpha
        self.max_alpha = max_alpha
        self.alpha_range = [min_alpha+ (x / number_of_alphas)*(max_alpha-min_alpha) for x in range(number_of_alphas)]

        self.min_c = min_c
        self.max_c = max_c
        self.c_range = [min_c+ (x / number_of_c)*(max_c-min_c) for x in range(number_of_c)]

        self.probability_space = {}
        self.dict_probabilities()
        self.best_alpha,self.best_c = self.likelihood()
    
    def Fehr_Schmidt(self, receivor, alpha):
        u = receivor - alpha * ((10 - receivor) - receivor)
        
        return u
    
    def probability(self, receivor, alpha, c=1):
        u = self.Fehr_Schmidt(receivor, alpha)
        p_1 = math.exp(u * c) / (1 + math.exp(u * c))

        return p_1
    

    def dict_probabilities(self):
        self.probability_space = {}
        for alpha in self.alpha_range:
            for c1 in self.c_range:
                probabilities = []
                for receivor in range(1,6):
                    p_1 = self.probability(receivor, alpha,c=c1)
                    probabilities.append(p_1)
                self.probability_space[(alpha,c1)] = probabilities



    def likelihood(self):
        likelihoods = []
        alpha_dict = {}
        c_dict={}
        for alpha,c in self.probability_space:
            prob_all_states = self.probability_space[alpha,c]
            
            Log_L = 0
            for _, test in self.data.iterrows():
                receivor = test['receivor'] 
                prob_state = prob_all_states[int(receivor-1)]    
                if prob_state * test['choose'] + (1 - prob_state) * (1 - test['choose'])==0:
                    log_prob_state=0
                else:
                    log_prob_state = math.log(prob_state * test['choose'] + (1 - prob_state) * (1 - test['choose']))
                Log_L += log_prob_state

            likelihoods.append(Log_L)
            c_dict[Log_L]=c
            alpha_dict[Log_L] = alpha
    
        return alpha_dict[max(likelihoods)],c_dict[max(likelihoods)]
            

    def plot(self):
        plt.title(f'Best alpha {self.best_alpha} Best c {self.best_c} subject {self.subject}')
        #print(self.probability_space)
        plt.plot(self.probability_space[(self.best_alpha,self.best_c)])
        plt.show()

    def plot_x2(self):
        listt=[0]*5
        for i, test in self.data.iterrows(): 
            if test['choose'] == 1:
                Rece=test['receivor']
                listt[int(Rece)-1]+=1/8
        plt.plot(listt,'o')
        self.plot()
    
    def alpha_map(self):
        number_of_plots = 5
        for k in range(int(self.number_of_alphas/number_of_plots)):
            # Create figure and subplots
            fig, axs = plt.subplots(number_of_plots, number_of_plots, sharex=True, sharey=True, figsize = (20,20))

            # Loop over subplots and plot data
            for i in range(number_of_plots):
                for j in range(number_of_plots):
                    alpha = self.alpha_range[j+(k*number_of_plots)]
                    c1 = self.c_range[i]
                    axs[i,j].plot(self.probability_space[(alpha,c1)])
                    axs[i,j].set_title(f'a={round(alpha,2)}, c={round(c1,2)}')

            # Set common x and y labels
            fig.text(0.5, 0.04, 'x', ha='center')
            fig.text(0.04, 0.5, 'y', va='center', rotation='vertical')

            # Adjust layout
            fig.tight_layout()

            # Show plot
            plt.show()
    
    def alpha_map_joint(self):
        number_of_plots = 5
        for k in range(int(self.number_of_alphas/number_of_plots**2)):
            # Create figure and subplots
            fig, axs = plt.subplots(number_of_plots, number_of_plots, sharex=True, sharey=True, figsize = (20,20))

            # Loop over subplots and plot data
            for i in range(number_of_plots):
                for j in range(number_of_plots):
                    alpha = self.alpha_range[j+(i*number_of_plots)+(k*number_of_plots**2)]
                    c1 = self.c_range[int(len(self.c_range)/2)]
                    axs[i,j].plot(self.probability_space[(alpha,c1)])
                    axs[i,j].set_title(f'a={round(alpha,3)}, c={round(c1,3)}')

            # Set common x and y labels
            fig.text(0.5, 0.04, 'x', ha='center')
            fig.text(0.04, 0.5, 'y', va='center', rotation='vertical')

            # Adjust layout
            fig.tight_layout()

            # Show plot
            plt.show()