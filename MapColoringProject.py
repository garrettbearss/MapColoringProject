# MapColoringProject.py
# Garrett Bearss, Srinivasa Sai Keerthan Challa, Leslie Nworie
# 12/8/24

import json
import matplotlib.pyplot as plt
import networkx as nx
import scipy as sp

#Note: Change file path to the location of the OhioCountyData.json file.
filePath = r"C:\Users\garre\Downloads\MapColoringProject\OhioCountyData.json"
colors = ['Red', 'Green', 'Yellow', 'Orange']
greatLakesAndOceans = ['Lake Erie', 'Lake Ontario', 'Lake Michigan', 'Lake Huron', 'Lake Superior', 'Atlantic Ocean', 'Pacific Ocean']

#Map Coloring Algorithm
class MapColoringAlgorithm:
    def __init__(self, counties, colorSet):
        #Initializes the counties, colors, and coloring array.
        self.counties = counties
        self.colors = colorSet
        self.coloring = {county: None for county in self.counties}

    def checkColor(self, county, color):
        #Checks if a color is valid for a given county.
        for neighbor in self.counties[county]:
            #If the neighbor is colored and the color is the same as the given color, return False.
            if neighbor in self.coloring and self.coloring[neighbor] == color:
                return False
        #If the color is valid, return True.
        return True
    
    def getMostConstrainedCounty(self, counties):
        #Gets the most constrained county.
        #Initializes the minimum number of colors and the most constrained county.
        minColors = float('inf')
        mostConstrained = []
        #Iterates through the counties.
        for county in counties:
            #If the county is not colored.
            if self.coloring[county] is None:
                #Gets the number of possible colors for the county.
                possibleColors = sum(1 for color in self.colors if self.checkColor(county, color))
                #If the number of possible colors is less than the minimum number of colors.
                if possibleColors < minColors:
                    #Sets the minimum number of colors to the number of possible colors.
                    minColors = possibleColors
                    #Sets the most constrained county to the county.
                    mostConstrained = [county]
                #If the number of possible colors is equal to the minimum number of colors.
                elif possibleColors == minColors:
                    #Appends the county to the most constrained county.
                    mostConstrained.append(county)
        #Returns the most constrained county.
        return mostConstrained

    def getMostConstrainingCounty(self, counties):
        #Gets the most constraining county.
        #Initializes the maximum number of constraints and the most constraining county.
        maxConstraints = -1
        mostConstraining = []
        #Iterates through the counties.
        for county in counties:
            #If the county is not colored.
            if self.coloring[county] is None:
                #Gets the number of constraints for the county.
                constraints = sum(1 for neighbor in self.counties[county] if self.coloring[neighbor] is None)
                #If the number of constraints is greater than the maximum number of constraints.
                if constraints > maxConstraints:
                    #Sets the maximum number of constraints to the number of constraints.
                    maxConstraints = constraints
                    #Sets the most constraining county to the county.
                    mostConstraining = [county]
                #If the number of constraints is equal to the maximum number of constraints.
                elif constraints == maxConstraints:
                    #Appends the county to the most constraining county.
                    mostConstraining.append(county)
        #Returns the most constraining county.
        return mostConstraining

    def getLeastConstrainedCounty(self, counties):
        #Gets the least constrained county.
        #Initializes the maximum number of colors and the least constrained county.
        maxColors = -1
        leastConstrained = []
        #Iterates through the counties.
        for county in counties:
            #If the county is not colored.
            if self.coloring[county] is None:
                #Gets the number of possible colors for the county.
                possibleColors = sum(1 for color in self.colors if self.checkColor(county, color))
                #If the number of possible colors is greater than the maximum number of colors.
                if possibleColors > maxColors:
                    #Sets the maximum number of colors to the number of possible colors.
                    maxColors = possibleColors
                    #Sets the least constrained county to the county.
                    leastConstrained = [county]
                #If the number of possible colors is equal to the maximum number of colors.
                elif possibleColors == maxColors:
                    #Appends the county to the least constrained county.
                    leastConstrained.append(county)
        #Returns the least constrained county.
        return leastConstrained

    def selectNextCounty(self, counties, initialCounty):
        #Selects the next county to color using heuristics.
        # Prioritize the initial county if it is uncolored.
        if self.coloring[initialCounty] is None:
            return initialCounty

        # Get the most constrained county
        mostConstrained = self.getMostConstrainedCounty(counties)
        # If there's only one most constrained county, return it.
        if len(mostConstrained) == 1:
            return mostConstrained[0]
        
        # Get the most constraining county among the most constrained counties.
        mostConstraining = self.getMostConstrainingCounty(mostConstrained)
        # If there's only one most constraining county, return it.
        if len(mostConstraining) == 1:
            return mostConstraining[0]
        
        # Get the least constrained county among the most constraining counties.
        leastConstrained = self.getLeastConstrainedCounty(mostConstraining)
        # If there's only one least constrained county, return it
        if len(leastConstrained) == 1:
            return leastConstrained[0]
        
        # If there are multiple least constrained counties, return the first one.
        return leastConstrained[0]
    
    def backtrack(self, counties, initialCounty):
        #Backtracks through the counties.
        #If there are no counties left to color, return True.
        if not counties:
            return True
        #Selects the next county to color using heuristics.
        nextCounty = self.selectNextCounty(counties, initialCounty)
        #If the next county is a Great Lake or one of the Oceans.
        if nextCounty in greatLakesAndOceans:
            #Colors the next county blue.
            self.coloring[nextCounty] = 'Blue'
            #Prints the look ahead table.
            self.printLookAheadTable()
            #Shows the graph.
            self.showGraph()
            #If the look ahead table doesn't result in a county having no remaining color.
            if self.checkLookAheadTable():
                #Recursively calls the backtrack function with the remaining counties.
                if self.backtrack([county for county in counties if county != nextCounty], initialCounty):
                    return True
            #Sets the color of the next county to None.
            self.coloring[nextCounty] = None
        else:
            #Iterates through the colors.
            for color in self.colors:
                #If the color is valid for the next county.
                if self.checkColor(nextCounty, color):
                    #Sets the color of the next county to the color.
                    self.coloring[nextCounty] = color
                    #Prints the look ahead table.
                    self.printLookAheadTable()
                    #Shows the graph.
                    self.showGraph()
                    #If the look ahead table doesn't result in a county having no remaining color.
                    if self.checkLookAheadTable():
                        #Recursively calls the backtrack function with the remaining counties.
                        if self.backtrack([county for county in counties if county != nextCounty], initialCounty):
                            return True
                    #Sets the color of the next county to None.
                    self.coloring[nextCounty] = None
        #Returns False if the color of the next county cannot be set.
        return False
    
    def colorMap(self, initialCounty):
        #Colors the map using backtracking.
        #Sets the initial county to the first county in the list of counties.
        counties = list(self.counties.keys())
        #Removes the initial county from the list of counties.
        counties.remove(initialCounty)
        #Inserts the initial county at the beginning of the list of counties.
        counties.insert(0, initialCounty)
        #Sets the color of the initial county to the first color in the list of colors.
        if self.backtrack(counties, initialCounty):
            return self.coloring
        #Returns None if the map cannot be colored.
        return None
    
    def checkLookAheadTable(self):
    #Checks if the look ahead table results in a county having no remaining color.
    #Iterates through the counties.
        for county in self.counties:
            #If the county is not colored.
            if self.coloring[county] is None:
                #Gets the possible colors for the county.
                possibleColors = {color for color in self.colors if self.checkColor(county, color)}
                #If the county is in the list of lakes and oceans, set possible colors to Blue.
                if county in greatLakesAndOceans:
                    possibleColors = {'Blue'}
                #If there are no possible colors for the county, return False.
                if not possibleColors:
                    return False
        #Returns True if all counties have possible colors.
        return True

    def printLookAheadTable(self):
        #Prints the look ahead table.
        for county in self.counties:
            #If the county is colored, print the county and the color.
            if self.coloring[county] is not None:
                #Prints the county and the color.
                print(f"{county}: {self.coloring[county]}")
            else:
                #Gets the possible colors for the county.
                possibleColors = {color for color in self.colors if self.checkColor(county, color)}
                #If the county is in the list of lakes and oceans, set possible colors to Blue.
                if county in greatLakesAndOceans:
                    possibleColors = {'Blue'}
                #Prints the county and the possible colors.
                print(f"{county}: {possibleColors}")
        print("\n")
    
    def showGraph(self):
        #Shows the graph of the map.
        G = nx.Graph()
        #Iterates through the counties and their neighbors.
        for county, neighbors in self.counties.items():
            #Adds the county to the graph.
            G.add_node(county)
            #Iterates through the neighbors.
            for neighbor in neighbors:
                #Adds the neighbor to the graph.
                G.add_edge(county, neighbor)
        
        #Sets the color map for the graph.
        colorMap = []
        #Iterates through the nodes in the graph.
        for node in G:
            #If the node is colored, appends the color to the color map.
            if node in self.coloring and self.coloring[node] is not None:
                #Appends the color to the color map.
                colorMap.append(self.coloring[node])
            #If the node is not colored, appends gray to the color map.
            else:
                #Appends gray to the color map.
                colorMap.append('gray')  # Default color for uncolored nodes

        #Sets the position of the nodes in the graph.
        pos = nx.kamada_kawai_layout(G)
        #If graph has two or more clusters
        #pos = nx.spring_layout(G)

        #Shows the graph.
        figManager = plt.get_current_fig_manager()
        #Zooms the graph to fit the screen.
        #For Windows
        figManager.window.state('zoomed')
        # For other operating systems
        #figManager.window.showMaximized

        #Draws the graph.
        nx.draw(G, pos, node_color=colorMap, with_labels=True, node_size=500, font_size=10, font_color='black')
        #Shows the graph.
        plt.show()

def getInfoFromFile(filePath):
    #Gets the information from the file.
    with open(filePath, 'r') as file:
        #Loads the data from the file.
        data = json.load(file)
    #Returns the map coloring algorithm data.
    return MapColoringAlgorithm(
        counties=data,
        colorSet=colors
    )


def main():
    #Main function to run the map coloring algorithm.
    run = True
    #Runs the map coloring algorithm.
    while(run):
        #Gets the user input for the start county.
        choice = input("\nEnter County as start point: ")
        #Gets the information from the file.
        map = getInfoFromFile(filePath)
        #If the choice is not in the counties, print invalid county and break out of run loop.
        if choice not in map.counties:
            print("\nInvalid County")
            break
        #Colors the map.
        result = map.colorMap(choice)
        #If the result is not None, print the result.
        if result:
            print("\nMap Coloring Successful")
            for county, color in result.items():
                print(f"{county}: {color}")
        #If the result is None, print map coloring failed.
        else:
            print("\nMap Coloring Failed")
        #Asks the user if they would like to run again.
        run = input("\nWould you like to run again? (y/n) ") == 'y'
        

if __name__ == "__main__":
    main()
