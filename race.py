import thread, time, sys
from Tkinter import *

# задаем дистанцию и цвета бегунов
distance = 300
colors = ["Red","Orange","Yellow","Green","Blue","DarkBlue","Violet"]
nrunners = len(colors)

def quit():
  """Выход из программы"""
  tk.quit()
  sys.exit(0)
  
# окно и основа для прямоугольников
tk = Tk()
tk.title("Гонки")
c = Canvas(tk, width=distance, height=len(colors)*20, bg="White")
c.pack()

# прямоугольники 
rects = []  
for i in range(nrunners):
  rects.append(c.create_rectangle(0, i*20, 0, i*20+10, fill=colors[i]))

b = Button(text="Go", command=tk.quit)  # кнопка пуска
b.pack(side=LEFT)
qb = Button(text="Quit", command=quit)  # кнопка выхода
qb.pack(side=RIGHT)

def run(n):
  """Программа бега n-го участника"""
  while 1:
    graph_lock.acquire()
    positions[n] = positions[n] + 1  # двигаемся на шаг
    for i in range(1000):
      pass
    if positions[n] == distance:  # если добежал до финиша
      if not champion:   # и чемпионское место пусто
        champion = colors[n]
      graph_lock.release()
      break
    graph_lock.release()

def prepare():
  """На старт!"""
  champion = None
  for i in range(nrunners):
    thread.start_new_thread(run, (i,))

graph_lock = thread.allocate_lock()
while 1:
  b.config(state=NORMAL); qb.config(state=NORMAL)
  tk.mainloop()  # ждем действий зрителя
  b.config(state=DISABLED); qb.config(state=DISABLED)
  graph_lock.acquire()
  positions = [0]*nrunners  # На старт!
  prepare()                 # Внимание!
  graph_lock.release()      # Марш!
  # главный поток (судья) ждет, пока финишируют все участники
  while reduce(lambda x, y: x+y, positions, 0) < distance*nrunners:
    graph_lock.acquire()
    for n in range(nrunners):
      c.coords(rects[n], 0, n*20, positions[n], n*20+10)
    tk.update_idletasks()
    graph_lock.release()
  for n in range(nrunners):
    c.coords(rects[n], 0, n*20, positions[n], n*20+10)
  b.config(bg=champion)  # окрашиваем кнопку цвет победителя
  tk.update_idletasks()

