#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  MastersMain.py
#  
#  Copyright 2015 Fernando Bachega <fernando@bahamuth>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  



# System
import datetime
import time
import pygtk
pygtk.require('2.0')

import gtk
import gobject
import sys

import os
import json
from  pprint import pprint

import pango

#------------------------GUI------------------------#
from gui.FileChooserWindow    import FileChooserWindow 
from gui.NewProjectDialog     import NewProjectDialog
from gui.WorkspaceDialog      import WorkspaceDialog
from gui.ProjectChooserDialog import ProjectChooserDialog
from gui.MonteCarloDialog     import MonteCarloDialog
#from WindowControl          import WindowControl
#from MCwindow               import MonteCarloSimulationWindow
#from MastersWorkSpaceDialog import WorkSpaceDialog
#from BoxSetupDialog         import BoxSetupDialog


class MastersMain():


    def __init__(self):
        print '           Intializing MasterGUI object          '
        
        # ------------- MASTERS GUI CONFIG FILE -------------- #
        self.HOME          = os.environ.get('HOME')
        self.configMASTERS = os.path.join(self.HOME, '.config/MASTERS/')
        #------------------------------------------------------#
        path = os.getcwd()
        self.gui  = os.path.join(path, 'gui')
        
        #---------------------------------- MasterGUI --------------------------------#
        self.builder = gtk.Builder()                                                  #
        self.builder.add_from_file(os.path.join(self.gui, "MastersMainWindow.glade")) #
        self.builder.add_from_file(os.path.join(self.gui, "MessageDialogs.glade")) #
        self.win     = self.builder.get_object("window1")                             #
        self.win.show()                                                               #
        self.builder.connect_signals(self)                                            #
                                                                                      #
        self.text_view = self.builder.get_object("textview1")                         #
        self.text_view.modify_font(pango.FontDescription("monospace 10"))             #
        #-----------------------------------------------------------------------------#

        
        self.projects = {}
        self.selectedID  = None
        #self.selectedObj = None    
        

        
        #---------------------------------------------------------#
        #                PROJECT HISTORY DATA                     #
        #---------------------------------------------------------#      
        try:
            self.projects = json.load(open(self.configMASTERS + 'ProjectHistory.dat'))
            pprint(self.projects)
        except:
            self.projects = {}
        

        self.ActivedProject = None    
        
        
        #---------------------------------------------------------#
        #                  MASTERS GUI CONFIG                     #
        #---------------------------------------------------------#
        self.GUIConfig = {                              
                       'HideWorkSpaceDialog': False,  
                       'WorkSpace'          : self.HOME,  
                       'History'            : {}   } 
        self.Load_GUI_ConfigFile()
        #---------------------------------------------------------#

        
        #---------------------------------------Dialogs and Windows------------------#
        #self.WindowControl    = WindowControl   (self.builder, self.projects )      #
        self.NewProjectDialog     = NewProjectDialog(self)                           #
        self.WorkSpaceDialog      = WorkspaceDialog (self)                           #
        self.ProjectChooserDialog = ProjectChooserDialog(self)                       #
        self.MessageDialogQuestion= self.builder.get_object('messagedialog_question')#
        self.MessageDialogError   = self.builder.get_object('messagedialog_error')   #
        self.MonteCarloDialog     = MonteCarloDialog(self)
        #----------------------------------------------------------------------------#

        
        # testing the workspace dialog True/False 
        if self.GUIConfig['HideWorkSpaceDialog'] == False:
            self.WorkSpaceDialog.dialog.run()
            self.WorkSpaceDialog.dialog.hide()

        # if project existis -  open project list
        if self.projects != {}:
            pprint(self.projects)
            self.LoadProjectChooserDialog()
   
        if self.projects == {}:
            self.LoadNewProjectDialog()


    
    
    
    ''' 
        --------------------------------------------------
    
                        GUI CONFIG METHODS
    
        --------------------------------------------------
    ''' 
        
    def Load_GUI_ConfigFile (self, filename = None):
        """ Function doc """
        #.config
        path = os.path.join(self.HOME ,'.config', 'MASTERS', 'GUI.config')
        
        try:
            self.GUIConfig = json.load(open(path)) 
        except:
            print 'error: GUIConfig file not found'
            print 'open WorkSpace Dialog'

    def Save_GUI_ConfigFile(self):
        """ Function doc """
        path = os.path.join(self.HOME,'.config')
        if not os.path.exists (path): 
            os.mkdir (path)

        path = os.path.join(path, 'MASTERS')
        if not os.path.exists (path): 
            os.mkdir (path)
        
        filename = os.path.join(path,'GUI.config')
        json.dump(self.GUIConfig, open(filename, 'w'), indent=2)


    ''' 
        --------------------------------------------------
    
                        GUI METHODS
    
        --------------------------------------------------
    ''' 
    def LoadProjectChooserDialog (self):
        """ Function doc """
        self.ProjectChooserDialog.AddProjectHistoryToTreeview()
        self.ProjectChooserDialog.dialog.run()
        self.ProjectChooserDialog.dialog.hide()

    def LoadNewProjectDialog (self):
        """ Function doc """
        self.NewProjectDialog.dialog.run()
        self.NewProjectDialog.dialog.hide()

    def AddJobHistoryToTreeview (self, liststore = None, Jobs = None ):
        #self.ActivedProject = projectID
        try:
            Jobs   = self.projects[self.ActivedProject]['Jobs']
            Folder = self.projects[self.ActivedProject]['Folder']

            liststore = self.builder.get_object("liststore1")
            
            try:
                #self.WindowControl.AddJobHistoryToTreeview(liststore, Jobs)
                model = self.builder.get_object('liststore1')
                model = liststore

                numbers = list(Jobs)      # this is necessary to sorte the Jobs dic
                numbers2 = []
                
                for i in numbers:
                    numbers2.append(int(i))
                numbers2.sort()
                model.clear()
                #print model
                
                for i in numbers2:
                    i = str(i)
                    
                    if Jobs[str(i)]==None:
                        pass
                    else:
                        data = [str(i), Jobs[i]['Type'],Jobs[i]['Start'],Jobs[i]['End'],Jobs[i]['Energy'],Jobs[i]['Title'] ]
                        #print i, data
                        model.append(data)
            except:
                pass
            text = 'Project: ' + self.projects[self.ActivedProject]['ProjectName'] + '    Directory:' + Folder
            self.STATUSBAR_SET_TEXT(text)
        
        except:
            model = self.builder.get_object('liststore1')
            model.clear()

    def LoadFileToTextView(self, filename):
        ## add Loading message to status bar and ensure GUI is current
        fin = open(filename, "r")
        text = fin.read()
        fin.close()
        
        # disable the text view while loading the buffer with the text
        self.text_view.set_sensitive(False)
        buff = self.text_view.get_buffer()
        buff.set_text(text)
        buff.set_modified(False)
        self.text_view.set_sensitive(True)
    
    def DeleteProject (self, projectID):
        """ Function doc """
        self.projects[projectID] = None
        json.dump(self.projects, open(os.path.join(self.configMASTERS ,'ProjectHistory.dat'), 'w'), indent=2)
        self.AddJobHistoryToTreeview()
    
    def DeleteJob (self, jobID):
        """ Function doc """
        if jobID == "0":
            print 'The Initial coordenates can not be removed. Please remove the whole project'
        else:
            self.projects[self.ActivedProject]['Jobs'][str(jobID)] = None
            json.dump(self.projects, open(os.path.join(self.configMASTERS ,'ProjectHistory.dat'), 'w'), indent=2)
            self.AddJobHistoryToTreeview()
            
    def STATUSBAR_SET_TEXT(self, text):
        """ Function doc """
        self.builder.get_object('statusbar1').push(0, text)


    #------------------------------------------------#
    #               TOOLBAR  METHODS                 #
    #------------------------------------------------#

    def on_toolbutton_LoadProjectChooserDialog_clicked(self, button):
        """ Function doc """
        self.LoadProjectChooserDialog ()

    def on_toolbutton_NewProject_clicked(self, button):
        self.LoadNewProjectDialog()

    def on_button_DeleteCurrentProject_clicked (self, button):
        """ Function doc """
        if self.ActivedProject == None:
            print 'No project in memory'
            pass
        
        else:
            self.MessageDialogQuestion.format_secondary_text("Delete the selected project - "+self.ActivedProject+"?")
            a = self.MessageDialogQuestion.run()  # possible "a" valors                                                           
            self.MessageDialogQuestion.hide()                                                                  
            # -8  -  yes   
            # -9  -  no    
            # -4  -  close 
            # -5  -  OK                                                                                                       
            # -6  -  Cancel                                                                                                   
            if a == -8:
                self.DeleteProject (self.ActivedProject)
                buff = self.text_view.get_buffer()
                buff.set_text("")
            else:
                pass
    
    def on_toolbutton_DeleteSelectedJob_clicked (self, button):
        """ Function doc """
        tree          = self.builder.get_object('treeview3')
        selection     = tree.get_selection()
        model         = tree.get_model()
        (model, iter) = selection.get_selected()
        if iter != None:
            jobID       = str(model.get_value(iter, 0))
            #print jobID
            
            self.MessageDialogQuestion.format_secondary_text("Delete the selected job - "+ jobID + "?")
            a = self.MessageDialogQuestion.run()                                                            
            self.MessageDialogQuestion.hide()                                                               
            # -8  -  yes   
            # -9  -  no    
            # -4  -  close 
            # -5  -  OK                                                              
            # -6  -  Cancel                                                                                           

            if a == -8:
                print jobID
                self.DeleteJob (jobID)
                buff = self.text_view.get_buffer()
                buff.set_text("")
            else:
                pass
        pass

    def on_toolbutton_MonteCarlo_clicked (self, button):
        """ Function doc """
        self.MonteCarloDialog.ImportCellValorsFromProject()
        self.MonteCarloDialog.dialog.run()
        self.MonteCarloDialog.dialog.hide()


    def testGTKMatplotLib(self, button):
        """ Function doc """
        from matplotlib.figure import Figure
        from numpy import arange, sin, pi

        # uncomment to select /GTK/GTKAgg/GTKCairo
        #from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
        from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
        from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar


        box = self.builder.get_object('vbox4')
        self.graph = box

        f = Figure(figsize=(5, 4), dpi=100)
        a = f.add_subplot(111)
        #t = arange(0.0,3.0,0.01)
        #s = sin(2*pi*t)
        t = range(0, 10)
        s = range(0, 10)

        t = [0,
             5,
             10,
             15,
             20,
             25,
             30,
             35,
             40,
             45,
             50,
             55,
             60,
             65,
             70,
             75,
             80,
             85,
             90,
             95,
             100,
             105,
             110,
             115,
             120,
             125,
             130,
             135,
             140,
             145,
             150,
             155,
             160,
             165,
             170,
             175,
             180,
             185,
             190,
             195,
             200]

        s = [-913.53086808,
             -1978.05074306,
             -2218.21815405,
             -2333.01919415,
             -2391.82858579,
             -2435.17776079,
             -2486.44564867,
             -2543.07423428,
             -2571.71716511,
             -2598.62940311,
             -2616.98004127,
             -2631.60794731,
             -2648.00535887,
             -2661.72725012,
             -2675.65233140,
             -2686.34375946,
             -2696.94907090,
             -2708.65130605,
             -2718.73853503,
             -2726.36193409,
             -2732.59504750,
             -2737.83623730,
             -2742.33435229,
             -2745.28712806,
             -2748.82036113,
             -2752.12502818,
             -2754.57566090,
             -2756.97531091,
             -2758.83136980,
             -2760.53521449,
             -2762.79017667,
             -2764.47319544,
             -2765.99011566,
             -2767.77186148,
             -2770.20329165,
             -2772.66204338,
             -2775.05818125,
             -2776.97966619,
             -2779.02106271,
             -2781.43441141,
             -2783.70324049]

        a.plot(t, s, 'ko', t, s, 'k')
        #a.plot(x, y, 'ko',x, y,'k')
        canvas = FigureCanvas(f)  # a gtk.DrawingArea
        self.graph.pack_start(canvas)
        toolbar = NavigationToolbar(canvas, self.graph)
        self.graph.pack_end(toolbar, False, False)
        self.graph.show_all()
        # gtk.main()
    
    #------------------------------------------------#
    #               TREEVIEW  METHODS                #
    #------------------------------------------------#         
    def on_treeview3_button_release_event(self, tree, event):
        """ Function doc """
        if event.button == 3:
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            if iter != None:
                self.selectedID  = str(model.get_value(iter, 1))
                self.selectedObj = str(model.get_value(iter, 2))

                self.builder.get_object('TreeViewObjLabel').set_label('- ' +self.selectedID+' -' )
                widget = self.builder.get_object('treeview_menu')
                widget.popup(None, None, None, event.button, event.time)
            
        if event.button == 1:
            #print "Mostrar menu de contexto botao1"
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            
            if iter != None:
                #print model, iter
                JobID         = model.get_value(iter, 0)
                pymol_object  = model.get_value(iter, 2)  # @+
                #print _object
                #pprint (self.projects[self.ActivedProject]['Jobs'][JobID])
                filename = self.projects[self.ActivedProject]['Jobs'][JobID]['Output']
                #print filename
                self.LoadFileToTextView(filename)
            
            
            
            
    def run(self):
        gtk.main()




def main():
    masters = MastersMain()
    masters.run()
    return 0

if __name__ == '__main__':
	main()
