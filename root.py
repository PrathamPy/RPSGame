#__________________________________________________________________________________________________
#--------------------------------------------------------------------------------------------------
#SETTING UP APP------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#__________________________________________________________________________________________________



#----------------------------------------------------------------------------------------
#Importing Modules
#----------------------------------------------------------------------------------------


#--::Built-In Modules::--#
from PIL import ImageTk, Image
from tkinter import ttk
import tkinter as tk
import socket
import random
import time
import json
import sys

#--::Custom Modules::--#
import fontloader as fl
import account as acc
import database as db

#------------------------------------------------------------------------------
#Initializing Predefined Variables
#------------------------------------------------------------------------------
rps_vs = [["rock", "scissors", "paper"], ["paper", "rock", "scissors"],
         ["scissors", "paper", "rock"]]

private_key = "rps-multiplayer-game-2634e-firebase-adminsdk-sjh5v-85fa55a650.json"
db_ = db.FirebaseDB(private_key)

username = "PKing"

#______________________________________________________________________________
#------------------------------------------------------------------------------
#MAIN CODE---------------------------------------------------------------------
#------------------------------------------------------------------------------
#______________________________________________________________________________



#------------------------------------------------------------------------------
#APP CLASS
#------------------------------------------------------------------------------
class App(tk.Tk):
    '''
    Contains all functions and variables for generating and updating the GUI of
    the application.
    '''

    #--::Predefined Fonts::--#
    fredoka_path = r"Fonts\FredokaOne-Regular.ttf"
    righteous_path = r"Fonts\Righteous-Regular.ttf"
    lobster_path = r"Fonts\Lobster-Regular.ttf"
    fredoka_one = fl.loadfont(fredoka_path)
    righteous = fl.loadfont(righteous_path)
    lobster = fl.loadfont(lobster_path)

    HEAD_FONT1 = (fredoka_one, 40, "underline")
    SBHD_FONT1 = (fredoka_one, 25)
    ALL_FONT1 = (fredoka_one, 15)
    ALL_FONT2 = (righteous, 15)
    LBL_FONT1 = (lobster, 35)
    LBL_FONT2 = (righteous, 20)
    BTN_FONT1 = (righteous, 25)

    def __init__(self):
        '''
        Generates the UI for the Home Screen and Play Screen and starts other GUI
        related processes.
        '''

        #--::Initializing root window::--#
        super().__init__()
        print("self", self)

        self.rock_img = ImageTk.PhotoImage(Image.open(r"Images/rock.jpg"))
        self.paper_img = ImageTk.PhotoImage(Image.open(r"Images/paper.jpg"))
        self.scissor_img = ImageTk.PhotoImage(Image.open(r"Images/scissors.jpg"))

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.geometry("{}x{}".format(self.screen_width, self.screen_height))

        #--::Home Frame::--#
        self.home_f = tk.Frame(self)
        self.home_f.pack(fill = "both", expand = 1)

        self.HF_on_btn = tk.Button(self.home_f, text = "Play Online", padx = 10, pady = 5,
                                   font = self.BTN_FONT1, relief = "groove",
                                   command = self.show_popup)
        self.HF_on_btn.place(relx = 0.75, rely = 0.45, anchor = "center")

        self.HF_off_btn = tk.Button(self.home_f, text = "Play with Computer", padx = 10, pady = 5,
                                    font = self.BTN_FONT1, relief = "groove",
                                    command = self.show_popup)
        self.HF_off_btn.place(relx = 0.75, rely = 0.75, anchor = "center")

        self.HF_wdgs = (self.HF_on_btn, self.HF_off_btn)
        self.HF_wdg_plcs = ((0.75, 0.45, "center"), (0.75, 0.55, "center"))

        #--::Offline Frame::--#
        self.offl_f = tk.Frame(self)

        self.OF_head = tk.Label(self.offl_f, text = "OOPS! We couldn't connect to internet.",
            font = self.HEAD_FONT1)

        self.OF_sbhd = tk.Label(self.offl_f, text = "Try Reconnecting or ", font = self.SBHD_FONT1)
        self.OF_game_btn = tk.Button(self.offl_f, text = "Play with Computer", padx = 10, pady = 5,
                                     font = self.BTN_FONT1, relief = "groove",
                                     command = self.show_popup)

        self.OF_wdgs = (self.OF_head, self.OF_sbhd, self.OF_game_btn)
        self.OF_wdg_plcs = ((0.5, 0.25, "center"), (0.15, 0.5, "w"), (0.75, 0.5, "center"))

        #--::Play Frame::--#
        self.play_f = tk.Frame(self)

        self.PF_ani_lbl = tk.Label(self, bg = "red", width = self.screen_width,
                                   font = self.HEAD_FONT1, height = self.screen_height)

        self.PF_head = tk.Label(self.play_f, font = self.HEAD_FONT1)
        self.PF_sub_head = tk.Label(self.play_f, font = self.SBHD_FONT1)

        self.PF_p1_bar = ttk.Progressbar(self.play_f, orient = "vertical", length = 350,
                                         mode = "determinate", value = 0)
        self.PF_p1_cpt = tk.Label(self.play_f, font = self.LBL_FONT2)
        self.PF_p1_opt = tk.Label(self.play_f)

        self.PF_p2_bar = ttk.Progressbar(self.play_f, orient = "vertical", length = 350,
                                         mode = "determinate", value = 0)
        self.PF_p2_cpt = tk.Label(self.play_f, font = self.LBL_FONT2)
        self.PF_p2_opt = tk.Label(self.play_f)

        self.PF_rock_btn = tk.Button(self.play_f, image = self.rock_img, bg = "gray", height = 105,
                                     width = 105,command = lambda: self.played("rock"))
        self.PF_paper_btn = tk.Button(self.play_f, image = self.paper_img, bg = "gray",
                                      height = 105, width = 105)
        self.PF_scissor_btn = tk.Button(self.play_f, image = self.scissor_img, bg = "gray",
                                        height = 105, width = 105)

        self.PF_rmtch_btn = tk.Button(self.play_f, font = self.ALL_FONT1, padx = 10, pady = 5,
                                      text = "Rematch")
        self.PF_home_btn = tk.Button(self.play_f, font = self.ALL_FONT1, padx = 10, pady = 5,
                                     text = "Back to Home",
                                     command = lambda: self.shift_to_frame(self.home_f))

        self.PF_wdgs = (self.PF_head, self.PF_sub_head, self.PF_p1_bar, self.PF_p2_bar,
                        self.PF_p1_cpt, self.PF_p2_cpt, self.PF_p1_opt, self.PF_p2_opt,
                        self.PF_rock_btn, self.PF_paper_btn, self.PF_scissor_btn)
        self.PF_wdg_plcs = ((0.5, 0.1, "center"), (0.5, 0.25, "center"), (0.1, 0.4, "w"),
                            (0.9, 0.4, "e"), (0.1, 0.75, "center"), (0.9, 0.75, "center"),
                            (0.1, 0.85, "center"), (0.9, 0.85, "center"), (0.3, 0.5, "center"),
                            (0.5, 0.5, "center"), (0.7, 0.5, "center"))

        #--::Bindings::--#
        def on_enter(e):
            '''
            Method which changes the background color of the widget received
            (Either rock, paper or scissor btn.)

            Parameters:
            -----------
                e: Event returned by tkinter (No need to specify when calling)
            '''
            e.widget["bg"] = "#00CED1"

        def on_leave(e):
            '''
            Method which changes the background color of the widget received
            (Either rock, paper or scissor btn.)

            Parameters:
            -----------
                e: Event returned by tkinter (No need to specify when calling)
            '''
            e.widget["bg"] = "gray"

        self.PF_rock_btn.bind("<Enter>", on_enter)
        self.PF_paper_btn.bind("<Enter>", on_enter)
        self.PF_scissor_btn.bind("<Enter>", on_enter)
        self.PF_rock_btn.bind("<Leave>", on_leave)
        self.PF_paper_btn.bind("<Leave>", on_leave)
        self.PF_scissor_btn.bind("<Leave>", on_leave)

        #--::Calling Other Functions::--#
        self.is_connected()
        self.popup()

    def is_connected(self):
        '''
        Checks if the computer is connected to the internet and subsequently
        updates the self.connected variable.

        Returns
        -------
        bool
            Returns True / False based on the connection

        '''
        try:
            sock = socket.create_connection(("www.google.com", 80))
            if sock is not None:
                print('Closing socket')
                sock.close()
            self.connected = True
            return True
        except OSError:
            self.shift_to_frame(self.home_f, self.offl_f, self.OF_wdgs, self.OF_wdg_plcs,
                                self.HF_wdgs)
            self.connected = False
            return False

    def shift_to_frame(self, prev_f, frame, c_wdgs, c_wdgplcs, p_wdgs):
        '''
        Changes the current frame being displayed on the Tk by unpacking and
        packing frames and their widgets

        Parameters:
        ----------
        prev_f : Tkinter frame widget (Must start with self)
            The previous frame which is unpacked
        frame : Tkinter frame widget (Must start with self)
            The frame which is to be packed
        c_wdgs : List / Tuple
            The list of widgets inside 'frame' which are to be packed
        c_wdgplcs : 2-d List / Tuple
            The list of widget placements corresponding to c_wdgs
        p_wdgs : List / Tuple
            The list of widgets inside 'prev_f' which are to be unpacked

        Returns
        -------
        None.

        '''
        prev_f.pack_forget()

        for wdg in p_wdgs:
            wdg.place_forget()

        frame.pack(fill = "both", expand = 1)

        for wdg in c_wdgs:
            wdgplc = c_wdgplcs[c_wdgs.index(wdg)]
            relx = wdgplc[0]
            rely = wdgplc[1]
            anchor = wdgplc[2]
            wdg.place(relx = relx, rely = rely, anchor = anchor)

    def popup(self):
        '''
        Generates the variables needed to create popups with the help of the
        popup module. Meant to organize the code.

        Returns
        -------
        None.

        '''

        def retrieve():
            '''
            Returns all inputs from the user in the new game popup for creating
            a match.

            Returns
            -------
            match_settings : list
                Contains a list of all values from the inputs of the popup.

            '''
            match_settings = []
            for dp in self.PO_inps:
                val = dp.get()
                match_settings.append(val)

            return match_settings

        #--::Creating Popup Window::--#
        self.popup = tk.Toplevel(self)
        self.popup.geometry("450x450")
        self.popup.withdraw()

        #--::Creating Widgets::--#
        self.PO_head = tk.Label(master = self.popup, text = "NEW ONLINE GAME",
                                font = self.SBHD_FONT1)
        self.PO_pl_inp_lbl = tk.Label(master = self.popup, text = "Players", font = self.ALL_FONT2)
        self.PO_md_inp_lbl = tk.Label(master = self.popup, text = "Mode", font = self.ALL_FONT2)
        self.PO_tg_inp_lbl = tk.Label(master = self.popup, text = "Target", font = self.ALL_FONT2)

        self.PO_pl_inp_dp = ttk.Combobox(master = self.popup, values = [2])
        self.PO_md_inp_dp = ttk.Combobox(master = self.popup, values = ["Score Target"])
        self.PO_tg_inp_dp = ttk.Combobox(master = self.popup, state = "readonly",
                                         values = [2, 3, 5, 8, 10, 15, 20])
        self.PO_pl_inp_dp.current(0)
        self.PO_md_inp_dp.current(0)
        self.PO_tg_inp_dp.current(0)

        self.PO_ok_btn = tk.Button(self.popup, text = "Create Game", font = self.ALL_FONT1,
                                   command = lambda: self.start_match(retrieve()))
        self.PO_ca_btn = tk.Button(master = self.popup, text = "Cancel", font = self.ALL_FONT1)

        if isinstance(self, OfflineGame):
            self.PO_head["text"] = "NEW OFFLINE GAME"

        #--::Widget Placements::--#
        self.PO_wdg_plcs = ((0.5, 0.1, "center"), (0.1, 0.25, "w"), (0.1, 0.45, "w"),
                            (0.1, 0.65, "w"), (0.5, 0.35, "center"), (0.5, 0.55, "center"),
                            (0.5, 0.75, "center"), (0.15, 0.9, "w"), (0.85, 0.9, "e"))

        #--::Popup Widgets::--#
        self.PO_wdgs = (self.PO_head, self.PO_pl_inp_lbl, self.PO_md_inp_lbl,
                        self.PO_tg_inp_lbl, self.PO_pl_inp_dp, self.PO_md_inp_dp,
                        self.PO_tg_inp_dp, self.PO_ok_btn, self.PO_ca_btn)
        self.PO_inps = (self.PO_pl_inp_dp, self.PO_md_inp_dp, self.PO_tg_inp_dp)

    def show_popup(self):
        '''
        Shows popup toplevel and places all other popup widgets on it.

        Returns
        -------
        None.

        '''
        self.popup.deiconify()

        for wdg in self.PO_wdgs:
            wdg_plc = self.PO_wdg_plcs[self.PO_wdgs.index(wdg)]
            relx = wdg_plc[0]
            rely = wdg_plc[1]
            anchor = wdg_plc[2]
            wdg.place(relx = relx, rely = rely, anchor = anchor)

    def close_popup(self):
        '''
        Closes the popup toplevel and place_forget()'s all other popup widgets.

        Returns
        -------
        None.

        '''
        self.popup.withdraw()

        for wdg in self.PO_wdgs:
            wdg.place_forget()

