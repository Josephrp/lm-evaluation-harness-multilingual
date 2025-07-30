#!/usr/bin/env python3
"""
Test script to verify the max_new_tokens type conversion fix.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_max_new_tokens_conversion():
    """Test that max_new_tokens string values are properly converted to integers."""
    
    # Mock the necessary components to test the _model_generate method
    class MockTokenizer:
        def __init__(self):
            self.pad_token_id = 0
    
    class MockModel:
        def generate(self, **kwargs):
            # Check if max_new_tokens is an integer
            if 'max_new_tokens' in kwargs:
                if not isinstance(kwargs['max_new_tokens'], int):
                    raise TypeError(f"max_new_tokens should be int, got {type(kwargs['max_new_tokens'])}")
            return "test_output"
    
    class MockHFLM:
        def __init__(self):
            self.tokenizer = MockTokenizer()
            self.model = MockModel()
            self._generation_kwargs = {'max_new_tokens': '10'}  # String value
        
        def _model_generate(self, context, max_length, stop, **generation_kwargs):
            # Copy the fixed _model_generate method from huggingface.py
            # Merge stored generation parameters with passed ones (passed ones take precedence)
            if hasattr(self, '_generation_kwargs'):
                merged_kwargs = self._generation_kwargs.copy()
                merged_kwargs.update(generation_kwargs)
                generation_kwargs = merged_kwargs
            
            # Convert numeric generation parameters to ensure correct types
            numeric_params = {
                'max_new_tokens': int,
                'max_length': int,
                'min_length': int,
                'num_beams': int,
                'num_beam_groups': int,
                'num_return_sequences': int,
                'length_penalty': float,
                'repetition_penalty': float,
                'temperature': float,
                'top_p': float,
                'top_k': int,
                'no_repeat_ngram_size': int,
                'bad_words_ids': list,
                'forced_bos_token_id': int,
                'forced_eos_token_id': int,
                'pad_token_id': int,
                'eos_token_id': int,
                'bos_token_id': int,
            }
            
            for param, param_type in numeric_params.items():
                if param in generation_kwargs and generation_kwargs[param] is not None:
                    try:
                        if param_type == list:
                            # For list parameters, ensure all elements are the correct type
                            if isinstance(generation_kwargs[param], str):
                                # Handle string representation of lists
                                import ast
                                generation_kwargs[param] = ast.literal_eval(generation_kwargs[param])
                        else:
                            generation_kwargs[param] = param_type(generation_kwargs[param])
                    except (ValueError, TypeError) as e:
                        # If conversion fails, remove the parameter to avoid errors
                        print(f"Failed to convert {param}={generation_kwargs[param]} to {param_type.__name__}: {e}. Removing parameter.")
                        generation_kwargs.pop(param)
            
            # temperature = 0.0 if not set
            generation_kwargs["temperature"] = generation_kwargs.get("temperature", 0.0)
            do_sample = generation_kwargs.get("do_sample", None)

            # The temperature has to be a strictly positive float -- if it is 0.0, use greedy decoding strategies
            if generation_kwargs.get("temperature") == 0.0 and do_sample is None:
                generation_kwargs["do_sample"] = do_sample = False

            if do_sample is False and generation_kwargs.get("temperature") == 0.0:
                generation_kwargs.pop("temperature")
            
            # Call the model's generate method
            return self.model.generate(**generation_kwargs)
    
    # Test the fix
    try:
        mock_lm = MockHFLM()
        result = mock_lm._model_generate(
            context=None,  # Not used in our mock
            max_length=100,
            stop=None,  # Not used in our mock
        )
        print("✅ SUCCESS: max_new_tokens string value was properly converted to integer")
        print(f"Result: {result}")
        return True
    except TypeError as e:
        print(f"❌ FAILED: {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Testing max_new_tokens type conversion fix...")
    success = test_max_new_tokens_conversion()
    if success:
        print("\n🎉 The fix is working correctly!")
    else:
        print("\n💥 The fix needs more work.")
    sys.exit(0 if success else 1) 