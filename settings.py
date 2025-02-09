import pyfiglet
# Optional import to check for CUDA functionality.
#import torch

# Use the below settings to alter behavior of the main application.

SPEECHRATE = 250                               # Change the speech rate of speed.
VOICEVOLUME = 1                                # Adjust the relative volume of the voice.
KEY1 = '1'                                     # Key binging for low detail screen reads.
KEY2 = '2'                                     # Key bindingg for higher detail screen reads.
KEY3 = '3'                                     # Key binding for screenshots.
KEYQUIT = ']'                                  # Key binding for exiting the program.

# The options for the below priority dictate the order that the model attempts to read options.
# The priority should be read as: First try to find option[0] then try to find option[1]

# Options Description:
# 'title' = The title block of menu items when the cursor hovers over an item.
# 'item' = Reads the popup in the center of the screen when hovered over in world minerals or items.
# 'info' = Reads the main text block in menu items, dialoge blocks, or new quest blocks.
# 'quest' = Reads the quest block in the bottom right of the screen.

PRIORITY_QUEUE1 = ['title', 'item']           # Priority of items to read for low detail items.
PRIORITY_QUEUE2 = ['info', 'quest']            # Priority of items to read for high detail items.

def print_menu():
    print(pyfiglet.figlet_format("No Man's Access"))
    print(f"Press '{KEY1}' for simple items like items or title blocks")
    print(f"Press '{KEY2}' for more indepth info like the quest log and menu content")
    print(f"Press '{KEY3}' to take a screenshot for training")
    print(f"Press '{KEYQUIT}' to quit.")

# Uncomment the below to demonstrate if CUDA cores are available
#print(f"CUDA cores available for use: {torch.cuda.is_available()}")

# Prints header menu
print_menu()