import pymol2
from pymol import cmd
import gtk
import gtk.gtkgl
import gobject

glconfig = gtk.gdkgl.Config(mode=(gtk.gdkgl.MODE_RGB |
                                  gtk.gdkgl.MODE_DOUBLE |
                                  gtk.gdkgl.MODE_DEPTH))

class PymolWindow(object):

    def __init__(self):
        self.glarea = self.create_glarea()
        self.pymol = pymol2.PyMOL(self.glarea)
        self.slab = 50
        self.zoom = 1.0
        self.angle = 0.0
        self.sprite = None
        self.zfactor = 0.005
        self.Zero_pointerx = 0
        self.Zero_pointery = 0
        self.ZeroX = 0
        self.ZeroY = 0
        self.clicado = False


    def create_glarea(self):
        glarea = gtk.gtkgl.DrawingArea(glconfig)
        glarea.set_size_request(600, 400)
        glarea.connect_after('realize', self.init)
        glarea.connect('configure_event', self.reshape)
        glarea.connect('expose_event', self.draw)
        glarea.connect('map_event', self.map)
        glarea.set_events(glarea.get_events() | gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK |
        gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK | gtk.gdk.KEY_PRESS_MASK)                      

        glarea.connect("button_press_event", self.mousepress)      
        glarea.connect("button_release_event", self.mouserelease)  
        glarea.connect("motion_notify_event", self.mousemove)      
        glarea.connect("scroll_event", self.slabchange)
        glarea.set_can_focus(True)
        return glarea


    def draw(self, glarea, event):
        # Get surface and context
        glcontext = glarea.get_gl_context()
        gldrawable = glarea.get_gl_drawable()

        # Start opengl context
        if not gldrawable.gl_begin(glcontext):
            return

        # Actual drawing
        sprite = self.sprite
        angle = self.angle
        zoom = self.zoom

        # Clear screen
        #rabbyt.clear((0.0, 0.0, 0.0))

        # Render sprite
        if sprite is not None:
            sprite.rot = angle
            sprite.scale = zoom
            sprite.render()

        # Flush screen
        gldrawable.swap_buffers()
        self.pymol.draw()
        # End opengl context
        gldrawable.gl_end()

        return True
    # Resizing function

    def reshape(self, glarea, event):

        reshape = event
        reshape_x = reshape.width
        reshape_y = reshape.height

        self.pymol.reshape(reshape_x, reshape_y, 0)
        self.pymol.idle()
        # pymol.draw()

        # Get surface and context
        glcontext = glarea.get_gl_context()
        gldrawable = glarea.get_gl_drawable()

        # Start opengl context
        if not gldrawable.gl_begin(glcontext):
            return

        # Get widget dimensions
        x, y, width, height = self.glarea.get_allocation()

        self.pymol.reshape(width, height, True)

        # Reset rabbyt viewport
        #rabbyt.set_viewport((width, height))
        # rabbyt.set_default_attribs()

        # End opengl context
        self.pymol.draw()
        gldrawable.swap_buffers()
        gldrawable.gl_end()
        #

        return True

    # Initialization function
    def init(self, glarea):
        print 'init'
        # Get surface and context
        glcontext = glarea.get_gl_context()
        gldrawable = glarea.get_gl_drawable()

        # Start opengl context
        if not gldrawable.gl_begin(glcontext):
            return

        # Get widget dimensions
        x, y, width, height = glarea.get_allocation()

        # Reset rabbyt viewport
        #rabbyt.set_viewport((width, height))
        # rabbyt.set_default_attribs()

        # Get sprite variable

        # Load sprite
        #sprite = rabbyt.Sprite('sprite.png')

        # End opengl context
        gldrawable.gl_end()

        return True

    # Idle function
    def idle(self, glarea):
        # Get vars
        angle = self.angle
        zoom = self.zoom
        zfactor = self.zfactor

        # Update angle
        angle += 1.0
        if angle > 359:
            angle = 0.0

        # Update zoom
        if zoom > 10 or zoom < 1:
            zfactor = -zfactor
            zoom += zfactor

        # Needed for synchronous updates
        if glarea.window:
            glarea.window.invalidate_rect(glarea.allocation, False)
            glarea.window.process_updates(False)

        return True

    # Map events function
    def map(self, glarea, event):
        # print 'map'
        # Add idle event
        gobject.idle_add(self.idle, glarea)
        return True

    def slabchange(self, button, event):
        #self.slab = self.self.slab
        #print self.self.slab
        x, y, width, height = self.glarea.get_allocation()
        if event.direction == gtk.gdk.SCROLL_UP:
            step = 1.5
            self.slab = self.slab + step
            self.slab = self.slab + step
            # if  self.slab >=100:
            #   self.slab = 100
        else:
            step = -1.5
            self.slab = self.slab + step

            if self.slab <= -5:
                self.slab = -5

        self.pymol.cmd.clip('slab', self.slab)
        return step
        self.pymol.button(button, 0, x, y, 0)
        self.pymol.idle()

    def show_context_menu(self, widget, event):
        x, y, state = event.window.get_pointer()
        if clicado:
            if event.button == 3:
                widget.popup(None, None, None, event.button, event.time)

    def mousepress(self, button, event):
        ZeroX = self.ZeroX
        ZeroY = self.ZeroY
        clicado = self.clicado
        
        ZeroX, ZeroY, state = event.window.get_pointer()
        
        #print ZeroX, ZeroY
        
        x, y, width, height = self.glarea.get_allocation()

            
        if event.button == 3:
            clicado = True
            #print 'gordao'
            x, y, width, height = self.glarea.get_allocation()
            #print x, y, width, height
            mousepress = event
            button = mousepress.button - 1
            pointerx = int(mousepress.x)
            pointery = int(mousepress.y)
            calc_y = height - pointery
            #print pointerx,pointery,calc_y
            #cmd.zoom(buffer=calc_y)
            self.pymol.button(button, 0, pointerx , calc_y, 0)

            
        if event.button != 3:
            x, y, width, height = self.glarea.get_allocation()
            mousepress = event
            button = mousepress.button - 1
            pointerx = int(mousepress.x)
            pointery = int(mousepress.y)
            calc_y = height - pointery
            self.pymol.button(button, 0, pointerx, calc_y, 0)

    def mouserelease(self, button, event):
        x, y, width, height = self.glarea.get_allocation()
        mouserelease = event
        button = mouserelease.button - 1
        pointerx = int(mouserelease.x)
        pointery = int(mouserelease.y)
        calc_y = height - pointery
        self.pymol.button(button, 1, pointerx, calc_y, 0)
        
    def mousemove(self, button, event):
        clicado = self.clicado
        Zero_pointerx = self.Zero_pointerx
        Zero_pointery = self.Zero_pointery

        x, y, width, height = self.glarea.get_allocation()
        clicado = False
        mousemove = event
        pointerx = int(mousemove.x)
        pointery = int(mousemove.y)

        calc_y2  = (float(Zero_pointery - pointery))/10.0
        calc_y   = height - pointery
        
        self.pymol.drag(pointerx, calc_y, 0)
        self.pymol.idle()

    def my_menu_func(self, menu):
        print "Menu clicado"
        def on_spinbutton_change_value(self, widget, event):
            """ Function doc """
            print 'teste'
            self.DrawCell()
