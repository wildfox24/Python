import Tkinter
icon='''R0lGODdhFQAVAPMAAAQ2PESapISCBASCBMTCxPxmNCQiJJya/ISChGRmzPz+/PxmzDQyZDQyZDQy
ZDQyZCwAAAAAFQAVAAAElJDISau9Vh2WMD0gqHHelJwnsXVloqDd2hrMm8pYYiSHYfMMRm53ULlQ
HGFFx1MZCciUiVOsPmEkKNVp3UBhJ4Ohy1UxerSgJGZMMBbcBACQlVhRiHvaUsXHgywTdycLdxyB
gm1vcTyIZW4MeU6NgQEBXEGRcQcIlwQIAwEHoioCAgWmCZ0Iq5+hA6wIpqislgGhthEAOw==
'''

root = Tkinter.Tk()
iconImage=Tkinter.PhotoImage(master=root, data=icon)
Tkinter.Button(image=iconImage).pack()
root.mainloop()
