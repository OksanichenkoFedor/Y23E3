# Copyright (c) 2018 Esben Rossel
 # All rights reserved.
 #
 # Author: Esben Rossel <esbenrossel@gmail.com>
 #
 # Redistribution and use in source and binary forms, with or without
 # modification, are permitted provided that the following conditions
 # are met:
 # 1. Redistributions of source code must retain the above copyright
 #    notice, this list of conditions and the following disclaimer.
 # 2. Redistributions in binary form must reproduce the above copyright
 #    notice, this list of conditions and the following disclaimer in the
 #    documentation and/or other materials provided with the distribution.
 #
 # THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
 # ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 # IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 # ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
 # FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 # DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 # OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 # HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 # LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 # OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 # SUCH DAMAGE.

#plotting is derived from https://matplotlib.org/examples/user_interfaces/embedding_in_tk.html
import matplotlib
import tkinter as tk
import config
from matplotlib.patches import  Ellipse
from matplotlib.lines import Line2D
from count_plot_array import count_wave, np, count_pure, count_intence
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler

from matplotlib.figure import Figure





class buildplot(tk.Frame):
    def __init__(self, master):
        #create canvas
        self.f = Figure(figsize=(10, 5), dpi=100, tight_layout=True)
        self.ax1 = self.f.add_subplot(111)
        #self.ax2 = self.ax1.twinx()
        self.is_drawen = 0
        self.master = master
        self.main_frame = None

        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(self.f, master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, columnspan=2)
        self.canvas.mpl_connect("motion_notify_event", self.move_mouse_event)
        self.canvas.mpl_connect("button_press_event", self.click_mouse_event)
        self.canvas.mpl_connect("button_release_event", self.unclick_mouse_event)

        self.ax1.set_xlim([-1000, 5000])

        toolbarFrame = tk.Frame(master=master)
        toolbarFrame.grid(row=1, columnspan=2, sticky="w")
        toolbar1 = NavigationToolbar2Tk(self.canvas, toolbarFrame)

        def on_key_event(event):
            print('you pressed %s' % event.key)
            key_press_handler(event, self.canvas, self.toolbar)

    def update_plot(self, current_master=None):
        self.ax1.clear()

        #self.ax2.clear()
        if (config.is_make_spec == 1):

            # пересчёт config.pltData16 и рисование графика

            for i in range(config.num_plots):
                config.pltFullData16[i] = (config.rxFullData16[i][10] + config.rxFullData16[i][11]) / 2 - \
                                          config.rxFullData16[i]
                config.offset = (config.pltFullData16[i][18] + config.pltFullData16[i][20] + config.pltFullData16[i][
                    22] + config.pltFullData16[i][24] - config.pltFullData16[i][19] - config.pltFullData16[i][21] -
                                 config.pltFullData16[i][23] - config.pltFullData16[i][24]) / 4
                for j in range(1847):
                    # config.pltFullData16[i][2 * j] = config.pltFullData16[i][2 * j] - config.offset
                    pass
            count_wave()
            self.ax1.set_ylabel("Интенсивность")
            self.ax1.set_xlabel("Длина волны(нм)")
            start = min(config.data[0][0][0], config.data[1][0][0])
            end = max(config.data[0][0][-1], config.data[1][0][-1])
            config.plot_width = end - start
            config.plot_height = 2260
            self.ax1.axis([start, end, -10, 2250])
            if config.to_draw_divided == 1:
                ymin = min(config.data[2][1])
                ymax = max(config.data[2][1])
                #self.ax2.axis([start, end, ymin, ymax])
                config.plot_height = ymax-ymin
        else:
            for i in range(config.num_plots):
                if (config.datainvert == 1):
                    config.pltFullData16[i] = (config.rxFullData16[i][10] + config.rxFullData16[i][11]) / 2 - \
                                              config.rxFullData16[i]
                    # This subtracts the average difference between even and odd pixels from the even pixels
                    if (config.balanced == 1):
                        config.offset = (config.pltFullData16[i][18] + config.pltFullData16[i][20] +
                                         config.pltFullData16[i][22] + config.pltFullData16[i][
                                             24] - config.pltFullData16[i][19] - config.pltFullData16[i][21] -
                                         config.pltFullData16[i][23] - config.pltFullData16[i][24]) / 4
                        for j in range(1847):
                            config.pltFullData16[i][2 * j] = config.pltFullData16[i][2 * j] - config.offset

            if (config.datainvert == 1):
                count_pure()
                self.ax1.set_ylabel("Интенсивность")
                config.plot_width = config.data_inv_axis[1] - config.data_inv_axis[0]
                config.plot_height = config.data_inv_axis[3] - config.data_inv_axis[2]
                self.ax1.axis(config.data_inv_axis)
                if config.to_draw_divided == 1:
                    ymin = min(config.data[2][1])
                    ymax = max(config.data[2][1])
                    #self.ax2.axis([config.data_inv_axis[0], config.data_inv_axis[1], ymin, ymax])
                    config.plot_height = ymax - ymin
            else:
                # plot raw data
                #config.data = [config.pltFullData16[],1]
                count_pure()
                self.ax1.set_ylabel("Псевдо Интенсивность")
                config.plot_width = config.data_not_inv_axis[1] - config.data_not_inv_axis[0]
                config.plot_height = config.data_not_inv_axis[3] - config.data_not_inv_axis[2]
                self.ax1.axis(config.data_not_inv_axis)
                if config.to_draw_divided == 1:
                    ymin = min(config.data[2][1])
                    ymax = max(config.data[2][1])
                    #self.ax2.axis([config.data_not_inv_axis[0], config.data_not_inv_axis[1], ymin, ymax])
                    config.plot_height = ymax - ymin

            self.ax1.set_xlabel("Номер пикселя")

        self.ax1.plot(config.data[0][0], config.data[0][1])
        self.ax1.set_xlim(config.x_lim)
        if current_master==None:
            self.master.update_intence(count_intence())
            print("ddffd")
        else:
            current_master.update_intence(count_intence())

        line_left = Line2D([config.intence_x0,config.intence_x0], [0, 2250], color=config.l_col,
                           linestyle="--", linewidth=config.l_lw)
        line_right = Line2D([config.intence_x1, config.intence_x1], [0, 2250], color=config.r_col,
                            linestyle="--", linewidth=config.r_lw)
        line_bottom = Line2D(config.x_lim, [config.bottom_bound, config.bottom_bound], color=config.b_col,
                             linestyle="--", linewidth=config.b_lw)


        xlim = self.ax1.get_xlim()
        delta_x = xlim[1]-xlim[0]
        ylim = self.ax1.get_ylim()
        self.ymax = ylim[1]
        delta_y = ylim[1] - ylim[0]
        self.radius = 200
        size = self.f.get_size_inches() * self.f.dpi
        self.delta_xy = (delta_y/size[1])/(delta_x/size[0])

        self.circle_left = Ellipse((config.intence_x0, ylim[1]-0.55*int(self.delta_xy*self.radius)), int(self.radius),
                              int(self.delta_xy*self.radius), color=config.l_col)
        self.circle_left_xy = [config.intence_x0, ylim[1] - 0.55 * int(self.delta_xy * self.radius)]
        self.circle_right = Ellipse((config.intence_x1, ylim[1] - 0.55 * int(self.delta_xy * self.radius)), int(self.radius),
                              int(self.delta_xy * self.radius), color=config.r_col)
        self.circle_right_xy = [config.intence_x1, ylim[1] - 0.55 * int(self.delta_xy * self.radius)]
        self.circle_bottom = Ellipse((config.x_lim[0]+0.55 * int(self.radius), config.bottom_bound), int(self.radius),
                              int(self.delta_xy * self.radius), color=config.b_col)
        self.circle_bottom_xy = [config.x_lim[0]+0.55 * int(self.radius), config.bottom_bound]

        self.radius = self.radius

        self.ax1.add_line(line_left)
        self.ax1.add_line(line_right)
        self.ax1.add_line(line_bottom)

        #self.ax1.add_patch(self.circle_left)
        #self.ax1.add_patch(self.circle_right)
        #self.ax1.add_patch(self.circle_bottom)

        #self.master.IntenceVar = str(sum(config.data[0][1]))
        #print(sum(config.data[0][1]))
        #self.ax1.plot(config.data[1][0], config.data[1][1])
        if config.to_draw_divided==1:
            pass
            #self.ax2.plot(config.data[2][0], config.data[2][1], color = "g")
        #self.ax1.grid()
        self.is_drawen=1
        self.canvas.draw()

    def update_lines(self, current_master=None):
        line_left = Line2D([config.intence_x0, config.intence_x0], [0, 2250], color="r", linestyle="--")
        line_right = Line2D([config.intence_x1, config.intence_x1], [0, 2250], color="r", linestyle="--")

        self.ax1.add_line(line_left)
        self.ax1.add_line(line_right)
        self.ax1.grid()
        self.canvas.draw()

    def move_mouse_event(self, event):
        x = event.xdata
        y = event.ydata
        if config.push_down:
            if   config.what_push == "bottom" and x!=None:
                if y + config.curr_delta <= config.max_bottom_bound and y + config.curr_delta > 0:
                    config.bottom_bound = int(y + config.curr_delta)
                    self.master.bds_bot_value.set(config.bottom_bound)
            elif config.what_push == "right" and x!=None:
                if x + config.curr_delta <= config.num_pixels and x + config.curr_delta > config.intence_x0:
                    config.intence_x1 = int(x + config.curr_delta)
                    self.master.bdsl_scale["to"] = config.intence_x1
                    self.master.bdsr_scale.set(config.intence_x1)
            elif config.what_push == "left" and x!=None:
                if x + config.curr_delta <= config.intence_x1 and (x + config.curr_delta) > 0:
                    config.intence_x0 = int(x + config.curr_delta)
                    self.master.bdsr_scale["from"] = config.intence_x0
                    self.master.bdsl_scale.set(config.intence_x0)


        elif x != None and y != None:

            if (self.circle_bottom_xy[1] - event.ydata) ** 2 < (self.delta_xy*config.crit_delta) ** 2:
                config.l_lw = config.norm_val
                config.r_lw = config.norm_val
                config.b_lw = config.act_val
                config.b_col = "y"
                config.r_col = "r"
                config.l_col = "r"
            elif (self.circle_right_xy[0] - event.xdata) ** 2 < config.crit_delta ** 2:
                config.l_lw = config.norm_val
                config.r_lw = config.act_val
                config.b_lw = config.norm_val
                config.b_col = "r"
                config.r_col = "y"
                config.l_col = "r"
            elif (self.circle_left_xy[0] - event.xdata) ** 2 < config.crit_delta ** 2:
                config.l_lw = config.act_val
                config.r_lw = config.norm_val
                config.b_lw = config.norm_val
                config.b_col = "r"
                config.r_col = "r"
                config.l_col = "y"
            else:
                config.l_lw = config.norm_val
                config.r_lw = config.norm_val
                config.b_lw = config.norm_val
                config.b_col = "r"
                config.r_col = "r"
                config.l_col = "r"

        if not config.updating_for_cursor:
            config.updating_for_cursor = True
            self.update_plot(self.master)
            config.updating_for_cursor = False

    def click_mouse_event(self, event):
        config.push_down = True
        #delta_bot2 = (self.circle_bottom_xy[0] - event.xdata) ** 2 + (
        #            (self.circle_bottom_xy[1] - event.ydata) / (self.delta_xy)) ** 2
        #delta_r2 = (self.circle_right_xy[0] - event.xdata) ** 2 + (
        #            (self.circle_right_xy[1] - event.ydata) / (self.delta_xy)) ** 2
        #delta_l2 = (self.circle_left_xy[0] - event.xdata) ** 2 + (
        #            (self.circle_left_xy[1] - event.ydata) / (self.delta_xy)) ** 2
        if event.ydata==None or event.xdata==None:
            return 0
        if   (self.circle_bottom_xy[1] - event.ydata) ** 2 < config.crit_delta**2:
            config.b_col = "g"
            config.what_push = "bottom"
            config.curr_delta = config.bottom_bound - event.ydata
        elif (self.circle_right_xy[0] - event.xdata) ** 2 < config.crit_delta**2:
            config.r_col = "g"
            config.what_push = "right"
            config.curr_delta = config.intence_x1 - event.xdata
        elif (self.circle_left_xy[0] - event.xdata) ** 2 < config.crit_delta**2:
            config.l_col = "g"
            config.what_push = "left"
            config.curr_delta = config.intence_x0 - event.xdata
        else:
            pass
            config.what_push = "none"
            config.push_down = False
            return 0

        if not config.updating_for_cursor:
            config.updating_for_cursor = True
            self.update_plot(self.master)
            config.updating_for_cursor = False



    def unclick_mouse_event(self, event):
        if config.what_push == "bottom":
            config.b_col = "y"
        elif config.what_push == "right":
            config.r_col = "y"
        elif config.what_push == "left":
            config.l_col = "y"
        config.push_down = False
        config.what_push = "none"
        if not config.updating_for_cursor:
            config.updating_for_cursor = True
            self.update_plot(self.master)
            config.updating_for_cursor = False


    def print_event(self, event):
        if config.is_clever_cursor == 1:
            if self.is_drawen == 0:
                return 0
            if event.xdata == None:
                return 0
            if event.ydata == None:
                return 0
            self.update_plot()

            curr_ind = count_ind(event.xdata)

            curr_checking = config.curr_checking
            if config.to_draw_divided == 1:
                curr_checking = 2

            liney = Line2D([config.data[curr_checking][0][curr_ind],
                            config.data[curr_checking][0][curr_ind]], [0, 2250], color="r")

            linex = Line2D([0, 5000], [config.data[curr_checking][1][curr_ind],
                                       config.data[curr_checking][1][curr_ind]], color="r")


            curr_str = "X: " + str(round(config.data[curr_checking][0][curr_ind])) + "\n" + \
                       "Y: " + str(round(config.data[curr_checking][1][curr_ind]))
            if curr_checking == 2:
                curr_str = "X: " + str(round(config.data[curr_checking][0][curr_ind])) + "\n" + \
                           "Y: " + str(round(config.data[curr_checking][1][curr_ind], 2))

            #self.main_frame.update_coords(curr_checking, curr_ind)

            x_add = 1
            y_add = 1
            if config.data[curr_checking][0][curr_ind]*2 > config.plot_width:
                x_add = -1
            if config.data[curr_checking][1][curr_ind]*2 > config.plot_height:
                y_add = -1
            #config.plot_width = end - start
            #config.plot_height = 2260


            ellipse = matplotlib.patches.Ellipse(xy=(config.data[curr_checking][0][curr_ind],
                                                     config.data[curr_checking][1][curr_ind]),
                                                 width=config.plot_width*0.01, height=config.plot_height*0.02, color='r', fill=True)

            if config.to_draw_divided == 1:
                pass
                #self.ax2.add_line(liney)
                #self.ax2.add_line(linex)
                #self.ax2.add_patch(ellipse)
                #self.ax2.text(config.data[curr_checking][0][curr_ind] + x_add * config.plot_width * 0.031,
                #              config.data[curr_checking][1][curr_ind] + y_add * config.plot_height * 0.04,
                #              curr_str, ha="center", va="center")
            else:
                self.ax1.add_line(liney)
                self.ax1.add_line(linex)
                self.ax1.add_patch(ellipse)
                self.ax1.text(config.data[curr_checking][0][curr_ind] + x_add * config.plot_width * 0.031,
                              config.data[curr_checking][1][curr_ind] + y_add * config.plot_height * 0.04,
                              curr_str, ha="center", va="center")
            #circle1 = matplotlib.patches.Circle((config.data[curr_checking][0][curr_ind],
            #                                     config.data[curr_checking][1][curr_ind]), radius=20, fill=True,
            #                                   color="r")
            # self.ax1.add_patch(circle1)



            self.canvas.draw()






def count_ind(x):
    left_ind = 0
    right_ind = len(config.data[config.curr_checking][0])
    curr_ind = 0
    while (right_ind-left_ind)>1:
        curr_ind = int((left_ind+right_ind)/2)
        if config.data[config.curr_checking][0][curr_ind]<x:
            left_ind = curr_ind
        elif config.data[config.curr_checking][0][curr_ind]>x:
            right_ind = curr_ind
        else:
            right_ind = curr_ind
            left_ind = curr_ind
    return curr_ind
