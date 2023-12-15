import tkinter as tk
import random

# Constants
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 10
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 10
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
BRICK_ROWS = 4
BRICK_COLS = 10
BRICK_COLORS = ["red", "orange", "yellow", "green", "blue"]

# Initialize the game variables
ball_speed = 2
ball_dx = ball_speed
ball_dy = -ball_speed
paddle_speed = 60
score = 0

# Create the main window
root = tk.Tk()
root.title("Brick Breaker")
root.geometry(f"{WIDTH}x{HEIGHT}")

# Canvas widget for drawing
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# Create the paddle
paddle = canvas.create_rectangle(
    WIDTH // 2 - PADDLE_WIDTH // 2,
    HEIGHT - PADDLE_HEIGHT - 10,
    WIDTH // 2 + PADDLE_WIDTH // 2,
    HEIGHT - 10,
    fill="white"
)

# Create the ball
ball = canvas.create_oval(
    WIDTH // 2 - BALL_RADIUS,
    HEIGHT // 2 - BALL_RADIUS,
    WIDTH // 2 + BALL_RADIUS,
    HEIGHT // 2 + BALL_RADIUS,
    fill="white"
)

# Create the bricks
bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick = canvas.create_rectangle(
            col * BRICK_WIDTH,
            row * BRICK_HEIGHT,
            (col + 1) * BRICK_WIDTH,
            (row + 1) * BRICK_HEIGHT,
            fill=random.choice(BRICK_COLORS),
            outline="white"
        )
        bricks.append(brick)

# Create a label for displaying the score
score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 12), fg="white", bg="black")
score_label.pack()

# Function to move the paddle
def move_paddle(event):
    x, y, _, _ = canvas.coords(paddle)
    if event.keysym == "Left" and x > 0:
        canvas.move(paddle, -paddle_speed, 0)
    elif event.keysym == "Right" and x + PADDLE_WIDTH < WIDTH:
        canvas.move(paddle, paddle_speed, 0)

# Bind the paddle movement to left and right arrow keys
root.bind("<Left>", move_paddle)
root.bind("<Right>", move_paddle)

# Function to update the game state
#update_id = None
def update():
    #global ball_dx, ball_dy, update_id  # Declare update_id as a global variabl
    global ball_dx, ball_dy, score

    # Move the ball
    canvas.move(ball, ball_dx, ball_dy)

    # Get the current position of the ball
    x1, y1, x2, y2 = canvas.coords(ball)

    # Check for collisions with the walls
    if x1 <= 0 or x2 >= WIDTH:
        ball_dx = -ball_dx
    if y1 <= 0:
        ball_dy = -ball_dy

    # Check for collisions with the paddle
    if y2 >= HEIGHT - PADDLE_HEIGHT - 10 and canvas.coords(paddle)[0] < x2 < canvas.coords(paddle)[2]:
        ball_dy = -ball_dy

    # Check for collisions with the bricks
    for brick in bricks:
        if canvas.coords(ball) and canvas.coords(brick):
            brick_x1, brick_y1, brick_x2, brick_y2 = canvas.coords(brick)
            if brick_x1 < x2 < brick_x2 and brick_y1 < y2 < brick_y2:
                canvas.delete(brick)
                bricks.remove(brick)
                ball_dy = -ball_dy
                score += 10
                update_score()

    # Check if the ball goes below the paddle (game over)
    if y2 >= HEIGHT:
        canvas.create_text(WIDTH // 2, HEIGHT // 2, text=f"Game Over\nScore: {score}", font=("Helvetica", 20), fill="white")
        root.after_cancel(update_id)

    # Check if all bricks are destroyed (win)
    if not bricks:
        canvas.create_text(WIDTH // 2, HEIGHT // 2, text=f"You Win!\nScore: {score}", font=("Helvetica", 20), fill="white")
        root.after_cancel(update_id)

    # Call the update function again after a delay
    update_id = root.after(10, update)

# Function to update the score label
def update_score():
    score_label.config(text=f"Score: {score}")

# Start the game loop
update_id = root.after(10, update)

# Run the Tkinter event loop
root.mainloop()
