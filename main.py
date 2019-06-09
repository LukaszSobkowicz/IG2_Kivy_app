from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.garden.mapview import MapMarker, MarkerMapLayer
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.uix.floatlayout import FloatLayout
import functions as f
import numpy as np
import os

class LoadDialog(FloatLayout): #klasa okna wyboru pliku
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    
class Analyse(BoxLayout): #klasa root
    search_long = ObjectProperty()
    search_lat = ObjectProperty()
    my_map = ObjectProperty()
    p1_: ObjectProperty()
    p2_: ObjectProperty()
    p3_: ObjectProperty()
    p4_: ObjectProperty()
    p5_: ObjectProperty()
    p6_: ObjectProperty()
    p7_: ObjectProperty()
    p8_: ObjectProperty()
    pth_: ObjectProperty()
            
    def Data(self):        
        filename = self.pth_.text
        if filename.endswith('.gpx'):
            lon, lat, el, dates = f.load_file(filename)
            lat = lat[::5]   #wybiera co 5 znacznik 
            lon = lon[::5]
            self.draw_route(lat,lon)
            distance, vsr, dH, dHp, dHz, Hmax, Hmin, h, m, s = f.param(lon, lat, el, dates)#wczytuje parametry
            self.p1_.text = str("{:.2f}".format(distance))#wypisanie parametrów
            self.p2_.text = str("{:.3f}".format(dH))
            self.p3_.text = str(int(dHp))
            self.p4_.text = str(int(dHz))
            self.p5_.text = str("{:.1f}".format(vsr))
            self.p6_.text = str(h)+":"+str(m)+":"+str(s)
            self.p7_.text = str("{:.3f}".format(Hmin))
            self.p8_.text = str("{:.3f}".format(Hmax))
        else:
            self.pth_.text = "!!! nieodpowiedni format pliku (*.gpx) !!!"
                       
    def filedialog(self):#wyswietlenie okna wczytania
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
    
    def dismiss_popup(self):
        self._popup.dismiss()
            
    def load(self, path, filename):
        with open(os.path.join(path, filename[0])):
            self.pth_.text = str(filename[0])
            self.dismiss_popup()
                 
    def draw_route(self,lat,lon):#narysowanie trasy
        data_lay = MarkerMapLayer()
        self.my_map.set_zoom_at(11, 0, 0, scale=None)
        lat_ = float(np.mean(lat))
        lon_ = float(np.mean(lon))
        self.my_map.center_on(lat_, lon_)
        self.my_map.add_layer(data_lay) # my_map jest obiektem klasy MapView
        for point in zip(lat,lon):
            self.draw_marker(*point,layer = data_lay)
            
    def draw_marker(self, lat, lon, layer = None):
        markerSource = 'dot.png'
        if lat != None and lon != None:
            marker = MapMarker(lat = lat, lon = lon, source = markerSource)
            self.my_map.add_marker(marker, layer = layer)

class MapApp(App):
    def build(self):
        return Analyse()

Factory.register('LoadDialog', cls=LoadDialog)

if __name__ == '__main__':
    MapApp().run()
    
    