import sys
import json
from vision import get_answer as get_vision_answer
from stats import predict_claim_probability
from llm import rag_answer
import torch

def main(image_path, stats_sample):
    # Set up device for vision model
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # Execute vision model
    vision_output = get_vision_answer(image_path, device, 480)
    
    # Save vision model output to JSON file
    vision_output_json_path = 'vision_output.json'
    with open(vision_output_json_path, 'w') as json_file:
        json.dump({'vision_output': vision_output}, json_file)
    
    print(f"Vision model output saved to {vision_output_json_path}")
    
    # Execute stats model
    # Convert string input to list of floats
    stats_sample_list = [float(item) for item in stats_sample.strip('[]').split(',')]
    stats_output = predict_claim_probability(stats_sample_list)

    with open('stats_output.json','w') as json_file:
        json.dump({'stats':stats_putput},json_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main_script.py <image_path> '<stats_sample>'")
        sys.exit(1)
    
    image_path = sys.argv[1]
    stats_sample = sys.argv[2]
    
    main(image_path, stats_sample)
