from metaflow import FlowSpec, step
import pandas as pd
import numpy as np
import pickle

def modelo_base(X):
  pred = X[:, 0] * X[:, 1] + np.log(X[:, 0])
  return pred

def custom_model(X):
    pass
    return 0

class ML_flow(FlowSpec):

    @step
    def start(self):
        self.next(self.get_data)
    
    @step
    def get_data(self):
        print('--->Reading_data<--')
        self.data = pd.read_csv('sales_tamales_inc.csv')
        model_data_2 =  self.data[['month', 'sales', 'cal_category']].copy()
        model_data_2['Wmonth'] = [0.75 if x == 1 or x ==12 else 0.5 for x in model_data_2['month']]
        model_data_2['Wcal'] = [0.3 if x == 'Light' or x == 'Zero' else 0.5 for x in model_data_2['cal_category']]  
        model_data_2['Wcomp'] = model_data_2['Wcal']/(model_data_2['Wmonth']+model_data_2['Wcal'])
        del model_data_2['month']
        del model_data_2['cal_category']
        del model_data_2['Wmonth']
        del model_data_2['Wcal']
        Y = model_data_2.to_numpy()
        self.data = Y
        
        self.next(self.fit_base, self.fit_custom)

    @step
    def fit_base(self):
        print('--->Training Base model<--')
        self.preds = modelo_base(self.data)
        print(self.preds)
        self.next(self.validating_base)
        
    @step
    def validating_base(self):
        print('---->validating Base<---')
        #AQUI VA LA VALIDACION DEL MODLEO BASE
        self.perf = 0.3
        self.next(self.join)

    @step
    def fit_custom(self):
        #AQUI VA EL TRAINING DEL MODELO CUSTOM
        print('--->Training Custom<---')
        self.preds = custom_model(self.data)
        print(self.preds)
        self.next(self.validating_custom)

    @step
    def validating_custom(self):
        print('--->Validating Custom<----')
        self.perf = 0
        self.next(self.join)


    @step
    #SE UNEN LAS DOS RAMAS DE LOS MODELOS Y SE IMPRIMEN LAS METRICAS 
    #CON BASE EN EL MEJOR DESEMEPEÑO SE CREA LA VERSION DEL MODELO
    def join(self, inputs):
        print('Branch base  is %s' % inputs.validating_base.perf)
        print('Branch custom %s' % inputs.validating_custom.perf)
        if inputs.validating_base.perf > inputs.validating_custom.perf:
            print('-->exporting model (base)<---')
            pkl_filename = "pickle_model.pkl"
            with open(pkl_filename, 'wb') as file:
                pickle.dump(modelo_base, file)
        else:
            print('-->exporting model (custom)<---')
            pkl_filename = "pickle_model.pkl"
            with open(pkl_filename, 'wb') as file:
                pickle.dump(custom_model, file)
        
        self.next(self.end)

    @step
    def end(self):
        pass

if __name__ == '__main__':
    ML_flow()
