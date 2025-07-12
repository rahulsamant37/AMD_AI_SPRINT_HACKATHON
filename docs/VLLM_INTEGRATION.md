# vLLM DeepSeek Integration Setup

This document explains how to set up and run SchedulAI with vLLM DeepSeek integration instead of OpenAI.

## Prerequisites

1. **vLLM Server**: You need a running vLLM server with DeepSeek model
2. **Google API Credentials**: For Calendar and Gmail integration
3. **Python Environment**: Python 3.8+ with required dependencies

## vLLM Server Setup

### Option 1: Using the provided notebook
Use the `resources/vLLM_Inference_Servering_DeepSeek.ipynb` notebook to start the vLLM server:

```bash
HIP_VISIBLE_DEVICES=0 vllm serve /home/user/Models/deepseek-ai/deepseek-llm-7b-chat \
    --gpu-memory-utilization 0.9 \
    --swap-space 16 \
    --disable-log-requests \
    --dtype float16 \
    --max-model-len 2048 \
    --tensor-parallel-size 1 \
    --host 0.0.0.0 \
    --port 3000 \
    --num-scheduler-steps 10 \
    --max-num-seqs 128 \
    --max-num-batched-tokens 2048 \
    --max-model-len 2048 \
    --distributed-executor-backend "mp"
```

### Option 2: Custom vLLM setup
If you have your own vLLM server, ensure it's running and accessible at the configured URL.

## Environment Configuration

1. Copy the environment example file:
```bash
cp env.example .env
```

2. Update the vLLM configuration in `.env`:
```bash
# vLLM Server Configuration
VLLM_BASE_URL=http://localhost:3000
VLLM_MODEL_PATH=/home/user/Models/deepseek-ai/deepseek-llm-7b-chat
VLLM_TEMPERATURE=0.3
VLLM_MAX_TOKENS=2000
```

3. Configure Google API credentials (same as before):
```bash
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_TOKEN_FILE=token.pickle
```

## Key Changes from OpenAI Integration

### 1. Service Layer
- **Old**: `vLLM server=config.vLLM server)`
- **New**: `VLLMService()` with HTTP requests to vLLM server

### 2. Function Calling
- **Old**: Native vLLM DeepSeek Function Calling
- **New**: Prompt engineering to simulate function calling with DeepSeek

### 3. Configuration
- **Old**: `vLLM server`, `# vLLM model path configuration
- **New**: `VLLM_BASE_URL`, `VLLM_MODEL_PATH`

### 4. Response Handling
- **Old**: Direct OpenAI response objects
- **New**: Compatibility layer that mimics OpenAI response structure

## Testing the Integration

1. **Health Check**: The application will automatically perform a health check on startup
2. **Function Calling**: Test with a simple meeting request to verify function calling works
3. **Logs**: Check application logs for vLLM communication details

## Troubleshooting

### vLLM Server Issues
- Ensure the vLLM server is running and accessible
- Check the port configuration matches your setup
- Verify the model path is correct

### Function Calling Issues
- The DeepSeek model uses prompt engineering for function calling
- Check logs to see if functions are being detected and executed
- May require prompt tuning for optimal performance

### Performance Considerations
- vLLM server response times may differ from OpenAI
- Adjust timeout settings if needed
- Monitor GPU memory usage on the vLLM server

## Benefits of vLLM Integration

1. **Local Deployment**: Run entirely on your infrastructure
2. **Cost Control**: No per-token charges
3. **Privacy**: Data doesn't leave your environment
4. **Customization**: Full control over the model and parameters
5. **AMD GPU Support**: Optimized for AMD hardware with ROCm

## Fallback to OpenAI

If needed, you can fallback to OpenAI by:
1. Installing the `openai` package: `pip install openai==1.3.6`
2. Updating the imports in `agent_service.py`
3. Switching the client initialization back to OpenAI
4. Setting the `vLLM server` in your environment

The configuration supports both setups for easy migration.
