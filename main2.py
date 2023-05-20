import customtkinter
import cv2
import tkinter
from tkintermapview import TkinterMapView
from PIL import Image, ImageTk


customtkinter.set_default_color_theme("blue")
customtkinter.set_appearance_mode("Dark")


class App(customtkinter.CTk):

    APP_NAME = "AVP-MOOS v0.1"
    WIDTH = 1000
    HEIGHT = 800

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        self.marker_list = []

        #Variáveis auxiliares
        self.camera_on = False

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(4, weight=1)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Set Marker",
                                                command=self.set_marker_event)
        self.button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Clear Markers",
                                                command=self.clear_marker_event)
        self.button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Câmera",
                                                command=self.open_camera)
        self.button_3.grid(pady=(20, 0), padx=(20, 20), row=2, column=0)

        self.button_4 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Desativar Mapas",
                                                command=self.destroy_maps)
        self.button_4.grid(pady=(20, 0), padx=(20, 20), row=3, column=0)

        

        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Servidor de Mapas:", anchor="w")
        self.map_label.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite"],
                                                                       command=self.change_map)
        self.map_option_menu.grid(row=6, column=0, padx=(20, 20), pady=(10, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Aparência:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=(20, 20), pady=(10, 20))

        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)
        
        

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))
        self.map_widget.set_overlay_tile_server("http://tiles.openseamap.org/seamark//{z}/{x}/{y}.png")

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            placeholder_text="type address")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_event)

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Search",
                                                width=90,
                                                command=self.search_event)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        ###Imagem da camera
        self.vid = cv2.VideoCapture('teste.mp4')
        self.camera_width , self.camera_height = 800,600

        # Set the width and height
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_width)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_height)

        # Create a label and display it on app
        self.text_var = tkinter.StringVar(value="")
        self.label_widget = customtkinter.CTkLabel(self,textvariable=self.text_var)
        self.label_widget.grid(row=0,column=2,sticky="nsew",rowspan=1,columnspan=3)


        # Set default values
        self.map_widget.set_position(-22.911663710002028, -43.15942144574782) #Posição inicial do mapa
        self.map_widget.set_zoom(15) 
        #self.map_widget.set_address("Rio de Janeiro")
        self.map_option_menu.set("Google normal")
        self.appearance_mode_optionemenu.set("Dark")

        #Frame com slider para controle de velocidade   
        

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent",width=200,height=200)
        self.slider_progressbar_frame.grid(row=0, column=5, padx=(20, 0), pady=(90, 0), sticky="nsew") #Mexer no pady se quiser abaixar mais o frame
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(5, weight=0)
        self.slider_progressbar_frame.grid_rowconfigure(6, weight=2)
        self.slider_progressbar_frame.grid_rowconfigure(1, weight=1)
        
        #Label do Controle Remoto
        self.label_machine = customtkinter.CTkLabel(master=self.slider_progressbar_frame, text="Controle Remoto")
        self.label_machine.configure(font=("Segoe UI", 30))
        self.label_machine.grid(row=0, column=0, columnspan=1, padx=(10,0), pady=(10,30), sticky="")

        #Label do Leme
        self.label_machine = customtkinter.CTkLabel(master=self.slider_progressbar_frame, text="Leme")
        self.label_machine.configure(font=("Segoe UI", 20))
        self.label_machine.grid(row=3, column=0, columnspan=1, padx=(10,0), pady=(10,20), sticky="")

        #Label das Máquinas
        
        self.label_machine = customtkinter.CTkLabel(master=self.slider_progressbar_frame, text="Máquinas")
        self.label_machine.configure(font=("Segoe UI", 20))
        self.label_machine.grid(row=1, column=0, columnspan=1, padx=(190,0), pady=(20,20), sticky="")

        self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame,width=300)
        self.progressbar_2.grid(row=5, column=0, padx=(20, 10), pady=(0, 0),sticky="nsew")
        
        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=-30, to=30, number_of_steps=60)
        self.slider_1.grid(row=4, column=0, padx=(20, 10), pady=(15, 15), sticky="ew")
        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=100, orientation="vertical",height=400)
        self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 15), pady=(20, 10))
        self.slider_2.set(0) #Zero o slider de máquinas
        self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical",height=400)
        self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(20, 10))

        #Configurando a barra de progresso
        self.slider_1.configure(command=self.update_value_leme) #Configurei o slider para setar a barra de progresso
        self.progressbar_3.set(self.slider_2.get())
        self.slider_2.configure(command=self.update_value_maquinas)

        #Porcentagem de Máquinas 
        self.label_machine = customtkinter.CTkLabel(master=self.slider_progressbar_frame, text=str(int(self.slider_2.get()*100))+"%")
        self.label_machine.configure(font=("Segoe UI", 15))
        self.label_machine.grid(row=0, column=2, columnspan=1, padx=(5,15), pady=(5,5), sticky="n")

        #Angulo do Leme
        self.label_leme = customtkinter.CTkLabel(master=self.slider_progressbar_frame, text=str(int(self.slider_1.get()))+"°")
        self.label_leme.configure(font=("Segoe UI", 25))
        self.label_leme.grid(row=6, column=0, columnspan=2,rowspan=1, padx=(5,10), pady=(0,10), sticky="s")

        #Escolha de modo de controle remoto
        
        #Texto
        self.label_controle = customtkinter.CTkLabel(master=self.slider_progressbar_frame, text="Modo de controle")
        self.label_controle.configure(font=("Segoe UI", 25))
        self.label_controle.grid(row=9, column=0, rowspan=1, columnspan=2, padx=(5,10), pady=(60,15), sticky="")
        
        #Menu para escolha
        self.combobox = customtkinter.CTkOptionMenu(master=self.slider_progressbar_frame,
                                       values=["Manual", "Teclado", "Joystick"],
                                       command=self.optionmenu_callback)
        self.combobox.grid(row=10, column=0, rowspan=1,columnspan=2, padx=(5,10), pady=(0,205), sticky="")

    def optionmenu_callback(self,choice):
        print("optionmenu dropdown clicked:", choice)

    def update_value_maquinas(self,other):
        print(other)
        self.progressbar_3.set(self.slider_2.get())
        self.label_machine.configure(text=str(int(self.slider_2.get()*100))+"%")

    def update_value_leme(self,other):
        print(other)
        self.progressbar_2.set(self.slider_1.get())
        self.label_leme.configure(text=str(int(self.slider_1.get()))+"°")
        

    def destroy_maps(self):
        self.map_widget.destroy() #Deleta o mapa
        self.entry.destroy() #Deleta a pesquisa
        self.button_5.destroy() #Deleta o botão de pesquisa
        self.button_4.configure(command=self.open_maps,text="Ativar Mapas") #Configura o botão para ativar os mapas novamente
        #self.frame_right.grid_columnconfigure(3, weight=2) #Configura o grid para que o label da câmera ocupe todo o espaço
        self.label_widget.grid(row=0, rowspan=1, column=1, columnspan=3, sticky="nswe") #Coloco a câmera no centro

        

    def open_maps(self):
        self.label_widget.grid(row=0, rowspan=1, column=2, columnspan=3, sticky="nswe") #Câmera no canto
        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))
        self.map_widget.set_overlay_tile_server("http://tiles.openseamap.org/seamark//{z}/{x}/{y}.png")
        self.map_widget.set_position(-22.911663710002028, -43.15942144574782) #Posição inicial do mapa
        self.map_widget.set_zoom(15) 
        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            placeholder_text="type address")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_event)

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Search",
                                                width=90,
                                                command=self.search_event)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)
        self.button_4.configure(command=self.destroy_maps,text="Desativar Mapas")

    def destroy_camera(self):
        self.label_widget.destroy() #Destruo o label da câmera
        self.button_3.configure(command=self.destroy_camera,text="Câmera")
        #Crio o label de novo
        self.label_widget = customtkinter.CTkLabel(self,textvariable=self.text_var)
        if (self.map_widget.winfo_exists() == 1): #Checa se o mapa está ativo
            self.label_widget.grid(row=0, rowspan=1, column=2, columnspan=3, sticky="nswe")
        else:
            self.label_widget.grid(row=0, rowspan=1, column=1, columnspan=3, sticky="nswe")
        self.button_3.configure(command=self.open_camera) #Configuro para abrir a câmera novamente

    def open_camera(self):
            self.button_3.configure(command=self.destroy_camera,text="Desativar Câmera") #Coloco o botão para tirar a câmera
  
            # Capture the video frame by frame
            _, frame = self.vid.read()
        
            # Convert image from one color space to other
            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        
            # Capture the latest frame and transform to image
            captured_image = Image.fromarray(opencv_image)
        
            # Convert captured image to photoimage
            photo_image = ImageTk.PhotoImage(image=captured_image)
        
            # Displaying photoimage in the label
            self.label_widget.photo_image = photo_image
        
            # Configure image in the label
            self.label_widget.configure(image=photo_image)
        
            # Repeat the same process after every 10 seconds
            self.label_widget.after(10, self.open_camera)


    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())

    def set_marker_event(self):
        current_position = self.map_widget.get_position()
        self.marker_list.append(self.map_widget.set_marker(current_position[0], current_position[1]))

    def clear_marker_event(self):
        for marker in self.marker_list:
            marker.delete()

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
            self.map_widget.set_overlay_tile_server("http://tiles.openseamap.org/seamark//{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
            self.map_widget.set_overlay_tile_server("http://tiles.openseamap.org/seamark//{z}/{x}/{y}.png")
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
            self.map_widget.set_overlay_tile_server("http://tiles.openseamap.org/seamark//{z}/{x}/{y}.png")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()