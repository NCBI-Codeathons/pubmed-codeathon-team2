import pandas as pd
import sklearn


def one_hot_a_column(df, column_name):
        '''
        One-hot encode the a column for feature creation.
        INPUT: df = a pandas dataframe that includes the column of 'column_name' in which each cell contains a list of pubtypes.
        OUTPUT: .data_one_hot = a dataframe with the additional columns that are one-hot encoded and begin with the prefix 'pubtype_'
        '''
        #change from column of lists to string
        df[column_name] = df[column_name].apply(', '.join).astype(str)
        # replace commas with a double underscore
        df[column_name] = df[column_name].apply(lambda x: x.replace(', ','__'))
        #replace spaces with single underscore
        df[column_name] = df[column_name].apply(lambda x: x.replace(' ','_'))
        #create dummies and join to the original data frame with new features prepended with 'pubtype'
        df = df.join(pd.get_dummies(df.pubtype, prefix=column_name))
        df.drop(columns=[column_name],inplace=True)

        return df

