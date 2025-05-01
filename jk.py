import tkinter as tk
import random

class KawaiiRobotGirl:
    def __init__(self, root):
        self.root = root
        self.root.title("Doraemon - AI Assistant 🤖")
        self.canvas = tk.Canvas(root, width=400, height=520, bg="#87CEEB")  # Sky blue background
        self.canvas.pack()

        self.emotion = "happy"

        # Draw Doraemon's body
        # Main body (blue)
        self.canvas.create_oval(100, 100, 300, 400, fill="#0066CC", outline="#003366", width=3)
        
        # White belly
        self.canvas.create_oval(120, 150, 280, 350, fill="#FFFFFF", outline="#003366", width=2)
        
        # Pocket
        self.canvas.create_oval(170, 200, 230, 250, fill="#FFFFFF", outline="#003366", width=2)
        
        # Bell
        self.canvas.create_oval(190, 260, 210, 280, fill="#FFD700", outline="#B8860B", width=2)
        self.canvas.create_line(200, 280, 200, 290, fill="#B8860B", width=2)
        
        # Head
        self.canvas.create_oval(80, 50, 320, 150, fill="#0066CC", outline="#003366", width=3)
        
        # White face (more round)
        self.canvas.create_oval(100, 60, 300, 140, fill="#FFFFFF", outline="#003366", width=2)
        
        # Eyes (adjusted for rounder face)
        self.left_eye = self.canvas.create_oval(150, 70, 190, 110, fill="#FFFFFF", outline="#003366", width=2)
        self.left_pupil = self.canvas.create_oval(165, 85, 175, 95, fill="#000000")
        
        self.right_eye = self.canvas.create_oval(210, 70, 250, 110, fill="#FFFFFF", outline="#003366", width=2)
        self.right_pupil = self.canvas.create_oval(225, 85, 235, 95, fill="#000000")
        
        # Nose (adjusted position)
        self.nose = self.canvas.create_oval(195, 100, 205, 110, fill="#FF0000", outline="#990000", width=1)
        
        # Whiskers (adjusted for rounder face)
        # Left whiskers
        self.canvas.create_line(100, 95, 80, 90, fill="#003366", width=2)
        self.canvas.create_line(100, 105, 80, 105, fill="#003366", width=2)
        self.canvas.create_line(100, 115, 80, 120, fill="#003366", width=2)
        
        # Right whiskers
        self.canvas.create_line(300, 95, 320, 90, fill="#003366", width=2)
        self.canvas.create_line(300, 105, 320, 105, fill="#003366", width=2)
        self.canvas.create_line(300, 115, 320, 120, fill="#003366", width=2)

        # Mouth (adjusted for rounder face)
        self.mouth = self.canvas.create_arc(160, 100, 240, 120, start=0, extent=-180, style=tk.CHORD, fill="#FFFFFF", outline="#003366", width=2)

        # Message label
        self.label = self.canvas.create_text(200, 450, text="System OK. Feeling happy! 🤖", font=("Consolas", 14), fill="#003366")

        # Emotion buttons
        self.create_emotion_buttons()

        self.blinking = False
        self.animate()

    def create_emotion_buttons(self):
        emotions = ["Happy", "Sad", "Angry", "Surprised"]
        colors = ["#0066CC", "#003366", "#990000", "#FFD700"]  # Doraemon colors
        for i, emo in enumerate(emotions):
            btn = tk.Button(
                self.root, text=emo, font=("Consolas", 10, "bold"),
                bg=colors[i], fg="#FFFFFF", command=lambda e=emo.lower(): self.set_emotion(e)
            )
            btn.place(x=50 + i*85, y=480, width=80, height=30)

    def animate(self):
        if not self.blinking:
            self.blinking = True
            self.canvas.after(2500, self.blink)
        self.root.after(1000, self.animate)

    def blink(self):
        self.canvas.itemconfig(self.left_pupil, state='hidden')
        self.canvas.itemconfig(self.right_pupil, state='hidden')
        self.root.after(150, self.unblink)

    def unblink(self):
        self.canvas.itemconfig(self.left_pupil, state='normal')
        self.canvas.itemconfig(self.right_pupil, state='normal')
        self.blinking = False

    def set_emotion(self, emotion):
        self.emotion = emotion
        if emotion == "happy":
            self.canvas.itemconfig(self.mouth, start=0, extent=-180, fill="#FFFFFF")
            self.canvas.itemconfig(self.label, text="System OK. Feeling happy! 🤖")
        elif emotion == "sad":
            self.canvas.itemconfig(self.mouth, start=0, extent=180, fill="#FFFFFF")
            self.canvas.itemconfig(self.label, text="System alert... sadness detected. 😢")
        elif emotion == "angry":
            self.canvas.itemconfig(self.mouth, start=20, extent=140, fill="#FFFFFF")
            self.canvas.itemconfig(self.label, text="Warning. Frustration rising! 😠")
        elif emotion == "surprised":
            self.canvas.itemconfig(self.mouth, start=0, extent=360, fill="#FFFFFF")
            self.canvas.itemconfig(self.label, text="System shocked! What happened!? 😲")

# Run it!
if __name__ == "__main__":
    root = tk.Tk()
    app = KawaiiRobotGirl(root)
    root.mainloop()