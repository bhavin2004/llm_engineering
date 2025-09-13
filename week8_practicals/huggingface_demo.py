import modal
from modal import Image,App

app = App("huggingface_demo")
image = Image.debian_slim().pip_install("torch", "transformers", "bitsandbytes", "accelerate")
secret = [modal.Secret.from_name('hf-secret')]

GPU = "T4"
MODEL_NAME= "meta-llama/Meta-Llama-3.1-8B"

@app.function(
    image=image,
    gpu=GPU,
    secrets=secret
)
def model_run(prompt:str)->str:
    import os
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, set_seed
    
    quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type='nf4',
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_storage=torch.bfloat16
    )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = 'right'
    
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, 
        quantization_config=quant_config,
        device_map="auto"
    )
    
    set_seed(50)
    
    input=tokenizer.encode(prompt,return_tensors='pt').to('cuda')
    attention_mask=torch.ones(input.shape,device='cuda')
    output = model.generate(input,attention_mask=attention_mask,max_new_tokens=5,num_return_sequences=1)
    return tokenizer.decode(output[0],skip_special_tokens=True)