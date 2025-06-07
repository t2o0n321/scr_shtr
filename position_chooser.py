import tkinter as tk
import yaml
import time

class MousePositionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Set Mouse Positions")
        
        # Make window semi-transparent
        self.root.attributes('-alpha', 0.7)
        
        # Set full-screen mode without title bar
        self.root.attributes('-fullscreen', True)
        self.root.overrideredirect(True)
        
        # Create a gray canvas
        self.canvas = tk.Canvas(root, bg='gray', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        # Bind left mouse click to set position
        self.canvas.bind('<Button-1>', self.set_position)
        
        # Bind Escape key to save positions and exit
        self.root.bind('<Escape>', self.save_and_exit)
        
        # Store markers, labels, and positions
        self.positions = []
        self.markers = []
        self.labels = []

    def set_position(self, event):
        # Get click coordinates
        x, y = event.x, event.y
        
        # If third click, reset positions, markers, and labels
        if len(self.positions) >= 2:
            # Clear canvas markers and labels
            for marker in self.markers:
                self.canvas.delete(marker)
            for label in self.labels:
                self.canvas.delete(label)
            # Reset lists
            self.positions = []
            self.markers = []
            self.labels = []
        
        # Add new position and marker
        marker_size = 5
        marker = self.canvas.create_oval(
            x - marker_size, y - marker_size,
            x + marker_size, y + marker_size,
            fill='red'
        )
        self.markers.append(marker)
        
        # Add label to the right of the click position
        label_text = str(len(self.positions) + 1)  # "1" or "2"
        label = self.canvas.create_text(
            x + 20, y,  # 20 pixels to the right
            text=label_text,
            fill='red',  # Changed to red
            font=('Arial', 12, 'bold')
        )
        self.labels.append(label)
        self.positions.append((x, y))
        
        # Schedule label removal after 2 seconds
        self.root.after(2000, lambda: self.remove_label(label))

    def remove_label(self, label_id):
        if label_id in self.labels:
            self.canvas.delete(label_id)
            self.labels.remove(label_id)

    def save_and_exit(self, event):
        # Save positions to YAML file
        if self.positions:
            data = {
                'positions': [
                    {'x': pos[0], 'y': pos[1]} for pos in self.positions
                ]
            }
            with open('positions.yaml', 'w') as f:
                yaml.dump(data, f, default_flow_style=False)
        
        # Exit the application
        self.root.quit()

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MousePositionGUI(root)
    root.mainloop()