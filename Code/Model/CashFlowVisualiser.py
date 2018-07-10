from DataProcessing.American.DataParser import DataParser as DataParser


class CashFlowVisualiser:

    def __init__(self):
        print "CFV"

        df = self.Get_Sample_Data()
        print df


    def Get_Sample_Data(self):
        df = DataParser().AmericanCombo_i(-1)

        return df



if __name__ == '__main__':
    CashFlowVisualiser()
