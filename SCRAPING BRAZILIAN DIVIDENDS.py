#!/usr/bin/env python
# coding: utf-8

# In[ ]:


### SCRAPING BRAZILIAN DIVIDENDS         ## FUNDS 


# In[1]:


# LIBRARIES
import tabula
import PyPDF2
import csv
import os
import pandas as ps
import numpy as np


# In[2]:


# Acessing directory
os.chdir("C:\\Users\\aline\\OneDrive\\Área de Trabalho\\Code")
#os.listdir()


# In[3]:


# Accessing Link list 

csv_data = ps.read_csv('SAMPLE_COTISTAS.csv')

links = ps.DataFrame(csv_data, columns=['LINK'])
 


# In[4]:


import os
os.environ['R_HOME'] = 'C:\\Users\\aline\\anaconda3\\envs\\r-tutorial\\Lib\\R'


# In[5]:


get_ipython().run_line_magic('load_ext', 'rpy2.ipython')
# Source : https://www.askpython.com/python/examples/use-r-and-python-in-the-same-notebook#:~:text=To%20use%20R%20and%20python%20simultaneously%20in%20the%20same%20notebook,activate%20the%20rpy2%20package%20first.&text=rpy2%20is%20a%20high%2Dlevel,NumPy%20and%20pandas%20data%20structures.
#https://stackoverflow.com/questions/68031659/using-rpy2-in-jupyter-notebook-but-there-is-no-output-error-in-withvisible


# In[6]:


get_ipython().run_cell_magic('R', '-i links', '# open links, screenshot, save  as pdf on your local directory\n#install.packages("webshot")\n\nlibrary(webshot)\n\n\nfor (url in links) {\n  webshot(url, file = paste(as.character(seq_len(length(url))),".pdf",sep=""),vwidth = 500,vheight = 500)\n    }')


# In[6]:


#Import pdfs as tables

dividends = ps.DataFrame()
div = ps.DataFrame()

pdf_folder = "C:\\Users\\aline\\OneDrive\\Área de Trabalho\\Code"  
paths = [fn for fn in os.listdir(pdf_folder) if fn.endswith('.pdf')]
    
for path in paths:
    dividends = dividends.append(tabula.read_pdf(path, pages = 'all', pandas_options={'header': None}, multiple_tables=True)[1:])


# In[47]:


# DATA CLEANING
ps.set_option('display.max_rows', None) #see all rows

div1 = dividends.drop(dividends.columns[[1, 2, 3]], axis=1)  # DROP COLUMNS 1,2,3


div1.columns = ["Data", "Rendimento", "Amortizacao"] # rename columns

div2 = div1.replace("Rendimento",np.nan)  # DELETING "RENDIMENTO"
div3 = div2.replace("Amortização",np.nan) # DELETING "AMORTIZACAO"

div4 = div3.dropna(how='all') #drop rolls with all NAN

div5= div4.drop(4, axis=0) # droping row 4 "ATO SOCIETARIO"

div5['Data'] = div5['Data'].replace(np.nan, "Tipo de Amortizacao")


# In[48]:


#RENAMING COLUMNS
div6 =div5.transpose()

div7 = div6.rename(columns={div6.columns[0]: 'ISIN',
                            div6.columns[1]: 'Data Base',
                            div6.columns[2]: 'Valor',
                            div6.columns[3]: 'Data de Pagamento',
                            div6.columns[4]: 'Periodo de Referencia',
                            div6.columns[5]: 'Isento IR',
                            div6.columns[7]: 'Tipo Amortizacao'})

#COPY ISIN TO EMPTY CELLS BELOW
div8 = div7['ISIN'].fillna(method='ffill')
div7['ISIN']=div8    

#REMOVING FIRST ROW
div9 = div7.tail(-1)
div9["Tipo Amortizacao"]


# In[44]:


ISIN = div9['ISIN'].stack(dropna=False).reset_index()
Tipo_Amortizacao = div9['Tipo Amortizacao'].stack(dropna=False).reset_index(drop=True)
Isento_IR = div9['Isento IR'].stack(dropna=False).reset_index(drop=True)
Valor = div9['Valor'].stack(dropna=False).reset_index(drop=True)
Data_Pagamento = div9['Data de Pagamento'].stack(dropna=False).reset_index(drop=True)
Data_Base = div9['Data Base'].stack(dropna=False).reset_index(drop=True)
Periodo_Referencia = div9['Periodo de Referencia'].stack(dropna=False).reset_index(drop=True)


combined = ps.concat([ISIN,Tipo_Amortizacao,Isento_IR,Valor,Data_Pagamento,Data_Base,Periodo_Referencia],axis=1)
combined.reset_index(drop=True)


# In[45]:


# CLEANING
combined = combined.drop('level_1', axis=1) #drop level_1

# RENAMING COLUMNS
combined.columns.values[0] = "Type"
combined.columns.values[1] = "ISIN"
combined.columns.values[2] = "Tipo de Amortizacao"
combined.columns.values[3] = "Isento IR"
combined.columns.values[4] = "Valor"
combined.columns.values[5] = "Data de Pagamento"
combined.columns.values[6] = "Data Base"
combined.columns.values[7] = "Periodo de Referencia"

#DELETE Código ISIN:
combined['ISIN'] = combined['ISIN'].str.replace('Código ISIN:','')

#DELETE ALL ROWS WHERE VALOR, PAGAMENTO, DATA BASE ARE NAN 
combined1 = combined.dropna(subset=['Valor', 'Data de Pagamento', 'Data Base'],how='all')
combined1.reset_index(drop=True)


# In[46]:


# INSERTING NEW COLUMNS 

# VALUE MARKER 
combined1.insert(loc=3, column='Value Marker', value=['' for i in range(combined1.shape[0])])
combined1

#TAX MARKER
combined1.insert(loc=5, column='Tax Marker', value=['' for i in range(combined1.shape[0])])
combined1['Tax Marker'] = np.where(combined1['Isento IR']=='Sim', 'SF', '')

#TAX VALUE
combined1.insert(loc=6, column='Tax Value', value=['' for i in range(combined1.shape[0])])
combined1['Tax Value'] = np.where(combined1['Isento IR']=='Sim', '0%', '')


# EX DATE 
combined1.insert(loc=9, column='Ex Date', value=['' for i in range(combined1.shape[0])])

#SOURCE CODE
combined1.insert(loc=12, column='Source Code', value=['SE29' for i in range(combined1.shape[0])])
combined1

#SOURCE DATE
combined1.insert(loc=13, column='Source Date', value=['' for i in range(combined1.shape[0])])


#SOURCE TIME
combined1.insert(loc=14, column='Source Time', value=['' for i in range(combined1.shape[0])])
combined1


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




