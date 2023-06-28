import numpy as np
import matplotlib.pyplot as plt
import theano.tensor as tt  

class utility_functions():
    def __init__(self, responder=1):
        self.responder = responder
        self.overall_payoff = 10
        self.proposer = self.overall_payoff - responder
    
    #Calculat the probabilety given utility
    def P(self,u):
        return 1/(1+np.exp(-u))
    

    #utility function
    def Fehr_Schmidt(self, alpha):
        u = self.responder - alpha * (self.proposer - self.responder)
        return u
    
    #utility function    
    def U1(self, lambda_1):
        return lambda_1 * self.proposer
    
    #utility function
    def U2(self, lambda_2):
        return lambda_2 * self.overall_payoff
    
    #utility function
    def U3(self, lambda_3):
        return lambda_3 * self.responder
    
    #utility function
    def U4(self, lambda_4):
        return lambda_4 * (self.responder-self.proposer)


    #utility function
    def U5(self, lambdas):
        lambda_1=lambdas[0]
        lambda_3=lambdas[1]
        return self.U1(lambda_1) + self.U3(lambda_3)

    def set_responder(self,responder):
        self.responder = responder
        self.overall_payoff
        self.proposer = self.overall_payoff - responder

        #adds utility function
    def add_us(self,u1,u2):
        lam=lambda input :u1(input[0])+u2(input[1])
        lam.__name__=f'[{u1.__name__} + {u2.__name__}]'
        return lam
    
    def substraction_us(self,u1,u2):
        lam=lambda input :u1(input[0])-u2(input[1])
        lam.__name__=f'[{u1.__name__} - {u2.__name__}]'
        return lam

    def multiplication_us(self,u1,u2):
        lam=lambda input :u1(input[0])*u2(input[1])
        lam.__name__=f'[{u1.__name__} * {u2.__name__}]'
        return lam

    #input list[element]
    #element is all the paremeters for the U funktions 
    #eks U5 elmment = lambdas = tubel(lambda_1,lambda_3)
    #eks U1 elmment = lambda_1
    def map_u(self,u , inputs):
    #map[u,list1[p1],list2[p2],....,listn[pn]]  
    #list n have len 6 that contains the p for the difrent r's [1,2,3,4,5,lamda]
    #p have len difrent lamdas tested and contans list 
        map=[None]*(len(inputs)+1)
        map[0]=u.__name__
        for i,input in enumerate(inputs):
            five_p_list=[None]*6
            for r in range(1,6):
                self.responder = r
                self.proposer = self.overall_payoff - r
                five_p_list[r-1] = self.P( u(input) ) 
            five_p_list[5]=input
            map[i+1]=five_p_list
        return map
    

    #map = list2[list1[p]]  
    #list 1 len 5 that contains the p for the difrent r's
    #list 2 have len difrent lamdas tested and contans list 
    def plot(self,map,Titel=None):
        for five_p_list in map[1:]:
            try:
                plt.plot([1,2,3,4,5],five_p_list[:-1], label=f'{round(five_p_list[-1],2)}')
            except:
                plt.plot([1,2,3,4,5],five_p_list[:-1], label=f'{five_p_list[-1]}')
        if Titel:
            plt.title(f'{Titel} = {map[0]}')
        else:
            plt.title(f'{map[0]}')
        plt.xlabel('Responder')
        plt.ylabel('Probability for acceptance')
        plt.legend()
        plt.show()

    


