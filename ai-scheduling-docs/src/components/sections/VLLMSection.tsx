import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { CodeBlock } from "../CodeBlock";
import { Server, ExternalLink, Zap, Cpu, AlertCircle } from "lucide-react";

export const VLLMSection = () => {
  const deepseekCommand = `HIP_VISIBLE_DEVICES=0 vllm serve /home/user/Models/deepseek-ai/deepseek-llm-7b-chat \\
        --gpu-memory-utilization 0.9 \\
        --swap-space 16 \\
        --disable-log-requests \\
        --dtype float16 \\
        --max-model-len 2048 \\
        --tensor-parallel-size 1 \\
        --host 0.0.0.0 \\
        --port 3000 \\
        --num-scheduler-steps 10 \\
        --max-num-seqs 128 \\
        --max-num-batched-tokens 2048 \\
        --max-model-len 2048 \\
        --distributed-executor-backend "mp"`;

  const llamaCommand = `HIP_VISIBLE_DEVICES=0 vllm serve /home/user/Models/meta-llama/Meta-Llama-3.1-8B-Instruct \\
        --gpu-memory-utilization 0.3 \\
        --swap-space 16 \\
        --disable-log-requests \\
        --dtype float16 \\
        --max-model-len 2048 \\
        --tensor-parallel-size 1 \\
        --host 0.0.0.0 \\
        --port 4000 \\
        --num-scheduler-steps 10 \\
        --max-num-seqs 128 \\
        --max-num-batched-tokens 2048 \\
        --max-model-len 2048 \\
        --distributed-executor-backend "mp"`;

  const usageExample = `import openai

# Here's how we configured the client to connect to our server
client = openai.OpenAI(
    base_url="http://localhost:3000/v1",  # Our DeepSeek model on port 3000
    api_key="dummy-key"  # vLLM doesn't require a real key, so we used a placeholder
)

# We made requests like this to our model
response = client.chat.completions.create(
    model="/home/user/Models/deepseek-ai/deepseek-llm-7b-chat",
    messages=[
        {"role": "user", "content": "Schedule a meeting for next Tuesday"}
    ],
    temperature=0.7,
    max_tokens=512
)

print(response.choices[0].message.content)`;

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold mb-4 bg-gradient-primary bg-clip-text text-transparent">
          How We Set Up Our vLLM Server
        </h2>
        <p className="text-muted-foreground text-lg">
          We successfully set up a high-performance LLM inference server with vLLM on the AMD MI300X GPU.
        </p>
      </div>

      {/* vLLM Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-primary/10">
              <Server className="h-5 w-5 text-accent" />
            </div>
            Why We Chose vLLM
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground mb-6">
            We chose vLLM, an open-source library, because it allowed us to achieve high throughput and low latency for our LLM inference. It was designed to optimize text generation by batching requests efficiently and making full use of the powerful GPU resources we had.
          </p>

          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center p-4 rounded-lg bg-muted/50 border border-border/50">
              <Zap className="h-8 w-8 mx-auto mb-3 text-accent" />
              <h4 className="font-semibold mb-2">High Throughput</h4>
              <p className="text-sm text-muted-foreground">We achieved maximum performance by using its optimized batching.</p>
            </div>
            <div className="text-center p-4 rounded-lg bg-muted/50 border border-border/50">
              <Cpu className="h-8 w-8 mx-auto mb-3 text-ai-blue" />
              <h4 className="font-semibold mb-2">Low Latency</h4>
              <p className="text-sm text-muted-foreground">We got the fast response times needed for our real-time application.</p>
            </div>
            <div className="text-center p-4 rounded-lg bg-muted/50 border border-border/50">
              <Server className="h-8 w-8 mx-auto mb-3 text-ai-purple" />
              <h4 className="font-semibold mb-2">GPU Optimization</h4>
              <p className="text-sm text-muted-foreground">We fully utilized the AMD MI300X GPU's powerful resources.</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Model Setup */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-secondary/10">
              <Cpu className="h-5 w-5 text-ai-blue" />
            </div>
            The Models We Deployed
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="deepseek" className="w-full">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="deepseek">DeepSeek LLM 7B</TabsTrigger>
              <TabsTrigger value="llama">Llama 3.1 8B</TabsTrigger>
            </TabsList>
            <br />
            
            <TabsContent value="deepseek" className="space-y-6">
              <div className="flex items-start gap-4">
                <Badge className="bg-accent/10 text-accent border-accent/20">
                  Port 3000
                </Badge>
                <div>
                  <h4 className="font-semibold text-foreground mb-2">DeepSeek LLM 7B Chat</h4>
                  <p className="text-muted-foreground">
                    We chose this model because it is optimized for conversational AI and was great for our scheduling logic.
                  </p>
                </div>
              </div>
              
              <Alert>
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>
                  <strong>How we set it up:</strong> We opened a new terminal in Jupyter and ran the following command.
                </AlertDescription>
              </Alert>

              <CodeBlock language="bash" title="Command to Start Our DeepSeek Server">
                {deepseekCommand}
              </CodeBlock>

              <div className="pt-4">
                <Button variant="outline" asChild>
                  <a 
                    href="https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant/blob/main/vLLM_Inference_Servering_DeepSeek.ipynb" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="flex items-center gap-2"
                  >
                    <ExternalLink className="h-4 w-4" />
                    View Our DeepSeek Notebook
                  </a>
                </Button>
              </div>
            </TabsContent>
            
            <TabsContent value="llama" className="space-y-6">
              <div className="flex items-start gap-4">
                <Badge className="bg-ai-blue/10 text-ai-blue border-ai-blue/20">
                  Port 4000
                </Badge>
                <div>
                  <h4 className="font-semibold text-foreground mb-2">Meta-Llama-3.1-8B-Instruct</h4>
                  <p className="text-muted-foreground">
                    We also used the latest instruction-tuned model from Meta, which excelled at following complex instructions.
                  </p>
                </div>
              </div>
              
              <Alert>
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>
                  <strong>How we set it up:</strong> We opened a new terminal in Jupyter and ran the following command.
                </AlertDescription>
              </Alert>

              <CodeBlock language="bash" title="Command to Start Our Llama Server">
                {llamaCommand}
              </CodeBlock>

              <div className="pt-4">
                <Button variant="outline" asChild>
                  <a 
                    href="https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant/blob/main/vLLM_Inference_Servering_LLaMA.ipynb" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="flex items-center gap-2"
                  >
                    <ExternalLink className="h-4 w-4" />
                    View Our Llama Notebook
                  </a>
                </Button>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      {/* Usage Example */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-accent/10">
              <Zap className="h-5 w-5 text-ai-cyan" />
            </div>
            How We Used the Server
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground mb-4">
            Once our vLLM server was up and running, we interacted with it using this simple, OpenAI-compatible API:
          </p>
          
          <CodeBlock language="python" title="our_client_example.py">
            {usageExample}
          </CodeBlock>
        </CardContent>
      </Card>

      {/* Configuration Notes */}
      <Card>
        <CardHeader>
          <CardTitle>The Configuration Parameters We Used</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <h4 className="font-semibold text-foreground">Our Performance Settings</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><code className="text-accent">--gpu-memory-utilization</code> We used this to control GPU memory usage.</li>
                <li><code className="text-accent">--max-num-seqs</code> We set the max number of concurrent sequences.</li>
                <li><code className="text-accent">--max-num-batched-tokens</code> We used this for batching optimization.</li>
              </ul>
            </div>
            <div className="space-y-4">
              <h4 className="font-semibold text-foreground">Our Network Settings</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><code className="text-accent">--host 0.0.0.0</code> We used this to accept connections from any IP.</li>
                <li><code className="text-accent">--port 3000/4000</code> These were the ports for each of our models.</li>
                <li><code className="text-accent">--disable-log-requests</code> We used this to reduce log verbosity.</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};