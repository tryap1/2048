import tkinter as tk
import colors
import random


#create game class that will  inherit from the Tkinter Frame widget
#this is where the game is run and where the GUI is constructed
class Game(tk.Frame):
    
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048")
        
    #create GUI outline which is a 4 by 4 grid
        self.maingrid = tk.Frame(self, bg = colors.GRID_COLOR, bd = 3, 
                                 width = 600, height = 600)
        
        self.maingrid.grid(pady= (100,0))
        
        self.makeGUI()
        self.start_2048()
        
        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)
        
        self.mainloop()
        
    def makeGUI(self):
        self.cells = []
        
        for i in range(4):
            row = []
            
            for j in range(4):
                cell_frame = tk.Frame(self.maingrid, 
                                      bg = colors.EMPTY_CELL_COLOR,
                                      width = 150,
                                      height = 150)
                cell_frame.grid(row = i, column = j, padx = 5, pady = 5)
                
                cell_number = tk.Label(self.maingrid, 
                                       bg =colors.EMPTY_CELL_COLOR)
                cell_number.grid(row = i, column = j)
                
                cell_data = {'frame': cell_frame, 'number': cell_number}
                row.append(cell_data)
            
            self.cells.append(row)   
           
        score_frame = tk.Frame(self)
        score_frame.place(relx = 0.5, y = 45, anchor = 'center')
        tk.Label(score_frame, 
                 text = 'Score',
                 font = colors.SCORE_LABEL_FONT).grid(row = 0)
        
        self.score_label = tk.Label(score_frame, text ='0', 
                                    font = colors.SCORE_FONT
                                    )
        self.score_label.grid(row = 1)         
        
    #Fills an empty board with 2 randomly placed 2s to start the game    
    def start_2048(self):
        #Create a matrix of zeroes; ie a list of lists containing zeros
        self.matrix = [[0]*4 for _ in range(4)]
        
        #fill 2 random cells with 2s
        row =  random.randint(0,3)
        col = random.randint(0,3)
        
        self.matrix[row][col] = 2
        #Place 2 into radomly assigned cell
        #Alter GUI to reflect placement of 2
        self.cells[row][col]['frame'].configure(bg = colors.CELL_COLORS[2])
        self.cells[row][col]['number'].configure(bg = colors.CELL_COLORS[2],
                                        fg = colors.CELL_NUMBER_COLORS[2],
                                        font = colors.CELL_NUMBER_FONTS[2],
                                        text = '2')
        
        #To fill the 2nd random 2, lets choose a random unfilled cell:
        while(self.matrix[row][col] != 0):
            row =  random.randint(0,3)
            col = random.randint(0,3)
            
        self.matrix[row][col] = 2 
        self.cells[row][col]['frame'].configure(bg = colors.CELL_COLORS[2])
        self.cells[row][col]['number'].configure(bg = colors.CELL_COLORS[2],
                                        fg = colors.CELL_NUMBER_COLORS[2],
                                        font = colors.CELL_NUMBER_FONTS[2],
                                        text = '2')

        #initial score of the game
        self.score = 0

    def stack(self):
        #Compresses all NON ZERO numbers to one side of the board
        #initialised compressed matrix
        new_matrix = [[0]*4 for _ in range(4)]
        #use a nested for loop to check for non zeros
        
        for i in range(4):
            fill_position = 0
            
            for j in range(4):
                if self.matrix[i][j] !=0 :
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position +=1
        
        self.matrix = new_matrix            
                
                
    def combine(self):
        #Merges 2 tiles of the same value to their sum
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] !=0 and self.matrix[i][j] == self.matrix[i][j+1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j+1] = 0
                    self.score += self.matrix[i][j]

    #The above 2 functions only cater to a left-referenced action,
    #To allow for other directions, we need a inverse and transpose function
                    
    def inverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3-j])
                
        self.matrix = new_matrix
        
    def transpose(self):
        new_matrix = [[0]*4 for _ in range (4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
                
        self.matrix = new_matrix

    #After the player has made a move, we need a function to add a new tile
    #Randomly assign a 2 or a 4, to 2 random zero cells

    def add_tile(self):
        row =  random.randint(0,3)
        col = random.randint(0,3)
        while(self.matrix[row][col] != 0):
            row =  random.randint(0,3)
            col = random.randint(0,3)
        
        self.matrix[row][col]= random.choice([2,4])
        
    #Update the GUI after each turn
        
    def updateGUI(self):
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == 0:
                    self.cells[i][j]['frame'].configure(
                        bg = colors.EMPTY_CELL_COLOR)
                    self.cells[i][j]['number'].configure(
                        bg = colors.EMPTY_CELL_COLOR,
                        text = '')
                    
                else:
                    self.cells[i][j]['frame'].configure(
                        bg = colors.CELL_COLORS[self.matrix[i][j]])
                    self.cells[i][j]['number'].configure(
                        bg = colors.CELL_COLORS[self.matrix[i][j]],
                        fg = colors.CELL_NUMBER_COLORS[self.matrix[i][j]],
                        font = colors.CELL_NUMBER_FONTS[self.matrix[i][j]],
                        text = str(self.matrix[i][j]))
                    
                    self.score_label.configure(text = self.score)
                    self.update_idletasks()
                    
    #Arrow Key Functions, 
    #Noting that the above functions were written left-referenced
    def left(self, event):
        self.stack()
        self.combine()
        self.stack()
        self.add_tile()
        self.updateGUI()
        self.game_over()
    
    #To compress to the right, inverse the matrix, stack, reinverse and update    
    def right(self, event):
        self.inverse()
        self.stack()
        self.combine()
        self.stack()
        self.inverse()
        self.add_tile()
        self.updateGUI()
        self.game_over()
        
    #To compress to the top, transpose the matrix so that it is left aligned    
    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_tile()
        self.updateGUI()
        self.game_over()
        
    #To compress to the bottom, transpose and inverse so it is left aligned    
    def down(self, event):
        self.transpose()
        self.inverse()
        self.stack()
        self.combine()
        self.stack()
        self.inverse()
        self.transpose()
        self.add_tile()
        self.updateGUI()
        self.game_over()
        
        
                    
    #Check if game is over
    #Available moves check:
    def horizontal_exists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j+1]:
                    return True
        return False
    
    def vertical_exists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i+1][j]:
                    return True
        return False        
        
    def game_over(self):
        #Win Condition: 2048 present on board
        if any(2048 in row for row in self.matrix):
            win_frame = tk.Frame(self.maingrid,borderwidth = 2)
            win_frame.place(relx = 0.5, rely = 0.5, anchor = "center")
            tk.Label(win_frame, 
                     bg = colors.WINNER_BG,
                     fg = colors.GAME_OVER_FONT_COLOR,
                     font = colors.GAME_OVER_FONT,
                     text = "YOU WON :DD" ).pack()
        #Lose Condition: No playable moves left
        #No Zeros exist, No horizontal moves exist, No Vertial moves exist
        
        if not any(0 in row for row in self.matrix) and not self.horizontal_exists() and not self.vertical_exists():
            lose_frame = tk.Frame(self.maingrid,borderwidth = 2)
            lose_frame.place(relx = 0.5, rely = 0.5, anchor = "center")
            tk.Label(lose_frame, 
                     bg = colors.LOSER_BG,
                     fg = colors.GAME_OVER_FONT_COLOR,
                     font = colors.GAME_OVER_FONT,
                     text = "YOU LOST D':" ).pack()
            
def main():           
    Game()

if __name__ == "__main__":
    main()
           