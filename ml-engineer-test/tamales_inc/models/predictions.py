from metaflow import FlowSpec, step
import pandas as pd
import numpy as np
import pickle
import json 

class API_response():
    def __init__(self,X):
        self.X = X

class Pred_flow(FlowSpec): 

    @step
    def start(self):
        self.next(self.get_data)
    
    @step
    def get_data(self):
        X = res.X
        vals = np.asarray(X)
        vals = vals.reshape(1,2)
        self.vals = vals
        print('--->Reading_data<--')
        self.next(self.pred)

    @step
    def pred(self):
        predictions = self.vals[:, 0] * self.vals[:, 1] + np.log(self.vals[:, 0])
        print(predictions[0])
        data = {'PREDICTION':predictions[0]}
        with open('res.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print('DONE')
        self.next(self.end)
        

    @step
    def end(self):
        return 

if __name__ == '__main__':
    res = API_response([1000, 0.3])
    Pred_flow()
    
    
