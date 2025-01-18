from datahandler import DatasetHandlerIF

class TrainingDataSetHandler :
    @DatasetHandlerIF
    def LoadData(self, filePath: str) -> None:
        pass

    @DatasetHandlerIF
    def ValidateData(self) -> None:
        pass

    @DatasetHandlerIF
    def SumOfDeviation(self, referenceData: pd.DataFrame) -> Union[float, pd.DataFrame]:
        pass

    @DatasetHandlerIF
    def PlotDataset(self, title: str, xLabel: str, yLabel: str) -> Figure:
        pass

    @DatasetHandlerIF
    def SaveToDatabase(self, dbConnection, tableName: str) -> None:

        pass