#------------------------------------------------------------------------------
#RPSGAME CLASS
#------------------------------------------------------------------------------
class RPSGame(App):
    '''
    Creates an RPS Game and contains functions for tasks related to the game
    that are common for both OnlineGame() and OfflineGame() classes.
    '''

    def __init__(self):
        '''
        Calls the parent class. Meant to continue the flow of inheritance.

        Returns
        -------
        None.

        '''
        super().__init__()

    def place_wdgs(self):
        self.PF_ani_lbl.place_forget()
        for wdg in self.PF_wdgs:
            wdgplc = self.PF_wdg_plcs[self.PF_wdgs.index(wdg)]
            relx = wdgplc[0]
            rely = wdgplc[1]
            anchor = wdgplc[2]
            wdg.place(relx = relx, rely = rely, anchor = anchor)

    def remove_wdgs(self, plcal = True):
        for wdg in self.PF_wdgs:
            wdg.place_forget()
        if plcal:
            self.PF_ani_lbl.place(relx = 0.5, rely = 0.5, anchor = "center")

    def start_round(self):

        def rd_animate():
            #--::Animation::--#
            self.remove_wdgs()
            self.PF_ani_lbl["text"] = "ROUND {}".format(self.round_no)
            self.after(1000, self.place_wdgs)

        print("start_round")
        #--::Creation of round dictionary::--#
        self.round = {}

        #--::Animation::--#
        rd_animate()

    def start_match(self, p1, p2, match_settings):
        '''
        Creates a RPS Game and intializes the player scores and afterwards starts
        the match.

        Parameters
        ----------
        p1 : str
            Name of the player 1. Used for display in the GUI
        p2 : str
            Name of the player 2. Used for display in the GUI
        match_settings : list
            A list containing match details received from the popup

        Returns
        -------
        None.

        '''
        print("start_mtch")

        def mtch_animate():
            '''
            Creates a countdown that occupies the screen for 4 seconds and then disappears.

            Returns
            -------
            None.

            '''
            print("mtch_animate")
            #--::Animation::--#

            #--Placing ani_lbl--#
            self.PF_ani_lbl.place(relx = 0.5, rely = 0.5, anchor = "center")

            #--Animation--#
            for i in range(3):
                val = str(3 - i)
                self.PF_ani_lbl["text"] = "Match starts in:\n{}".format(val)
                self.after(1000)

            self.PF_ani_lbl["text"] = "GO!"

            #--Displacing ani_lbl--#
            self.PF_ani_lbl.place_forget()

            #--::Starting Round::--#
            self.start_round()

        #--::Initializing Game Variables::--#

        #--Initializing Player Variables--#
        self.p1 = p1
        self.p2 = p2
        self.p1_score = 0
        self.p2_score = 0
        self.pl_scores = [self.p1_score, self.p2_score]

        #--Initializing Other Variables--#
        self.rounds = {}
        self.match_settings = {
            "Players": int(match_settings[0]),
            "Mode": match_settings[1],
            "Target": int(match_settings[2])
            }
        self.players = self.match_settings["Players"]
        self.mode = self.match_settings["Mode"]
        self.target = self.match_settings["Target"]

        self.match_finished = False
        self.round_no = 1

        #--::Starting Match::--#
        if self.connected:
            self.shift_to_frame(self.home_f, self.play_f, self.PF_wdgs, self.PF_wdg_plcs,
                              self.HF_wdgs)
        else:
            self.shift_to_frame(self.offl_f, self.play_f, self.PF_wdgs, self.PF_wdg_plcs,
                              self.OF_wdgs)

        self.close_popup()

        self.PF_head["text"] = "{}     vs.     {}".format(self.p1, self.p2)
        self.PF_p1_cpt["text"] = self.p1
        self.PF_p2_cpt["text"] = self.p2

        self.after(10, mtch_animate)

    def finish_round(self, p1opt, p2opt):
        '''
        Decides the winner, displays it and then starts the next round.

        Parameters
        ----------
        p1opt : str
            Option which player 1 chose.
        p2opt : str
            Option which player 2 chose.

        Returns
        -------
        None.

        '''

        #--::Decision of Winner::--#
        for opt in rps_vs:
            if p1opt == opt[0]:
                if p2opt == opt[1]:
                    winner = self.p1
                    self.p1_score += 1

                elif p2opt == opt[2]:
                    winner = self.p2
                    self.p2_score += 1
                else:
                    winner = "Draw"
                    self.p1_score += 0.5
                    self.p2_score += 0.5

        #--::Updation of Information::--#

        #--Updation of GUI--#
        self.PF_p1_opt["text"] = p1opt
        self.PF_p2_opt["text"] = p2opt

        if winner != "Draw":
            self.PF_sub_head["text"] = "{} Wins the Round!".format(winner)
        else:
            self.PF_sub_head["text"] = "Its a Draw!"

        #--Updation of Data--#
        self.round["Winner"] = winner
        self.rounds[f"Round {self.round_no}"] = self.round
        self.round_no += 1

        #--::Continuation of Game::--#
        if self.p1_score != self.p2_score:
            if self.p1_score > self.match_settings["Target"]:
                self.finish_mtch(self.p1)
            elif self.p2_score > self.match_settings["Target"]:
                self.finish_mtch(self.p2)
            else:
                self.start_round()
        else:
            if self.p1_score > self.match_settings["Target"]:
                self.finish_mtch("DRAW")

    def finish_mtch(self, winner):
        '''
        Ends the match, decides the winner, updates the database(if online game)
        and also gives options to return back to home or to rematch.

        Returns
        -------
        None.

        '''
        if winner != "Draw":
            self.PF_sub_head["text"] = "{} WINS THE MATCH!".format(winner)
        else:
            self.PF_sub_head["text"] = "ITS A DRAW!"

        self.PF_home_btn.place(relx = 0.25, rely = 0.8, anchor = 'center')

        self.PF_rmtch_btn.place(relx = 0.75, rely = 0.8, anchor = 'center')

class OfflineGame(RPSGame):
    def __init__(self):
        super().__init__()

    def start_match(self, match_settings):
        super().start_match(username, "Computer", match_settings)

    def start_round(self):
        super().start_round()

    def played(self, opt):
        comp_opt = random.choice(["rock", "paper", "scissors"])
        super().finish_round(opt, comp_opt)

def main():
    off_obj = OfflineGame()
    off_obj.mainloop()

if __name__ == "__main__":
    main()
