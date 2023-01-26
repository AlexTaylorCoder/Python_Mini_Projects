import pandas

#READ
data = pandas.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")

#CHECK LENGTH FOR EACH COL
gray = len(data[data["Primary Fur Color"] == "Gray"])
black = len(data[data["Primary Fur Color"] == "Black"])
red = len(data[data["Primary Fur Color"] == "Cinnamon"])


#SAVE TO DICT
data_dict = {
    "Fur Color": ["Gray","Black","Cinnamon"],
    "Count": [gray,black,red]
}

count_data = pandas.DataFrame(data_dict)
count_data.to_csv("count_data.csv")
