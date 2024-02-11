import sys
from vision import get_answer as get_vision_answer
from stats import predict_claim_probability
from llm import rag_answer
import torch

def main(image_path, stats_sample):
    # Set up device for vision model
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # Execute vision model
    vision_output = get_vision_answer(image_path, device, 480)
    
    # Execute stats model
    # Convert string input to list of floats
    stats_sample_list = [float(item) for item in stats_sample.strip('[]').split(',')]
    stats_output = predict_claim_probability(stats_sample_list)
    
    # Prepare input for LLM model
    llm_input_message = f"Vision Model Output: {vision_output}. Stats Model Output: {stats_output}."
    
    # Execute LLM model
    llm_response = rag_answer(llm_input_message)
    
    print("\nFinal LLM Response:", llm_response)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main_script.py <image_path> '<stats_sample>'")
        sys.exit(1)
    
    image_path = sys.argv[1]
    stats_sample = sys.argv[2]
    
    main(image_path, stats_sample)
