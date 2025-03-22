import os
import json
import glob
import re
from pathlib import Path

def load_gen_video_data():
    """
    Load data from gen_video directory and create a JSON file with success indicators.
    The value is 0 or 1 based on whether the video is in the success category.
    """
    # Base directory for generated videos
    base_dir = Path('/Users/lr-2002/project/videoagent/data/gen_video')
    
    # Get all task directories
    task_dirs = [d for d in base_dir.iterdir() if d.is_dir()]
    
    result_data = []
    
    # Define success patterns - this would need to be adjusted based on actual success criteria
    # For this example, we'll consider videos with even-numbered examples as successful
    def is_success(task_name, example_num):
        return int(example_num) % 2 == 0
    
    # Define task descriptions
    task_descriptions = {
        "hammer-v2-goal-observable": "use hammer to nail the nail",
        "basketball-v2-goal-observable": "move the ball to the basket",
        "button-press-v2-goal-observable": "press the button",
        "button-press-topdown-v2-goal-observable": "press the button from top to down",
        "handle-press-v2-goal-observable": "press the handle"
    }
    
    for task_dir in task_dirs:
        task_name = task_dir.name
        
        # Get task description
        task_description = task_descriptions.get(task_name, "complete the task")
        
        # Get all numbered directories (these represent different examples)
        example_dirs = [d for d in task_dir.iterdir() if d.is_dir() and d.name.isdigit()]
        
        for example_dir in example_dirs:
            # Get the example number
            example_num = example_dir.name
            
            # Find the GIF file
            gif_files = list(example_dir.glob('*_out.gif'))
            if not gif_files:
                continue
                
            gif_file = gif_files[0]
            
            # Create a video path (using the format from the example)
            # In this case, we'll use the task name and example number
            video_path = f"{task_name}/{example_num}/{gif_file.name}"
            
            # Determine success (1) or failure (0)
            success = 1 if is_success(task_name, example_num) else 0
            
            # Create entry with the format from the example
            entry = {
                "video": video_path,
                "conversations": [
                    {
                        "from": "human",
                        "value": f"<video>This video's target is to use the robot arm to achieve {task_description}."
                    },
                    {
                        "from": "gpt",
                        "value": str(success)
                    }
                ]
            }
            
            # Add success indicator to the entry
            entry["success"] = success
            
            result_data.append(entry)
    
    # Write the result to a JSON file
    output_file = Path('/Users/lr-2002/project/videoagent/data/video_data.json')
    with open(output_file, 'w') as f:
        json.dump(result_data, f, indent=4)
    
    print(f"Generated JSON file with {len(result_data)} entries at {output_file}")
    return result_data

if __name__ == "__main__":
    load_gen_video_data()